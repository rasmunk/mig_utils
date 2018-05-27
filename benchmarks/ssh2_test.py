import os
import math
import hashlib
import sys
import time
import socket
import mig.io
from ssh2.session import Session
from ssh2.sftp import LIBSSH2_FXF_READ, LIBSSH2_FXF_WRITE, LIBSSH2_FXF_CREAT, \
    LIBSSH2_SFTP_S_IRUSR, LIBSSH2_SFTP_S_IWUSR, LIBSSH2_SFTP_S_IRGRP, LIBSSH2_SFTP_S_IROTH


def current_milli_time():
    return int(round(time.time() * 1000))


def print_progress(total_size, transfer_counter, start_time, size):
    current_time = time.time()
    transfer_counter += size
    percentage = (total_transfer / total_size) * 100

    mb_interval += size * pow(10, -6)
    sec_interval = current_time - sec_delta
    print("Progress {:.1f} % {:.2f} MB/s".format(percentage, mb_interval / sec_interval), end='\r')

    if sec_interval > 10.0:
        sec_interval = 0
        sec_delta = current_time
        mb_interval = 0.0


if __name__ == "__main__":
    sharelink = 'I8gkG328a5'
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(("io.idmc.dk", 22))
    s = Session()
    s.handshake(sock)
    s.userauth_password(sharelink, sharelink)
    s.open_session()
    sftp = s.sftp_init()
    start = time.time()

    #total_size = sftp.lstat("AVS5M_10X_50keV_LE1_8s_recon_Export.tif").filesize
    transfer_counter = 0

    sec_delta = time.time()
    sec_interval = 0
    mb_interval = 0.0
    # Reading file
    share = mig.io.IDMCSftpShare(sharelink, sharelink)
    write_file = "write_test"
    content = share.read('fisk')
    with share.open(write_file, 'w') as w_file:
        w_file.write(b'sdfsdfsf')

    write_content = share.read(write_file)
    print(write_content)
    share.remove(write_file)


    # with sftp.open("AVS5M_10X_50keV_LE1_8s_recon_Export.tif",
    #                LIBSSH2_FXF_READ, LIBSSH2_SFTP_S_IRUSR) as fh, \
    #         open('read_test_file.tif', 'wb') as local_file:
    #         for size, data in fh:
    #             current_time = time.time()
    #             transfer_counter += size
    #             percentage = (transfer_counter / total_size) * 100
    #
    #             mb_interval += size * pow(10, -6)
    #             sec_interval = current_time - sec_delta
    #             print("Progress {:.1f} % {:.2f} MB/s".format(percentage, mb_interval / sec_interval), end='\r')
    #             if sec_interval > 10.0:
    #                 sec_interval = 0
    #                 sec_delta = current_time
    #                 mb_interval = 0.0
    #
    #             local_file.write(data)
    #
    # print("Finished file read in {}".format(time.time() - start,))
    assert total_size == os.path.getsize('read_test_file.tif')

    mode = LIBSSH2_SFTP_S_IRUSR | \
           LIBSSH2_SFTP_S_IWUSR | \
           LIBSSH2_SFTP_S_IRGRP | \
           LIBSSH2_SFTP_S_IROTH
    flags = LIBSSH2_FXF_CREAT | LIBSSH2_FXF_WRITE

    write_start = time.time()
    sec_delta = time.time()
    transfer_counter = 0
    total_size = os.path.getsize("read_test_file.tif")
    write_size = pow(2, 15)
    mb_interval = 0.0

    read_digest = hashlib.sha1(open('read_test_file.tif', 'rb').read(33554432)).hexdigest()

    with open('read_test_file.tif', 'rb') as local_file, \
            sftp.open('upload_test.tif', flags, mode) as remote_fh:
        for data in iter(lambda: local_file.read(write_size), b''):
            remote_fh.write(data)
            size = sys.getsizeof(data)
            transfer_counter += size
            percentage = (transfer_counter / total_size) * 100

            mb_interval += size * pow(10, -6)
            sec_interval = time.time() - sec_delta
            mb_s = mb_interval / sec_interval

            print("Progress {:.1f} % {:.2f} MB/s".format(percentage, mb_s), end='\r')
            if sec_interval > 10.0:
                sec_interval = 0
                sec_delta = time.time()
                mb_interval = 0.0

    print("Finished file transfer in {}".format(time.time() - write_start))