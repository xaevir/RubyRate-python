<%inherit file="/base.mako"/>
<% 
def altrow(index):
    if index%2==0:
        row = 'even'    
    else:
        row = 'odd' 
    return row
%>

<table id="items">
    <tr>
        <th>Product</th>
        <th>Description</th>
        <th>Update</th>
        <th>Delete</th>
    </tr>
    <% index = 0 %>
    % for item in items:
        <% index +=1 %>
    <tr class="${altrow(index)}">
        <td><a href="/items/${item['name']}">${item['prooduct']}</a></td>
        <td>${item['description']}</td>
        <td><a href="/items/${item['name']}/edit">edit</a></td>
        <td><a href="/items/${item['name']}/delete">delete</a></td>
    </tr>
    % endfor
</table>
