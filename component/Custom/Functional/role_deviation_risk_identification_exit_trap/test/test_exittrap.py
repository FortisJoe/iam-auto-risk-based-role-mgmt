from idmlib.components.test import CommonTest
from unittest.mock import MagicMock, patch, PropertyMock

from Functional.role_deviation_risk_analysis.analyse import (
    DeviationType,
    RiskInformation,
    RiskAnalysisInput,
    RoleDeviationRiskAnalysis
)
from Functional.role_deviation_risk_identification_exit_trap.exit import (
    ExitTrap
)


class TestExitTrap(CommonTest):

    @patch.object(RoleDeviationRiskAnalysis, "analyse")
    def test_exittrap_ends_for_child_parentreqid(self, analyse):
        exit = MagicMock()
        request = MagicMock()
        req = PropertyMock(return_value=request)
        type(exit).request = req
        parentreqid = PropertyMock(return_value="NEW-EMPLOYEE")
        autoressig = PropertyMock(return_value=None)
        type(request).parentreqid = parentreqid
        type(request).autoressig = autoressig
        exit_trap = ExitTrap(exit, {})
        exit_trap.wf_request_completed()
        analyse.assert_not_called()

    @patch.object(RoleDeviationRiskAnalysis, "analyse")
    def test_exittrap_ends_for_child_autoressig(self, analyse):
        exit = MagicMock()
        request = MagicMock()
        req = PropertyMock(return_value=request)
        type(exit).request = req
        parentreqid = PropertyMock(return_value=None)
        autoressig = PropertyMock(return_value="AUTORES")
        type(request).parentreqid = parentreqid
        type(request).autoressig = autoressig
        exit_trap = ExitTrap(exit, {})
        exit_trap.wf_request_completed()
        analyse.assert_not_called()

    @patch.object(RoleDeviationRiskAnalysis, "analyse")
    def test_exittrap_ends_for_request_status_not_C(self, analyse):
        exit = MagicMock()
        request = MagicMock()
        req = PropertyMock(return_value=request)
        type(exit).request = req
        parentreqid = PropertyMock(return_value=None)
        autoressig = PropertyMock(return_value=None)
        type(request).parentreqid = parentreqid
        type(request).autoressig = autoressig
        status = PropertyMock(return_value="A")
        type(request).status = status
        exit_trap = ExitTrap(exit, {})
        exit_trap.wf_request_completed()
        analyse.assert_not_called()

    @patch.object(RoleDeviationRiskAnalysis, "analyse")
    @patch('idmlib.core.api')
    def test_exittrap_no_deviations(self, api, analyse):
        # Patches don't seem to work for static methods
        # mocked actions for calls in helper too.
        exit = MagicMock()
        request = MagicMock()
        req = PropertyMock(return_value=request)
        type(exit).request = req
        parentreqid = PropertyMock(return_value=None)
        autoressig = PropertyMock(return_value=None)
        type(request).parentreqid = parentreqid
        type(request).autoressig = autoressig
        status = PropertyMock(return_value="C")
        type(request).status = status
        recipient = MagicMock()
        recip = PropertyMock(return_value=recipient)
        type(exit).recipient = recip
        role = MagicMock()
        role.roleid = "ROLE1"
        roles = PropertyMock(return_value=[role])
        type(recipient).roles = roles
        api.RoleResourceList.side_effect = [
            [
                {
                    "membertype": "TEMPLATE",
                    "memberid": "AD_TEMPLATE"
                }
            ],
            [
                {
                    "membertype": "MANAGEDGROUP",
                    "memberid": "AD",
                    "groupid": "Group1"
                }
            ]
        ]
        api.ResourceGet.return_value = [
            [
                "hostid",
                "AD"
            ]
        ]
        group = MagicMock()
        group.hostid.return_value = "AD"
        group.groupid.return_value = "Group1"
        api.ResourceFind.return_value = [
            {
                "resourceid": "AD_TEMPLATE",
                "resourceid2": ""
            }
        ]
        account = MagicMock()
        accounts = PropertyMock(return_value=[account])
        type(recipient).accounts = accounts
        acct_ad = PropertyMock(return_value="AD")
        type(account).hostid = acct_ad
        group = MagicMock()
        grp_ad = PropertyMock(return_value="AD")
        type(group).hostid = grp_ad
        grp_id = PropertyMock(return_value="Group1")
        type(group).groupid = grp_id
        groups = PropertyMock(return_value=[group])
        type(recipient).groups = groups
        exit_trap = ExitTrap(exit, {})
        exit_trap.wf_request_completed()
        analyse.assert_not_called()

    @patch.object(RoleDeviationRiskAnalysis, "analyse")
    @patch('idmlib.core.api')
    def test_exittrap_1_surplus_account(self, api, analyse):
        # Patches don't seem to work for static methods
        # mocked actions for calls in helper too.
        exit = MagicMock()
        request = MagicMock()
        req = PropertyMock(return_value=request)
        type(exit).request = req
        parentreqid = PropertyMock(return_value=None)
        autoressig = PropertyMock(return_value=None)
        type(request).parentreqid = parentreqid
        type(request).autoressig = autoressig
        status = PropertyMock(return_value="C")
        type(request).status = status
        recipient = MagicMock()
        recip = PropertyMock(return_value=recipient)
        type(exit).recipient = recip
        role = MagicMock()
        role.roleid = "ROLE1"
        roles = PropertyMock(return_value=[role])
        type(recipient).roles = roles
        api.RoleResourceList.side_effect = [
            [
                {
                    "membertype": "TEMPLATE",
                    "memberid": "AD_TEMPLATE"
                }
            ],
            [
                {
                    "membertype": "MANAGEDGROUP",
                    "memberid": "AD",
                    "groupid": "Group1"
                }
            ]
        ]
        api.ResourceGet.return_value = [
            [
                "hostid",
                "AD"
            ]
        ]
        group = MagicMock()
        group.hostid.return_value = "AD"
        group.groupid.return_value = "Group1"
        api.ResourceFind.side_effect = [
            [
                {
                    "resourceid": "AD_TEMPLATE",
                    "resourceid2": ""
                }
            ],
            [
                {
                    "resourceid": "SAP_GRC_TEMPLATE",
                    "resourceid2": ""
                }
            ]
        ]
        account = MagicMock()
        account2 = MagicMock()
        accounts = PropertyMock(return_value=[
            account,
            account2
        ])
        type(recipient).accounts = accounts
        acct_ad = PropertyMock(return_value="AD")
        type(account).hostid = acct_ad
        acct2_ad = PropertyMock(return_value="SAP_GRC")
        type(account2).hostid = acct2_ad
        group = MagicMock()
        grp_ad = PropertyMock(return_value="AD")
        type(group).hostid = grp_ad
        grp_id = PropertyMock(return_value="Group1")
        type(group).groupid = grp_id
        groups = PropertyMock(return_value=[group])
        type(recipient).groups = groups
        api.ResourceAttrsGet.return_value = [
            {"name": "SURPLUS_CONFIDENTIALITY_IMPACT", "value": "5"},
            {"name": "SURPLUS_INTEGRITY_IMPACT", "value": "6"},
            {"name": "SURPLUS_AVAILABILITY_IMPACT", "value": "7"},
            {"name": "SURPLUS_ANNUAL_RISK_OF_OCCURRENCE", "value": "8.9"}
        ]
        exit_trap = ExitTrap(exit, {})
        exit_trap.wf_request_completed()
        analyse.assert_called_once()
        result_risk_analysis = analyse.call_args_list[0][0][0]
        assert recipient == result_risk_analysis.profile
        assert account2 == result_risk_analysis.resource
        assert DeviationType.SURPLUS == result_risk_analysis.type_of_deviation
        assert 5 == result_risk_analysis.risk_information.confidentiality_impact
        assert 6 == result_risk_analysis.risk_information.integrity_impact
        assert 7 == result_risk_analysis.risk_information.availability_impact
        assert 8.9 == result_risk_analysis.risk_information.annual_rate_of_occurrence

    @patch.object(RoleDeviationRiskAnalysis, "analyse")
    @patch('idmlib.core.api')
    def test_exittrap_1_surplus_group(self, api, analyse):
        # Patches don't seem to work for static methods
        # mocked actions for calls in helper too.
        exit = MagicMock()
        request = MagicMock()
        req = PropertyMock(return_value=request)
        type(exit).request = req
        parentreqid = PropertyMock(return_value=None)
        autoressig = PropertyMock(return_value=None)
        type(request).parentreqid = parentreqid
        type(request).autoressig = autoressig
        status = PropertyMock(return_value="C")
        type(request).status = status
        recipient = MagicMock()
        recip = PropertyMock(return_value=recipient)
        type(exit).recipient = recip
        role = MagicMock()
        role.roleid = "ROLE1"
        roles = PropertyMock(return_value=[role])
        type(recipient).roles = roles
        api.RoleResourceList.side_effect = [
            [
                {
                    "membertype": "TEMPLATE",
                    "memberid": "AD_TEMPLATE"
                }
            ],
            [
                {
                    "membertype": "MANAGEDGROUP",
                    "memberid": "AD",
                    "groupid": "Group1"
                }
            ]
        ]
        api.ResourceGet.return_value = [
            [
                "hostid",
                "AD"
            ]
        ]
        group = MagicMock()
        group.hostid.return_value = "AD"
        group.groupid.return_value = "Group1"
        api.ResourceFind.return_value = [
            {
                "resourceid": "AD_TEMPLATE",
                "resourceid2": ""
            }
        ]
        account = MagicMock()
        accounts = PropertyMock(return_value=[account])
        type(recipient).accounts = accounts
        acct_ad = PropertyMock(return_value="AD")
        type(account).hostid = acct_ad
        group = MagicMock()
        grp_ad = PropertyMock(return_value="AD")
        type(group).hostid = grp_ad
        grp_id = PropertyMock(return_value="Group1")
        type(group).groupid = grp_id
        group2 = MagicMock()
        grp2_ad = PropertyMock(return_value="AD")
        type(group2).hostid = grp2_ad
        grp2_id = PropertyMock(return_value="Group3")
        type(group2).groupid = grp2_id
        groups = PropertyMock(return_value=[group,group2])
        type(recipient).groups = groups
        api.ResourceAttrsGet.return_value = [
            {"name": "SURPLUS_CONFIDENTIALITY_IMPACT", "value": "5"},
            {"name": "SURPLUS_INTEGRITY_IMPACT", "value": "6"},
            {"name": "SURPLUS_AVAILABILITY_IMPACT", "value": "7"},
            {"name": "SURPLUS_ANNUAL_RISK_OF_OCCURRENCE", "value": "8.9"}
        ]
        exit_trap = ExitTrap(exit, {})
        exit_trap.wf_request_completed()
        analyse.assert_called_once()
        result_risk_analysis = analyse.call_args_list[0][0][0]
        assert recipient == result_risk_analysis.profile
        assert group2 == result_risk_analysis.resource
        assert DeviationType.SURPLUS == result_risk_analysis.type_of_deviation
        assert 5 == result_risk_analysis.risk_information.confidentiality_impact
        assert 6 == result_risk_analysis.risk_information.integrity_impact
        assert 7 == result_risk_analysis.risk_information.availability_impact
        assert 8.9 == result_risk_analysis.risk_information.annual_rate_of_occurrence

    @patch.object(RoleDeviationRiskAnalysis, "analyse")
    @patch('idmlib.core.api')
    def test_exittrap_1_deficit_account(self, api, analyse):
        # Patches don't seem to work for static methods
        # mocked actions for calls in helper too.
        exit = MagicMock()
        request = MagicMock()
        req = PropertyMock(return_value=request)
        type(exit).request = req
        parentreqid = PropertyMock(return_value=None)
        autoressig = PropertyMock(return_value=None)
        type(request).parentreqid = parentreqid
        type(request).autoressig = autoressig
        status = PropertyMock(return_value="C")
        type(request).status = status
        recipient = MagicMock()
        recip = PropertyMock(return_value=recipient)
        type(exit).recipient = recip
        role = MagicMock()
        role.roleid = "ROLE1"
        roles = PropertyMock(return_value=[role])
        type(recipient).roles = roles
        api.RoleResourceList.side_effect = [
            [
                {
                    "membertype": "TEMPLATE",
                    "memberid": "AD_TEMPLATE"
                },
                {
                    "membertype": "TEMPLATE",
                    "memberid": "SAP_GRC_TEMPLATE"
                }
            ],
            [
                {
                    "membertype": "MANAGEDGROUP",
                    "memberid": "AD",
                    "groupid": "Group1"
                }
            ]
        ]
        api.ResourceGet.side_effect = [
            [
                [
                    "hostid",
                    "AD"
                ]
            ],
            [
                [
                    "hostid",
                    "SAP_GRC"
                ]
            ]
        ]
        group = MagicMock()
        group.hostid.return_value = "AD"
        group.groupid.return_value = "Group1"

        def get_template_for_host(self, *args, **kwargs):
            target_id = args[0][0][1]
            if target_id == "AD":
                return [
                    {
                        "resourceid": "AD_TEMPLATE",
                        "resourceid2": ""
                    }
                ]
            elif target_id == "SAP_GRC":
                return [
                    {
                        "resourceid": "SAP_GRC_TEMPLATE",
                        "resourceid2": ""
                    }
                ]

        api.ResourceFind.side_effect = get_template_for_host
        account = MagicMock()
        accounts = PropertyMock(return_value=[account])
        type(recipient).accounts = accounts
        acct_ad = PropertyMock(return_value="AD")
        type(account).hostid = acct_ad
        group = MagicMock()
        grp_ad = PropertyMock(return_value="AD")
        type(group).hostid = grp_ad
        grp_id = PropertyMock(return_value="Group1")
        type(group).groupid = grp_id
        groups = PropertyMock(return_value=[group])
        type(recipient).groups = groups
        api.ResourceAttrsGet.return_value = [
            {"name": "DEFICIT_CONFIDENTIALITY_IMPACT", "value": "1"},
            {"name": "DEFICIT_INTEGRITY_IMPACT", "value": "2"},
            {"name": "DEFICIT_AVAILABILITY_IMPACT", "value": "3"},
            {"name": "DEFICIT_ANNUAL_RISK_OF_OCCURRENCE", "value": "4.5"}
        ]
        exit_trap = ExitTrap(exit, {})
        exit_trap.wf_request_completed()
        analyse.assert_called_once()
        result_risk_analysis = analyse.call_args_list[0][0][0]
        assert recipient == result_risk_analysis.profile
        assert "SAP_GRC_TEMPLATE" == result_risk_analysis.resource.tplid
        assert "SAP_GRC" == result_risk_analysis.resource.hostid
        assert DeviationType.DEFICIT == result_risk_analysis.type_of_deviation
        assert 1 == result_risk_analysis.risk_information.confidentiality_impact
        assert 2 == result_risk_analysis.risk_information.integrity_impact
        assert 3 == result_risk_analysis.risk_information.availability_impact
        assert 4.5 == result_risk_analysis.risk_information.annual_rate_of_occurrence

    @patch.object(RoleDeviationRiskAnalysis, "analyse")
    @patch('idmlib.core.api')
    def test_exittrap_1_deficit_group(self, api, analyse):
        # Patches don't seem to work for static methods
        # mocked actions for calls in helper too.
        exit = MagicMock()
        request = MagicMock()
        req = PropertyMock(return_value=request)
        type(exit).request = req
        parentreqid = PropertyMock(return_value=None)
        autoressig = PropertyMock(return_value=None)
        type(request).parentreqid = parentreqid
        type(request).autoressig = autoressig
        status = PropertyMock(return_value="C")
        type(request).status = status
        recipient = MagicMock()
        recip = PropertyMock(return_value=recipient)
        type(exit).recipient = recip
        role = MagicMock()
        role.roleid = "ROLE1"
        roles = PropertyMock(return_value=[role])
        type(recipient).roles = roles
        api.RoleResourceList.side_effect = [
            [
                {
                    "membertype": "TEMPLATE",
                    "memberid": "AD_TEMPLATE"
                }
            ],
            [
                {
                    "membertype": "MANAGEDGROUP",
                    "memberid": "AD",
                    "groupid": "Group1"
                },
                {
                    "membertype": "MANAGEDGROUP",
                    "memberid": "AD",
                    "groupid": "Group3"
                }
            ]
        ]
        api.ResourceGet.return_value = [
            [
                "hostid",
                "AD"
            ]
        ]
        group = MagicMock()
        group.hostid.return_value = "AD"
        group.groupid.return_value = "Group1"
        api.ResourceFind.return_value = [
            {
                "resourceid": "AD_TEMPLATE",
                "resourceid2": ""
            }
        ]
        account = MagicMock()
        accounts = PropertyMock(return_value=[account])
        type(recipient).accounts = accounts
        acct_ad = PropertyMock(return_value="AD")
        type(account).hostid = acct_ad
        group = MagicMock()
        grp_ad = PropertyMock(return_value="AD")
        type(group).hostid = grp_ad
        grp_id = PropertyMock(return_value="Group1")
        type(group).groupid = grp_id
        groups = PropertyMock(return_value=[group])
        type(recipient).groups = groups
        api.ResourceAttrsGet.return_value = [
            {"name": "DEFICIT_CONFIDENTIALITY_IMPACT", "value": "1"},
            {"name": "DEFICIT_INTEGRITY_IMPACT", "value": "2"},
            {"name": "DEFICIT_AVAILABILITY_IMPACT", "value": "3"},
            {"name": "DEFICIT_ANNUAL_RISK_OF_OCCURRENCE", "value": "4.5"}
        ]
        exit_trap = ExitTrap(exit, {})
        exit_trap.wf_request_completed()
        analyse.assert_called_once()
        result_risk_analysis = analyse.call_args_list[0][0][0]
        assert recipient == result_risk_analysis.profile
        assert "Group3" == result_risk_analysis.resource.groupid
        assert "AD" == result_risk_analysis.resource.hostid
        assert DeviationType.DEFICIT == result_risk_analysis.type_of_deviation
        assert 1 == result_risk_analysis.risk_information.confidentiality_impact
        assert 2 == result_risk_analysis.risk_information.integrity_impact
        assert 3 == result_risk_analysis.risk_information.availability_impact
        assert 4.5 == result_risk_analysis.risk_information.annual_rate_of_occurrence

    @patch.object(RoleDeviationRiskAnalysis, "analyse")
    @patch('idmlib.core.api')
    def test_exittrap_1_of_each(self, api, analyse):
        # Patches don't seem to work for static methods
        # mocked actions for calls in helper too.
        exit = MagicMock()
        request = MagicMock()
        req = PropertyMock(return_value=request)
        type(exit).request = req
        parentreqid = PropertyMock(return_value=None)
        autoressig = PropertyMock(return_value=None)
        type(request).parentreqid = parentreqid
        type(request).autoressig = autoressig
        status = PropertyMock(return_value="C")
        type(request).status = status
        recipient = MagicMock()
        recip = PropertyMock(return_value=recipient)
        type(exit).recipient = recip
        role = MagicMock()
        role.roleid = "ROLE1"
        roles = PropertyMock(return_value=[role])
        type(recipient).roles = roles
        api.RoleResourceList.side_effect = [
            [
                {
                    "membertype": "TEMPLATE",
                    "memberid": "AD_TEMPLATE"
                },
                {
                    "membertype": "TEMPLATE",
                    "memberid": "AZURE_TEMPLATE"
                }
            ],
            [
                {
                    "membertype": "MANAGEDGROUP",
                    "memberid": "AD",
                    "groupid": "Group1"
                },
                {
                    "membertype": "MANAGEDGROUP",
                    "memberid": "AD",
                    "groupid": "Group3"
                }
            ]
        ]

        def get_host_for_template(self, *args, **kwargs):
            template_id = self
            if template_id == "AD_TEMPLATE":
                return [
                    (
                        "hostid",
                        "AD"
                    )
                ]
            elif template_id == "AZURE_TEMPLATE":
                return [
                    (
                        "hostid",
                        "AZURE_AD"
                    )
                ]

        api.ResourceGet.side_effect = get_host_for_template

        def get_template_for_host(self, *args, **kwargs):
            target_id = args[0][0][1]
            if target_id == "AD":
                return [
                    {
                        "resourceid": "AD_TEMPLATE",
                        "resourceid2": ""
                    }
                ]
            elif target_id == "SAP_GRC":
                return [
                    {
                        "resourceid": "SAP_GRC_TEMPLATE",
                        "resourceid2": ""
                    }
                ]
            elif target_id == "AZURE_AD":
                return [
                    {
                        "resourceid": "AZURE_TEMPLATE",
                        "resourceid2": ""
                    }
                ]

        api.ResourceFind.side_effect = get_template_for_host

        account = MagicMock()
        account2 = MagicMock()
        accounts = PropertyMock(return_value=[
            account,
            account2
        ])
        type(recipient).accounts = accounts
        acct_ad = PropertyMock(return_value="AD")
        type(account).hostid = acct_ad
        acct2_ad = PropertyMock(return_value="SAP_GRC")
        type(account2).hostid = acct2_ad
        group = MagicMock()
        grp_ad = PropertyMock(return_value="AD")
        type(group).hostid = grp_ad
        grp_id = PropertyMock(return_value="Group1")
        type(group).groupid = grp_id
        group2 = MagicMock()
        grp2_ad = PropertyMock(return_value="AD")
        type(group2).hostid = grp2_ad
        grp2_id = PropertyMock(return_value="Group4")
        type(group2).groupid = grp2_id
        groups = PropertyMock(return_value=[group, group2])
        type(recipient).groups = groups
        api.ResourceAttrsGet.side_effect = [
            [
                {"name": "SURPLUS_CONFIDENTIALITY_IMPACT", "value": "5"},
                {"name": "SURPLUS_INTEGRITY_IMPACT", "value": "6"},
                {"name": "SURPLUS_AVAILABILITY_IMPACT", "value": "7"},
                {"name": "SURPLUS_ANNUAL_RISK_OF_OCCURRENCE", "value": "8.9"}
            ],
            [
                {"name": "SURPLUS_CONFIDENTIALITY_IMPACT", "value": "5"},
                {"name": "SURPLUS_INTEGRITY_IMPACT", "value": "6"},
                {"name": "SURPLUS_AVAILABILITY_IMPACT", "value": "7"},
                {"name": "SURPLUS_ANNUAL_RISK_OF_OCCURRENCE", "value": "8.9"}
            ],
            [
                {"name": "DEFICIT_CONFIDENTIALITY_IMPACT", "value": "1"},
                {"name": "DEFICIT_INTEGRITY_IMPACT", "value": "2"},
                {"name": "DEFICIT_AVAILABILITY_IMPACT", "value": "3"},
                {"name": "DEFICIT_ANNUAL_RISK_OF_OCCURRENCE", "value": "4.5"}
            ],
            [
                {"name": "DEFICIT_CONFIDENTIALITY_IMPACT", "value": "1"},
                {"name": "DEFICIT_INTEGRITY_IMPACT", "value": "2"},
                {"name": "DEFICIT_AVAILABILITY_IMPACT", "value": "3"},
                {"name": "DEFICIT_ANNUAL_RISK_OF_OCCURRENCE", "value": "4.5"}
            ]
        ]
        exit_trap = ExitTrap(exit, {})
        exit_trap.wf_request_completed()
        assert 4 == len(analyse.call_args_list)
        surplus_acct_risk_analysis = analyse.call_args_list[0][0][0]
        assert recipient == surplus_acct_risk_analysis.profile
        assert account2 == surplus_acct_risk_analysis.resource
        assert DeviationType.SURPLUS == surplus_acct_risk_analysis.type_of_deviation
        assert 5 == surplus_acct_risk_analysis.risk_information.confidentiality_impact
        assert 6 == surplus_acct_risk_analysis.risk_information.integrity_impact
        assert 7 == surplus_acct_risk_analysis.risk_information.availability_impact
        assert 8.9 == surplus_acct_risk_analysis.risk_information.annual_rate_of_occurrence
        surplus_grp_risk_analysis = analyse.call_args_list[1][0][0]
        assert recipient == surplus_grp_risk_analysis.profile
        assert "Group4" == surplus_grp_risk_analysis.resource.groupid
        assert "AD" == surplus_grp_risk_analysis.resource.hostid
        assert DeviationType.SURPLUS == surplus_grp_risk_analysis.type_of_deviation
        assert 5 == surplus_grp_risk_analysis.risk_information.confidentiality_impact
        assert 6 == surplus_grp_risk_analysis.risk_information.integrity_impact
        assert 7 == surplus_grp_risk_analysis.risk_information.availability_impact
        assert 8.9 == surplus_grp_risk_analysis.risk_information.annual_rate_of_occurrence
        deficit_acct_risk_analysis = analyse.call_args_list[2][0][0]
        assert recipient == deficit_acct_risk_analysis.profile
        assert "AZURE_TEMPLATE" == deficit_acct_risk_analysis.resource.tplid
        assert "AZURE_AD" == deficit_acct_risk_analysis.resource.hostid
        assert DeviationType.DEFICIT == deficit_acct_risk_analysis.type_of_deviation
        assert 1 == deficit_acct_risk_analysis.risk_information.confidentiality_impact
        assert 2 == deficit_acct_risk_analysis.risk_information.integrity_impact
        assert 3 == deficit_acct_risk_analysis.risk_information.availability_impact
        assert 4.5 == deficit_acct_risk_analysis.risk_information.annual_rate_of_occurrence
        deficit_grp_risk_analysis = analyse.call_args_list[3][0][0]
        assert recipient == deficit_grp_risk_analysis.profile
        assert "Group3" == deficit_grp_risk_analysis.resource.groupid
        assert "AD" == deficit_grp_risk_analysis.resource.hostid
        assert DeviationType.DEFICIT == deficit_grp_risk_analysis.type_of_deviation
        assert 1 == deficit_grp_risk_analysis.risk_information.confidentiality_impact
        assert 2 == deficit_grp_risk_analysis.risk_information.integrity_impact
        assert 3 == deficit_grp_risk_analysis.risk_information.availability_impact
        assert 4.5 == deficit_grp_risk_analysis.risk_information.annual_rate_of_occurrence
