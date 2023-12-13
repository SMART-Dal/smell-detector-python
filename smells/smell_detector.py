class SmellDetector:
    def detect(self, module, config):
        """Detects smells within the given module based on the provided configuration."""
        raise NotImplementedError


class ImplementationSmellDetector(SmellDetector):
    """Base class for all implementation smell detectors."""
    pass


class DesignSmellDetector(SmellDetector):
    """Base class for all design smell detectors."""
    pass
