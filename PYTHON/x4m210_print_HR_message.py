#!/usr/bin/env python
""" \example x4m210_print_HR_message.py

# Target module:
# X4M210

# Introduction:
# This is an example of how to print out Heart Rate and Respiration output from X4M210 module.

# prerequisite:
# ModuleConnector python lib is installed, check XeThruSensorsIntroduction application note to get detail

# Command to run:
# Use "python x4m210_print_HR_message.py" to print application message. If device is not be automatically recognized,add argument "-d com8" to specify device. change "com8" with your device name, using "--help" to see other options. Using TCP server address as device name is also supported by specify TCP address like "-d tcp://192.168.1.169:3000". Adding "-r" to enable recording during application messages printing out.
"""
from __future__ import print_function, division
import sys
from optparse import OptionParser

from pymoduleconnector import *
from pymoduleconnector.extras.auto import auto


def print_x4m210_messages(device_name):
    mc = ModuleConnector(device_name)

    x4m210 = mc.get_x4m200()

    x4m210.load_profile(0x6b5c1609)

    x4m210.set_detection_zone(0.4, 1.0)
    #x4m210.set_output_control(0x20020102, 1)
    x4m210.set_noisemap_control(6)

    x4m210.set_sensor_mode(0x1, 0)

    import time
    while True:
        if x4m210.peek_message_vital_signs():
            vs = x4m210.read_message_vital_signs()

            print("------------------------------------------------")
            print("Vital Signs Message")
            print("Frame Counter = " + str(vs.frame_counter))
            print("Sensor State = " + str(vs.sensor_state))
            print("")
            print("Respiration Rate = " + str(vs.respiration_rate))
            print("Respiration Distance = " + str(vs.respiration_distance))
            print("Respiration Confidence = " + str(vs.respiration_confidence))
            print("")
            print("Heart Rate = " + str(vs.heart_rate))
            print("Heart Distance = " + str(vs.heart_distance))
            print("Heart Confidence = " + str(vs.heart_confidence))
            print("")
            """
            print("Normalized Movement Slow = " + str(normalized_movement_slow))
            print("Normalized Movement Fast = " + str(normalized_movement_fast))
            print("Normalized Movement Start = " + str(normalized_movement_start))
            print("Normalized Movement End = " + str(normalized_movement_end))
            """
            print("------------------------------------------------")
            print("")


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
    print_x4m210_messages(device_name)


if __name__ == "__main__":
    main()
