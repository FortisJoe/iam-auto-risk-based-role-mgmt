from idmlib.components.test import CommonTest
from unittest.mock import MagicMock, patch
from Functional.role_deviation_common_library.helper import (
    get_target_accounts_in_roles,
    get_groups_in_roles,
    get_template_for_hostid,
    get_account_risk_information,
    get_group_risk_information
)
from Functional.role_deviation_risk_analysis.analyse import (
    RiskInformation
)
from idmlib.idapi import APIError


class TestCommonLibrary(CommonTest):

    @patch('idmlib.core.api')
    def test_get_target_accounts_in_roles_no_templates(self, api):
        """ Tests result when no templates in roles """
        profile = MagicMock()
        roles = list()
        role = MagicMock()
        roles.append(role)
        profile.roles = roles
        role.roleid = "ROLE1"
        api.RoleResourceList.return_value = [
            {
                "membertype": "ROLE"
            }
        ]
        accounts = get_target_accounts_in_roles(profile)
        self.assertSetEqual(accounts, set())

    @patch('idmlib.core.api')
    def test_get_target_accounts_in_roles_has_template_value_but_causes_api_error(self, api):
        """ Tests result when template in role which doesn't exist """
        profile = MagicMock()
        roles = list()
        role = MagicMock()
        roles.append(role)
        profile.roles = roles
        role.roleid = "ROLE1"
        api.RoleResourceList.side_effect = APIError(15, "No Such Template")
        with self.assertRaises(APIError):
            get_target_accounts_in_roles(profile)

    @patch('idmlib.core.api')
    def test_get_target_accounts_in_roles_1_template(self, api):
        """ Tests result when one template in roles """
        profile = MagicMock()
        roles = list()
        role = MagicMock()
        roles.append(role)
        profile.roles = roles
        role.roleid = "ROLE1"
        api.RoleResourceList.return_value = [
            {
                "membertype": "TEMPLATE",
                "memberid": "AD_TEMPLATE"
            }
        ]
        api.ResourceGet.return_value = [
            [
                "hostid",
                "AD"
            ]
        ]
        accounts = get_target_accounts_in_roles(profile)
        results = set()
        results.add("AD")
        self.assertSetEqual(accounts, results)

    @patch('idmlib.core.api')
    def test_get_target_accounts_in_roles_2_templates(self, api):
        """ Tests result when 2 template in roles """
        profile = MagicMock()
        roles = list()
        role = MagicMock()
        roles.append(role)
        profile.roles = roles
        role.roleid = "ROLE1"
        api.RoleResourceList.return_value = [
            {
                "membertype": "TEMPLATE",
                "memberid": "AD_TEMPLATE"
            },
            {
                "membertype": "TEMPLATE",
                "memberid": "SAP_GRC_TEMPLATE"
            }
        ]
        api.ResourceGet.side_effect = [
            [
                (
                    "hostid",
                    "AD"
                )
            ],
            [
                (
                    "hostid",
                    "SAP_GRC"
                )
            ]
        ]
        accounts = get_target_accounts_in_roles(profile)
        results = set()
        results.add("AD")
        results.add("SAP_GRC")
        self.assertSetEqual(accounts, results)

    def test_get_groups_in_roles_no_groups(self):
        """ Tests result when no groups in roles """
        profile = MagicMock()
        groups = list()
        profile.groups = groups
        result_groups = get_groups_in_roles(profile)
        self.assertSetEqual(result_groups, set())

    def test_get_groups_in_roles_1_group(self):
        """ Tests result when 1 group in roles """
        profile = MagicMock()
        groups = list()
        group = MagicMock()
        group.hostid = "AD"
        group.groupid = "Group1"
        groups.append(group)
        profile.groups = groups
        result_groups = get_groups_in_roles(profile)
        expected = set()
        expected.add("AD:Group1")
        self.assertSetEqual(result_groups, expected)

    def test_get_groups_in_roles_2_groups(self):
        """ Tests result when 2 groups in roles """
        profile = MagicMock()
        groups = list()
        group1 = MagicMock()
        group1.hostid = "AD"
        group1.groupid = "Group1"
        group2 = MagicMock()
        group2.hostid = "SAP_GRC"
        group2.groupid = "Group2"
        groups.append(group1)
        groups.append(group2)
        profile.groups = groups
        result_groups = get_groups_in_roles(profile)
        expected = set()
        expected.add("AD:Group1")
        expected.add("SAP_GRC:Group2")
        self.assertSetEqual(result_groups, expected)

    @patch('idmlib.core.api')
    def test_get_template_for_hostid_no_result(self, api):
        """ Tests result when no target found for template """
        api.ResourceFind.return_value = []
        result = get_template_for_hostid("AD")
        self.assertIsNone(result)

    @patch('idmlib.core.api')
    def test_get_template_for_hostid_find_result(self, api):
        """ Tests result when template found for target """
        api.ResourceFind.return_value = [
            {
                "resourceid": "AD_TEMPLATE",
                "resourceid2": ""
            }
        ]
        result = get_template_for_hostid("AD")
        self.assertEqual(result, "AD_TEMPLATE")

    @patch('idmlib.core.api')
    def test_get_account_risk_info_deficit(self, api):
        """ Tests getting account risk info """
        api.ResourceAttrsGet.return_value = [
            {"name": "DEFICIT_CONFIDENTIALITY_IMPACT", "value": "1"},
            {"name": "DEFICIT_INTEGRITY_IMPACT", "value": "2"},
            {"name": "DEFICIT_AVAILABILITY_IMPACT", "value": "3"},
            {"name": "DEFICIT_ANNUAL_RISK_OF_OCCURRENCE", "value": "4.0"}
        ]
        risk_info = get_account_risk_information("AD_TEMPLATE")
        self.assertEqual(risk_info.confidentiality_impact, 1)
        self.assertEqual(risk_info.integrity_impact, 2)
        self.assertEqual(risk_info.availability_impact, 3)
        self.assertEqual(risk_info.annual_rate_of_occurrence, 4.0)

    @patch('idmlib.core.api')
    def test_get_account_risk_info_surplus(self, api):
        """ Tests getting account risk info """
        api.ResourceAttrsGet.return_value = [
            {"name": "SURPLUS_CONFIDENTIALITY_IMPACT", "value": "5"},
            {"name": "SURPLUS_INTEGRITY_IMPACT", "value": "6"},
            {"name": "SURPLUS_AVAILABILITY_IMPACT", "value": "7"},
            {"name": "SURPLUS_ANNUAL_RISK_OF_OCCURRENCE", "value": "8.9"}
        ]
        risk_info = get_account_risk_information("AD_TEMPLATE", is_surplus=True)
        self.assertEqual(risk_info.confidentiality_impact, 5)
        self.assertEqual(risk_info.integrity_impact, 6)
        self.assertEqual(risk_info.availability_impact, 7)
        self.assertEqual(risk_info.annual_rate_of_occurrence, 8.9)

    @patch('idmlib.core.api')
    def test_get_group_risk_info_deficit(self, api):
        """ Tests getting group risk info """
        api.ResourceAttrsGet.return_value = [
            {"name": "DEFICIT_CONFIDENTIALITY_IMPACT", "value": "1"},
            {"name": "DEFICIT_INTEGRITY_IMPACT", "value": "2"},
            {"name": "DEFICIT_AVAILABILITY_IMPACT", "value": "3"},
            {"name": "DEFICIT_ANNUAL_RISK_OF_OCCURRENCE", "value": "4.0"}
        ]
        risk_info = get_group_risk_information("AD", "Group1")
        self.assertEqual(risk_info.confidentiality_impact, 1)
        self.assertEqual(risk_info.integrity_impact, 2)
        self.assertEqual(risk_info.availability_impact, 3)
        self.assertEqual(risk_info.annual_rate_of_occurrence, 4.0)

    @patch('idmlib.core.api')
    def test_get_group_risk_info_surplus(self, api):
        """ Tests getting group risk info """
        api.ResourceAttrsGet.return_value = [
            {"name": "SURPLUS_CONFIDENTIALITY_IMPACT", "value": "5"},
            {"name": "SURPLUS_INTEGRITY_IMPACT", "value": "6"},
            {"name": "SURPLUS_AVAILABILITY_IMPACT", "value": "7"},
            {"name": "SURPLUS_ANNUAL_RISK_OF_OCCURRENCE", "value": "8.9"}
        ]
        risk_info = get_group_risk_information("AD", "Group1", is_surplus=True)
        self.assertEqual(risk_info.confidentiality_impact, 5)
        self.assertEqual(risk_info.integrity_impact, 6)
        self.assertEqual(risk_info.availability_impact, 7)
        self.assertEqual(risk_info.annual_rate_of_occurrence, 8.9)
