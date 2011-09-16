<%inherit file="/base.mako"/>
<%def name="page_name()">item-view</%def>
<% from rubyrate.utility import pretty_date %>

<h1>${item.product}</h1>

<table id="items">
    <tr>
        <th>Description</th>
        <th>Quantity</th>
        <th>Lead Time</th>
        <th>Area Code</th>
        <th>Price Range </th>
        <th>International pricing</th>
        <th>Posted:</th>
    </tr>
    <tr>
        <td>${item.description}</td>
        <td>${item.quantity}</td>
        <td>${item.lead_time}</td>
        <td>${item.area_code}</td>
        <td>${getattr(item, 'price_range', 'not specified')}</td>
        <td>${item.international}</td>
        <td>${pretty_date(item.created)}</td>
    </tr>
</table>
