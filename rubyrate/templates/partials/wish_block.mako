<%def name="wish_block(wish_data, shorten=False, size='small', reply=True, view=False)">
<% 
class Wish: 
    pass 
wish = Wish()    
# assume its an object 
if hasattr(wish_data, '__dict__'): 
    wish.__dict__ = wish_data.__dict__
else: # its a dict
    wish.__dict__ = wish_data
%>
<% url = request.resource_url%>

    <blockquote class="bubble tip-left">
        <p>
            % if shorten and len(wish.content) > 160:
                ${wish.content[0:160]} 
                <a href="/wishes/${wish._id}" class="more"
                >...more</a>
            % else:
                ${wish.content}
            % endif
        </p>
        % if request.user._id != wish.user_id and reply:
            <a href="/wishes/${wish._id}/messages/create" class="btn-reply btn-reply-${size}"
                >reply</a>
        % endif
        <div class="zip-code">
            ${wish.zip_code}
        </div>
    </blockquote>
</%def>
   
