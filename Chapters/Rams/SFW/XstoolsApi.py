#!/usr/bin/python
# -*- coding: utf-8 -*-
# /***********************************************************************************
# *   This program is free software; you can redistribute it and/or
# *   modify it under the terms of the GNU General Public License
# *   as published by the Free Software Foundation; either version 2
# *   of the License, or (at your option) any later version.
# *
# *   This program is distributed in the hope that it will be useful,
# *   but WITHOUT ANY WARRANTY; without even the implied warranty of
# *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# *   GNU General Public License for more details.
# *
# *   You should have received a copy of the GNU General Public License
# *   along with this program; if not, write to the Free Software
# *   Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA
# *   02111-1307, USA.
# *
# *   (c)2011 - X Engineering Software Systems Corp. (www.xess.com)
# ***********************************************************************************/

'''
This file provides an interface between the XSTOOLs API DLL and the
rest of the Python code.
'''

import types
import sys
import os
from ctypes import *

# Load the xstoolsApi DLL that provides access to the XuLA board.
print os.getcwd()
xstoolsApi = cdll.LoadLibrary(os.path.join(os.getcwd(), 'XstoolsApi.dll'))

# Provide shorter names for the XSTOOLs API subroutines.
MemInit = xstoolsApi.XsMemInit
MemWrite = xstoolsApi.XsMemWrite
MemRead = xstoolsApi.XsMemRead
DutInit = xstoolsApi.XsDutInit
DutWrite = xstoolsApi.XsDutWrite
DutRead = xstoolsApi.XsDutRead

# Create prototypes so the Python interpreter can detect function invocation errors.
MemInit.argtypes = [c_uint, c_uint, POINTER(c_uint), POINTER(c_uint)]
MemWrite.argtypes = [c_void_p, c_uint, POINTER(c_ulonglong), c_uint]
MemRead.argtypes = [c_void_p, c_uint, POINTER(c_ulonglong), c_uint]
DutInit.argtypes = [c_uint, c_uint, POINTER(c_uint), POINTER(c_uint)]
DutWrite.argtypes = [c_void_p, POINTER(c_ubyte), c_uint]
DutRead.argtypes = [c_void_p, POINTER(c_ubyte), c_uint]


class XsMem:

    '''Class for reading/writing to RAM-like circuits in the FPGA of an XESS board.'''

    def __init__(self, usbId, moduleId):
        '''Get the RAM parameters from the FPGA.'''

        cAddrWidth = c_uint(0)
        cDataWidth = c_uint(0)
        # Open a link to the memory circuit in the FPGA and get the widths of the address and data buses.
        self.mem = MemInit(c_uint(usbId), c_uint(moduleId),
                            byref(cAddrWidth), byref(cDataWidth))
        if self.mem == 0:
            print "Couldn't get a handle for the RAM in the XESS board!"
            sys.exit()
        self.addrWidth = cAddrWidth.value  # Store address width.
        self.dataWidth = cDataWidth.value  # Store data word width.

    def Read(self, startAddr, buffer=0):
        '''Read enough words from the RAM in the FPGA to fill the buffer.'''

        # If buffer is just a scalar ref instead of a list, then make it into a list.
        if type(buffer) != types.ListType:
            buffer = [0]  # Create a new, single-item buffer.
        cBuffer = (c_ulonglong * len(buffer))()  # Create a ctypes buffer the same size as the given buffer.
        # Fill the ctypes buffer with values from the memory circuit in the FPGA.
        MemRead(self.mem, c_uint(startAddr), cBuffer,
                c_uint(len(buffer)))
        # Transfer the ctypes buffer contents to the buffer given by the calling routine.
        for i in range(0, len(buffer)):
            buffer[i] = cBuffer[i]
        return buffer[0]  # If just a scalar was passed, this returns the single value read from the FPGA register.

    def Write(self, startAddr, buffer):
        '''Write all the words from the buffer to the RAM in the FPGA.'''

        # If buffer is just a scalar ref instead of a list, then make it into a list containing the scalar.
        if type(buffer) != types.ListType:
            buffer = [buffer]
        cBuffer = (c_ulonglong * len(buffer))()  # Create a ctypes buffer the same size as the given buffer.
        # Transfer the values to be written to the FPGA into the ctypes buffer.
        for i in range(0, len(buffer)):
            cBuffer[i] = buffer[i]
        # Write the ctypes buffer to the memory circuit in the FPGA.
        MemWrite(self.mem, c_uint(startAddr), cBuffer,
                 c_uint(len(buffer)))


