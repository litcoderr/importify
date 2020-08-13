"""
This demo demonstrates parse() method that implements argument parsing fucntionality based on object elements.
"""

from . import MasterConfig


if __name__ == "__main__":
    # Initialize Serializable Instance
    master_config = MasterConfig()

    # Parse. Done !!
    master_config.parse()

    # Checkout result
    print(master_config.export_dict())

