from idmlib import core
from idmlib.components import component_log
from idmlib.idapi import APIError

from Functional.role_deviation_risk_analysis.analyse import (
    DeviationType,
    RiskInformation,
    RiskAnalysisInput
)

log = component_log.getChild(__name__)


def get_target_accounts_in_roles(profile):
    """ Fetches targets of accounts from users roles

    :param idmlib.idmobject.Profile profile: The user profile
    :return: Set of targets of accounts in the profiles roles
    :rtype: set
    """
    targets_with_accounts_in_roles = set()
    for role in profile.roles:
        for resource in core.api.RoleResourceList(
                role.roleid,
                True,
                True,
                True
        ):
            if resource["membertype"] == "TEMPLATE":
                template_id = resource["memberid"]
                try:
                    for result in core.api.ResourceGet(
                            template_id,
                            "",
                            "",
                            "TMPL"
                    ):
                        if result[0] == "hostid":
                            targets_with_accounts_in_roles.add(result[1])
                            break
                except APIError as e:
                    log.error(
                        f'Failed to find details for template '
                        f'{template_id}',
                        exc_info=e
                    )
    return targets_with_accounts_in_roles


def get_groups_in_roles(profile):
    """ Fetches groups from users roles

    :param idmlib.idmobject.Profile profile: The user profile
    :return: Set of groups in the profiles roles in format hostid:groupid
    :rtype: set
    """
    groups_in_roles = set()
    for group in profile.groups:
        groups_in_roles.add(f"{group.hostid}:{group.groupid}")
    return groups_in_roles


def get_template_for_hostid(hostid):
    """ Finds a template id for a target

    :param str hostid: The id of a target
    :return: the id of a template for that system
    :rtype: str
    """
    for resource in core.api.ResourceFind("TMPL", [("targetid", hostid)]):
        return resource["resourceid"]


def get_account_risk_information(template_id, is_surplus=False):
    """ Fetches risk information for an account

    :param str template_id: The ID of the template
    :param bool is_surplus: True if we want surplus risk, False if deficit
    :return: The surplus or deficit risk information for an account
    :rtype: Functional.role_deviation_risk_analysis.analyse.RiskInformation
    """
    attrs = _get_attributes(is_surplus)
    return _fetch_risk_resource_attributes(attrs, "TMPL", template_id)


def get_group_risk_information(hostid, groupid, is_surplus=False):
    """ Gets group risk information

    :param str hostid: The target id of the group
    :param str groupid: The group id of the group
    :param bool is_surplus: True if we want surplus risk, False if deficit
    :return: The surplus or deficit risk information for a group
    :rtype: Functional.role_deviation_risk_analysis.analyse.RiskInformation
    """

    attrs = _get_attributes(is_surplus)
    return _fetch_risk_resource_attributes(attrs, "MGRP", hostid, groupid)


def _get_attributes(is_surplus):
    if is_surplus:
        attrs = [
            "SURPLUS_CONFIDENTIALITY_IMPACT",
            "SURPLUS_INTEGRITY_IMPACT",
            "SURPLUS_AVAILABILITY_IMPACT",
            "SURPLUS_ANNUAL_RISK_OF_OCCURRENCE"
        ]
    else:
        attrs = [
            "DEFICIT_CONFIDENTIALITY_IMPACT",
            "DEFICIT_INTEGRITY_IMPACT",
            "DEFICIT_AVAILABILITY_IMPACT",
            "DEFICIT_ANNUAL_RISK_OF_OCCURRENCE"
        ]
    return attrs


def _fetch_risk_resource_attributes(attrs, restype, resourceid1, resourceid2=""):
    confidentiality = None
    integrity = None
    availability = None
    aro = None
    for resource in core.api.ResourceAttrsGet(
            resourceid1,
            resourceid2,
            restype,
            attrs
    ):
        if resource["name"].endswith("CONFIDENTIALITY_IMPACT"):
            confidentiality = int(resource["value"])
        elif resource["name"].endswith("INTEGRITY_IMPACT"):
            integrity = int(resource["value"])
        elif resource["name"].endswith("AVAILABILITY_IMPACT"):
            availability = int(resource["value"])
        elif resource["name"].endswith("ANNUAL_RISK_OF_OCCURRENCE"):
            aro = float(resource["value"])
    return RiskInformation(confidentiality, integrity, availability, aro)
