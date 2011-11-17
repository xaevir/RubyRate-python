<%inherit file="/base.mako"/>
<%namespace file="/partials/heading_block.mako" import="heading_block"/>

<%def name="body_id()">${page_name or 'form-page'}</%def>

    <%def name="heading_caller()">
        % if heading:
            ${heading_block(heading)}
        % endif
    </%def>

% if content:
    <div id="c1">${literal(content)}</div>
% endif

${literal(form)}


