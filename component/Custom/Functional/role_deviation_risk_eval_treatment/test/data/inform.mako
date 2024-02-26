<%def name="subject()">
    Subject Inform
</%def>
<%def name="body_html()">
    HTML Inform (${str(risk_input.type_of_deviation)}, ${risk_score}, ${treatment.classification})
</%def>