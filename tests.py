#! usr/bin/python3
# -*- coding: utf8 -*-
#
# Flicket - copyright Paul Bourne: evereux@gmail.com

import os
import sys
import unittest

from coverage import coverage

from tests.base_dir import base_dir
from tests.main import TestCase

if __name__ == '__main__':

    cov = coverage(branch=True, omit=['flask/*', 'tests.py', 'env*', 'migrate'])
    cov.start()
    unittest.main()
    cov.stop()
    cov.start()
    print('\n\nCoveragae Reports:\n')
    cov.report()
    print('\nHTML version: {}'.format(os.path.join(base_dir, 'tmp/coverage/index.html')))
    cov.html_report(directory='tmp/coverage')
    cov.erase()
