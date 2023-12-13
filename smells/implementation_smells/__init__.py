from .long_identifier import LongIdentifierDetector
from .long_method import LongMethodDetector
from .long_parameter_list import LongParameterListDetector

DETECTORS = {
    'LongMethod': LongMethodDetector(),
    'LongIdentifier': LongIdentifierDetector(),
    'LongParameterList': LongParameterListDetector(),
}
