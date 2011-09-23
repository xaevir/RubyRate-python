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
        <th>Update</th>
        <th>Delete</th>
        <th>Answer</th>
    </tr>
    <% index = 0 %>
    % for item in items:
        <% index +=1 %>
    <tr class="${altrow(index)}">
        <td><a href="/wishes/${item['_id']}">${item['product']}</a></td>
        <td><a href="/wishes/${item['_id']}/edit">edit</a></td>
        <td><a href="/wishes/${item['_id']}/delete">delete</a></td>
        <td><a href="/wishes/${item['_id']}/answers">Answer</a></td>
    </tr>
    % endfor
</table>
