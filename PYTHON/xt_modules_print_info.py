#!/usr/bin/env python
""" \example xt_module_print_info.py

# Target module:
# X4M200
# X4M300
# X4M03(XEP)

# Introduction:
# This is an example of how to print out XeThru Module infromation.

# prerequisite:
# ModuleConnector python lib is installed, check XeThruSensorsIntroduction application note to get detail

# Command to run:
# Use "xt_module_print_info.py" directly. If device is not be automatically recognized,add argument "-d com8" to specify device. change "com8" with your device name.

"""
from __future__ import print_function, division
import sys
from optparse import OptionParser

import pymoduleconnector
from pymoduleconnector import ModuleConnector
from pymoduleconnector.extras.auto import auto
from pymoduleconnector.ids import *


def print_module_info(device_name):
    # Stop running application and set module in manual mode.
    mc = ModuleConnector(device_name)
    app = mc.get_x4m200()
    # we have to go to manual mode
    # app.set_sensor_mode(XTS_SM_STOP, 0)
    # app.set_sensor_mode(XTS_SM_MANUAL, 0)
    # Stop running application and set module in manual mode.
    try:
        app.set_sensor_mode(XTS_SM_STOP, 0)  # Make sure no profile is running.
    except RuntimeError:
        # Profile not running, OK
        pass
    try:
        app.set_sensor_mode(XTS_SM_MANUAL, 0)  # Manual mode.
    except RuntimeError:
        # Maybe already running at X4driver level
        pass
    xep = mc.get_xep()
    pong = xep.ping()
    print("")
    print("********** XeThru Module Information **********")
    print("")
    print('Received pong=', hex(pong) + ' connection build!')
    print('FirmWareID =', xep.get_system_info(XTID_SSIC_FIRMWAREID))
    print('Version =', xep.get_system_info(XTID_SSIC_VERSION))
    print('Build =', xep.get_system_info(XTID_SSIC_BUILD))
    print('VersionList =', xep.get_system_info(XTID_SSIC_VERSIONLIST))

    # Following three item only supported by XeThru Sensor, e.g.X4M200, X4M300. X4M03 does not these information and will feedback error message when read.
    try:
        OrderCode = "X4Mxx"
        OrderCode = xep.get_system_info(XTID_SSIC_ORDERCODE)
        print('OrderCode =', OrderCode)
        print('ItemNumber =', xep.get_system_info(XTID_SSIC_ITEMNUMBER))
        print('SerialNumber =', xep.get_system_info(XTID_SSIC_SERIALNUMBER))
    except:
        # This is not a sensor but a development kit running XEP.
        pass
    mc.close()
    return OrderCode


def print_x4_settings(xep):
    # Check values (to confirm we have the values we want):
    print("")
    print("********** Current X4 settings **********")
    print("")
    print("iterations: " + str(xep.x4driver_get_iterations()))
    print("pulses_per_step: " + str(xep.x4driver_get_pulses_per_step()))
    print("dac_step: " + str(xep.x4driver_get_dac_step()))
    print("dac_min: " + str(xep.x4driver_get_dac_min()))
    print("dac_max: " + str(xep.x4driver_get_dac_max()))
    print("prf_div: " + str(xep.x4driver_get_prf_div()))
    print("tx_power: " + str(xep.x4driver_get_tx_power()))
    print("tx_center_frequency: " + str(xep.x4driver_get_tx_center_frequency()))
    print("downconversion: " + str(xep.x4driver_get_downconversion()))
    print("Frame area offset: " + str(xep.x4driver_get_frame_area_offset()))
    frame_area = xep.x4driver_get_frame_area()
    print("Frame Area: " + str(frame_area.start) + " to " + str(frame_area.end))


def main():
    parser = OptionParser()
    parser.add_option(
        "-d",
        "--device",
        dest="device_name",
        help="Seral port name used by target XeThru sensor, i.e com8, /dev/ttyACM0",
        metavar="FILE")

    (options, args) = parser.parse_args()
    if options.device_name:
        device_name = options.device_name
    else:
        try:
            device_name = auto()[0]
        except:
            print("Fail to find serial port, please specify it by use -d!")
            raise

    print_module_info(device_name)


if __name__ == "__main__":
    main()