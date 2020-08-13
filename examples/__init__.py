# temporary for test use
import sys
sys.path.insert(0, "/Users/litcoderr/project/loadit")
#####
"""
This demonstrates how you can construct a serializable configuration object
"""
from loadit import Serializable


class MasterConfig(Serializable):
    def __init__(self):
        self.loadit_is_awesome = True
        self.loadit_sub_config = NestedConfig()


class NestedConfig(Serializable):
    def __init__(self):
        self.loadit_is_legit = True
        self.loadit_sub_sub_config = NestedNestedConfig()


class NestedNestedConfig(Serializable):
    def __init__(self):
        self.loadit_can_go_deep = True
