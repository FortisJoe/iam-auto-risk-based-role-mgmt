from idmlib.components import component_log

from Functional.role_deviation_risk_classification.model import (
    RiskClassficiationEvalTreatmentLookup
)
from Functional.role_deviation_risk_eval_treatment.treatment import (
    RiskTreatment
)

log = component_log.getChild(__name__)


class RiskEvaluation:
    _instance = None
    _treatment = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(RiskEvaluation, cls).__new__(cls)
            cls._instance._treatment = RiskTreatment()
        return cls._instance

    def evaluate(self, risk_input, risk_score):
        treatment = RiskClassficiationEvalTreatmentLookup.get_treatment_for_risk_level(
            risk_score,
            str(risk_input.type_of_deviation)
        )
        if treatment.treatment == "No Action":
            self._treatment.take_no_action(
                risk_input,
                risk_score,
                treatment
            )
        elif treatment.treatment == "Inform":
            self._treatment.inform(
                risk_input,
                risk_score,
                treatment
            )
        elif treatment.treatment == "Action":
            self._treatment.raise_access_request(
                risk_input,
                risk_score,
                treatment
            )
        else:
            log.error(f"Supplied Risk Treatment {treatment.treatment} is not recognised.")
