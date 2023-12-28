import logging

from ..smell_detector import DesignSmellDetector


class HubLikeModularizationDetector(DesignSmellDetector):
    def _detect_smells(self, module, config):
        smells = []
        try:
            max_fan_in = config.get('max_fan_in', 5)
            max_fan_out = config.get('max_fan_out', 5)

            for sm_class in module.classes:
                fan_in = sm_class.metrics['fan_in']
                fan_out = sm_class.metrics['fan_out']
                if fan_in >= max_fan_in and fan_out >= max_fan_out:
                    detail = f"Class '{sm_class.name}' acts as a hub with fan-in of {fan_in} and fan-out of {fan_out}."
                    smell = self._create_smell(module.name, sm_class, detail, sm_class.start_line)
                    if smell:
                        smells.append(smell)
        except Exception as e:
            logging.error(f"Error detecting Hub-Like Modularization smells in module {module.name}: {e}", exc_info=True)

        return smells
