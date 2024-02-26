import os

from idmlib import core
from idmlib.components.test import CommonTest, InstalledComponent, CommonModel
from idmlib.idmemail import Email
from idmlib.idmobject import Request
from unittest.mock import MagicMock, patch

from Functional.role_deviation_risk_analysis.analyse import DeviationType
from Functional.hid_global_configuration.config import ConfigData
from Functional.hid_global_configuration.model import GlobalConfiguration

from Functional.role_deviation_risk_eval_treatment.treatment import RiskTreatment


class TestRiskTreatment(CommonTest):

    @classmethod
    def setUp(cls):
        """Performs set up for the test class."""

        InstalledComponent(
            'Functional.hid_global_configuration').install()

    @classmethod
    def tearDown(cls):
        """Performs tear down for the test class."""

        InstalledComponent(
            'Functional.hid_global_configuration').teardown()

    @patch("idmlib.idmemail.Email")
    @patch("idmlib.idmobject.Request")
    def test_take_no_action(self, email, request):
        GlobalConfiguration.create(
            namespace="RDRM",
            setting="NO_ACTION_EMAIL_MAKO",
            key=None,
            value="component\\Custom\\Functional\\role_deviation_risk_eval_treatment\\test\\data\\no_action.mako",
            description=None
        )
        GlobalConfiguration.create(
            namespace="RDRM",
            setting="NOTIFY_EMAIL_MAKO",
            key=None,
            value="component\\Custom\\Functional\\role_deviation_risk_eval_treatment\\test\\data\\notify.mako",
            description=None
        )
        GlobalConfiguration.create(
            namespace="RDRM",
            setting="ACTION_EMAIL_MAKO",
            key=None,
            value="component\\Custom\\Functional\\role_deviation_risk_eval_treatment\\test\\data\\action.mako",
            description=None
        )
        GlobalConfiguration.create(
            namespace="RDRM",
            setting="NO_ACTION_EMAIL",
            key=None,
            value="no@action.com",
            description=None
        )
        GlobalConfiguration.create(
            namespace="RDRM",
            setting="NOTIFY_EMAIL",
            key=None,
            value="notify@email.com",
            description=None
        )
        GlobalConfiguration.create(
            namespace="RDRM",
            setting="ACTION_EMAIL",
            key=None,
            value="action@email.com",
            description=None
        )
        GlobalConfiguration.create(
            namespace="RDRM",
            setting="PDR",
            key=None,
            value="THE_PDR",
            description=None
        )
        risk_input = MagicMock()
        risk_input.type_of_deviation = DeviationType.SURPLUS
        risk_score = 12.3
        treatment = MagicMock()
        treatment.classification = "Low"
        risk_treatment = RiskTreatment()
        risk_treatment.take_no_action(risk_input, risk_score, treatment)
        email.set_from.assert_called_with(core.instance.mail_sender_email)
        email.add_to.assert_called_with("no@action.com")
        email.set_content.assert_called_with("HTML No Action", html=True)
        email.set_subject.assert_called_with(f"Subject No Action (Surplus, 12.3, Low)")
        email.send_smtp.asset_called()
        request.preqid.assert_not_called()
        request.recipid.assert_not_called()
        request.attr_actions_populate.assert_not_called()
        request.reason.assert_not_called()
        request.log.assert_not_called()
        request.api_submit.assert_not_called()

