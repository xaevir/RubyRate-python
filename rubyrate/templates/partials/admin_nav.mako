<%def name="admin_nav()">
<% url = request.resource_url%>

% if 'admin' in request.user.groups:
    <ul>
        <li><a href="/">create login email</a></li>
    </ul>
% endif
</%def>

