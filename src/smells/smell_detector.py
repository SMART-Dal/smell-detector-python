from abc import abstractmethod, ABC


class SmellDetector:
    def detect(self, module, config):
        """Detects smells within the given module based on the provided configuration."""
        raise NotImplementedError


class ImplementationSmellDetector(SmellDetector, ABC):
    """Base class for all implementation smell detectors."""

    @abstractmethod
    def detect(self, module, config):
        super().detect(module, config)

    def _create_smell(self, module_name, entity, detail, line=None):
        smell = {
            'module': module_name,
            'type': self.__class__.__name__.replace('Detector', ''),
            'entity_name': entity.name,
            'location': f"Line {line}",
            'details': detail
        }
        return smell

    @staticmethod
    def _iterate_functions_and_methods(module):
        """Yield all functions and methods from the given module."""
        for function in module.functions:
            yield function
        for py_class in module.classes:
            for method in py_class.methods:
                yield method


class DesignSmellDetector(SmellDetector):
    """Base class for all design smell detectors."""
    pass
