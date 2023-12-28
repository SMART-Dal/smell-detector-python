from .broken_hierarchy import BrokenHierarchyDetector
from .broken_modularization import BrokenModularizationDetector
from .deep_hierarchy import DeepHierarchyDetector
from .deficient_encapsulation import DeficientEncapsulationDetector
from .hub_like_modularization import HubLikeModularizationDetector
from .imperative_abstraction import ImperativeAbstractionDetector
from .insufficient_modularization import InsufficientModularizationDetector
from .missing_hierarchy import MissingHierarchyDetector
from .multifaceted_abstraction import MultifacetedAbstractionDetector
from .multipath_hierarchy import MultipathHierarchyDetector
from .rebellious_hierarchy import RebelliousHierarchyDetector
from .unexploited_encapsulation import UnexploitedEncapsulationDetector
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
    'WideHierarchy': WideHierarchyDetector(),
    'DeficientEncapsulation': DeficientEncapsulationDetector(),
    'UnexploitedEncapsulation': UnexploitedEncapsulationDetector(),
    'BrokenModularization': BrokenModularizationDetector(),
    'InsufficientModularization': InsufficientModularizationDetector(),
    'HubLikeModularization': HubLikeModularizationDetector()
}
