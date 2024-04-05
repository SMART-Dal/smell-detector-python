import logging
from ..smell_detector import ArchitectureSmellDetector
from ...metrics import calculate_module_loc

class GodComponentDetector(ArchitectureSmellDetector):
    def _detect_smells(self, package_details, config):
        all_smells = []

        loc_threshold = 27000
        num_classes_threshold = 30
        
        for package_name, modules in package_details.items():
            logging.info(f"Starting God Component detection in package: {package_name}")
            smells=[]
            total_loc = 0
            total_num_classes = 0
            entity = Entity("God Component")

            for module in modules:
                loc = calculate_module_loc(module)
                num_classes = len(module.classes)
                total_loc += loc
                total_num_classes += num_classes

            if total_loc > loc_threshold or total_num_classes > num_classes_threshold:
                detail = f"The package {package_name} has {total_loc} LOC and {total_num_classes} classes, which exceeds the thresholds."
                smells.append(self._create_smell(package_name, entity, detail))
                
            all_smells.extend(smells)
            logging.info(
                f"Completed God Component detection in package: {package_name}. Total smells detected: {len(smells)}"
            )
        
        return all_smells

class Entity:
    def __init__(self, name):
        self.name = name