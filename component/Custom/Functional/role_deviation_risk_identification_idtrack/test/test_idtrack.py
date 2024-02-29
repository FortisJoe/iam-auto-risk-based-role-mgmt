from idmlib.components.test import CommonTest
from idmlib.idmobject import Profile
from unittest.mock import MagicMock, patch, PropertyMock

from Functional.role_deviation_risk_analysis.analyse import (
    DeviationType,
    RiskInformation,
    RiskAnalysisInput,
    RoleDeviationRiskAnalysis
)
from Functional.role_deviation_risk_identification_idtrack.idtrack import (
    IDTrack
)


class TestExitTrap(CommonTest):

    @patch.object(RoleDeviationRiskAnalysis, "analyse")
    def test_diff_account_added_no_profile(self, analyse):
        idtrack_plugin = MagicMock()
        idtrack = IDTrack(idtrack_plugin, {})
        change = MagicMock()
        idtrack.diff_account_added([], {}, None, change)
        analyse.assert_not_called()

    @patch.object(RoleDeviationRiskAnalysis, "analyse")
    def test_diff_account_added_profile_not_profile(self, analyse):
        idtrack_plugin = MagicMock()
        idtrack = IDTrack(idtrack_plugin, {})
        change = MagicMock()
        profile = MagicMock()
        idtrack.diff_account_added([], {}, profile, change)
        analyse.assert_not_called()

    @patch.object(RoleDeviationRiskAnalysis, "analyse")
    def test_diff_account_added_profile_not_valid(self, analyse):
        idtrack_plugin = MagicMock()
        idtrack = IDTrack(idtrack_plugin, {})
        change = MagicMock()
        profile = MagicMock(spec=Profile)
        is_valid = PropertyMock(return_value=False)
        type(profile).is_valid = is_valid
        idtrack.diff_account_added([], {}, profile, change)
        analyse.assert_not_called()

    @patch.object(RoleDeviationRiskAnalysis, "analyse")
    @patch('idmlib.core.api')
    def test_diff_account_added_role_with_account_no_added_account(self, api, analyse):
        idtrack_plugin = MagicMock()
        idtrack = IDTrack(idtrack_plugin, {})
        change = MagicMock()
        profile = MagicMock(spec=Profile)
        is_valid = PropertyMock(return_value=True)
        type(profile).is_valid = is_valid
        role = MagicMock()
        role.roleid = "ROLE1"
        roles = PropertyMock(return_value=[role])
        type(profile).roles = roles
        api.RoleResourceList.return_value = [
            {
                "membertype": "TEMPLATE",
                "memberid": "AD_TEMPLATE"
            },
            {
                "membertype": "MANAGEDGROUP",
                "memberid": "AD",
                "groupid": "Group1"
            }
        ]
        api.ResourceGet.return_value = [
            [
                "hostid",
                "AD"
            ]
        ]
        idtrack.diff_account_added([], {}, profile, change)
        analyse.assert_not_called()

    @patch.object(RoleDeviationRiskAnalysis, "analyse")
    @patch('idmlib.core.api')
    def test_diff_account_added_role_with_account_added_account_is_in_role(self, api, analyse):
        idtrack_plugin = MagicMock()
        idtrack = IDTrack(idtrack_plugin, {})
        change = MagicMock()
        profile = MagicMock(spec=Profile)
        is_valid = PropertyMock(return_value=True)
        type(profile).is_valid = is_valid
        role = MagicMock()
        role.roleid = "ROLE1"
        roles = PropertyMock(return_value=[role])
        type(profile).roles = roles
        api.RoleResourceList.return_value = [
            {
                "membertype": "TEMPLATE",
                "memberid": "AD_TEMPLATE"
            },
            {
                "membertype": "MANAGEDGROUP",
                "memberid": "AD",
                "groupid": "Group1"
            }
        ]
        api.ResourceGet.return_value = [
            [
                "hostid",
                "AD"
            ]
        ]
        account = MagicMock()
        hostid = PropertyMock(return_value="AD")
        type(account).hostid = hostid
        idtrack.diff_account_added([account], {}, profile, change)
        analyse.assert_not_called()

    @patch.object(RoleDeviationRiskAnalysis, "analyse")
    @patch('idmlib.core.api')
    def test_diff_account_added_role_with_no_account_new_account(self, api, analyse):
        idtrack_plugin = MagicMock()
        idtrack = IDTrack(idtrack_plugin, {})
        change = MagicMock()
        profile = MagicMock(spec=Profile)
        is_valid = PropertyMock(return_value=True)
        type(profile).is_valid = is_valid
        role = MagicMock()
        role.roleid = "ROLE1"
        roles = PropertyMock(return_value=[role])
        type(profile).roles = roles
        api.RoleResourceList.return_value = [
            {
                "membertype": "MANAGEDGROUP",
                "memberid": "AD",
                "groupid": "Group1"
            }
        ]
        account = MagicMock()
        hostid = PropertyMock(return_value="AD")
        type(account).hostid = hostid
        api.ResourceFind.return_value = [
            {
                "resourceid": "AD_TEMPLATE",
                "resourceid2": ""
            }
        ]
        api.ResourceAttrsGet.return_value = [
            {"name": "SURPLUS_CONFIDENTIALITY_IMPACT", "value": "5"},
            {"name": "SURPLUS_INTEGRITY_IMPACT", "value": "6"},
            {"name": "SURPLUS_AVAILABILITY_IMPACT", "value": "7"},
            {"name": "SURPLUS_ANNUAL_RISK_OF_OCCURRENCE", "value": "8.9"}
        ]
        idtrack.diff_account_added([account], {}, profile, change)
        analyse.assert_called_once()
        result_risk_analysis = analyse.call_args_list[0][0][0]
        assert profile == result_risk_analysis.profile
        assert account == result_risk_analysis.resource
        assert DeviationType.SURPLUS == result_risk_analysis.type_of_deviation
        assert 5 == result_risk_analysis.risk_information.confidentiality_impact
        assert 6 == result_risk_analysis.risk_information.integrity_impact
        assert 7 == result_risk_analysis.risk_information.availability_impact
        assert 8.9 == result_risk_analysis.risk_information.annual_rate_of_occurrence

    @patch.object(RoleDeviationRiskAnalysis, "analyse")
    @patch('idmlib.core.api')
    def test_diff_account_added_role_with_account_added_account_is_not_in_role(self, api, analyse):
        idtrack_plugin = MagicMock()
        idtrack = IDTrack(idtrack_plugin, {})
        change = MagicMock()
        profile = MagicMock(spec=Profile)
        is_valid = PropertyMock(return_value=True)
        type(profile).is_valid = is_valid
        role = MagicMock()
        role.roleid = "ROLE1"
        roles = PropertyMock(return_value=[role])
        type(profile).roles = roles
        api.RoleResourceList.return_value = [
            {
                "membertype": "TEMPLATE",
                "memberid": "AD_TEMPLATE"
            },
            {
                "membertype": "MANAGEDGROUP",
                "memberid": "AD",
                "groupid": "Group1"
            }
        ]
        api.ResourceGet.return_value = [
            [
                "hostid",
                "AD"
            ]
        ]
        account = MagicMock()
        hostid = PropertyMock(return_value="SAP_GRC")
        type(account).hostid = hostid
        api.ResourceFind.return_value = [
            {
                "resourceid": "SAP_GRC_TEMPLATE",
                "resourceid2": ""
            }
        ]
        api.ResourceAttrsGet.return_value = [
            {"name": "SURPLUS_CONFIDENTIALITY_IMPACT", "value": "5"},
            {"name": "SURPLUS_INTEGRITY_IMPACT", "value": "6"},
            {"name": "SURPLUS_AVAILABILITY_IMPACT", "value": "7"},
            {"name": "SURPLUS_ANNUAL_RISK_OF_OCCURRENCE", "value": "8.9"}
        ]
        idtrack.diff_account_added([account], {}, profile, change)
        analyse.assert_called_once()
        result_risk_analysis = analyse.call_args_list[0][0][0]
        assert profile == result_risk_analysis.profile
        assert account == result_risk_analysis.resource
        assert DeviationType.SURPLUS == result_risk_analysis.type_of_deviation
        assert 5 == result_risk_analysis.risk_information.confidentiality_impact
        assert 6 == result_risk_analysis.risk_information.integrity_impact
        assert 7 == result_risk_analysis.risk_information.availability_impact
        assert 8.9 == result_risk_analysis.risk_information.annual_rate_of_occurrence

    @patch.object(RoleDeviationRiskAnalysis, "analyse")
    def test_diff_account_deleted_no_profile(self, analyse):
        idtrack_plugin = MagicMock()
        idtrack = IDTrack(idtrack_plugin, {})
        change = MagicMock()
        idtrack.diff_account_deleted([], {}, None, change)
        analyse.assert_not_called()

    @patch.object(RoleDeviationRiskAnalysis, "analyse")
    def test_diff_account_deleted_profile_not_profile(self, analyse):
        idtrack_plugin = MagicMock()
        idtrack = IDTrack(idtrack_plugin, {})
        change = MagicMock()
        profile = MagicMock()
        idtrack.diff_account_deleted([], {}, profile, change)
        analyse.assert_not_called()

    @patch.object(RoleDeviationRiskAnalysis, "analyse")
    def test_diff_account_deleted_profile_not_valid(self, analyse):
        idtrack_plugin = MagicMock()
        idtrack = IDTrack(idtrack_plugin, {})
        change = MagicMock()
        profile = MagicMock(spec=Profile)
        is_valid = PropertyMock(return_value=False)
        type(profile).is_valid = is_valid
        idtrack.diff_account_deleted([], {}, profile, change)
        analyse.assert_not_called()

    @patch.object(RoleDeviationRiskAnalysis, "analyse")
    @patch('idmlib.core.api')
    def test_diff_account_deleted_role_with_account_no_deleted_account(self, api, analyse):
        idtrack_plugin = MagicMock()
        idtrack = IDTrack(idtrack_plugin, {})
        change = MagicMock()
        profile = MagicMock(spec=Profile)
        is_valid = PropertyMock(return_value=True)
        type(profile).is_valid = is_valid
        role = MagicMock()
        role.roleid = "ROLE1"
        roles = PropertyMock(return_value=[role])
        type(profile).roles = roles
        api.RoleResourceList.return_value = [
            {
                "membertype": "TEMPLATE",
                "memberid": "AD_TEMPLATE"
            },
            {
                "membertype": "MANAGEDGROUP",
                "memberid": "AD",
                "groupid": "Group1"
            }
        ]
        api.ResourceGet.return_value = [
            [
                "hostid",
                "AD"
            ]
        ]
        idtrack.diff_account_deleted([], {}, profile, change)
        analyse.assert_not_called()

    @patch.object(RoleDeviationRiskAnalysis, "analyse")
    @patch('idmlib.core.api')
    def test_diff_account_deleted_role_with_account_deleted_account_is_in_role(self, api, analyse):
        idtrack_plugin = MagicMock()
        idtrack = IDTrack(idtrack_plugin, {})
        change = MagicMock()
        profile = MagicMock(spec=Profile)
        is_valid = PropertyMock(return_value=True)
        type(profile).is_valid = is_valid
        role = MagicMock()
        role.roleid = "ROLE1"
        roles = PropertyMock(return_value=[role])
        type(profile).roles = roles
        api.RoleResourceList.return_value = [
            {
                "membertype": "TEMPLATE",
                "memberid": "AD_TEMPLATE"
            },
            {
                "membertype": "MANAGEDGROUP",
                "memberid": "AD",
                "groupid": "Group1"
            }
        ]
        api.ResourceGet.return_value = [
            [
                "hostid",
                "AD"
            ]
        ]
        account = MagicMock()
        hostid = PropertyMock(return_value="AD")
        type(account).hostid = hostid
        api.ResourceFind.return_value = [
            {
                "resourceid": "AD_TEMPLATE",
                "resourceid2": ""
            }
        ]
        api.ResourceAttrsGet.return_value = [
            {"name": "DEFICIT_CONFIDENTIALITY_IMPACT", "value": "1"},
            {"name": "DEFICIT_INTEGRITY_IMPACT", "value": "2"},
            {"name": "DEFICIT_AVAILABILITY_IMPACT", "value": "3"},
            {"name": "DEFICIT_ANNUAL_RISK_OF_OCCURRENCE", "value": "4.5"}
        ]
        idtrack.diff_account_deleted([account], {}, profile, change)
        analyse.assert_called_once()
        result_risk_analysis = analyse.call_args_list[0][0][0]
        assert profile == result_risk_analysis.profile
        assert account == result_risk_analysis.resource
        assert DeviationType.DEFICIT == result_risk_analysis.type_of_deviation
        assert 1 == result_risk_analysis.risk_information.confidentiality_impact
        assert 2 == result_risk_analysis.risk_information.integrity_impact
        assert 3 == result_risk_analysis.risk_information.availability_impact
        assert 4.5 == result_risk_analysis.risk_information.annual_rate_of_occurrence

    @patch.object(RoleDeviationRiskAnalysis, "analyse")
    @patch('idmlib.core.api')
    def test_diff_account_deleted_role_with_no_account_deleted_account(self, api, analyse):
        idtrack_plugin = MagicMock()
        idtrack = IDTrack(idtrack_plugin, {})
        change = MagicMock()
        profile = MagicMock(spec=Profile)
        is_valid = PropertyMock(return_value=True)
        type(profile).is_valid = is_valid
        role = MagicMock()
        role.roleid = "ROLE1"
        roles = PropertyMock(return_value=[role])
        type(profile).roles = roles
        api.RoleResourceList.return_value = [
            {
                "membertype": "MANAGEDGROUP",
                "memberid": "AD",
                "groupid": "Group1"
            }
        ]
        account = MagicMock()
        hostid = PropertyMock(return_value="AD")
        type(account).hostid = hostid
        api.ResourceFind.return_value = [
            {
                "resourceid": "AD_TEMPLATE",
                "resourceid2": ""
            }
        ]
        idtrack.diff_account_deleted([account], {}, profile, change)
        analyse.assert_not_called()

    @patch.object(RoleDeviationRiskAnalysis, "analyse")
    @patch('idmlib.core.api')
    def test_diff_account_deleted_role_with_account_deleted_account_is_not_in_role(self, api, analyse):
        idtrack_plugin = MagicMock()
        idtrack = IDTrack(idtrack_plugin, {})
        change = MagicMock()
        profile = MagicMock(spec=Profile)
        is_valid = PropertyMock(return_value=True)
        type(profile).is_valid = is_valid
        role = MagicMock()
        role.roleid = "ROLE1"
        roles = PropertyMock(return_value=[role])
        type(profile).roles = roles
        api.RoleResourceList.return_value = [
            {
                "membertype": "TEMPLATE",
                "memberid": "AD_TEMPLATE"
            },
            {
                "membertype": "MANAGEDGROUP",
                "memberid": "AD",
                "groupid": "Group1"
            }
        ]
        api.ResourceGet.return_value = [
            [
                "hostid",
                "AD"
            ]
        ]
        account = MagicMock()
        hostid = PropertyMock(return_value="SAP_GRC")
        type(account).hostid = hostid
        api.ResourceFind.return_value = [
            {
                "resourceid": "SAP_GRC_TEMPLATE",
                "resourceid2": ""
            }
        ]
        idtrack.diff_account_deleted([account], {}, profile, change)
        analyse.assert_not_called()

    @patch.object(RoleDeviationRiskAnalysis, "analyse")
    def test_diff_group_member_added_no_profile(self, analyse):
        idtrack_plugin = MagicMock()
        idtrack = IDTrack(idtrack_plugin, {})
        change = MagicMock()
        idtrack.diff_group_member_added([], {}, None, change)
        analyse.assert_not_called()

    @patch.object(RoleDeviationRiskAnalysis, "analyse")
    def test_diff_group_member_added_profile_not_profile(self, analyse):
        idtrack_plugin = MagicMock()
        idtrack = IDTrack(idtrack_plugin, {})
        change = MagicMock()
        profile = MagicMock()
        idtrack.diff_group_member_added([], {}, profile, change)
        analyse.assert_not_called()

    @patch.object(RoleDeviationRiskAnalysis, "analyse")
    def test_diff_group_member_added_profile_not_valid(self, analyse):
        idtrack_plugin = MagicMock()
        idtrack = IDTrack(idtrack_plugin, {})
        change = MagicMock()
        profile = MagicMock(spec=Profile)
        is_valid = PropertyMock(return_value=False)
        type(profile).is_valid = is_valid
        idtrack.diff_group_member_added([], {}, profile, change)
        analyse.assert_not_called()

    @patch.object(RoleDeviationRiskAnalysis, "analyse")
    @patch('idmlib.core.api')
    def test_diff_group_member_added_role_with_account_no_added_account(self, api, analyse):
        idtrack_plugin = MagicMock()
        idtrack = IDTrack(idtrack_plugin, {})
        change = MagicMock()
        profile = MagicMock(spec=Profile)
        is_valid = PropertyMock(return_value=True)
        type(profile).is_valid = is_valid
        role = MagicMock()
        role.roleid = "ROLE1"
        roles = PropertyMock(return_value=[role])
        type(profile).roles = roles
        api.RoleResourceList.return_value = [
            {
                "membertype": "TEMPLATE",
                "memberid": "AD_TEMPLATE"
            },
            {
                "membertype": "MANAGEDGROUP",
                "memberid": "AD",
                "groupid": "Group1"
            }
        ]
        api.ResourceGet.return_value = [
            [
                "hostid",
                "AD"
            ]
        ]
        idtrack.diff_group_member_added([], {}, profile, change)
        analyse.assert_not_called()

    @patch.object(RoleDeviationRiskAnalysis, "analyse")
    @patch('idmlib.core.api')
    def test_diff_group_member_added_role_with_group_added_group_is_in_role(self, api, analyse):
        idtrack_plugin = MagicMock()
        idtrack = IDTrack(idtrack_plugin, {})
        change = MagicMock()
        profile = MagicMock(spec=Profile)
        is_valid = PropertyMock(return_value=True)
        type(profile).is_valid = is_valid
        role = MagicMock()
        role.roleid = "ROLE1"
        roles = PropertyMock(return_value=[role])
        type(profile).roles = roles
        api.RoleResourceList.return_value = [
            {
                "membertype": "TEMPLATE",
                "memberid": "AD_TEMPLATE"
            },
            {
                "membertype": "MANAGEDGROUP",
                "memberid": "AD",
                "groupid": "Group1"
            }
        ]
        group = MagicMock()
        hostid = PropertyMock(return_value="AD")
        type(group).hostid = hostid
        groupid = PropertyMock(return_value="Group1")
        type(group).groupid = groupid
        idtrack.diff_group_member_added([group], {}, profile, change)
        analyse.assert_not_called()

    @patch.object(RoleDeviationRiskAnalysis, "analyse")
    @patch('idmlib.core.api')
    def test_diff_group_member_added_role_with_no_group_new_group(self, api, analyse):
        idtrack_plugin = MagicMock()
        idtrack = IDTrack(idtrack_plugin, {})
        change = MagicMock()
        profile = MagicMock(spec=Profile)
        is_valid = PropertyMock(return_value=True)
        type(profile).is_valid = is_valid
        role = MagicMock()
        role.roleid = "ROLE1"
        roles = PropertyMock(return_value=[role])
        type(profile).roles = roles
        api.RoleResourceList.return_value = [
            {
                "membertype": "TEMPLATE",
                "memberid": "AD_TEMPLATE"
            }
        ]
        group = MagicMock()
        hostid = PropertyMock(return_value="AD")
        type(group).hostid = hostid
        groupid = PropertyMock(return_value="Group1")
        type(group).groupid = groupid
        api.ResourceAttrsGet.return_value = [
            {"name": "SURPLUS_CONFIDENTIALITY_IMPACT", "value": "5"},
            {"name": "SURPLUS_INTEGRITY_IMPACT", "value": "6"},
            {"name": "SURPLUS_AVAILABILITY_IMPACT", "value": "7"},
            {"name": "SURPLUS_ANNUAL_RISK_OF_OCCURRENCE", "value": "8.9"}
        ]
        idtrack.diff_group_member_added([group], {}, profile, change)
        analyse.assert_called_once()
        result_risk_analysis = analyse.call_args_list[0][0][0]
        assert profile == result_risk_analysis.profile
        assert group == result_risk_analysis.resource
        assert DeviationType.SURPLUS == result_risk_analysis.type_of_deviation
        assert 5 == result_risk_analysis.risk_information.confidentiality_impact
        assert 6 == result_risk_analysis.risk_information.integrity_impact
        assert 7 == result_risk_analysis.risk_information.availability_impact
        assert 8.9 == result_risk_analysis.risk_information.annual_rate_of_occurrence

    @patch.object(RoleDeviationRiskAnalysis, "analyse")
    @patch('idmlib.core.api')
    def test_diff_group_member_added_role_with_group_added_group_is_not_in_role(self, api, analyse):
        idtrack_plugin = MagicMock()
        idtrack = IDTrack(idtrack_plugin, {})
        change = MagicMock()
        profile = MagicMock(spec=Profile)
        is_valid = PropertyMock(return_value=True)
        type(profile).is_valid = is_valid
        role = MagicMock()
        role.roleid = "ROLE1"
        roles = PropertyMock(return_value=[role])
        type(profile).roles = roles
        api.RoleResourceList.return_value = [
            {
                "membertype": "TEMPLATE",
                "memberid": "AD_TEMPLATE"
            },
            {
                "membertype": "MANAGEDGROUP",
                "memberid": "AD",
                "groupid": "Group1"
            }
        ]
        group = MagicMock()
        hostid = PropertyMock(return_value="AD")
        type(group).hostid = hostid
        groupid = PropertyMock(return_value="Group3")
        type(group).groupid = groupid
        api.ResourceAttrsGet.return_value = [
            {"name": "SURPLUS_CONFIDENTIALITY_IMPACT", "value": "5"},
            {"name": "SURPLUS_INTEGRITY_IMPACT", "value": "6"},
            {"name": "SURPLUS_AVAILABILITY_IMPACT", "value": "7"},
            {"name": "SURPLUS_ANNUAL_RISK_OF_OCCURRENCE", "value": "8.9"}
        ]
        idtrack.diff_group_member_added([group], {}, profile, change)
        analyse.assert_called_once()
        result_risk_analysis = analyse.call_args_list[0][0][0]
        assert profile == result_risk_analysis.profile
        assert group == result_risk_analysis.resource
        assert DeviationType.SURPLUS == result_risk_analysis.type_of_deviation
        assert 5 == result_risk_analysis.risk_information.confidentiality_impact
        assert 6 == result_risk_analysis.risk_information.integrity_impact
        assert 7 == result_risk_analysis.risk_information.availability_impact
        assert 8.9 == result_risk_analysis.risk_information.annual_rate_of_occurrence

    @patch.object(RoleDeviationRiskAnalysis, "analyse")
    def test_diff_group_member_deleted_no_profile(self, analyse):
        idtrack_plugin = MagicMock()
        idtrack = IDTrack(idtrack_plugin, {})
        change = MagicMock()
        idtrack.diff_group_member_deleted([], {}, None, change)
        analyse.assert_not_called()

    @patch.object(RoleDeviationRiskAnalysis, "analyse")
    def test_diff_group_member_deleted_profile_not_profile(self, analyse):
        idtrack_plugin = MagicMock()
        idtrack = IDTrack(idtrack_plugin, {})
        change = MagicMock()
        profile = MagicMock()
        idtrack.diff_group_member_deleted([], {}, profile, change)
        analyse.assert_not_called()

    @patch.object(RoleDeviationRiskAnalysis, "analyse")
    def test_diff_group_member_deleted_profile_not_valid(self, analyse):
        idtrack_plugin = MagicMock()
        idtrack = IDTrack(idtrack_plugin, {})
        change = MagicMock()
        profile = MagicMock(spec=Profile)
        is_valid = PropertyMock(return_value=False)
        type(profile).is_valid = is_valid
        idtrack.diff_group_member_deleted([], {}, profile, change)
        analyse.assert_not_called()

    @patch.object(RoleDeviationRiskAnalysis, "analyse")
    @patch('idmlib.core.api')
    def test_diff_group_member_deleted_role_with_group_no_deleted_group(self, api, analyse):
        idtrack_plugin = MagicMock()
        idtrack = IDTrack(idtrack_plugin, {})
        change = MagicMock()
        profile = MagicMock(spec=Profile)
        is_valid = PropertyMock(return_value=True)
        type(profile).is_valid = is_valid
        role = MagicMock()
        role.roleid = "ROLE1"
        roles = PropertyMock(return_value=[role])
        type(profile).roles = roles
        api.RoleResourceList.return_value = [
            {
                "membertype": "TEMPLATE",
                "memberid": "AD_TEMPLATE"
            },
            {
                "membertype": "MANAGEDGROUP",
                "memberid": "AD",
                "groupid": "Group1"
            }
        ]
        idtrack.diff_group_member_deleted([], {}, profile, change)
        analyse.assert_not_called()

    @patch.object(RoleDeviationRiskAnalysis, "analyse")
    @patch('idmlib.core.api')
    def test_diff_group_member_deleted_role_with_group_deleted_group_is_in_role(self, api, analyse):
        idtrack_plugin = MagicMock()
        idtrack = IDTrack(idtrack_plugin, {})
        change = MagicMock()
        profile = MagicMock(spec=Profile)
        is_valid = PropertyMock(return_value=True)
        type(profile).is_valid = is_valid
        role = MagicMock()
        role.roleid = "ROLE1"
        roles = PropertyMock(return_value=[role])
        type(profile).roles = roles
        api.RoleResourceList.return_value = [
            {
                "membertype": "TEMPLATE",
                "memberid": "AD_TEMPLATE"
            },
            {
                "membertype": "MANAGEDGROUP",
                "memberid": "AD",
                "groupid": "Group1"
            }
        ]
        group = MagicMock()
        hostid = PropertyMock(return_value="AD")
        type(group).hostid = hostid
        groupid = PropertyMock(return_value="Group1")
        type(group).groupid = groupid
        api.ResourceAttrsGet.return_value = [
            {"name": "DEFICIT_CONFIDENTIALITY_IMPACT", "value": "1"},
            {"name": "DEFICIT_INTEGRITY_IMPACT", "value": "2"},
            {"name": "DEFICIT_AVAILABILITY_IMPACT", "value": "3"},
            {"name": "DEFICIT_ANNUAL_RISK_OF_OCCURRENCE", "value": "4.5"}
        ]
        idtrack.diff_group_member_deleted([group], {}, profile, change)
        analyse.assert_called_once()
        result_risk_analysis = analyse.call_args_list[0][0][0]
        assert profile == result_risk_analysis.profile
        assert group == result_risk_analysis.resource
        assert DeviationType.DEFICIT == result_risk_analysis.type_of_deviation
        assert 1 == result_risk_analysis.risk_information.confidentiality_impact
        assert 2 == result_risk_analysis.risk_information.integrity_impact
        assert 3 == result_risk_analysis.risk_information.availability_impact
        assert 4.5 == result_risk_analysis.risk_information.annual_rate_of_occurrence

    @patch.object(RoleDeviationRiskAnalysis, "analyse")
    @patch('idmlib.core.api')
    def test_diff_group_member_deleted_role_with_no_group_deleted_group(self, api, analyse):
        idtrack_plugin = MagicMock()
        idtrack = IDTrack(idtrack_plugin, {})
        change = MagicMock()
        profile = MagicMock(spec=Profile)
        is_valid = PropertyMock(return_value=True)
        type(profile).is_valid = is_valid
        role = MagicMock()
        role.roleid = "ROLE1"
        roles = PropertyMock(return_value=[role])
        type(profile).roles = roles
        api.RoleResourceList.return_value = [
            {
                "membertype": "TEMPLATE",
                "memberid": "AD_TEMPLATE"
            }
        ]
        group = MagicMock()
        hostid = PropertyMock(return_value="AD")
        type(group).hostid = hostid
        groupid = PropertyMock(return_value="Group1")
        type(group).groupid = groupid
        idtrack.diff_group_member_deleted([group], {}, profile, change)
        analyse.assert_not_called()

    @patch.object(RoleDeviationRiskAnalysis, "analyse")
    @patch('idmlib.core.api')
    def test_diff_group_member_deleted_role_with_group_deleted_group_is_not_in_role(self, api, analyse):
        idtrack_plugin = MagicMock()
        idtrack = IDTrack(idtrack_plugin, {})
        change = MagicMock()
        profile = MagicMock(spec=Profile)
        is_valid = PropertyMock(return_value=True)
        type(profile).is_valid = is_valid
        role = MagicMock()
        role.roleid = "ROLE1"
        roles = PropertyMock(return_value=[role])
        type(profile).roles = roles
        api.RoleResourceList.return_value = [
            {
                "membertype": "TEMPLATE",
                "memberid": "AD_TEMPLATE"
            },
            {
                "membertype": "MANAGEDGROUP",
                "memberid": "AD",
                "groupid": "Group1"
            }
        ]
        group = MagicMock()
        hostid = PropertyMock(return_value="SAP_GRC")
        type(group).hostid = hostid
        groupid = PropertyMock(return_value="Group2")
        type(group).groupid = groupid
        idtrack.diff_group_member_deleted([group], {}, profile, change)
        analyse.assert_not_called()
