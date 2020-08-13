"""
This demo demonstrates parse() method that implements argument parsing fucntionality based on object elements.

Usage:
"""

from . import MasterConfig


if __name__ == "__main__":
    master_config = MasterConfig()
    print('before parsing:')
    print(master_config.export_dict())
    
    # parse
    master_config.parse()
    
    print('after parseing:')
    print(master_config.export_dict())

