import logging

from ..smell_detector import ArchitectureSmellDetector

class GodComponentDetector(ArchitectureSmellDetector):
    def _detect_smells(self, module, config):
        logging.info(f"Starting God Component detection in module: {module.name}")
        smells = []
        loc_threshold=200
        num_classes_threshold=5

        loc = sum(function.end_line - function.start_line + 1 for function in module.functions)
        num_classes = len(module.classes)
        entity = Entity("God Component")
        
        if loc > loc_threshold or num_classes > num_classes_threshold:
            detail = f"The module has {loc} LOC and {num_classes} classes, which exceeds the thresholds."
            smells.append(self._create_smell(module.name, entity, detail))
        print(smells)
        

        logging.info(
            f"Completed God Component detection in module: {module.name}. Total smells detected: {len(smells)}"
        )
        return smells

class Entity:
    def __init__(self, name):
        self.name = name