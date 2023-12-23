from .complex_conditional import ComplexConditionalDetector
from .complex_method import ComplexMethodDetector
from .empty_catch_block import EmptyCatchBlockDetector
from .long_identifier import LongIdentifierDetector
from .long_method import LongMethodDetector
from .long_parameter_list import LongParameterListDetector
from .long_statement import LongStatementDetector
from .magic_number import MagicNumberDetector
from .missing_default import MissingDefaultDetector

DETECTORS = {
    'LongMethod': LongMethodDetector(),
    'LongIdentifier': LongIdentifierDetector(),
    'LongParameterList': LongParameterListDetector(),
    'ComplexMethod': ComplexMethodDetector(),
    'LongStatement': LongStatementDetector(),
    'ComplexConditional': ComplexConditionalDetector(),
    'EmptyCatchBlock': EmptyCatchBlockDetector(),
    'MagicNumber': MagicNumberDetector(),
    'MissingDefault': MissingDefaultDetector(),
}
