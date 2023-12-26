import logging

from .implementation_smells import DETECTORS as IMPL_SMELL_DETECTORS
from .design_smells import DETECTORS as DESIGN_SMELL_DETECTORS

# Initialize all detectors, including implementation and potentially design detectors in the future
ALL_DETECTORS = {}
ALL_DETECTORS.update(IMPL_SMELL_DETECTORS)
ALL_DETECTORS.update(DESIGN_SMELL_DETECTORS)


def get_detector(smell_name):
    try:
        detector = ALL_DETECTORS.get(smell_name)
        if detector is None:
            logging.warning(f"No detector found for smell: {smell_name}")
        return detector
    except Exception as e:
        logging.error(f"Error retrieving detector for smell {smell_name}: {e}", exc_info=True)
        return None
