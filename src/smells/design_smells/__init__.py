from .imperative_abstraction import ImperativeAbstractionDetector
from .unnecessary_abstraction import UnnecessaryAbstractionDetector

DETECTORS = {
    'ImperativeAbstraction': ImperativeAbstractionDetector(),
    'UnnecessaryAbstraction': UnnecessaryAbstractionDetector()
}