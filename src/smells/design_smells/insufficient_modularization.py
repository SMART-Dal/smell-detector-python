import logging

from ..smell_detector import DesignSmellDetector


class InsufficientModularizationDetector(DesignSmellDetector):
    def _detect_smells(self, module, config):
        smells = []
        try:
            for sm_class in module.classes:
                try:
                    metrics = sm_class.metrics
                    nopm = metrics['nopm']
                    wmc = metrics['wmc']
                    nom = metrics['nom']
                    loc = metrics['loc']

                    max_nopm = config.get('max_nopm', 10)
                    max_wmc = config.get('max_wmc', 15)
                    max_nom = config.get('max_nom', 20)
                    max_loc = config.get('max_loc', 300)

                    # Check if the class exceeds any of the thresholds
                    if nopm > max_nopm or wmc > max_wmc or nom > max_nom or loc > max_loc:
                        detail = f"Class '{sm_class.name}' might be insufficiently modularized with NOPM: {nopm}, WMC: {wmc}, NOM: {nom}, LOC: {loc}."
                        smell = self._create_smell(module.name, sm_class, detail, sm_class.start_line)
                        if smell:
                            smells.append(smell)

                except Exception as class_error:
                    logging.error(
                        f"Error checking Insufficient Modularization for class {sm_class.name} in module {module.name}: {class_error}",
                        exc_info=True)

            logging.info(f"Detected {len(smells)} Insufficient Modularization smells in {module.name}")
        except Exception as module_error:
            logging.error(f"Error detecting Insufficient Modularization smells in module {module.name}: {module_error}",
                          exc_info=True)

        return smells
