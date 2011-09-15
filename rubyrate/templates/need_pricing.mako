<%inherit file="/base.mako"/>
<%def name="page_name()">need-pricing</%def>
<% from rubyrate.utility import pretty_date %>
<table id="items">
    <tr>
        <th>Item</th>
        <th>Quantity</th>
        <th>Lead Time</th>
        <th>Area Code</th>
        <th>Price Range </th>
        <th>Internationl pricing</th>
        <th>Posted:</th>
    </tr>
    % for item in items:
    <tr>
        <td>${item['product']}</td>
        <td>${item['quantity']}</td>
        <td>${item['lead_time']}</td>
        <td>${item['area_code']}</td>
        <td>${item.get('price_range', 'not specified')}</td>
        <td>${item['international']}</td>
        <td>${pretty_date(item['created'])}</td>
    </tr>
    % endfor
</table>
