import time
import socket
from ssh2.session import Session
from ssh2.sftp import LIBSSH2_FXF_READ, LIBSSH2_SFTP_S_IRUSR


if __name__ == "__main__":
    sharelink = 'K2wzxDcEBm'
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(("io.idmc.dk", 22))
    s = Session()
    s.handshake(sock)
    s.userauth_password(sharelink, sharelink)
    s.open_session()
    sftp = s.sftp_init()
    now = time.time()

    # Reading file
    with sftp.open("AVS5M_10X_50keV_LE1_8s_recon_Export.tif",
                   LIBSSH2_FXF_READ, LIBSSH2_SFTP_S_IRUSR) as fh:
        for size, data in fh:
            pass
    print("Finished file read in {}".format(time.time() - now,))
