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
        <th>Wish</th>
        <th>Update</th>
        <th>Delete</th>
        <th>Owned By or Activation url</th>
    </tr>
    <% index = 0 %>
    % for wish in wishes:
        <% index +=1 %>
    <tr class="${altrow(index)}">
        <td><a href="/wishes/${wish['_id']}">${wish['content']}</a></td>
        <td><a href="/wishes/${wish['_id']}/edit">edit</a></td>
        <td><a href="/wishes/${wish['_id']}/delete">delete</a></td>
        <td style="width: 350px;">
        <% user = get_wish_owner(wish['user_id']) %>
        % try:
            ${user['username']}     
        % except:
            rubyrate.com/users/${wish['user_id']}/activate
        % endtry
        </td>
    </tr>
    % endfor
</table>
