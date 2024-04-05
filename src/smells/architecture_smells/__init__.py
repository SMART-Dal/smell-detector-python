from .cyclic_dependency import CyclicDependencyDetector
from .unstable_dependency import UnstableDependencyDetector
from .ambiguous_interface import AmbiguousInterfaceDetector
from .god_component import GodComponentDetector
from .feature_concentration import FeatureConcentrationDetector
from .scattered_functionality import ScatteredFunctionalityDetector
from .dense_structure import DenseStructureDetector

DETECTORS = {
    'CyclicDependency': CyclicDependencyDetector(),
    'UnstableDependency': UnstableDependencyDetector(),
    'AmbiguousInterface': AmbiguousInterfaceDetector(),
    'GodComponent': GodComponentDetector(),
    'FeatureConcentration': FeatureConcentrationDetector(),
    'ScatteredFunctionality': ScatteredFunctionalityDetector(),
    'DenseStructure': DenseStructureDetector()
}