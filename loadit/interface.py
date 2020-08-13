from typing import Tuple, Dict, Any, Optional, List
import sys
import json
import argparse

DELIM = "__"


class Serializable:
    def __init__(self):
        pass

    # Export Methods
    def export_dict(self) -> Dict[str, Any]:
        """export dictionary recursively
        
        Returns:
            Dictionary that consists child arguments recursively.
        """
        # Get current item in dictionary
        parent_dict = self.__dict__.copy()

        # Build child dictionary recursively
        for key, obj in parent_dict.items():
            if isinstance(obj, Serializable):
                parent_dict[key] = obj.export_dict()

        return parent_dict

    def export_json(self, path: str, ignore_error=True) -> bool:
        """

        Args:
            path: path of json file to be saved.

        Returns:
            succeed saving json file or not.
        """
        succeed = True
        try:
            # extract dictionary
            extracted_dict = self.export_dict()

            # save as json
            with open(path, 'w') as file:
                file.write(json.dumps(extracted_dict, ensure_ascii=False))
        except Exception as e:
            succeed= False
            print(e)        
            if not ignore_error:
                sys.exit()
        return succeed
    
    # Import Methods
    def import_dict(self, data: Dict[str, Any]):
        """Import arguments from dictionary
        
        Args:
            data: dictionary that consists child argument recursively.
        """
        for key, value in data.items():
            if hasattr(self, key):
                if isinstance(getattr(self, key), Serializable):
                    setattr(self, key, getattr(self, key).import_dict(value))
                else:
                    setattr(self, key, value)
        return self
    
    @classmethod
    def import_json(cls, path: str, ignore_error: bool = True)\
            -> Tuple[bool, Optional['Serializable']]:
        try:
            with open(path, 'r') as file:
                data = json.load(file)
            return True, cls().import_dict(data)
        except Exception as e:
            print(e)
            if not ignore_error:
                sys.exit()
            return False, None
    
    # Parsing related method
    def parse(self):
        """Implement argument parsing functionality based on object elements
        """
        parser = argparse.ArgumentParser() 
        for key, value in self.strip_dict().items():
            parser.add_argument('--{}'.format(key), type=type(value))
        args = parser.parse_args()
        print(vars(args))
        self.unstrip_dict(vars(args))

    # Utility
    def strip_dict(self, prefix: str = "") -> Dict[str, Any]:
        """Strips dictionary recursively.

        Args:
            prefix: prefix string.

        Returns:
            dictionary with stripped keys.
        """
        stripped_dict = {}
        for key, value in self.__dict__.items():
            if isinstance(value, Serializable):
                for k, v in value.strip_dict(prefix=prefix+key+DELIM).items():
                    stripped_dict[k] = v
            else:
                stripped_dict[prefix+key] = value
        return stripped_dict
    
    def unstrip_dict(self, data: Dict[str, Any]):
        """Unstrip parsed dictionary and save.

        Args:
            data: stripped dictionary
        """
        for key, value in data.items():
            key_path = key.split(DELIM)
            ref, k = self.get_attribute(key_path)
            setattr(ref, k, value)

    def get_attribute(self, key_path: List[str]):
        """Return key path corresponding instance

        Args:
            key_path: heirechical key path.

        Returns:
            key path corresponding instance
        """
        if len(key_path) > 1:
            child_attr_name = key_path.pop(0)
            return getattr(self, child_attr_name).get_attribute(key_path)
        else:
            return self, key_path[0]
