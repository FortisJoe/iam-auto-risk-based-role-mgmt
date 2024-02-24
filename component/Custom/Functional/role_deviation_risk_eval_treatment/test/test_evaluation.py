from idmlib.components.test import CommonTest
from unittest.mock import MagicMock, patch

from Functional.role_deviation_risk_analysis.analyse import (
    DeviationType,
    RiskInformation,
    RiskAnalysisInput
)
from Functional.role_deviation_risk_classification.model import (
    RiskClassficiationEvalTreatmentLookup
)
from Functional.role_deviation_risk_eval_treatment.evaluation import (
    RiskEvaluation
)
from Functional.role_deviation_risk_eval_treatment.treatment import (
    RiskTreatment
)


class TestRiskEvaluation(CommonTest):

    @patch.object(RiskTreatment, "take_no_action")
    def test_evaluation_surplus_no_treatment(self, take_no_action):
        evaluation = RiskEvaluation()
        risk_input = MagicMock()
        deviation = DeviationType.SURPLUS
        risk_input.type_of_deviation = deviation
        treatment = MagicMock()
        treatment.treatment = "No Action"
        with patch(RiskClassficiationEvalTreatmentLookup.get_treatment_for_risk_level, return_value=treatment) as p:
            evaluation.evaluate(risk_input, 97.6)
            p.assert_called_with(97.6, deviation)
            take_no_action.assert_called_with(risk_input, 97.6, treatment)

    @patch.object(RiskTreatment, "inform")
    def test_evaluation_surplus_inform(self, inform):
        evaluation = RiskEvaluation()
        risk_input = MagicMock()
        deviation = DeviationType.SURPLUS
        risk_input.type_of_deviation = deviation
        treatment = MagicMock()
        treatment.treatment = "Inform"
        with patch(
                RiskClassficiationEvalTreatmentLookup.get_treatment_for_risk_level,
                return_value=treatment) as p:
            evaluation.evaluate(risk_input, 97.6)
            p.assert_called_with(97.6, deviation)
            inform.assert_called_with(risk_input, 97.6, treatment)

    @patch.object(RiskTreatment, "action")
    def test_evaluation_surplus_action(self, action):
        evaluation = RiskEvaluation()
        risk_input = MagicMock()
        deviation = DeviationType.SURPLUS
        risk_input.type_of_deviation = deviation
        treatment = MagicMock()
        treatment.treatment = "Action"
        with patch(
                RiskClassficiationEvalTreatmentLookup.get_treatment_for_risk_level,
                return_value=treatment) as p:
            evaluation.evaluate(risk_input, 97.6)
            p.assert_called_with(97.6, deviation)
            action.assert_called_with(risk_input, 97.6, treatment)

    @patch.object(RiskTreatment, "take_no_action")
    @patch.object(RiskTreatment, "inform")
    @patch.object(RiskTreatment, "action")
    def test_evaluation_surplus_different_type(self, take_no_action, inform, action):
        evaluation = RiskEvaluation()
        risk_input = MagicMock()
        deviation = DeviationType.SURPLUS
        risk_input.type_of_deviation = deviation
        treatment = MagicMock()
        treatment.treatment = "Unknown"
        with patch(
                RiskClassficiationEvalTreatmentLookup.get_treatment_for_risk_level,
                return_value=treatment) as p:
            evaluation.evaluate(risk_input, 97.6)
            p.assert_called_with(97.6, deviation)
            take_no_action.assert_not_called()
            inform.assert_not_called()
            action.assert_not_called()

    @patch.object(RiskTreatment, "take_no_action")
    def test_evaluation_deficit_no_treatment(self, take_no_action):
        evaluation = RiskEvaluation()
        risk_input = MagicMock()
        deviation = DeviationType.DEFICIT
        risk_input.type_of_deviation = deviation
        treatment = MagicMock()
        treatment.treatment = "No Action"
        with patch(
                RiskClassficiationEvalTreatmentLookup.get_treatment_for_risk_level,
                return_value=treatment) as p:
            evaluation.evaluate(risk_input, 97.6)
            p.assert_called_with(97.6, deviation)
            take_no_action.assert_called_with(risk_input, 97.6, treatment)

    @patch.object(RiskTreatment, "inform")
    def test_evaluation_deficit_inform(self, inform):
        evaluation = RiskEvaluation()
        risk_input = MagicMock()
        deviation = DeviationType.DEFICIT
        risk_input.type_of_deviation = deviation
        treatment = MagicMock()
        treatment.treatment = "Inform"
        with patch(
                RiskClassficiationEvalTreatmentLookup.get_treatment_for_risk_level,
                return_value=treatment) as p:
            evaluation.evaluate(risk_input, 97.6)
            p.assert_called_with(97.6, deviation)
            inform.assert_called_with(risk_input, 97.6, treatment)

    @patch.object(RiskTreatment, "action")
    def test_evaluation_deficit_action(self, action):
        evaluation = RiskEvaluation()
        risk_input = MagicMock()
        deviation = DeviationType.DEFICIT
        risk_input.type_of_deviation = deviation
        treatment = MagicMock()
        treatment.treatment = "Action"
        with patch(
                RiskClassficiationEvalTreatmentLookup.get_treatment_for_risk_level,
                return_value=treatment) as p:
            evaluation.evaluate(risk_input, 97.6)
            p.assert_called_with(97.6, deviation)
            action.assert_called_with(risk_input, 97.6, treatment)

    @patch.object(RiskTreatment, "take_no_action")
    @patch.object(RiskTreatment, "inform")
    @patch.object(RiskTreatment, "action")
    def test_evaluation_deficit_different_type(self, take_no_action, inform,
                                               action):
        evaluation = RiskEvaluation()
        risk_input = MagicMock()
        deviation = DeviationType.DEFICIT
        risk_input.type_of_deviation = deviation
        treatment = MagicMock()
        treatment.treatment = "Unknown"
        with patch(
                RiskClassficiationEvalTreatmentLookup.get_treatment_for_risk_level,
                return_value=treatment) as p:
            evaluation.evaluate(risk_input, 97.6)
            p.assert_called_with(97.6, deviation)
            take_no_action.assert_not_called()
            inform.assert_not_called()
            action.assert_not_called()
