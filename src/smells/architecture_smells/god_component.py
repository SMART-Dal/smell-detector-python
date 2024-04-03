import logging
from ..smell_detector import ArchitectureSmellDetector
from ...metrics import calculate_module_loc

class GodComponentDetector(ArchitectureSmellDetector):
    def _detect_smells(self, package, config):
        logging.info(f"Starting God Component detection in package: {package.name}")
        smells = []
        loc_threshold = 27000
        num_classes_threshold = 30
        
        total_loc = 0
        total_num_classes = 0
        entity = Entity("God Component")
        
        for module in package.modules:
            loc = calculate_module_loc(module)
            num_classes = len(module.classes)
            total_loc += loc
            total_num_classes += num_classes
        print(total_loc)
        print(total_num_classes)

        if total_loc > loc_threshold or total_num_classes > num_classes_threshold:
            detail = f"The package has {total_loc} LOC and {total_num_classes} classes, which exceeds the thresholds."
            smells.append(self._create_smell(package.name, entity, detail))
        
        logging.info(
            f"Completed God Component detection in package: {package.name}. Total smells detected: {len(smells)}"
        )
        return smells

class Entity:
    def __init__(self, name):
        self.name = name