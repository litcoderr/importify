

from typing import Tuple, Dict, Any, Optional, List
import sys
import json
import argparse

DELIM = "."


def json_serializable(x):
    try:
        json.dumps(x)
        return True
    except:
        return False


class Serializable:
    def __init__(self):
        self.parser = SerializableParser(instance=self)

    # Export Methods
    def export_dict(self) -> Dict[str, Any]:
        """export dictionary recursively

        Returns:
            Dictionary that consists child arguments recursively.
        """
        # Get current item in dictionary
        parent_dict = self.__dict__.copy()

        # Build child dictionary recursively
        delete_queue = []
        for key, obj in parent_dict.items():
            if isinstance(obj, Serializable):
                parent_dict[key] = obj.export_dict()
            elif not json_serializable(obj):
                delete_queue.append(key)

        # delete non json serializables
        for key in delete_queue:
            del parent_dict[key]

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
            succeed = False
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
    def import_json(cls, path: str, ignore_error: bool = True) \
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

    # Parsing Method
    def parse(self):
        self.parser.parse()

    def parse_(self):
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
                for k, v in value.strip_dict(prefix=prefix + key + DELIM).items():
                    stripped_dict[k] = v
            else:
                stripped_dict[prefix + key] = value
        return stripped_dict

    # Utility
    @staticmethod
    def is_base(key):
        BASE = ['parser']
        return key in BASE

    def strip(self, prefix: str = "") -> Dict[str, Any]:
        """ Strip arguments.

        Args:
            instance: Parent Serializable instance
            prefix: Prefix string.

        Returns:
            Stripped dictionary.
        """
        stripped_dicts = {}
        for key, value in self.__dict__.items():
            if isinstance(value, Serializable):
                for child_key, child_value in value.strip(prefix=prefix+key+DELIM).items():
                    stripped_dicts[child_key] = child_value
            elif Serializable.is_base(key):
                continue
            else:
                stripped_dicts[prefix+key] = value
        return stripped_dicts

    def unstrip(self, data: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
        """Unstrip parsed dictionary and save.

        Args:
            data: stripped dictionary

        Returns:
            Dictionary consisting reference and key to value
        """
        result = {}
        for key, value in data.items():
            key_path = key.split(DELIM)
            ref, k = self.get_attribute(key_path)
            result[key] = {"reference": ref, "key": k, "value": value}
        return result

    def get_attribute(self, key_path: List[str]) -> Tuple[Any, str]:
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


class SerializableParser:
    def __init__(self, instance):
        self.instance = instance

    def parse(self):
        """Parse method.
        """
        # Strip dicts for parser
        dicts = self.instance.strip()

        # Parse
        boolean_keys = []
        parser = argparse.ArgumentParser()
        for key, value in dicts.items():
            if type(value) == bool:
                boolean_keys.append(key)
                if value:
                    default = "True"
                else:
                    default = "False"
                parser.add_argument('--{key}'.format(key=key), type=str, choices=["True", "False"], default=default,
                                    help="boolean option.")
            else:
                parser.add_argument('--{key}'.format(key=key), type=type(value), default=value)
        args = vars(parser.parse_args())

        # Deal with stringed boolean attributes
        for key in boolean_keys:
            if args[key] == "True":
                args[key] = True
            else:
                args[key] = False

        # Unstrip and Update
        for stripped_key, res in self.instance.unstrip(args).items():
            setattr(res["reference"], res["key"], res["value"])
