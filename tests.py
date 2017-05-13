#! usr/bin/python3
# -*- coding: utf8 -*-
#
# Flicket - copyright Paul Bourne: evereux@gmail.com

import os
import unittest

from coverage import coverage

from tests.base_dir import base_dir
# from tests.pages import TestCasePages
from tests.tickets import TestCaseTickets

if __name__ == '__main__':

    # cov = coverage(branch=True, omit=['*python-env*', 'migrate', 'env*', 'tests*'])
    # cov.start()
    unittest.main(exit=False)
    # cov.stop()
    # cov.save()
    # print('\n\nCoverage Report:\n')
    # cov.report()
    # print('\nHTML version: {}'.format(os.path.join(base_dir, 'tmp/coverage/index.html')))
    # cov.html_report(directory='tmp/coverage')
    # cov.erase()
