"""
This demo demonstrates import_json() method that imports data from json file and loads recursively.

Usage:
"""
from . import MasterConfig


if __name__ == "__main__":
    import os
    import json

    # Set json file path
    current_file_path = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_file_path, "exported.json")
    
    # Import from json
    succeded, master_config= MasterConfig.import_json(path=file_path, ignore_error=True)

    if succeded:
        print('succeded...')
        print(master_config.export_dict())
    else:
        print('failed to import json')

