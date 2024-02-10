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
    RiskAnalysisInput,
    RoleDeviationRiskAnalysis
)


class IDTrack(ExtScript):
    """The IDTrack plugin to detect role deviations via tracked changes"""

    def __init__(self, idtrack, state):
        """ __init__

        :param idtrack: The 'Functional.im_idtrack.idtrack.IDTrack plugin
        :param dict state: IDTrack state
        """
        super().__init__()
        self.idtrack = idtrack
        self.state = state
        self.log = component_log.getChild(__name__)
        self.risk_analysis = RoleDeviationRiskAnalysis()

    def diff_account_added(self, accounts, reqdict, profile, change):
        """Process accounts that were added.

        :param list accounts: New :any:`idmlib.idmobject.ResourceAccount`
        objects.
        :param change: The :any:`idmlib.diffset.DiffItem` change.
        :param profile: The :any:`idmlib.idmobject.Profile`, if available.
        :param dict reqdict: A dict of requests, passed to all diff_* methods.

        """

        if profile and profile.is_valid:
            targets_with_accounts_in_roles = get_target_accounts_in_roles(
                profile
            )
            for account in accounts:
                if account.hostid not in targets_with_accounts_in_roles:
                    template_id = get_template_for_hostid(account.hostid)
                    risk_info = get_account_risk_information(
                        template_id,
                        is_surplus=True
                    )
                    risk_input = RiskAnalysisInput(
                        profile,
                        account,
                        DeviationType.SURPLUS,
                        risk_info
                    )
                    self.risk_analysis.analyse(risk_input)

    def diff_account_deleted(self, accounts, reqdict, profile, change):
        """Process accounts that were deleted.

        :param list accounts: Deleted :any:`idmlib.idmobject.ResourceAccount` 
        objects.
        :param change: The :any: `idmlib.diffset.DiffItem` change.
        :param profile: The :any:`idmlib.idmobject.Profile`, if available.
        :param dict reqdict: A dict of requests, passed to all diff_* methods.

        """
        if profile and profile.is_valid:
            targets_with_accounts_in_roles = get_target_accounts_in_roles(
                profile
            )
            for account in accounts:
                if account.hostid in targets_with_accounts_in_roles:
                    template_id = get_template_for_hostid(account.hostid)
                    risk_info = get_account_risk_information(
                        template_id
                    )
                    risk_input = RiskAnalysisInput(
                        profile,
                        account,
                        DeviationType.DEFICIT,
                        risk_info
                    )
                    self.risk_analysis.analyse(risk_input)

    def diff_group_member_added(self, groups, reqdict, profile, change):
        """Process profile-centric group membership additions.

        :param list groups: Added :any:`idmlib.idmobject.ResourceGroup`
        objects.
        :param change: The :any: `idmlib.diffset.DiffItem` change.
        :param profile: The :any:`idmlib.idmobject.Profile`, if available.
        :param dict reqdict: A dict of requests, passed to all diff_* methods.

        """
        if profile and profile.is_valid:
            groups_in_roles = get_groups_in_roles(profile)
            for group in groups:
                group_concat = f"{group.hostid}:{group.groupid}"
                if group_concat not in groups_in_roles:
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

    def diff_group_member_deleted(self, groups, reqdict, profile, change):
        """Process profile-centric group membership deletions.

        :param list groups: Deleted :any:`idmlib.idmobject.ResourceGroup`
        objects.
        :param change: The :any: `idmlib.diffset.DiffItem` change.
        :param profile: The :any:`idmlib.idmobject.Profile`, if available.
        :param dict reqdict: A dict of requests, passed to all diff_* methods.

        """
        if profile and profile.is_valid:
            groups_in_roles = get_groups_in_roles(profile)
            for group in groups:
                group_concat = f"{group.hostid}:{group.groupid}"
                if group_concat in groups_in_roles:
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




