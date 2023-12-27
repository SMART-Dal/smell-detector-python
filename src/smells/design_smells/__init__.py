from .broken_hierarchy import BrokenHierarchyDetector
from .deep_hierarchy import DeepHierarchyDetector
from .imperative_abstraction import ImperativeAbstractionDetector
from .missing_hierarchy import MissingHierarchyDetector
from .multifaceted_abstraction import MultifacetedAbstractionDetector
from .multipath_hierarchy import MultipathHierarchyDetector
from .rebellious_hierarchy import RebelliousHierarchyDetector
from .unnecessary_abstraction import UnnecessaryAbstractionDetector
from .unutilized_abstraction import UnutilizedAbstractionDetector
from .wide_hierarchy import WideHierarchyDetector

DETECTORS = {
    'ImperativeAbstraction': ImperativeAbstractionDetector(),
    'UnnecessaryAbstraction': UnnecessaryAbstractionDetector(),
    'MultifacetedAbstraction': MultifacetedAbstractionDetector(),
    'UnutilizedAbstraction': UnutilizedAbstractionDetector(),
    'DeepHierarchy': DeepHierarchyDetector(),
    'MultipathHierarchy': MultipathHierarchyDetector(),
    'RebelliousHierarchy': RebelliousHierarchyDetector(),
    'MissingHierarchy': MissingHierarchyDetector(),
    'BrokenHierarchy': BrokenHierarchyDetector(),
    'WideHierarchy': WideHierarchyDetector()
}
