from enum import Enum

from Functional.role_deviation_risk_eval_treatment.evaluation import RiskEvaluation


class DeviationType(Enum):
    SURPLUS = 1
    DEFICIT = 2

    def __str__(self):
        if self.value == self.SURPLUS:
            return "Surplus"
        else:
            return "Deficit"


class RiskInformation:
    
    def __init__(self, confidentiality_impact, integrity_impact, availability_impact, annual_rate_of_occurrence):
        """

        :param confidentiality_impact: The impact on confidentiality
        :type confidentiality_impact: int
        :param integrity_impact: The impact on integrity
        :type integrity_impact: int
        :param availability_impact: The impact on availability
        :type availability_impact: int
        :param annual_rate_of_occurrence: How often per year this risk occurs
        :type annual_rate_of_occurrence: double
        
        
        """
        self.confidentiality_impact = confidentiality_impact
        self.integrity_impact = integrity_impact
        self.availability_impact = availability_impact
        self.annual_rate_of_occurrence = annual_rate_of_occurrence


class RiskAnalysisInput:
    
    def __init__(self, profile, resource, type_of_deviation, risk_information):
        """

        :param profile: User Profile who has deviation
        :type profile: idmlib.idmobject.Profile
        :param resource: The resource in deviation
        :type resource: idmlib.idmobject._BaseResource
        :param type_of_deviation: The type of deviation - Surplus or Deficit
        :type type_of_deviation: DeviationType
        :param risk_information: The risk information for this resource and
        type of deviation
        :type risk_information: RiskInformation

        """
        self.profile = profile
        self.resource = resource
        self.type_of_deviation = type_of_deviation
        self.risk_information = risk_information


class RoleDeviationRiskAnalysis:
    _instance = None
    _evaluation = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(RoleDeviationRiskAnalysis, cls).__new__(cls)
            cls._instance._evaluation = RiskEvaluation()
        return cls._instance

    def analyse(self, risk_input):
        """

        :type risk_input: RiskAnalysisInput
        """
        info = risk_input.risk_information
        risk_score = info.annual_rate_of_occurrence * (
                info.availability_impact +
                info.confidentiality_impact +
                info.integrity_impact
        )
        self._evaluation.evaluate(
            risk_input,
            risk_score
        )