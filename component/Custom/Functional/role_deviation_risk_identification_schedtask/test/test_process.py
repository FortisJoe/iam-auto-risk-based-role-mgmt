from idmlib.components.test import CommonTest
from unittest.mock import MagicMock, patch, PropertyMock

from Functional.role_deviation_risk_analysis.analyse import (
    DeviationType,
    RiskInformation,
    RiskAnalysisInput,
    RoleDeviationRiskAnalysis
)
from Functional.role_deviation_risk_identification_schedtask.process import (
    RiskIdentification
)


class TestExitTrap(CommonTest):

    @patch.object(RoleDeviationRiskAnalysis, "analyse")
    @patch('idmlib.core.api')
    def test_process_ends_no_users(self, api, analyse):
        api.UserList.return_value = []
        process = RiskIdentification()
        process.process()
        analyse.assert_not_called()

    @patch.object(RoleDeviationRiskAnalysis, "analyse")
    @patch('idmlib.core.api')
    def test_process_ends_for_profile_not_valid(self, api, analyse):
        # patching idmlib.idmobject.Profile doesn't work.
        # mock internal calls
        user = dict()
        user["userid"] = "Profile1"
        api.UserList.return_value = [user]
        user = dict()
        user["userid"] = "Profile2"
        api.UserGetByID.return_value = user
        process = RiskIdentification()
        process.process()
        analyse.assert_not_called()

    @patch.object(RoleDeviationRiskAnalysis, "analyse")
    @patch('idmlib.core.api')
    def test_process_no_deviations(self, api, analyse):
        # patching idmlib.idmobject.Profile doesn't work.
        # mock internal calls
        # Patches don't seem to work for static methods
        # mocked actions for calls in helper too.
        user = dict()
        user["userid"] = "Profile1"
        api.UserList.return_value = [user]
        api.UserGetByID.return_value = user
        api.RoleGetByUser.return_value = ["ROLE1"]
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
        api.ResourceFind.return_value = [
            {
                "resourceid": "AD_TEMPLATE",
                "resourceid2": ""
            }
        ]
        api.UserAccountsGet.return_value = [
            {
                "longid": "AD\\Profile1",
                "shortid": "Profile1",
                "targetid": "AD",
                "tgroupid": "AD",
                "tsynch": False,
                "unqpass": False
            }
        ]
        api.UserGroupsGet.return_value = [
            {
                "longid": "AD\\Profile1",
                "groupid": "Group1",
                "targetid": "AD",
                "direct": 1
            }
        ]
        process = RiskIdentification()
        process.process()
        analyse.assert_not_called()

    @patch.object(RoleDeviationRiskAnalysis, "analyse")
    @patch('idmlib.core.api')
    def test_process_1_surplus_account(self, api, analyse):
        # Patches don't seem to work for static methods
        # mocked actions for calls in helper too.
        # Patches don't seem to work for static methods
        # mocked actions for calls in helper too.
        user = dict()
        user["userid"] = "Profile1"
        api.UserList.return_value = [user]
        api.UserGetByID.return_value = user
        api.RoleGetByUser.return_value = ["ROLE1"]
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
        api.UserAccountsGet.return_value = [
            {
                "longid": "AD\\Profile1",
                "shortid": "Profile1",
                "targetid": "AD",
                "tgroupid": "AD",
                "tsynch": False,
                "unqpass": False
            },
            {
                "longid": "PROFILE1",
                "shortid": "Profile1",
                "targetid": "SAP_GRC",
                "tgroupid": "SAP_GRC",
                "tsynch": False,
                "unqpass": False
            }
        ]
        api.UserGroupsGet.return_value = [
            {
                "longid": "AD\\Profile1",
                "groupid": "Group1",
                "targetid": "AD",
                "direct": 1
            }
        ]
        api.ResourceAttrsGet.return_value = [
            {"name": "SURPLUS_CONFIDENTIALITY_IMPACT", "value": "5"},
            {"name": "SURPLUS_INTEGRITY_IMPACT", "value": "6"},
            {"name": "SURPLUS_AVAILABILITY_IMPACT", "value": "7"},
            {"name": "SURPLUS_ANNUAL_RISK_OF_OCCURRENCE", "value": "8.9"}
        ]
        process = RiskIdentification()
        process.process()
        analyse.assert_called_once()
        result_risk_analysis = analyse.call_args_list[0][0][0]
        assert "Profile1" == result_risk_analysis.profile.userid
        assert "PROFILE1" == result_risk_analysis.resource.acctid
        assert "SAP_GRC" == result_risk_analysis.resource.hostid
        assert DeviationType.SURPLUS == result_risk_analysis.type_of_deviation
        assert 5 == result_risk_analysis.risk_information.confidentiality_impact
        assert 6 == result_risk_analysis.risk_information.integrity_impact
        assert 7 == result_risk_analysis.risk_information.availability_impact
        assert 8.9 == result_risk_analysis.risk_information.annual_rate_of_occurrence

    @patch.object(RoleDeviationRiskAnalysis, "analyse")
    @patch('idmlib.core.api')
    def test_process_1_surplus_group(self, api, analyse):
        # Patches don't seem to work for static methods
        # mocked actions for calls in helper too.
        # Patches don't seem to work for static methods
        # mocked actions for calls in helper too.
        user = dict()
        user["userid"] = "Profile1"
        api.UserList.return_value = [user]
        api.UserGetByID.return_value = user
        api.RoleGetByUser.return_value = ["ROLE1"]
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
        api.ResourceFind.return_value = [
            {
                "resourceid": "AD_TEMPLATE",
                "resourceid2": ""
            }
        ]
        api.UserAccountsGet.return_value = [
            {
                "longid": "AD\\Profile1",
                "shortid": "Profile1",
                "targetid": "AD",
                "tgroupid": "AD",
                "tsynch": False,
                "unqpass": False
            }
        ]
        api.UserGroupsGet.return_value = [
            {
                "longid": "AD\\Profile1",
                "groupid": "Group1",
                "targetid": "AD",
                "direct": 1
            },
            {
                "longid": "AD\\Profile1",
                "groupid": "Group3",
                "targetid": "AD",
                "direct": 1
            }
        ]
        api.ResourceAttrsGet.return_value = [
            {"name": "SURPLUS_CONFIDENTIALITY_IMPACT", "value": "5"},
            {"name": "SURPLUS_INTEGRITY_IMPACT", "value": "6"},
            {"name": "SURPLUS_AVAILABILITY_IMPACT", "value": "7"},
            {"name": "SURPLUS_ANNUAL_RISK_OF_OCCURRENCE", "value": "8.9"}
        ]
        process = RiskIdentification()
        process.process()
        analyse.assert_called_once()
        result_risk_analysis = analyse.call_args_list[0][0][0]
        assert "Profile1" == result_risk_analysis.profile.userid
        assert "AD\\Profile1" == result_risk_analysis.resource.acctid
        assert "AD" == result_risk_analysis.resource.hostid
        assert "Group3" == result_risk_analysis.resource.groupid
        assert DeviationType.SURPLUS == result_risk_analysis.type_of_deviation
        assert 5 == result_risk_analysis.risk_information.confidentiality_impact
        assert 6 == result_risk_analysis.risk_information.integrity_impact
        assert 7 == result_risk_analysis.risk_information.availability_impact
        assert 8.9 == result_risk_analysis.risk_information.annual_rate_of_occurrence

    @patch.object(RoleDeviationRiskAnalysis, "analyse")
    @patch('idmlib.core.api')
    def test_process_1_deficit_account(self, api, analyse):
        # Patches don't seem to work for static methods
        # mocked actions for calls in helper too.
        # Patches don't seem to work for static methods
        # mocked actions for calls in helper too.
        user = dict()
        user["userid"] = "Profile1"
        api.UserList.return_value = [user]
        api.UserGetByID.return_value = user
        api.RoleGetByUser.return_value = ["ROLE1"]
        api.RoleResourceList.return_value = [
            {
                "membertype": "TEMPLATE",
                "memberid": "AD_TEMPLATE"
            },
            {
                "membertype": "TEMPLATE",
                "memberid": "SAP_GRC_TEMPLATE"
            },
            {
                "membertype": "MANAGEDGROUP",
                "memberid": "AD",
                "groupid": "Group1"
            }
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
        api.UserAccountsGet.return_value = [
            {
                "longid": "AD\\Profile1",
                "shortid": "Profile1",
                "targetid": "AD",
                "tgroupid": "AD",
                "tsynch": False,
                "unqpass": False
            }
        ]
        api.UserGroupsGet.return_value = [
            {
                "longid": "AD\\Profile1",
                "groupid": "Group1",
                "targetid": "AD",
                "direct": 1
            }
        ]
        api.ResourceAttrsGet.return_value = [
            {"name": "DEFICIT_CONFIDENTIALITY_IMPACT", "value": "1"},
            {"name": "DEFICIT_INTEGRITY_IMPACT", "value": "2"},
            {"name": "DEFICIT_AVAILABILITY_IMPACT", "value": "3"},
            {"name": "DEFICIT_ANNUAL_RISK_OF_OCCURRENCE", "value": "4.5"}
        ]
        process = RiskIdentification()
        process.process()
        analyse.assert_called_once()
        result_risk_analysis = analyse.call_args_list[0][0][0]
        assert "Profile1" == result_risk_analysis.profile.userid
        assert "SAP_GRC_TEMPLATE" == result_risk_analysis.resource.tplid
        assert "SAP_GRC" == result_risk_analysis.resource.hostid
        assert DeviationType.DEFICIT == result_risk_analysis.type_of_deviation
        assert 1 == result_risk_analysis.risk_information.confidentiality_impact
        assert 2 == result_risk_analysis.risk_information.integrity_impact
        assert 3 == result_risk_analysis.risk_information.availability_impact
        assert 4.5 == result_risk_analysis.risk_information.annual_rate_of_occurrence

    @patch.object(RoleDeviationRiskAnalysis, "analyse")
    @patch('idmlib.core.api')
    def test_process_1_deficit_group(self, api, analyse):
        # Patches don't seem to work for static methods
        # mocked actions for calls in helper too.
        # Patches don't seem to work for static methods
        # mocked actions for calls in helper too.
        user = dict()
        user["userid"] = "Profile1"
        api.UserList.return_value = [user]
        api.UserGetByID.return_value = user
        api.RoleGetByUser.return_value = ["ROLE1"]
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
        api.UserAccountsGet.return_value = [
            {
                "longid": "AD\\Profile1",
                "shortid": "Profile1",
                "targetid": "AD",
                "tgroupid": "AD",
                "tsynch": False,
                "unqpass": False
            }
        ]
        api.UserGroupsGet.return_value = [
            {
                "longid": "AD\\Profile1",
                "groupid": "Group1",
                "targetid": "AD",
                "direct": 1
            }
        ]
        api.ResourceAttrsGet.return_value = [
            {"name": "DEFICIT_CONFIDENTIALITY_IMPACT", "value": "1"},
            {"name": "DEFICIT_INTEGRITY_IMPACT", "value": "2"},
            {"name": "DEFICIT_AVAILABILITY_IMPACT", "value": "3"},
            {"name": "DEFICIT_ANNUAL_RISK_OF_OCCURRENCE", "value": "4.5"}
        ]
        process = RiskIdentification()
        process.process()
        analyse.assert_called_once()
        result_risk_analysis = analyse.call_args_list[0][0][0]
        assert "Profile1" ==  result_risk_analysis.profile.userid
        assert "Group3" == result_risk_analysis.resource.groupid
        assert "AD" == result_risk_analysis.resource.hostid
        assert DeviationType.DEFICIT == result_risk_analysis.type_of_deviation
        assert 1 == result_risk_analysis.risk_information.confidentiality_impact
        assert 2 == result_risk_analysis.risk_information.integrity_impact
        assert 3 == result_risk_analysis.risk_information.availability_impact
        assert 4.5 == result_risk_analysis.risk_information.annual_rate_of_occurrence

    @patch.object(RoleDeviationRiskAnalysis, "analyse")
    @patch('idmlib.core.api')
    def test_process_1_of_each(self, api, analyse):
        # Patches don't seem to work for static methods
        # mocked actions for calls in helper too.
        # Patches don't seem to work for static methods
        # mocked actions for calls in helper too.
        user = dict()
        user["userid"] = "Profile1"
        api.UserList.return_value = [user]
        api.UserGetByID.return_value = user
        api.RoleGetByUser.return_value = ["ROLE1"]
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

        api.UserAccountsGet.return_value = [
            {
                "longid": "AD\\Profile1",
                "shortid": "Profile1",
                "targetid": "AD",
                "tgroupid": "AD",
                "tsynch": False,
                "unqpass": False
            },
            {
                "longid": "PROFILE1",
                "shortid": "Profile1",
                "targetid": "SAP_GRC",
                "tgroupid": "SAP_GRC",
                "tsynch": False,
                "unqpass": False
            }
        ]
        api.UserGroupsGet.return_value = [
            {
                "longid": "AD\\Profile1",
                "groupid": "Group1",
                "targetid": "AD",
                "direct": 1
            },
            {
                "longid": "AD\\Profile1",
                "groupid": "Group4",
                "targetid": "AD",
                "direct": 1
            }
        ]
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
        process = RiskIdentification()
        process.process()
        assert 4 == len(analyse.call_args_list)
        surplus_acct_risk_analysis = analyse.call_args_list[0][0][0]
        assert "Profile1" == surplus_acct_risk_analysis.profile.userid
        assert "PROFILE1" == surplus_acct_risk_analysis.resource.acctid
        assert "SAP_GRC" == surplus_acct_risk_analysis.resource.hostid
        assert DeviationType.SURPLUS == surplus_acct_risk_analysis.type_of_deviation
        assert 5 == surplus_acct_risk_analysis.risk_information.confidentiality_impact
        assert 6 == surplus_acct_risk_analysis.risk_information.integrity_impact
        assert 7 == surplus_acct_risk_analysis.risk_information.availability_impact
        assert 8.9 == surplus_acct_risk_analysis.risk_information.annual_rate_of_occurrence
        surplus_grp_risk_analysis = analyse.call_args_list[1][0][0]
        assert "Profile1" == surplus_grp_risk_analysis.profile.userid
        assert "Group4" == surplus_grp_risk_analysis.resource.groupid
        assert "AD" == surplus_grp_risk_analysis.resource.hostid
        assert DeviationType.SURPLUS == surplus_grp_risk_analysis.type_of_deviation
        assert 5 == surplus_grp_risk_analysis.risk_information.confidentiality_impact
        assert 6 == surplus_grp_risk_analysis.risk_information.integrity_impact
        assert 7 == surplus_grp_risk_analysis.risk_information.availability_impact
        assert 8.9 == surplus_grp_risk_analysis.risk_information.annual_rate_of_occurrence
        deficit_acct_risk_analysis = analyse.call_args_list[2][0][0]
        assert "Profile1" == deficit_acct_risk_analysis.profile.userid
        assert "AZURE_TEMPLATE" == deficit_acct_risk_analysis.resource.tplid
        assert "AZURE_AD" == deficit_acct_risk_analysis.resource.hostid
        assert DeviationType.DEFICIT == deficit_acct_risk_analysis.type_of_deviation
        assert 1 == deficit_acct_risk_analysis.risk_information.confidentiality_impact
        assert 2 == deficit_acct_risk_analysis.risk_information.integrity_impact
        assert 3 == deficit_acct_risk_analysis.risk_information.availability_impact
        assert 4.5 == deficit_acct_risk_analysis.risk_information.annual_rate_of_occurrence
        deficit_grp_risk_analysis = analyse.call_args_list[3][0][0]
        assert "Profile1" == deficit_grp_risk_analysis.profile.userid
        assert "Group3" == deficit_grp_risk_analysis.resource.groupid
        assert "AD" == deficit_grp_risk_analysis.resource.hostid
        assert DeviationType.DEFICIT == deficit_grp_risk_analysis.type_of_deviation
        assert 1 == deficit_grp_risk_analysis.risk_information.confidentiality_impact
        assert 2 == deficit_grp_risk_analysis.risk_information.integrity_impact
        assert 3 == deficit_grp_risk_analysis.risk_information.availability_impact
        assert 4.5 == deficit_grp_risk_analysis.risk_information.annual_rate_of_occurrence

    @patch.object(RoleDeviationRiskAnalysis, "analyse")
    @patch('idmlib.core.api')
    def test_process_1_of_each_2_users(self, api, analyse):
        # Patches don't seem to work for static methods
        # mocked actions for calls in helper too.
        # Patches don't seem to work for static methods
        # mocked actions for calls in helper too.
        user = dict()
        user["userid"] = "Profile1"
        user2 = dict()
        user2["userid"] = "Profile2"
        api.UserList.return_value = [user, user2]
        api.UserGetByID.side_effect = [
            user,
            user2
        ]
        api.RoleGetByUser.return_value = ["ROLE1"]
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
            ],
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

        api.UserAccountsGet.side_effect = [
            [
                {
                    "longid": "AD\\Profile1",
                    "shortid": "Profile1",
                    "targetid": "AD",
                    "tgroupid": "AD",
                    "tsynch": False,
                    "unqpass": False
                },
                {
                    "longid": "PROFILE1",
                    "shortid": "Profile1",
                    "targetid": "SAP_GRC",
                    "tgroupid": "SAP_GRC",
                    "tsynch": False,
                    "unqpass": False
                }
            ],
            [
                {
                    "longid": "AD\\Profile2",
                    "shortid": "Profile2",
                    "targetid": "AD",
                    "tgroupid": "AD",
                    "tsynch": False,
                    "unqpass": False
                },
                {
                    "longid": "PROFILE2",
                    "shortid": "Profile2",
                    "targetid": "SAP_GRC",
                    "tgroupid": "SAP_GRC",
                    "tsynch": False,
                    "unqpass": False
                }
            ]
        ]
        api.UserGroupsGet.side_effect = [
            [
                {
                    "longid": "AD\\Profile1",
                    "groupid": "Group1",
                    "targetid": "AD",
                    "direct": 1
                },
                {
                    "longid": "AD\\Profile1",
                    "groupid": "Group4",
                    "targetid": "AD",
                    "direct": 1
                }
            ],
            [
                {
                    "longid": "AD\\Profile2",
                    "groupid": "Group1",
                    "targetid": "AD",
                    "direct": 1
                },
                {
                    "longid": "AD\\Profile2",
                    "groupid": "Group4",
                    "targetid": "AD",
                    "direct": 1
                }
            ]
        ]
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
            ],
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
        process = RiskIdentification()
        process.process()
        assert 8 == len(analyse.call_args_list)
        surplus_acct_risk_analysis = analyse.call_args_list[0][0][0]
        assert "Profile1" == surplus_acct_risk_analysis.profile.userid
        assert "PROFILE1" == surplus_acct_risk_analysis.resource.acctid
        assert "SAP_GRC" == surplus_acct_risk_analysis.resource.hostid
        assert DeviationType.SURPLUS == surplus_acct_risk_analysis.type_of_deviation
        assert 5 == surplus_acct_risk_analysis.risk_information.confidentiality_impact
        assert 6 == surplus_acct_risk_analysis.risk_information.integrity_impact
        assert 7 == surplus_acct_risk_analysis.risk_information.availability_impact
        assert 8.9 == surplus_acct_risk_analysis.risk_information.annual_rate_of_occurrence
        surplus_grp_risk_analysis = analyse.call_args_list[1][0][0]
        assert "Profile1" == surplus_grp_risk_analysis.profile.userid
        assert "Group4" == surplus_grp_risk_analysis.resource.groupid
        assert "AD" == surplus_grp_risk_analysis.resource.hostid
        assert DeviationType.SURPLUS == surplus_grp_risk_analysis.type_of_deviation
        assert 5 == surplus_grp_risk_analysis.risk_information.confidentiality_impact
        assert 6 == surplus_grp_risk_analysis.risk_information.integrity_impact
        assert 7 == surplus_grp_risk_analysis.risk_information.availability_impact
        assert 8.9 == surplus_grp_risk_analysis.risk_information.annual_rate_of_occurrence
        deficit_acct_risk_analysis = analyse.call_args_list[2][0][0]
        assert "Profile1" == deficit_acct_risk_analysis.profile.userid
        assert "AZURE_TEMPLATE" == deficit_acct_risk_analysis.resource.tplid
        assert "AZURE_AD" == deficit_acct_risk_analysis.resource.hostid
        assert DeviationType.DEFICIT == deficit_acct_risk_analysis.type_of_deviation
        assert 1 == deficit_acct_risk_analysis.risk_information.confidentiality_impact
        assert 2 == deficit_acct_risk_analysis.risk_information.integrity_impact
        assert 3 == deficit_acct_risk_analysis.risk_information.availability_impact
        assert 4.5 == deficit_acct_risk_analysis.risk_information.annual_rate_of_occurrence
        deficit_grp_risk_analysis = analyse.call_args_list[3][0][0]
        assert "Profile1" == deficit_grp_risk_analysis.profile.userid
        assert "Group3" == deficit_grp_risk_analysis.resource.groupid
        assert "AD" == deficit_grp_risk_analysis.resource.hostid
        assert DeviationType.DEFICIT == deficit_grp_risk_analysis.type_of_deviation
        assert 1 == deficit_grp_risk_analysis.risk_information.confidentiality_impact
        assert 2 == deficit_grp_risk_analysis.risk_information.integrity_impact
        assert 3 == deficit_grp_risk_analysis.risk_information.availability_impact
        assert 4.5 == deficit_grp_risk_analysis.risk_information.annual_rate_of_occurrence
        surplus_acct_risk_analysis2 = analyse.call_args_list[4][0][0]
        assert "Profile2" == surplus_acct_risk_analysis2.profile.userid
        assert "PROFILE2" == surplus_acct_risk_analysis2.resource.acctid
        assert "SAP_GRC" == surplus_acct_risk_analysis2.resource.hostid
        assert DeviationType.SURPLUS == surplus_acct_risk_analysis2.type_of_deviation
        assert 5 == surplus_acct_risk_analysis2.risk_information.confidentiality_impact
        assert 6 == surplus_acct_risk_analysis2.risk_information.integrity_impact
        assert 7 == surplus_acct_risk_analysis2.risk_information.availability_impact
        assert 8.9 == surplus_acct_risk_analysis2.risk_information.annual_rate_of_occurrence
        surplus_grp_risk_analysis2 = analyse.call_args_list[5][0][0]
        assert "Profile2" == surplus_grp_risk_analysis2.profile.userid
        assert "Group4" == surplus_grp_risk_analysis2.resource.groupid
        assert "AD" == surplus_grp_risk_analysis2.resource.hostid
        assert DeviationType.SURPLUS == surplus_grp_risk_analysis2.type_of_deviation
        assert 5 == surplus_grp_risk_analysis2.risk_information.confidentiality_impact
        assert 6 == surplus_grp_risk_analysis2.risk_information.integrity_impact
        assert 7 == surplus_grp_risk_analysis2.risk_information.availability_impact
        assert 8.9 == surplus_grp_risk_analysis2.risk_information.annual_rate_of_occurrence
        deficit_acct_risk_analysis2 = analyse.call_args_list[6][0][0]
        assert "Profile2" == deficit_acct_risk_analysis2.profile.userid
        assert "AZURE_TEMPLATE" == deficit_acct_risk_analysis2.resource.tplid
        assert "AZURE_AD" == deficit_acct_risk_analysis2.resource.hostid
        assert DeviationType.DEFICIT == deficit_acct_risk_analysis2.type_of_deviation
        assert 1 == deficit_acct_risk_analysis2.risk_information.confidentiality_impact
        assert 2 == deficit_acct_risk_analysis2.risk_information.integrity_impact
        assert 3 == deficit_acct_risk_analysis2.risk_information.availability_impact
        assert 4.5 == deficit_acct_risk_analysis2.risk_information.annual_rate_of_occurrence
        deficit_grp_risk_analysis2 = analyse.call_args_list[7][0][0]
        assert "Profile2" == deficit_grp_risk_analysis2.profile.userid
        assert "Group3" == deficit_grp_risk_analysis2.resource.groupid
        assert "AD" == deficit_grp_risk_analysis2.resource.hostid
        assert DeviationType.DEFICIT == deficit_grp_risk_analysis2.type_of_deviation
        assert 1 == deficit_grp_risk_analysis2.risk_information.confidentiality_impact
        assert 2 == deficit_grp_risk_analysis2.risk_information.integrity_impact
        assert 3 == deficit_grp_risk_analysis2.risk_information.availability_impact
        assert 4.5 == deficit_grp_risk_analysis2.risk_information.annual_rate_of_occurrence
