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

from xstools.xsdutio import *  # Import funcs/classes for PC <=> FPGA link.
from random import *  # Import some random number generator routines.

print '''
##################################################################
# This program tests the interface between the host PC and the FPGA 
# on the XuLA board that has been programmed to act as a subtractor.
##################################################################
'''

USB_ID = 0  # USB port index for the XuLA board connected to the host PC.
SUBTRACTOR_ID = 4  # This is the identifier for the subtractor in the FPGA.

# Create a subtractor intfc obj with two 8-bit inputs and one 8-bit output.
subtractor = XsDut(USB_ID, SUBTRACTOR_ID, [8, 8], [8])

# Test the subtractor by iterating through some random inputs.
for i in range(0, 100):
    minuend = randint(0, 127)  # Get a random, positive byte...
    subtrahend = randint(0, 127)  # And subtract this random byte from it.
    diff = subtractor.Exec(minuend, subtrahend)  # Use the subtractor in FPGA.
    print '%3d - %3d = %4d' % (minuend, subtrahend, diff.int),
    if diff.int == minuend - subtrahend:  # Compare Python result to FPGA's.
        print '==> CORRECT!'  # Print this if the differences match.
    else:
        print '==> ERROR!!!'  # Oops! Something's wrong with the subtractor.
