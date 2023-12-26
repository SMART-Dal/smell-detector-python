from .deep_hierarchy import DeepHierarchyDetector
from .imperative_abstraction import ImperativeAbstractionDetector
from .multifaceted_abstraction import MultifacetedAbstractionDetector
from .unnecessary_abstraction import UnnecessaryAbstractionDetector
from .unutilized_abstraction import UnutilizedAbstractionDetector

DETECTORS = {
    'ImperativeAbstraction': ImperativeAbstractionDetector(),
    'UnnecessaryAbstraction': UnnecessaryAbstractionDetector(),
    'MultifacetedAbstraction': MultifacetedAbstractionDetector(),
    'UnutilizedAbstraction': UnutilizedAbstractionDetector(),
    'DeepHierarchy': DeepHierarchyDetector()
}