class Bitvec(list):

    '''Class for storing and manipulating bits.'''
    
    def ___init__(self):
        list.__init__(self)
        
    def __setattr__(self, name, val):
        if name == 'unsigned' or name == 'int':
            v = val
            for i in range(0,len(self)):
                self[i] = (v & 1) and 1 or 0
                v >>= 1
        elif name == 'string':
            v = val[::-1] # Reverse the string so LSB comes first.
            for i in range(0, len(self)):
                self[i] = (v[i] == '1') and 1 or 0
        return val
        
    def __getattr__(self, name):
        if name == 'unsigned':
            val = 0
            for b in reversed(self):
                val = val * 2 + b
        elif name == 'int':
            val = self.unsigned
            if self[-1] == 1:
                val -= (1<<len(self))
        elif name == 'string':
            val = ''.join([str(b) for b in reversed(self)])
        return val

        
class XsDut:

    '''Class for sending inputs to a device-under-test (DUT) and reading back its response.'''

    def __init__(self, usbId, moduleId, inWidths=None, outWidths=None):
        '''Create a comm. channel to the DUT and get its parameters from the FPGA.'''

        cNumInputs = c_uint(0)
        cNumOutputs = c_uint(0)
        # Open a link to the DUT in the FPGA and get the number of inputs and outputs.
        self.dut = DutInit(c_uint(usbId), c_uint(moduleId),
                            byref(cNumInputs), byref(cNumOutputs))
        if self.dut == 0:
            print "Couldn't get a handle for the DUT in the XESS board!"
            sys.exit()
        self.numInputs = cNumInputs.value  # Store number of DUT inputs.
        self.numOutputs = cNumOutputs.value  # Store number of DUT outputs.
        self.SetInWidths(inWidths) # Store the bit widths of inputs.
        self.SetOutWidths(outWidths) # Store the bit widths of outputs.
        
    def SetInWidths(self, inWidths):
        if inWidths == None:
            self.inWidths = [self.numInputs]
        else:
            self.inWidths = inWidths
        
    def SetOutWidths(self, outWidths):
        if outWidths == None:
            self.outWidths = [self.numOutputs]
        else:
            self.outWidths = outWidths
        
    def Read(self):
        '''Read the outputs of the DUT and return them.'''
        
        cOutputs = (c_ubyte * self.numOutputs)()  # Create a ctypes list for storing the outputs.
        DutRead(self.dut, cOutputs, c_uint(self.numOutputs))  # Get the output levels from the DUT.
        if len(self.outWidths) == 1:
            return Bitvec(cOutputs)
        else:
            outputFields = []
            for w in self.outWidths:
                outputFields.append(Bitvec(cOutputs[:w]))
                cOutputs = cOutputs[w:]
            return outputFields

    def Write(self, *inputs):
        '''Write the inputs to the DUT.'''

        cInputs = (c_ubyte * self.numInputs)()  # Create a ctypes list the same size as the given input list.
        in_bits = []
        for i in range(0, len(inputs)):
            field = Bitvec([0] * self.inWidths[i])
            field.unsigned = inputs[i]
            in_bits.extend(field)
        # Transfer the input list into the ctypes buffer.
        for i in range(0, len(cInputs)):
            cInputs[i] = in_bits[i]
        # Write the input values to the DUT in the FPGA.
        DutWrite(self.dut, cInputs, c_uint(self.numInputs))
        
    def Exec(self, *inputs):
        '''Write and then read the DUT.'''
        self.Write(*inputs)
        return self.Read()
