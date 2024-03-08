from idmlib import core
from idmlib.idmobject import Profile, ResourceGroup, ResourceTemplate
from idmlib.components import component_log, extension


from Functional.role_deviation_common_library.helper import (
    get_account_risk_information,
    get_group_risk_information,
    get_groups_in_roles,
    get_target_accounts_in_roles,
    get_template_for_hostid
)

from Functional.role_deviation_risk_analysis.analyse import (
    DeviationType,
    RiskAnalysisInput,
    RoleDeviationRiskAnalysis
)


class RiskIdentification:
    """The script for sched tasks to detect role deviations"""

    def __init__(self):
        """ __init__

        :param idtrack: The 'Functional.im_idtrack.idtrack.IDTrack plugin
        :param dict state: IDTrack state
        """
        self.log = component_log.getChild(__name__)
        self.risk_analysis = RoleDeviationRiskAnalysis()

    def process(self):
        for user in core.api.UserList(1):
            profile = Profile(user["userid"])
            if profile.is_valid:
                role_accounts = get_target_accounts_in_roles(
                    profile
                )
                role_templates = dict()
                for target_id in role_accounts:
                    template_id = get_template_for_hostid(target_id)
                    template = ResourceTemplate(template_id, target_id)
                    role_templates[target_id] = template
                role_groups = get_groups_in_roles(
                    profile
                )
                role_group_dict = dict()
                for group_str in role_groups:
                    target_id = group_str.split(":")[0]
                    group_ip = group_str.split(":")[1]
                    role_group_dict[group_str] = ResourceGroup(group_ip,
                                                               target_id)

                user_accounts = set()
                target_accounts = dict()
                for account in profile.accounts:
                    user_accounts.add(account.hostid)
                    target_accounts[account.hostid] = account

                user_groups = set()
                groups_dict = dict()
                for group in profile.groups:
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
                    f"There are {deviations} total deviations for "
                    f"{profile.userid}.\r\n"
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
                        profile,
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
                        profile,
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
                        profile,
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
                        profile,
                        group,
                        DeviationType.DEFICIT,
                        risk_info
                    )
                    self.risk_analysis.analyse(risk_input)


if __name__ == "__main__":
    process = RiskIdentification()
    process.process()
