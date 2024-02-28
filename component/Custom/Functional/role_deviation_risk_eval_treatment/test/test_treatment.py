from idmlib import core
from idmlib.components.test import CommonTest, InstalledComponent
from idmlib.idapi import APIError
from idmlib.idmemail import Email
from idmlib.idmobject import Request
from unittest.mock import MagicMock, patch

from Functional.hid_global_configuration.model import GlobalConfiguration
from Functional.role_deviation_risk_analysis.analyse import DeviationType
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

    @patch.object(Email, "set_from")
    @patch.object(Email, "add_to")
    @patch.object(Email, "set_content")
    @patch.object(Email, "set_subject")
    @patch.object(Email, "send_smtp")
    @patch.object(Request, "api_submit")
    def test_take_no_action(self, api_submit, send_smtp, set_subject, set_content, add_to, set_from):
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
        set_from.assert_called_with(core.instance.mail_sender_email)
        add_to.assert_called_with("no@action.com")
        set_content.assert_called_with("HTML No Action (Surplus, 12.3, Low)", html=True)
        set_subject.assert_called_with(f"Subject No Action")
        send_smtp.asset_called()
        api_submit.assert_not_called()

    @patch.object(Email, "set_from")
    @patch.object(Email, "add_to")
    @patch.object(Email, "set_content")
    @patch.object(Email, "set_subject")
    @patch.object(Email, "send_smtp")
    @patch.object(Request, "api_submit")
    def test_inform(self, api_submit, send_smtp, set_subject, set_content, add_to, set_from):
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
            value="component\\Custom\\Functional\\role_deviation_risk_eval_treatment\\test\\data\\inform.mako",
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
        risk_input.type_of_deviation = DeviationType.DEFICIT
        risk_score = 45.6
        treatment = MagicMock()
        treatment.classification = "Medium"
        risk_treatment = RiskTreatment()
        risk_treatment.inform(risk_input, risk_score, treatment)
        set_from.assert_called_with(core.instance.mail_sender_email)
        add_to.assert_called_with("notify@email.com")
        set_content.assert_called_with("HTML Inform (Deficit, 45.6, Medium)", html=True)
        set_subject.assert_called_with(f"Subject Inform")
        send_smtp.asset_called()
        api_submit.assert_not_called()

    @patch.object(Email, "set_from")
    @patch.object(Email, "add_to")
    @patch.object(Email, "set_content")
    @patch.object(Email, "set_subject")
    @patch.object(Email, "send_smtp")
    @patch.object(Request, "api_submit")
    def test_action(self, api_submit, send_smtp, set_subject, set_content, add_to, set_from):
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
        risk_input.type_of_deviation = DeviationType.DEFICIT
        risk_score = 78.9
        profile = MagicMock()
        risk_input.profile.return_value = profile
        profile.userid.return_value = "user123"
        treatment = MagicMock()
        treatment.classification = "High"
        risk_treatment = RiskTreatment()
        risk_treatment.raise_access_request(risk_input, risk_score, treatment)
        set_from.assert_called_with(core.instance.mail_sender_email)
        add_to.assert_called_with("action@email.com")
        set_content.assert_called_with("HTML Action (Deficit, 78.9, High)", html=True)
        set_subject.assert_called_with(f"Subject Action")
        send_smtp.asset_called()
        api_submit.asset_called()

    @patch.object(Email, "set_from")
    @patch.object(Email, "add_to")
    @patch.object(Email, "set_content")
    @patch.object(Email, "set_subject")
    @patch.object(Email, "send_smtp")
    @patch.object(Request, "api_submit")
    @patch('idmlib.core.api')
    def test_action_fail_to_raise(self, api, api_submit, send_smtp, set_subject, set_content, add_to, set_from):
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
        risk_score = 45.6
        profile = MagicMock()
        risk_input.profile.return_value = profile
        profile.userid.return_value = "user123"
        treatment = MagicMock()
        treatment.classification = "High"
        api_submit.side_effect = APIError(24, "Attribute Errors")
        risk_treatment = RiskTreatment()
        risk_treatment.raise_access_request(risk_input, risk_score, treatment)
        set_from.assert_called_with(core.instance.mail_sender_email)
        add_to.assert_called_with("action@email.com")
        set_content.assert_called_with("HTML Action (Surplus, 45.6, High)", html=True)
        set_subject.assert_called_with(f"Subject Action")
        send_smtp.asset_called()
        api.WFRequestCancel.assert_called()
