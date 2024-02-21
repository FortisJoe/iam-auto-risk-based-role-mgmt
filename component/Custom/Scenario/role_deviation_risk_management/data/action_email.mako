<%def name="subject()">
    Role Access Remediation
</%def>
<%def name="body_html()">
    <%
    from idmlib.idmobject import ResourceGroup, ResourceTemplate
    from Functional.role_deviation_risk_analysis.analyse import DeviationType
    recipient_name = risk_info.profile.alias
    if isinstance(risk_info.resource, ResourceTemplate):
        deviation = f"{risk_info.resource.hostid} account"
    else:
        deviation = f"membership of {risk_info.resource.groupid} on the {risk.resource.hostid} system"
    deviation_type = str(risk_info.type_of_deviation)
    if risk_info.type_of_deviation == DeviationType.SURPLUS:
        action = "removed"
    else:
        action = "added"
    %>
    <html>
        <body>
            <p>Hello,</p>

            <p>${recipient_name} has an access deviation from the access defined by the roles they are a member of.</p>

            <p>They have a ${deviation_type} of a ${deviation}.</p>

            <p>As the risk level for a ${deviation_type} deviation for this access is deemed to be ${treatment.classification}, this access will have a request raised for it to be {action}.</p>

            <p>Many thanks,</p>

            <p>IT Security.</p>
        </body>
    </html>
</%def>