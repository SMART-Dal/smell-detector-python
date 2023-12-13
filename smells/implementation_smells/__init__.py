from .long_identifier import LongIdentifierDetector
from .long_parameter_list import LongParameterListDetector

DETECTORS = {
    'LongParameterList': LongParameterListDetector(),
    'LongIdentifier': LongIdentifierDetector(),
}
