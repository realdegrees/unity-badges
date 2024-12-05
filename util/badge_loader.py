import os
import importlib
from badges.badge import Badge
from typing import List

def load_badges() -> List[Badge]:
    instances = []
    base_path = os.path.dirname(__file__)
    class_folder = os.path.join(base_path, "../badges")

    for subfolder in os.listdir(class_folder):
        subfolder_path = os.path.join(class_folder, subfolder)
        badge_file = os.path.join(subfolder_path, "badge.py")
        if os.path.isfile(badge_file):
            module_name = f"badges.{subfolder}.badge"
            module = importlib.import_module(module_name)

            # Find all classes in the module that inherit from BaseClass
            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                if isinstance(attr, type) and issubclass(attr, Badge) and attr is not Badge:
                    instances.append(attr())  # Create an instance of the class

    return instances
