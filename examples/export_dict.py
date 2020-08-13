"""
This demo demonstrates export_dict() method that can extract dictionary from any Serializable object recursively.

Usage:
"""
from . import MasterConfig


if __name__ == "__main__":
    master_config = MasterConfig()
    
    extracted_dict = master_config.export_dict()
    
    print(extracted_dict)
