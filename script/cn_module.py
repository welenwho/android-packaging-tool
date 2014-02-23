# -*- coding: utf-8 -*-
__author__ = 'welen'
import sys

class UnicodeStreamFilter:
    def __init__(self, target):
        self.target = target
        self.encoding = 'utf-8'
        self.errors = 'replace'
        self.encode_to = self.target.encoding
    def write(self, s):
        if sys.version_info[0] != 3:
            if type(s) == str:
                s = s.decode("utf-8")
            s = s.encode(self.encode_to, self.errors).decode(self.encode_to)
        self.target.write(s)
    def flush(self):
        a=1

if sys.stdout.encoding == 'cp936':
    sys.stdout = UnicodeStreamFilter(sys.stdout)
