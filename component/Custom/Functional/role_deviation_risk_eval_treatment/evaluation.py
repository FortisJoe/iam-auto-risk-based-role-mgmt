from idmlib.components import component_log

from Functional.role_deviation_risk_classification.model import (
    RiskClassficiationEvalTreatmentLookup
)
from Functional.role_deviation_risk_eval_treatment.treatment import (
    RiskTreatment
)

log = component_log.getChild(__name__)


class RiskEvaluation:

    def __init__(self):
        """ Creates risk treatment object

        """
        self._treatment = RiskTreatment()

    def evaluate(self, risk_input, risk_score):
        """ Evaluates which treatment should occur

        :param risk_input: The Risk data for the risk
        :type risk_input:
        Functional.risk_deviation_risk_analysis.RiskInformation
        :param risk_score: The calculated risk score
        :type risk_score: double
        """
        treatment = RiskClassficiationEvalTreatmentLookup\
            .get_treatment_for_risk_level(
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
            log.error(
                f"Supplied Risk Treatment {treatment.treatment} is not "
                f"recognised."
            )
