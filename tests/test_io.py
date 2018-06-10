import unittest
import sys
import os
import six
import _io
import time
from random import random
from mig.io import ERDASSHFSShare, ERDASftpShare, \
    IDMCSSHFSShare, IDMCSftpShare, SFTPFileHandle

# Test input
try:
    with open('res/sharelinks.txt', 'r') as file:
        content = file.readlines()
    assert content is not None
    assert len(content) > 0
    sharelinks = dict((tuple(line.rstrip().split('=') for line in content)))
except IOError:
    # Travis
    assert 'ERDA_TEST_SHARE' in os.environ
    assert 'IDMC_TEST_SHARE' in os.environ

    sharelinks = {'ERDA_TEST_SHARE': os.environ['ERDA_TEST_SHARE'],
                  'IDMC_TEST_SHARE': os.environ['IDMC_TEST_SHARE']}


class ERDASSHFSShareTest(unittest.TestCase):
    share = None

    def setUp(self):
        # Open connection to a sharelink
        assert 'ERDA_TEST_SHARE' in sharelinks
        self.share = ERDASSHFSShare(sharelinks['ERDA_TEST_SHARE'])
        self.seed = str(random())[2:10]
        self.tmp_file = "".join(["tmp", self.seed])
        self.write_file = "".join(["write_test", self.seed])
        self.binary_file = "".join(['binary_test', self.seed])

    def tearDown(self):
        self.share.remove(self.tmp_file)
        self.share.remove(self.write_file)
        self.share.remove(self.binary_file)
        self.share = None

    def test_share(self):
        # List files/dirs in share
        self.share.write(self.tmp_file, six.text_type("sddsfsf"))
        self.assertIn(self.tmp_file, self.share.list())
        # Read file directly as string
        self.assertEqual(self.share.read(self.tmp_file), 'sddsfsf')
        # Read file directly as binary
        self.assertEqual(self.share.read_binary(self.tmp_file), b'sddsfsf')

        # Get a _io.TextIOWrapper object with automatic close
        with self.share.open(self.tmp_file, 'r') as fh:
            self.assertEqual(fh.read(), 'sddsfsf')

        # Get a default _io.TextIOWrapper object with manual lifetime
        fh = self.share.open(self.tmp_file, 'r')
        self.assertIsInstance(fh, _io.TextIOWrapper)
        self.assertEqual(fh.read(), 'sddsfsf')
        fh.close()

        # Writing strings to a file
        # six -> ensure py2/3 compatibility
        test_string = six.text_type('Hello There')
        test_num = six.text_type(42342342)
        test_float = six.text_type(3434.231)

        with self.share.open(self.write_file, 'w') as w_file:
            w_file.write(test_string)
            w_file.write(test_num)
            w_file.write(test_float)

        self.assertIn(test_string, self.share.read(self.write_file))
        self.assertIn(str(test_num), self.share.read(self.write_file))
        self.assertIn(str(test_float), self.share.read(self.write_file))

        # Writing binary to a file
        test_binary = b'Hello again'
        test_b_num = six.int2byte(255)
        with self.share.open(self.binary_file, 'wb') as b_file:
            b_file.write(test_binary)
            b_file.write(test_b_num)

        self.assertIn(test_binary, self.share.read_binary(self.binary_file))
        self.assertIn(test_b_num, self.share.read_binary(self.binary_file))


