from idmlib import core

templates = dict()
for resource in core.api.ResourceFind("TMPL", []):
    tmpl_id = resource["resourceid"]
    for result in core.api.ResourceGet(tmpl_id, "", "", "TMPL"):
        if result[0] == "hostid":
            templates[result[1]] = tmpl_id

for resource in core.api.ResourceFind("MGRP", []):
    mgrp_id1 = resource["resourceid"]
    mgrp_id2 = resource["resourceid2"]
    hostid = None
    shortid = None
    longid = None
    for result in core.api.ResourceGet(mgrp_id1, mgrp_id2, "", "MGRP"):
        if result[0] == "hostid":
            hostid = result[1]
        elif result[0] == "shortid":
            shortid = result[1]
        elif result[0] == "nosgroupname":
            longid = result[1]
    if hostid == "AD":
        role_id = shortid.upper().replace(" ", "_")
    else:
        role_id = f"{hostid}_{shortid.upper().replace(' ', '_')}"
    core.api.RoleCreate(role_id, shortid, 1, 1, 0)
    tmpl_id = templates[hostid]
    core.api.RoleResourceAdd(role_id, "TEMPLATE", tmpl_id, "", False)
    core.api.RoleResourceAdd(role_id, "MANAGEDGROUP", hostid, longid, False)
