<%inherit file="/base.mako"/>
<%def name="page_name()">item-list</%def>
<% from rubyrate.utility import pretty_date %>
<% 
def altrow(index):
    if index%2==0:
        row = 'even'    
    else:
        row = 'odd' 
    return row
%>

<h1>Recent items that need pricing</h1>

<table id="items">
    <tr>
        <th>Product</th>
        <th>Quantity</th>
        <th>Lead Time</th>
        <th>Area Code</th>
        <th>Price Range </th>
        <th>International pricing</th>
        <th>Posted:</th>
    </tr>
    <% index = 0 %>
    % for item in items:
        <% index +=1 %>
    <tr class="${altrow(index)}">
        <td><a href="/items/${item['_id']}">${item['product']}</a></td>
        <td>${item['quantity']}</td>
        <td>${item['lead_time']}</td>
        <td>${item['area_code']}</td>
        <td>${item.get('price_range', 'n/a')}</td>
        <td>${item.get('international', 'n/a')}</td>
        <td>${pretty_date(item['created'])}</td>
    </tr>
    % endfor
</table>
