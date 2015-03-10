# -*- coding: utf-8 -*-
from unittest import TestCase
from unittest.mock import mock_open, patch
import sys
import os
pjoin = os.path.join
import gpio

if sys.version_info.major < 3:
    bins = '__builtin__'
else:
    bins = 'builtins'

root = gpio.gpio_root


def mockargs(mock):
    return [m[0] for m in mock.call_args_list]


def assertInitialized(self, mfile, gpio=0):
    margs = mockargs(mfile)
    groot = pjoin(root, 'gpio{}'.format(gpio))
    self.assertEqual(margs[0], (pjoin(root, 'export'), 'w'))
    self.assertEqual(margs[1], (pjoin(groot, 'value'), 'w+'))
    self.assertEqual(margs[2], (pjoin(groot, 'direction'), 'w+'))
    self.assertEqual(margs[3], (pjoin(groot, 'drive'), 'w+'))


def reset(method):
    def wrapped(*args, **kwargs):
        gpio._open.clear()
        return method(*args, **kwargs)
    return wrapped


class TestRead(TestCase):
    @reset
    def test_basic(self):
        mopen = mock_open(read_data='0')
        with patch(bins + '.open', mopen, create=True) as m:
            result = gpio.read(0)
        assertInitialized(self, m)
        self.assertEqual(result, 0)


class TestWrite(TestCase):
    @reset
    def test_basic(self):
        mopen = mock_open(read_data='0')
        with patch(bins + '.open', mopen, create=True) as m:
            import pdb; pdb.set_trace()
            gpio.setup(0, gpio.OUT)
            gpio.set(0, 0)
        assertInitialized(self, m)
        written = mockargs(gpio._open[0]['value'].write)
        import ipdb; ipdb.set_trace()
