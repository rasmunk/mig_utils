import unittest
import sys
import os
import six
import _io
from mig.io import ERDASSHFSShare, ERDASftpShare, \
    IDMCSSHFSShare, IDMCSftpShare

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

    def tearDown(self):
        pass

    def test_share(self):
        # ERDA Sharelink example
        print("ERDA")
        # List files/dirs in share
        self.share.remove('tmp')
        self.share.write('tmp', six.text_type("sddsfsf"))
        self.assertIn('tmp', self.share.list())
        # Read file directly as string
        self.assertEqual(self.share.read('tmp'), 'sddsfsf')
        # Read file directly as binary
        self.assertEqual(self.share.read_binary('tmp'), b'sddsfsf')

        # Get a _io.TextIOWrapper object with automatic close
        with self.share.open('tmp', 'r') as tmp:
            self.assertEqual(tmp.read(), 'sddsfsf')

        # Get a default _io.TextIOWrapper object with manual lifetime
        tmp_file = self.share.open('tmp', 'r')
        self.assertIsInstance(tmp_file, _io.TextIOWrapper)
        self.assertEqual(tmp_file.read(), 'sddsfsf')
        tmp_file.close()

        # Writing strings to a file
        # six -> ensure py2/3 compatibility
        test_string = six.text_type('Hello There')
        test_num = six.text_type(42342342)
        test_float = six.text_type(3434.231)

        self.share.remove('write_test')
        with self.share.open('write_test', 'w') as w_file:
            w_file.write(test_string)
            w_file.write(test_num)
            w_file.write(test_float)

        self.assertIn(test_string, self.share.read('write_test'))
        self.assertIn(str(test_num), self.share.read('write_test'))
        self.assertIn(str(test_float), self.share.read('write_test'))

        # Writing binary to a file
        self.share.remove('binary_test')
        test_binary = b'Hello again'
        test_b_num = six.int2byte(255)
        with self.share.open('binary_test', 'wb') as b_file:
            b_file.write(test_binary)
            b_file.write(test_b_num)

        self.assertIn(test_binary, self.share.read_binary('binary_test'))
        self.assertIn(test_b_num, self.share.read_binary('binary_test'))


class IDMCSSHFSShareTest(unittest.TestCase):
    share = None

    def setUp(self):
        # Open connection to a sharelink
        assert 'IDMC_TEST_SHARE' in sharelinks
        self.share = IDMCSSHFSShare(sharelinks['IDMC_TEST_SHARE'])

    def tearDown(self):
        pass

    def test_share(self):
        # ERDA Sharelink example
        print("IDMC")
        # List files/dirs in share
        self.assertIn('fisk', self.share.list())
        # Read file directly as string
        self.assertEqual(self.share.read('fisk'), 'Torsk')
        # Read file directly as binary
        self.assertEqual(self.share.read_binary('fisk'), b'Torsk')

        # Get a _io.TextIOWrapper object with automatic close
        with self.share.open('fisk', 'r') as tmp:
            self.assertEqual(tmp.read(), 'Torsk')

        # Get a default _io.TextIOWrapper object with manual lifetime
        file = self.share.open('fisk', 'r')
        self.assertIsInstance(file, _io.TextIOWrapper)
        self.assertEqual(file.read(), 'Torsk')
        file.close()

        # Writing strings to a file
        # six -> ensure py2/3 compatibility
        test_string = six.text_type('Hello There')
        test_num = six.text_type(42342342)
        test_float = six.text_type(3434.231)

        self.share.remove('write_test')
        with self.share.open('write_test', 'w') as w_file:
            w_file.write(test_string)
            w_file.write(test_num)
            w_file.write(test_float)

        self.assertIn(test_string, self.share.read('write_test'))
        self.assertIn(test_num, self.share.read('write_test'))
        self.assertIn(test_float, self.share.read('write_test'))

        # Writing binary to a file
        self.share.remove('binary_test')
        test_binary = b'Hello again'
        test_b_num = six.int2byte(255)
        with self.share.open('binary_test', 'wb') as b_file:
            b_file.write(test_binary)
            b_file.write(test_b_num)

        self.assertIn(test_binary, self.share.read_binary('binary_test'))
        self.assertIn(test_b_num, self.share.read_binary('binary_test'))


class ERDASFTPShareTest(unittest.TestCase):
    share = None

    def setUp(self):
        assert 'ERDA_TEST_SHARE' in sharelinks
        self.share = ERDASftpShare(sharelinks['ERDA_TEST_SHARE'],
                                   sharelinks['ERDA_TEST_SHARE'])

    def tearDown(self):
        pass

    # TODO -> implement
    def test_share(self):
        assert 0 == 0


class IDMCSftpShareTest(unittest.TestCase):
    share = None

    def setUp(self):
        assert 'IDMC_TEST_SHARE' in sharelinks
        self.share = IDMCSftpShare(sharelinks['IDMC_TEST_SHARE'],
                                   sharelinks['IDMC_TEST_SHARE'])

    def tearDown(self):
        self.share = None

    def test_share(self):
        # List files/dirs in share
        self.assertIn('fisk', self.share.list())
        # # Read file directly as string
        self.assertEqual(self.share.read('fisk'), 'Torsk')
        # # # Read file directly as binary
        self.assertEqual(self.share.read_binary('fisk'), b'Torsk')

        # # six -> ensure py2/3 compatibility
        write_file = 'write_test'

        test_string = 'Hello There'
        test_num = 42342342
        test_float = 3434.231

        self.share.remove(write_file)
        self.share.write(write_file, test_string)
        self.share.write(write_file, test_num)
        self.share.write(write_file, test_float)

        self.assertIn(test_string, self.share.read('write_test'))
        self.assertIn(str(test_num), self.share.read('write_test'))
        self.assertIn(str(test_float), self.share.read('write_test'))

        # Writing binary to a file
        binary_file = 'binary_test'
        self.share.remove(binary_file)
        test_binary = b'Hello again'
        test_b_num = six.int2byte(255)
        self.share.write(binary_file, test_binary)
        self.share.write(binary_file, test_b_num)

        self.assertIn(test_binary, self.share.read_binary('binary_test'))
        self.assertIn(test_b_num, self.share.read_binary('binary_test'))

        # Read 100 mb image
        img = self.share.read_binary('kmeans.tif')
        self.assertGreaterEqual(sys.getsizeof(img), 133246888)
