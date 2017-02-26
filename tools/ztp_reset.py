#!/usr/bin/env python

"""This script will issue a 'write erase' command on a switch
and removes configuration/reloads with ZTP enabled"""

# TODO: Need to fix the reload now function - at the moment eAPI times out waiting for ACK. This is silly.

from getpass import getpass
import pyeapi
import argparse


def get_args():
    parser = argparse.ArgumentParser(
        description='Issue a write erase command on a switch and removes configuration/reloads with ZTP enabled')
    parser.add_argument('-u', '--user',
                        type=str,
                        help='Switch username - must have privilege 15. Default is admin',
                        default='admin',
                        required=True)
    parser.add_argument('-i', '--ip',
                        type=str,
                        help='Switch IP Addresses',
                        nargs='*',
                        required=True)
    args = parser.parse_args()
    return args


def erase(username, password, *args):
    for arg in args:
        node = pyeapi.connect(host=arg, username=username, password=password, return_node=True)
        node.enable('delete flash:/zerotouch-config')
        node.enable('write erase')
        node.enable('reload now')
        print "Resetting " + arg


def main():
    argu = get_args()

    password = getpass("Enter your switch password: ")

    erase(argu.user, password, *argu.ip)


if __name__ == "__main__":
    main()
