#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Copyright (C) 2016 Zhao Xin 赵鑫 <pythonchallenge@qq.com>
#
# STC-GO (宏晶STC8051系列单片机烧写程序)
# 作者：赵鑫

import sys
import argparse

STCGO_DESCRIPTION = ("stcgo, a command line program flash tool for STC 8051 "
                     "series microcontroller.\n"
                     "https://github.com/archtaurus/stcgo")
STCGO_DEFAULT_PORT = {"win32": "COM3",                                  # WIN
                      "darwi": "/dev/tty.usbserial",                    # MACOS
                      "linux": "/dev/ttyUSB0"}.get(sys.platform[:5])    # LINUX


class STCGO(object):

    def __init__(self):
        pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=STCGO_DESCRIPTION)
    parser.add_argument("name", help="what is your name?", type=str)
    args = parser.parse_args()
    print "Hello, %s!" % args.name
