import os

from idmlib import core, idmemail
from idmlib.idmobject import Request
from idmlib.components import component_log

from Functional.hid_email_notification import template
from Functional.hid_global_configuration.config import ConfigData

log = component_log.getChild(__name__)


class RiskTreatment:

    def __init__(self):
        config_rows = ConfigData("RDRM").get_rows()
        self._mako_template_root = core.instance.path_instance
        self._no_action_email_mako = None
        self._no_action_email_addresses = set()
        self._notify_email_mako = None
        self._notify_email_addresses = set()
        self._action_email_mako = None
        self._action_email_addresses = set()
        self._pdr_id = None
        for row in config_rows:
            if row.setting == "NO_ACTION_EMAIL_MAKO":
                self._no_action_email_mako = row.value
            elif row.setting == "NO_ACTION_EMAIL":
                self._no_action_email_addresses.add(row.value)
            elif row.setting == "NOTIFY_EMAIL_MAKO":
                self._notify_email_mako = row.value
            elif row.setting == "NOTIFY_EMAIL":
                self._notify_email_addresses.add(row.value)
            elif row.setting == "ACTION_EMAIL_MAKO":
                self._action_email_mako = row.value
            elif row.setting == "ACTION_EMAIL":
                self._action_email_addresses.add(row.value)
            elif row.setting == "PDR":
                self._pdr_id = row.value

    def take_no_action(
            self,
            risk_input,
            risk_score,
            treatment
    ):
        log.info(f"Taking no action for a risk score of {risk_score}, send email informing of this")
        template = self._get_mako_template(self._no_action_email_mako)
        html = template.get_body_html({"risk_input": risk_input, "risk_score": risk_score, "treatment": treatment}, None)
        subject = template.get_subject()
        self.send_email(self._no_action_email_addresses, html, subject)

    def inform(
            self,
            risk_input,
            risk_score,
            treatment
    ):
        log.info(f"Need to inmform for a risk score of {risk_score}, send email informing of this")
        template = self._get_mako_template(self._notify_email_mako)
        html = template.get_body_html({"risk_input": risk_input, "risk_score": risk_score, "treatment": treatment},
                                      None)
        subject = template.get_subject()
        self.send_email(self._notify_email_addresses, html, subject)

    def raise_access_request(
            self,
            risk_input,
            risk_score,
            treatment
    ):
        log.info(f"Need to raise an access request for a risk score of {risk_score}, send email informing of this")
        template = self._get_mako_template(self._action_email_mako)
        html = template.get_body_html({"risk_input": risk_input, "risk_score": risk_score, "treatment": treatment},
                                      None)
        subject = template.get_subject()
        self.send_email(self._action_email_addresses, html, subject)
        log.info(f"Raising an access request")
        request = Request
        request.preqid = self._pdr_id
        request.recipid = risk_input.profile.userid
        request.attr_actions_populate = True
        request.reason = (
            "Raising a request to correct a deviation from role access."
        )
        self.submit_request(request)

    def _get_mako_template(self, mako_template_path):
        """Fetches mako template

        :return: Mako Template
        :rtype Functional.hid_email_notification.template.MakoEmailTemplate:

        """

        if not os.path.isabs(mako_template_path):
            mako_template_path = os.path.join(
                self._mako_template_root, mako_template_path
            )

        return template.MakoEmailTemplate(mako_template_path, "en-us")

    def send_email(self, email_addresses, email_html, subject):
        """ Sends the email

        :param email_addresses: email addresses to send email to
        :type email_addresses: set
        :param email_html: email HTML content
        :type email_html: str
        :param subject: Email subject
        :type subject: str

        """
        emails = ", ".join(email_addresses)

        log.info(
            f"Sending the following email to {emails}\r\nSubject: {subject}"
        )
        try:
            emailer = idmemail.Email()
            emailer.set_from(core.instance.mail_sender_email)
            for email_address in email_addresses:
                emailer.add_to(email_address)
            emailer.set_content(email_html, html=True)
            emailer.set_subject(subject)
            emailer.send_smtp()
        except Exception as e:
            log.error(f"Failed to send email because {e}")

    def submit_request(self, request):
        # Distributes requests amongst app nodes
        serverid = 'RANDOM'
        # Attempt request submission.
        try:
            request.log = log
            request.api_submit(serverid=serverid)
        except Exception as e:
            log.exception(e)
            log.error('Failed to submit request.')

            # Attempt abandoned request cleanup.
            try:
                core.api.WFRequestCancel(
                    request.reqid,
                    request.recipid,
                    'Abandoned request cleanup.',
                    request.serverid
                )
                log.info('Successfully cleaned up unposted request.')
            except Exception as e:
                log.exception(e)
                log.error('Failed to cleanup unposted request.')

            return
