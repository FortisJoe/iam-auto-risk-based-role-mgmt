"""Defines the Policy and Logic model for using Risk Assessment."""
from Functional.hid_extdb.model import BaseModel
from peewee import Check, CompositeKey, DoubleField, TextField


class RiskClassficiationEvalTreatmentLookup(BaseModel):
    """Lookup table to lookup the risk level, and risk treatment, based on risk

    :var str deviation: If this lookup is for Deficit or Surplus
    :var str classification: Risk classification text for display.
    :var double min_score: Minimum risk score for this lookup
    :var double max_score: Maximum risk score for this lookup
    :var str treatment: Which risk treatment option should be used

    """
    deviation = TextField(
        null=False,
        column_name='Deviation',
        default='Deficit',
        constraints=[Check("Deviation IN ('Deficit', 'Surplus')")]
    )
    classification = TextField(
        null=False,
        column_name='Classification',
        default='Low',
        constraints=[Check("Classification IN ('Low', 'Medium', 'High')")]
    )
    min_score = DoubleField(
        null=False,
        column_name='MinimumScore',
        default=0
    )
    max_score = DoubleField(
        null=True,
        column_name='MaximumScore',
        constraints=[
            Check("MaximumScore IS NULL OR MaximumScore > MinimumScore")
        ]
    )
    treatment = TextField(
        null=False,
        column_name='Treatment',
        default='No Action',
        constraints=[Check("Treatment IN ('No Action', 'Inform', 'Action')")]
    )
    _column_order = [
        'Deviation', 'Classification', 'MinimumScore', 'MaximumScore',
        'Treatment', 'ComponentOwnerFQN'
    ]

    """ Lookup based on risk value and deviation

    :var double risk_value: Risk score for this lookup
    :var str deviation: If this lookup is for Deficit or Surplus.
    """
    @staticmethod
    def get_treatment_for_risk_level(risk_score, deviation):
        return RiskClassficiationEvalTreatmentLookup.select().where(
            RiskClassficiationEvalTreatmentLookup.deviation == deviation &
            RiskClassficiationEvalTreatmentLookup.min_score <= risk_score &
            (
                RiskClassficiationEvalTreatmentLookup.max_score >> None |
                RiskClassficiationEvalTreatmentLookup.min_score > risk_score
            )
        ).get()

    class Meta:
        """Meta class overrides for the Table"""

        table_name = 'role_deviation_risk_classification_evaluation_treatment'
        primary_key = CompositeKey("deviation", "min_score", "max_score")
