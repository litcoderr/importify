# Copyright 2020 by Youngchae James Chee.
# Github: https://github.com/litcoderr
# All rights reserved.
# This file is released under the "MIT License Agreement".
# Please see the LICENSE file.

"""
This demo demonstrates export_dict() method
that can extract dictionary from any Serializable object recursively.
"""
from . import MasterConfig


if __name__ == "__main__":
    master_config = MasterConfig()
    
    extracted_dict = master_config.export_dict()
