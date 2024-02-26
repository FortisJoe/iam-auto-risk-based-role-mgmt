<%def name="subject()">
    Subject Action
</%def>
<%def name="body_html()">
    HTML Action (${str(risk_input.type_of_deviation)}, ${risk_score}, ${treatment.classification})
</%def>