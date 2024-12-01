import os
import importlib
from badge import Badge
from typing import List

def load_badges() -> List[Badge]:
    instances = []
    base_path = os.path.dirname(__file__)
    class_folder = os.path.join(base_path, "badges")

    for filename in os.listdir(class_folder):
        if filename.endswith(".py"):
            module_name = f"badges.{filename[:-3]}"
            module = importlib.import_module(module_name)

            # Find all classes in the module that inherit from BaseClass
            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                if isinstance(attr, type) and issubclass(attr, Badge) and attr is not Badge:
                    instances.append(attr())  # Create an instance of the class

    return instances
