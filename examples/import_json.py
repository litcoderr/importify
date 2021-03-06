# Copyright 2020 by Youngchae James Chee.
# Github: https://github.com/litcoderr
# All rights reserved.
# This file is released under the "MIT License Agreement".
# Please see the LICENSE file.

"""
This demo demonstrates import_json() method
that imports data from json file and loads recursively.
"""
from . import MasterConfig


if __name__ == "__main__":
    import os

    # Set json file path
    current_file_path = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_file_path, "exported.json")
    
    # Import from json
    succeded, master_config = MasterConfig.import_json(path=file_path, ignore_error=True)
