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

print '''\n
##################################################################
# This program tests the interface between the host PC and the FPGA 
# on the XuLA board that has been programmed to act as a blinker.
# You should see the state of the LED displayed on the screen
# flip back-and-forth between one and zero about once per second.
##################################################################
'''
USB_ID = 0  # This is the USB port index for the XuLA board connected to the host PC.
BLINKER_ID = 1  # This is the identifier for the blinker in the FPGA.

# Create a blinker interface object that takes one 1-bit input and has one 1-bit output.
blinker = XsDutIo(USB_ID, BLINKER_ID, [1], [1])

while True: # Do this forever...
    led = blinker.Read() # Read the current state of the LED.
    print 'LED: %1d\r' % led.unsigned, # Print the LED state and return.
