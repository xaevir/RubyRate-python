<%inherit file="/base.mako"/>

<%def name="body_id()">${page_name or 'general'}</%def>

% if heading:
   <h1>${heading}</h1>
% endif

% if answer:
    ${literal(answer)}
% endif

% if answer:
    <h1>${answer_heading}</h1>
% endif

${literal(form)}

% if button:
    ${literal(button)}
% endif


