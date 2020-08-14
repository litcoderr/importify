# Copyright 2020 by Youngchae James Chee.
# Github: https://github.com/litcoderr
# All rights reserved.
# This file is released under the "MIT License Agreement".
# Please see the LICENSE file.

"""
This demonstrates how you can construct a serializable configuration object
"""
from importify import Serializable


class MasterConfig(Serializable):
    def __init__(self):
        super().__init__()
        self.is_awesome = True
        self.nested = NestedConfig()


class NestedConfig(Serializable):
    def __init__(self):
        self.is_legit = True
        self.double_nested = DoubleNestedConfig()


class DoubleNestedConfig(Serializable):
    def __init__(self):
        self.is_intuitive = True
