import logging
from abc import abstractmethod, ABC


class SmellDetector(ABC):
    @abstractmethod
    def detect(self, module, config):
        """Detects smells within the given module based on the provided configuration."""
        pass

    @abstractmethod
    def _detect_smells(self, module, config):
        """Actual smell detection logic to be implemented by child classes."""
        pass

    def _create_smell(self, module_name, entity, detail, line=None):
        try:
            smell = {
                'module': module_name,
                'type': self.__class__.__name__.replace('Detector', ''),
                'entity_name': entity.name,
                'location': f"Line {line}" if line else "Not specified",
                'details': detail
            }
            return smell
        except AttributeError as e:
            logging.error(f"Error creating smell for {module_name}: {e}")
            return None

    @staticmethod
    def _iterate_functions_and_methods(module):
        try:
            if module.functions is not None:
                for function in module.functions:
                    yield function
            if module.classes is not None:
                for py_class in module.classes:
                    if py_class.methods is not None:
                        for method in py_class.methods:
                            yield method
        except AttributeError as e:
            logging.error(f"Error iterating functions and methods in module {module.name}: {e}")


class ImplementationSmellDetector(SmellDetector):
    """Base class for all implementation smell detectors."""

    def detect(self, module, config):
        try:
            return self._detect_smells(module, config)
        except Exception as e:
            logging.error(f"Error detecting implementation smells in module {module.name}: {e}", exc_info=True)
            return []

    @abstractmethod
    def _detect_smells(self, module, config):
        """Actual smell detection logic to be implemented by child classes."""
        pass


class DesignSmellDetector(SmellDetector):
    """Base class for all design smell detectors."""

    def detect(self, module, config):
        try:
            return self._detect_smells(module, config)
        except Exception as e:
            logging.error(f"Error detecting design smells in module {module.name}: {e}", exc_info=True)
            return []

    @abstractmethod
    def _detect_smells(self, module, config):
        """Actual smell detection logic to be implemented by child classes."""
        pass
