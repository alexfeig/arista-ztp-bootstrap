#!/usr/bin/env python

"""This script is copied to a switch and executed. It does things"""

import logging
import time


def main():
    while True:
        print "This prints once a minute."
        time.sleep(60)


if __name__ == "__main__":
    main()
