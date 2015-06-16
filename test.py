#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'web'

import unittest
from selenium import webdriver


class TestUbuntuHomepage(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.PhantomJS('C:\bin\phantomjs.exe')

    def testTitle(self):
        self.driver.get('http://zn.t.dbn.cn/login.aspx')

    def tearDown(self):
        self.driver.quit()