class IDMCSSHFSShareTest(unittest.TestCase):
    share = None

    def setUp(self):
        # Open connection to a sharelink
        assert 'IDMC_TEST_SHARE' in sharelinks
        self.share = IDMCSSHFSShare(sharelinks['IDMC_TEST_SHARE'])
        self.seed = str(random())[2:10]
        self.tmp_file = "".join(["tmp", self.seed])
        self.write_file = "".join(["write_test", self.seed])
        self.binary_file = "".join(['binary_test', self.seed])

    def tearDown(self):
        self.share.remove(self.tmp_file)
        self.share.remove(self.write_file)
        self.share.remove(self.binary_file)
        self.share = None

    def test_share(self):
        # List files/dirs in share
        self.share.write(self.tmp_file, six.text_type("sddsfsf"))
        self.assertIn(self.tmp_file, self.share.list())
        # Read file directly as string
        self.assertEqual(self.share.read(self.tmp_file), 'sddsfsf')
        # Read file directly as binary
        self.assertEqual(self.share.read_binary(self.tmp_file), b'sddsfsf')

        # Get a _io.TextIOWrapper object with automatic close
        with self.share.open(self.tmp_file, 'r') as fh:
            self.assertEqual(fh.read(), 'sddsfsf')

        # Get a default _io.TextIOWrapper object with manual lifetime
        fh = self.share.open(self.tmp_file, 'r')
        self.assertIsInstance(fh, _io.TextIOWrapper)
        self.assertEqual(fh.read(), 'sddsfsf')
        fh.close()

        # Writing strings to a file
        # six -> ensure py2/3 compatibility
        test_string = six.text_type('Hello There')
        test_num = six.text_type(42342342)
        test_float = six.text_type(3434.231)

        with self.share.open(self.write_file, 'w') as w_file:
            w_file.write(test_string)
            w_file.write(test_num)
            w_file.write(test_float)

        self.assertIn(test_string, self.share.read(self.write_file))
        self.assertIn(str(test_num), self.share.read(self.write_file))
        self.assertIn(str(test_float), self.share.read(self.write_file))

        # Writing binary to a file
        test_binary = b'Hello again'
        test_b_num = six.int2byte(255)
        with self.share.open(self.binary_file, 'wb') as b_file:
            b_file.write(test_binary)
            b_file.write(test_b_num)

        self.assertIn(test_binary, self.share.read_binary(self.binary_file))
        self.assertIn(test_b_num, self.share.read_binary(self.binary_file))


class ERDASFTPShareTest(unittest.TestCase):
    share = None

    def setUp(self):
        assert 'ERDA_TEST_SHARE' in sharelinks
        self.share = ERDASftpShare(sharelinks['ERDA_TEST_SHARE'],
                                   sharelinks['ERDA_TEST_SHARE'])
        self.seed = str(random())[2:10]
        self.tmp_file = "".join(["tmp", self.seed])
        self.write_file = "".join(["write_test", self.seed])
        self.binary_file = "".join(['binary_test', self.seed])
        self.write_image = "".join(["kmeans_write.tif", self.seed])
        self.img = "kmeans.tif"

    def tearDown(self):
        self.share.remove(self.tmp_file)
        self.share.remove(self.write_file)
        self.share.remove(self.binary_file)
        self.share.remove(self.write_image)
        self.assertNotIn(self.write_image, self.share.list())
        self.share = None

    def test_share(self):
        tmp_share = self.share.open(self.tmp_file, 'w')
        tmp_share.write(six.text_type("sddsfsf"))
        tmp_share.close()
        self.assertIn(self.tmp_file, self.share.list())

        # Read file directly as string
        tmp_share = self.share.open(self.tmp_file, 'r')
        self.assertEqual(tmp_share.read(), "sddsfsf")
        tmp_share.close()

        # Read file directly as binary
        tmp_share = self.share.open(self.tmp_file, 'rb')
        self.assertEqual(tmp_share.read(), b'sddsfsf')
        tmp_share.close()

        # Get a SFTPHandle object with automatic close
        with self.share.open(self.tmp_file, 'r') as tmp:
            self.assertEqual(tmp.read(), "sddsfsf")

        # Get a default SFTPHandle object with manual lifetime
        fh = self.share.open(self.tmp_file, 'r')
        self.assertIsInstance(fh, SFTPFileHandle)
        self.assertEqual(fh.read(), "sddsfsf")
        fh.close()

        # Writing strings to a file
        test_string = "Hello There"
        test_num = 42342342
        test_float = 4234.234324

        with self.share.open(self.write_file, 'a') as w_file:
            w_file.write(six.b(test_string))
            w_file.write(six.b(str(test_num)))
            w_file.write(six.b(str(test_float)))

        with self.share.open(self.write_file, 'r') as w_file:
            f_content = w_file.read()
            self.assertIn(test_string, f_content)
            self.assertIn(six.text_type(test_num), f_content)
            self.assertIn(six.text_type(test_float), f_content)

        # Writing binary to a file
        test_binary = b'Hello again'
        test_b_num = six.int2byte(255)
        with self.share.open(self.binary_file, 'ab') as b_file:
            b_file.write(test_binary)
            b_file.write(test_b_num)

        b_file = self.share.open(self.binary_file, 'rb')
        f_content = b_file.read()
        self.assertIn(test_binary, f_content)
        self.assertIn(test_b_num, f_content)
        b_file.close()

        # Read 100 mb image
        with self.share.open(self.img, 'rb') as b_file:
            img = b_file.read()
            self.assertGreaterEqual(sys.getsizeof(img), 133246888)

            # write 100 mb image
            with self.share.open(self.write_image, 'wb') as new_b_file:
                new_b_file.write(img)

            # check that it is written
            with self.share.open(self.write_image, 'rb') as new_b_file:
                new_image = new_b_file.read()
                self.assertGreaterEqual(sys.getsizeof(new_image), 133246888)


