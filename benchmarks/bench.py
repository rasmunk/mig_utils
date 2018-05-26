import os
import time
from mig.io import IDMCShare
import skimage.io

# Test input
try:
    with open('../res/sharelinks.txt', 'r') as file:
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


def write_test():
    share = IDMCShare('K2wzxDcEBm')


def read_test():
    share = IDMCShare('K2wzxDcEBm')
    times = []
    projections = share.list('projections')
    for projection in projections:
        if projection.startswith('.'):
            continue
        path = os.path.join('projections', projection)
        t1 = time.time()
        data = share.read_binary(filename=path)
        t2 = time.time()
        times.append(t2 - t1)

    print("num_reads: {}".format(len(times)))
    print("total_time: {}".format(sum(times)))
    print("avg_read_time: {}".format(sum(times) / len(times)))


def test():
    share = IDMCShare('K2wzxDcEBm')


read_test()
