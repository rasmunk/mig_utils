import fs
import six
import socket
from abc import ABCMeta, abstractmethod
from fs.errors import ResourceNotFound
from ssh2.session import Session
from ssh2.sftp import LIBSSH2_FXF_READ, LIBSSH2_FXF_WRITE, LIBSSH2_FXF_CREAT, \
    LIBSSH2_SFTP_S_IRUSR, LIBSSH2_SFTP_S_IWUSR, LIBSSH2_SFTP_S_IRGRP, LIBSSH2_SFTP_S_IROTH, \
    LIBSSH2_FXF_APPEND
from ssh2.utils import wait_socket
from ssh2.error_codes import LIBSSH2_ERROR_EAGAIN


class DataStore(metaclass=ABCMeta):
    _client = None
    _target = ""

    def __init__(self, client):
        """
        :param client:
        This is the sshfs client instance,
        that is used to access the datastore
        """
        self._client = client

    @abstractmethod
    def open(self, path, flag='r'):
        ...

    @abstractmethod
    def read(self, path):
        ...


class SSHFSStore(DataStore):

    def __init__(self, username=None, password=None):
        assert username is not None
        assert password is not None
        client = fs.open_fs(
            "ssh://" + username + ":" + password + self._target)
        super(SSHFSStore, self).__init__(client)

    def geturl(self, path):
        return self._client.geturl(path)

    def list(self, path='.'):
        """
        :param path:
        file system path which items will be returned
        :return:
        A list of items in the path.
        There is no distinction between files and dirs
        """
        return self._client._sftp.listdir(path=path)

    def list_attr(self, path='.'):
        """
        :param path:
        directory path to be listed
        :return:
        A list of .SFTPAttributes objects
        """
        return self._client._sftp.listdir_attr(path=path)

    def read(self, path):
        """
        :param file:
        File to be read
        :return:
        a string of the content within file
        """
        with self._client.open(six.text_type(path)) as open_file:
            return open_file.read()

    def read_binary(self, path):
        """
        :param file:
        File to be read
        :return:
        a binary of the content within file
        """
        with self._client.openbin(six.text_type(path)) as open_file:
            return open_file.read()

    def open(self, path, flag='r'):
        """
        Used to get a python filehandler object
        :param path:
        the name of the file to be opened
        :param flag:
        which mode should the file be opened in
        :return:
        a _io.TextIOWrapper object with utf-8 encoding
        """
        return self._client.open(six.text_type(path), flag)

    def remove(self, path):
        """
        :param path:
        path to the file that should be removed
        :return:
        Bool, whether a file was removed or not
        """
        try:
            self._client.remove(path=six.text_type(path))
            return True
        except ResourceNotFound:
            return False

    def removedir(self, path):
        """
        :param path:
        path the dir that should be removed
        :return:
        Bool, whether a dir was removed or not
        """
        try:
            self._client.removedir(path=six.text_type(path))
            return True
        except ResourceNotFound:
            return False


class SFTPStore(DataStore):

    def __init__(self, username=None, password=None):
        assert username is not None
        assert password is not None

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self._target, 22))
        s = Session()
        s.handshake(sock)
        s.userauth_password(username, password)
        s.open_session()
        client = s.sftp_init()
        super(SFTPStore, self).__init__(client=client)

    def list(self, path='/'):
        with self._client.opendir(path) as fh:
            return [name.decode('utf-8') for size, name, attrs in fh.readdir()]

    def open(self, path, flag='r'):
        if flag == 'r':
            return self._client.open(six.text_type(path), LIBSSH2_FXF_READ, LIBSSH2_SFTP_S_IWUSR)
        else:
            w_flags = None
            if flag == 'w':
                w_flags = LIBSSH2_FXF_CREAT | LIBSSH2_FXF_WRITE
            elif flag == 'a':
                w_flags = LIBSSH2_FXF_CREAT | LIBSSH2_FXF_WRITE | LIBSSH2_FXF_APPEND
            mode = LIBSSH2_SFTP_S_IRUSR | \
                   LIBSSH2_SFTP_S_IWUSR | \
                   LIBSSH2_SFTP_S_IRGRP | \
                   LIBSSH2_SFTP_S_IROTH
            return self._client.open(six.text_type(path), w_flags, mode)

    def read(self, path):
        return self.read_binary(six.text_type(path)).decode('utf-8')

    def read_binary(self, path):
        with self.open(six.text_type(path)) as fh:
            size, data = fh.read()
            return data

    def remove(self, path):
        self._client.unlink(six.text_type(path))

    def write(self, path, data, flag='a'):
        with self.open(six.text_type(path), flag) as fh:
            if type(data) == bytes:
                fh.write(data)
            elif type(data) == str:
                fh.write(six.b(data))
            else:
                fh.write(six.b(str(data)))

# class AsyncSFTPStore(SFTPStore):
#
#      def __init__(self, username=None, password=None):
#          super(AsyncSFTPStore, self).__init__(username, password)
#
#     async def open(self, filename):



class ERDA:
    url = "io.erda.dk"


class IDMC:
    url = "io.idmc.dk"


# TODO -> cleanup duplication
class ErdaShare(SSHFSStore):

    def __init__(self, share_link):
        """
        :param share_link:
        This is the sharelink ID that is used to access the datastore,
        an overview over your sharelinks can be found at
        https://erda.dk/wsgi-bin/sharelink.py.
        """
        self._target = "@" + ERDA.url + "/"
        super(ErdaShare, self).__init__(username=share_link, password=share_link)


class ErdaSftpShare(SFTPStore):

    def __init__(self, username=None, password=None):
        self._target = ERDA.url
        super(ErdaSftpShare, self).__init__(username, password)


# TODO -> cleanup duplication
class IDMCShare(SSHFSStore):

    def __init__(self, share_link, **options):
        """
        :param share_link:
        This is the sharelink ID that is used to access the datastore,
        an overview over your sharelinks can be found at,
        https://erda.dk/wsgi-bin/sharelink.py.
        """
        self._target = "@" + IDMC.url + "/"
        super(IDMCShare, self).__init__(username=share_link, password=share_link)


class IDMCSftpShare(SFTPStore):

    def __init__(self, username=None, password=None):
        self._target = IDMC.url
        super(IDMCSftpShare, self).__init__(username, password)




# class ErdaHome(DataStore):
#     _target = ERDA.url
#
#     # TODO -> switch over to checking the OPENID session instead of username/password
#     def __init__(self, username, password):
#         """
#         :param username:
#         The username to the users ERDA home directory,
#         as can be found at https://erda.dk/wsgi-bin/settings.py?topic=sftp
#         :param password:
#         Same as user but the speficied password instead
#         """
#         client = SSHFS(ErdaHome._target, user=username, passwd=password)
#         super(ErdaHome, self).__init__(client=client)