class IDMCSftpShareTest(unittest.TestCase):
    share = None

    def setUp(self):
        assert 'IDMC_TEST_SHARE' in sharelinks
        self.share = IDMCSftpShare(sharelinks['IDMC_TEST_SHARE'],
                                   sharelinks['IDMC_TEST_SHARE'])
        self.seed = str(random())[2:10]
        self.tmp_file = "".join(["tmp", self.seed])
        self.write_file = "".join(["write_test", self.seed])
        self.binary_file = "".join(["binary_test", self.seed])
        self.write_image = "".join(["kmeans_write.tif", self.seed])
        self.img = "kmeans.tif"

    def tearDown(self):
        self.share.remove(self.tmp_file)
        self.share.remove(self.write_file)
        self.share.remove(self.binary_file)
        self.share.remove(self.write_image)
        self.share = None

    def test_share(self):
        tmp_share = self.share.open(self.tmp_file, 'w')
        tmp_share.write(six.text_type("sddsfsf"))
        tmp_share.close()
        self.assertIn(self.tmp_file, self.share.list())

        # Read file directly as string
        tmp_share = self.share.open(self.tmp_file, 'r')
        self.assertEqual(tmp_share.read(), "sddsfsf")
        tmp_share.close()

        # Read file directly as binary
        tmp_share = self.share.open(self.tmp_file, 'rb')
        self.assertEqual(tmp_share.read(), b'sddsfsf')
        tmp_share.close()

        # Get a SFTPHandle object with automatic close
        with self.share.open(self.tmp_file, 'r') as tmp:
            self.assertEqual(tmp.read(), "sddsfsf")

        # Get a default SFTPHandle object with manual lifetime
        fh = self.share.open(self.tmp_file, 'r')
        self.assertIsInstance(fh, SFTPFileHandle)
        self.assertEqual(fh.read(), "sddsfsf")
        fh.close()

        # Writing strings to a file
        test_string = "Hello There"
        test_num = 42342342
        test_float = 4234.234324

        with self.share.open(self.write_file, 'a') as w_file:
            w_file.write(six.b(test_string))
            w_file.write(six.b(str(test_num)))
            w_file.write(six.b(str(test_float)))

        with self.share.open(self.write_file, 'r') as w_file:
            f_content = w_file.read()
            self.assertIn(test_string, f_content)
            self.assertIn(six.text_type(test_num), f_content)
            self.assertIn(six.text_type(test_float), f_content)

        # Writing binary to a file
        test_binary = b'Hello again'
        test_b_num = six.int2byte(255)
        with self.share.open(self.binary_file, 'ab') as b_file:
            b_file.write(test_binary)
            b_file.write(test_b_num)

        b_file = self.share.open(self.binary_file, 'rb')
        f_content = b_file.read()
        self.assertIn(test_binary, f_content)
        self.assertIn(test_b_num, f_content)
        b_file.close()

        # Read 100 mb image
        with self.share.open(self.img, 'rb') as b_file:
            img = b_file.read()
            self.assertGreaterEqual(sys.getsizeof(img), 133246888)

            # write 100 mb image
            with self.share.open(self.write_image, 'wb') as new_b_file:
                new_b_file.write(img)

            # check that it is written
            with self.share.open(self.write_image, 'rb') as new_b_file:
                new_image = new_b_file.read()
                self.assertGreaterEqual(sys.getsizeof(new_image), 133246888)

