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
# Read the summation of the address * data products from the
# FSM + SDRAM application on the XuLA board.
##################################################################
'''
USB_ID = 0  # This is the USB port index for the XuLA board connected to the host PC.
DUT_ID = 255  # This is the default identifier for the DUT in the FPGA.

# Create an interface object to the FPGA with one 16-bit input and one 1-bit output.
dut = XsDutIo(USB_ID, DUT_ID, [16], [1])
sum = dut.Read(); # Read the 16-bit summation from the FPGA.
print 'Sum = %d\r' % sum.unsigned
