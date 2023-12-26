from .imperative_abstraction import ImperativeAbstractionDetector
from .multifaceted_abstraction import MultifacetedAbstractionDetector
from .unnecessary_abstraction import UnnecessaryAbstractionDetector

DETECTORS = {
    'ImperativeAbstraction': ImperativeAbstractionDetector(),
    'UnnecessaryAbstraction': UnnecessaryAbstractionDetector(),
    'MultifacetedAbstraction': MultifacetedAbstractionDetector()
}