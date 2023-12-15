from .complex_conditional import ComplexConditionalDetector
from .complex_method import ComplexMethodDetector
from .long_identifier import LongIdentifierDetector
from .long_method import LongMethodDetector
from .long_parameter_list import LongParameterListDetector
from .long_statement import LongStatementDetector

DETECTORS = {
    'LongMethod': LongMethodDetector(),
    'LongIdentifier': LongIdentifierDetector(),
    'LongParameterList': LongParameterListDetector(),
    'ComplexMethod': ComplexMethodDetector(),
    'LongStatement': LongStatementDetector(),
    'ComplexConditional': ComplexConditionalDetector(),
}
