from .implementation_smells import DETECTORS as IMPL_SMELL_DETECTORS

ALL_DETECTORS = {}
ALL_DETECTORS.update(IMPL_SMELL_DETECTORS)


def get_detector(smell_name):
    return ALL_DETECTORS.get(smell_name)
