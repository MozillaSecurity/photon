#!/usr/bin/env python
# coding: utf-8
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""
A utility for managing RAM disks.
"""
import os
import sys
import logging
import argparse

from core.photon import Photon, PhotonException
from core.config import PhotonConf


class PhotonCommandLine(object):
    """
    Command-line interface for Photon
    """
    HOME = os.path.dirname(os.path.abspath(__file__))
    VERSION = "0.1.0"
    CONFIG_PATH = os.path.relpath(os.path.join(HOME, 'conf'))
    PHOTON_CONFIG = os.path.join(CONFIG_PATH, 'photon.json')

    @classmethod
    def parse_args(cls):
        parser = argparse.ArgumentParser(
            description='Photon Runtime',
            prog=__file__,
            add_help=False,
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
            epilog='The exit status is 0 for non-failures and 1 for failures.')

        m = parser.add_argument_group('Mandatory Arguments')
        g = m.add_mutually_exclusive_group(required=True)
        g.add_argument('-create', action='store_true', help='create')
        g.add_argument('-destroy', metavar='mountpoint', type=str, help='destroy')

        o = parser.add_argument_group('Optional Arguments')
        o.add_argument('-size', metavar='size', type=int, help='size in mega-bytes.')
        o.add_argument('-photon', metavar='file', type=argparse.FileType(), default=cls.PHOTON_CONFIG,
                       help='Photon configuration')
        o.add_argument('-verbosity', metavar='{1..5}', default=2, type=int, choices=list(range(1, 6, 1)),
                       help='Level of verbosity for logging module.')
        o.add_argument('-h', '-help', '--help', action='help', help=argparse.SUPPRESS)
        o.add_argument('-version', action='version', version='%(prog)s {}'.format(cls.VERSION), help=argparse.SUPPRESS)

        return parser.parse_args()

    @staticmethod
    def pair_to_dict(args):
        return dict(kv.split('=', 1) for kv in args)

    @classmethod
    def main(cls):
        args = cls.parse_args()

        logging.basicConfig(format='[Photon] %(asctime)s %(levelname)s: %(message)s',
                            level=args.verbosity * 10,
                            datefmt='%Y-%m-%d %H:%M:%S')

        logging.info('Loading Photon configuration from %s' % args.photon.name)
        try:
            photon_conf = PhotonConf(args.photon.read())
        except PhotonException as e:
            logging.error(e)
            return 1

        photon = Photon(photon_conf)
        try:
            if args.create:
                photon.create(args.size)
            if args.destroy:
                photon.destroy(args.destroy)
        except PhotonException as e:
            logging.error(e)
            return 1
        except KeyboardInterrupt:
            print('')
            logging.info("Caught SIGINT - Aborting.")
            return 0
        finally:
            logging.info("Initiating shutdown routines.")
            try:
                pass
            except PhotonException as e:
                logging.error(e)
                return 1

        return 0


if __name__ == '__main__':
    sys.exit(PhotonCommandLine().main())
