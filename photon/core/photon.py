# coding: utf-8
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
import os
import random
import logging
import subprocess

class PhotonException(Exception):
    """
    Unrecoverable error in Photon.
    """
    pass


class Darwin(object):
    """
    Handler class for platform Darwin.
    """

    def create(self, size, name=None):
        sectors = 2048 * size

        if name is None:
            name = Photon.random_id()

        try:
            mountpoint = subprocess.check_output([
                'hdiutil', 'attach', '-nomount', 'ram://{}'.format(sectors)
            ])
        except subprocess.CalledProcessError as e:
            raise PhotonException(e)

        mountpoint = mountpoint.strip()

        try:
            subprocess.check_call([
                'diskutil', 'erasevolume', 'HFS+', name, mountpoint
            ])
        except subprocess.CalledProcessError as e:
            raise PhotonException(e)

        logging.info('JSON: {{"mountpoint": "{}"}}'.format(mountpoint))

        return mountpoint

    def destroy(self, mountpoint):
        try:
            subprocess.check_call(['umount', '-f', mountpoint])
        except subprocess.CalledProcessError as e:
            raise PhotonException(e)

        try:
            subprocess.check_call(['hdiutil', 'detach', mountpoint])
        except subprocess.CalledProcessError as e:
            raise PhotonException(e)


class Linux(object):
    """
    Handler class for platform Linux.
    """

    BASEPATH = "/tmp"

    def create(self, size, name=None):
        if name is None:
            while True:
                mountpoint = os.path.join(Linux.BASEPATH, Photon.random_id())
                if not os.path.exists(mountpoint):
                    break
        else:
            mountpoint = os.path.join(Linux.BASEPATH, name)
            if os.path.exists(mountpoint):
                raise PhotonException(
                    'Mount point {} exists'.format(mountpoint))

        os.mkdir(mountpoint)

        try:
            subprocess.check_call([
                'mount',
                '-t', 'tmpfs',
                '-o',
                'size={}m'.format(size),
                'tmpfs',
                mountpoint
            ])
        except subprocess.CalledProcessError as e:
            raise PhotonException(e)

        logging.info('JSON: {{"mountpoint": "{}"}}'.format(mountpoint))

        return mountpoint

    def destroy(self, mountpoint):
        try:
            subprocess.check_call(['umount', mountpoint])
            if os.path.exists(mountpoint):
                os.rmdir(mountpoint)
        except subprocess.CalledProcessError as e:
            raise PhotonException(e)


class Photon(object):
    """
    Photon base class.
    """

    def __init__(self, conf):
        self.conf = conf
        self.platform_id = os.sys.platform.capitalize()
        if self.platform_id not in globals():
            raise PhotonException(
                "Platform '{}' is not supported.".format(self.platform_id))
        else:
            self.platform = globals()[self.platform_id]

    def create(self, size, name=None):
        disk = self.platform()
        disk.create(size, name)

    def destroy(self, mountpoint):
        disk = self.platform()
        disk.destroy(mountpoint)

    @staticmethod
    def random_id():
        return 'photon_{0:0>6x}'.format(random.randint(0, 0xffffff))
