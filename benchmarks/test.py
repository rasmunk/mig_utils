import numpy as np
from mig.io import IDMCShare
from skimage.io import imread
import cv2
import sys
import h5py
import os
import paramiko
import socket
import time
import fs.errors as errors


def run():
    # reader = open('benchmarks/test_image.tiff', 'r')
    # f = reader.read()
    share = IDMCShare('K2wzxDcEBm')
    path = share.geturl('rec_8bit_ph03_cropC_kmeans_scale510.tif')
    with share.open('rec_8bit_ph03_cropC_kmeans_scale510.tif', 'r') as f:
        img = f.read()

    cv2.imshow("image", img)
    cv2.waitKey(0)


def progress(size, file_size):
    amt_transfer = (size / file_size) * 100
    print("{:.1f} %".format(amt_transfer), end="\r")


def sftp_test():
    client = paramiko.SSHClient()
    ssh_config = paramiko.SSHConfig()
    try:
        with open(os.path.realpath(os.path.expanduser('~/.ssh/config'))) as f:
            ssh_config.parse(f)
    except IOError:
        pass

    timeout = 10
    try:
        client.load_system_host_keys()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(
            socket.gethostbyname("io.idmc.dk"),
            username='K2wzxDcEBm',
            password='K2wzxDcEBm'
        )

        if timeout > 0:
            client.get_transport().set_keepalive(timeout)
        sftp = client.open_sftp()
        file_name = 'AVS5M_10X_50keV_LE1_8s_recon_Export.tif'
        sftp.get(file_name, file_name, progress)

    except (paramiko.ssh_exception.SSHException,
            paramiko.ssh_exception.NoValidConnectionsError,
            socket.gaierror, socket.timeout) as e:
        message = "Unable to connect to ssh: {}".format(e)
        raise errors.CreateFailed(message)


if __name__ == '__main__':
    sftp_test()
