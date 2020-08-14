# Copyright 2020 by Youngchae James Chee.
# Github: https://github.com/litcoderr
# All rights reserved.
# This file is released under the "MIT License Agreement".
# Please see the LICENSE file.

"""
This demo demonstrates export_json() method
that saves Serializable object to json file.
"""
from . import MasterConfig


if __name__ == "__main__":
    import os
    import json

    # Initialize configuration object
    master_config = MasterConfig()

    # Set json file path
    current_file_path = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_file_path, "exported.json")
    
    # Export to json
    succeded = master_config.export_json(path=file_path, ignore_error=True)
    print('Save status: {succeded}'.format(succeded=succeded))

    # Now lets see if json file has been succesfully saved.
    with open(file_path, 'r') as file:
        data = json.load(file)
