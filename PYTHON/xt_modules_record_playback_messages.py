#!/usr/bin/env python
""" \example xt_modules_record_playback_messages.py

# Target module:
#X4M200
#X4M300
#X4M03(XEP)

# Introduction:
# This is an example of how to record and play back XeThru Module output data.

# prerequisite:
# ModuleConnector python lib is installed, check XeThruSensorsIntroduction application note to get detail

# Command to run:
# 1. Use "xt_modules_record_playback_messages.py -r" directly. If device is not be automatically recognized,add argument "-d com8" to specify device. change "com8" with your device name.
# 2. Use "xt_modules_record_playback_messages.py -f xethru_recording_xxxx/xethru_recording_meta.dat" to configure player, need plot or print funciton to show recording data, so start_player is used by other examples.
"""
from __future__ import print_function, division
import sys
from optparse import OptionParser

import pymoduleconnector
from pymoduleconnector import ModuleConnector
from pymoduleconnector import DataType
from pymoduleconnector import DataRecorder
from pymoduleconnector import DataPlayer
from pymoduleconnector import RecordingOptions
from pymoduleconnector.extras.auto import auto
from pymoduleconnector.ids import *


def start_record(mc):

    def on_file_available(data_type, filename):
        print("Recording data message file available for data type: {}".format(data_type))
        print("  |- file: {}".format(filename))

    def on_meta_file_available(session_id, meta_filename):
        print("Recording meta file available with id: {}".format(session_id))
        print("  |- file: {}".format(meta_filename))
    directory = "."
    recorder = mc.get_data_recorder()
    recorder.subscribe_to_file_available(
        pymoduleconnector.AllDataTypes, on_file_available)
    recorder.subscribe_to_meta_file_available(on_meta_file_available)
    recorder.start_recording(pymoduleconnector.AllDataTypes, directory)


def start_player(meta_filename, depth=-1):
    print("start playback from: {}, depth: {}".format(meta_filename, depth))
# ! [Typical usage]
    player = DataPlayer(meta_filename, depth)
    dur = player.get_duration()
    print("Duration(ms): {}".format(dur))
    mc = ModuleConnector(player, log_level=0)
    # Control output
    player.set_filter(pymoduleconnector.AllDataTypes)
    player.set_playback_rate(1.0)
    player.set_loop_mode_enabled(True)
    player.play()
    print("Player start to palyback data. If print or plot function is configured, it should start to work!")
    return player


def main():
    parser = OptionParser()
    parser.add_option(
        "-d",
        "--device",
        dest="device_name",
        help="Seral port name used by target XeThru sensor, i.e com8, /dev/ttyACM0",
        metavar="FILE")
    parser.add_option(
        "-r",
        "--record",
        action="store_true",
        default=False,
        dest="record",
        help="Enable recording")
    parser.add_option(
        "-f",
        "--file",
        dest="meta_filename",
        metavar="FILE",
        help="meta file from recording")

    (options, args) = parser.parse_args()

    if not options.meta_filename:
        if options.device_name:
            device_name = options.device_name
        else:
            try:
                device_name = auto()[0]
            except:
                print("Fail to find serial port, please specify it by use -d!")
                raise
        mc = ModuleConnector(device_name)
        start_record(mc)
    else:
        start_player(meta_filename=options.meta_filename)


if __name__ == "__main__":
    main()
