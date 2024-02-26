from idmlib.components.test import CommonTest, InstalledComponent, CommonModel
from unittest.mock import ANY, MagicMock, patch

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

    @classmethod
    def setUp(cls):
        """Performs set up for the test class."""

        InstalledComponent(
            'Functional.role_deviation_risk_classification').install()

    @classmethod
    def tearDown(cls):
        """Performs tear down for the test class."""

        InstalledComponent(
            'Functional.role_deviation_risk_classification').teardown()

    @patch.object(RiskTreatment, "take_no_action")
    def test_evaluation_surplus_no_treatment(self, take_no_action):
        lookup = RiskClassficiationEvalTreatmentLookup(
            deviation="Surplus",
            classification="Low",
            min_score=0.0,
            max_score=100,
            treatment="No Action"
        )
        RiskClassficiationEvalTreatmentLookup.create(
            deviation="Surplus",
            classification="Low",
            min_score=0.0,
            max_score=100,
            treatment="No Action"
        )
        evaluation = RiskEvaluation()
        risk_input = MagicMock()
        deviation = DeviationType.SURPLUS
        risk_input.type_of_deviation = deviation
        evaluation.evaluate(risk_input, 97.6)
        take_no_action.assert_called_with(risk_input, 97.6, lookup)

    @patch.object(RiskTreatment, "inform")
    def test_evaluation_surplus_inform(self, inform):
        lookup = RiskClassficiationEvalTreatmentLookup(
            deviation="Surplus",
            classification="Low",
            min_score=0.0,
            max_score=100,
            treatment="Inform"
        )
        RiskClassficiationEvalTreatmentLookup.create(
            deviation="Surplus",
            classification="Low",
            min_score=0.0,
            max_score=100,
            treatment="Inform"
        )
        evaluation = RiskEvaluation()
        risk_input = MagicMock()
        deviation = DeviationType.SURPLUS
        risk_input.type_of_deviation = deviation
        evaluation.evaluate(risk_input, 97.6)
        inform.assert_called_with(risk_input, 97.6, lookup)

    @patch.object(RiskTreatment, "raise_access_request")
    def test_evaluation_surplus_action(self, action):
        lookup = RiskClassficiationEvalTreatmentLookup(
            deviation="Surplus",
            classification="Low",
            min_score=0.0,
            max_score=100,
            treatment="Action"
        )
        RiskClassficiationEvalTreatmentLookup.create(
            deviation="Surplus",
            classification="Low",
            min_score=0.0,
            max_score=100,
            treatment="Action"
        )
        evaluation = RiskEvaluation()
        risk_input = MagicMock()
        deviation = DeviationType.SURPLUS
        risk_input.type_of_deviation = deviation
        evaluation.evaluate(risk_input, 97.6)
        action.assert_called_with(risk_input, 97.6, lookup)

    @patch.object(RiskTreatment, "take_no_action")
    def test_evaluation_deficit_no_treatment(self, take_no_action):
        lookup = RiskClassficiationEvalTreatmentLookup(
            deviation="Deficit",
            classification="Low",
            min_score=0.0,
            max_score=100,
            treatment="No Action"
        )
        RiskClassficiationEvalTreatmentLookup.create(
            deviation="Deficit",
            classification="Low",
            min_score=0.0,
            max_score=100,
            treatment="No Action"
        )
        evaluation = RiskEvaluation()
        risk_input = MagicMock()
        deviation = DeviationType.DEFICIT
        risk_input.type_of_deviation = deviation
        evaluation.evaluate(risk_input, 97.6)
        take_no_action.assert_called_with(risk_input, 97.6, lookup)

    @patch.object(RiskTreatment, "inform")
    def test_evaluation_deficit_inform(self, inform):
        lookup = RiskClassficiationEvalTreatmentLookup(
            deviation="Deficit",
            classification="Low",
            min_score=0.0,
            max_score=100,
            treatment="Inform"
        )
        RiskClassficiationEvalTreatmentLookup.create(
            deviation="Deficit",
            classification="Low",
            min_score=0.0,
            max_score=100,
            treatment="Inform"
        )
        evaluation = RiskEvaluation()
        risk_input = MagicMock()
        deviation = DeviationType.DEFICIT
        risk_input.type_of_deviation = deviation
        evaluation.evaluate(risk_input, 97.6)
        inform.assert_called_with(risk_input, 97.6, lookup)

    @patch.object(RiskTreatment, "raise_access_request")
    def test_evaluation_deficit_action(self, action):
        lookup = RiskClassficiationEvalTreatmentLookup(
            deviation="Deficit",
            classification="Low",
            min_score=0.0,
            max_score=100,
            treatment="Action"
        )
        RiskClassficiationEvalTreatmentLookup.create(
            deviation="Deficit",
            classification="Low",
            min_score=0.0,
            max_score=100,
            treatment="Action"
        )
        evaluation = RiskEvaluation()
        risk_input = MagicMock()
        deviation = DeviationType.DEFICIT
        risk_input.type_of_deviation = deviation
        evaluation.evaluate(risk_input, 97.6)
        action.assert_called_with(risk_input, 97.6, lookup)
