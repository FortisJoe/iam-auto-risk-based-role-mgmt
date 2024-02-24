from idmlib.components.test import CommonTest
from unittest.mock import MagicMock, patch

from Functional.role_deviation_risk_analysis.analyse import (
    DeviationType,
    RiskInformation,
    RiskAnalysisInput,
    RoleDeviationRiskAnalysis
)
from Functional.role_deviation_risk_eval_treatment.evaluation import (
    RiskEvaluation
)


class TestRiskAnalysis(CommonTest):

    def test_deviation_type_surplus(self):
        deviation = DeviationType.SURPLUS
        self.assertEqual(str(deviation), "Surplus")

    def test_deviation_type_deficit(self):
        deviation = DeviationType.DEFICIT
        self.assertEqual(str(deviation), "Deficit")

    def test_risk_information(self):
        risk_info = RiskInformation(
            1,
            2,
            3,
            4.5
        )
        self.assertEqual(risk_info.confidentiality_impact, 1)
        self.assertEqual(risk_info.integrity_impact, 2)
        self.assertEqual(risk_info.availability_impact, 3)
        self.assertEqual(risk_info.annual_rate_of_occurrence, 4.5)

    def test_risk_analysis_input(self):
        profile = MagicMock()
        resource = MagicMock()
        type_of_deviation = DeviationType.SURPLUS
        risk_info = RiskInformation(
            1,
            2,
            3,
            4.5
        )
        risk_input = RiskAnalysisInput(
            profile,
            resource,
            type_of_deviation,
            risk_info
        )
        self.assertEqual(risk_input.profile, profile)
        self.assertEqual(risk_input.resource, resource)
        self.assertEqual(risk_input.type_of_deviation, type_of_deviation)
        self.assertEqual(risk_input.risk_information, risk_info)

    @patch.object(RiskEvaluation, "evaluate")
    def test_analyse(self, evaluate):
        analysis = RoleDeviationRiskAnalysis()
        risk_input = MagicMock()
        risk_info = MagicMock()
        risk_input.risk_information = risk_info
        risk_info.annual_rate_of_occurrence = 4.5
        risk_info.availability_impact = 1
        risk_info.confidentiality_impact = 2
        risk_info.integrity_impact = 3
        analysis.analyse(risk_input)
        evaluate.assert_called_with(risk_input, float(27))
