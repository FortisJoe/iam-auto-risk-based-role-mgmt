from idmlib import core
from idmlib.idmobject import Profile

for user in core.api.UserList(1):
    profile = Profile(user["userid"])
    for group in profile.groups:
        group_desc = group.groupname
        if not group_desc:
            for result in core.api.ResourceGet(group.hostid, group.groupid, "", "MGRP"):
                if result[0] == "shortid":
                    group_desc = result[1]
                    break
        if not group_desc:
            print(f"Failed to find group name for {group.groupid} on {group.hostid}")
            continue
        if group.hostid == "AD":
            role_id = group_desc.upper().replace(" ", "_")
        else:
            role_id = f"{group.hostid}_{group_desc.upper().replace(' ', '_')}"
        try:
            core.api.UserRoleAdd(profile.userid, role_id, 1)
        except Exception:
            print(f"Failed to add {profile.userid} to {role_id}")
