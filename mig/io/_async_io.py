from ._io import SFTPStore, SFTPFileHandle


class AsyncSFTPHandle(SFTPFileHandle):

    def __init__(self, fh, name):
        super().__init__(fh, name)

    def __iter__(self):
        return super().__iter__()

    def __next__(self):
        return super().__next__()

    def __enter__(self):
        return super().__enter__()

    def __exit__(self, exc_type, exc_val, exc_tb):
        super().__exit__(exc_type, exc_val, exc_tb)

    def close(self):
        super().close()

    def read(self, n: int = -1):
        return super().read(n)

    def write(self, path, data, flag='w'):
        super().write(path, data, flag)

    def seek(self, offset):
        super().seek(offset)

    def read_binary(self, n: int = -1):
        return super().read_binary(n)

    def tell(self):
        return super().tell()


class AsyncSFTPStore:
    pass