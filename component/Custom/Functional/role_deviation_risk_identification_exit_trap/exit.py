"""Exit trap extension: role deviation risk identification component"""

from idmlib.components import component_log
from idmlib.components.extension import ExtScript

from Functional.role_deviation_common_library.helper import (
    get_account_risk_information,
    get_group_risk_information,
    get_groups_in_roles,
    get_target_accounts_in_roles,
    get_template_for_hostid
)
from Functional.role_deviation_risk_analysis.analyse import (
    DeviationType,
    RiskInformation,
    RiskAnalysisInput,
    RoleDeviationRiskAnalysis
)

from idmlib.idmobject import ResourceGroup, ResourceTemplate


class ExitTrap(ExtScript):
    """The exit trap extension for role deviation risk identification.

    Identifies deviations from role definitions and sends them for analysis.

    :param exit_obj: The exit trap object
    :type exit_obj: idmlib.exit.Exit
    :param dict state: The state dictionary.

    """

    def __init__(self, exit_obj, state):

        super().__init__()
        self.exit = exit_obj
        self.state = state
        self.log = component_log.getChild(__name__)
        self.risk_analysis = RoleDeviationRiskAnalysis()

    def wf_request_completed(self):
        """Executes when the workflow request is completed"""

        request = self.exit.request

        if request.parentreqid or request.autoressig:
            self.log.info(
                "Request has a parent request, we do not run for child "
                "requests."
            )
            return

        if request.status != 'C':
            self.log.info('Wrong request status: {}. Cannot continue.'
                               .format(request.status))
            return

        recipient = self.exit.recipient

        role_accounts = get_target_accounts_in_roles(
            recipient
        )
        role_templates = dict()
        for target_id in role_accounts:
            template_id = get_template_for_hostid(target_id)
            template = ResourceTemplate(template_id, target_id)
            role_templates[target_id] = template
        role_groups = get_groups_in_roles(
            recipient
        )
        role_group_dict = dict()
        for group_str in role_groups:
            target_id = group_str.split(":")[0]
            group_ip = group_str.split(":")[1]
            role_group_dict[group_str] = ResourceGroup(group_ip, target_id)

        user_accounts = set()
        target_accounts = dict()
        for account in recipient.accounts:
            user_accounts.add(account.hostid)
            target_accounts[account.hostid] = account

        user_groups = set()
        groups_dict = dict()
        for group in recipient.groups:
            user_groups.add(f"{group.hostid}:{group.groupid}")
            groups_dict[f"{group.hostid}:{group.groupid}"] = group

        surplus_accounts = user_accounts.difference(role_accounts)
        deficit_accounts = role_accounts.difference(user_accounts)
        surplus_groups = user_groups.difference(role_groups)
        deficit_groups = role_groups.difference(user_groups)

        deviations = (
                len(surplus_accounts) +
                len(surplus_groups) +
                len(deficit_accounts) +
                len(deficit_groups)
        )

        self.log.info(
            f"There are {deviations} total deviations.\r\n"
            f"Surplus Accounts: {len(surplus_accounts)} "
            f"Groups: {len(surplus_groups)}\r\n"
            f"Deficit Accounts: {len(deficit_accounts)} "
            f"Groups: {len(deficit_groups)}"
        )

        for account in surplus_accounts:
            template_id = get_template_for_hostid(account)
            risk_info = get_account_risk_information(
                template_id,
                is_surplus=True
            )
            risk_input = RiskAnalysisInput(
                recipient,
                target_accounts[account],
                DeviationType.SURPLUS,
                risk_info
            )
            self.risk_analysis.analyse(risk_input)
        for group_str in surplus_groups:
            group = groups_dict[group_str]
            risk_info = get_group_risk_information(
                group.hostid,
                group.groupid,
                is_surplus=True
            )
            risk_input = RiskAnalysisInput(
                recipient,
                group,
                DeviationType.SURPLUS,
                risk_info
            )
            self.risk_analysis.analyse(risk_input)
        for account in deficit_accounts:
            template_id = get_template_for_hostid(account)
            risk_info = get_account_risk_information(
                template_id
            )
            risk_input = RiskAnalysisInput(
                recipient,
                role_templates[account],
                DeviationType.DEFICIT,
                risk_info
            )
            self.risk_analysis.analyse(risk_input)
        for group_str in deficit_groups:
            group = role_group_dict[group_str]
            risk_info = get_group_risk_information(
                group.hostid,
                group.groupid
            )
            risk_input = RiskAnalysisInput(
                recipient,
                group,
                DeviationType.DEFICIT,
                risk_info
            )
            self.risk_analysis.analyse(risk_input)

    def process(self):
        """The extension process method."""

        pass
