<%inherit file="/base.mako"/>
<%def name="page_name()">quote</%def>

<h1>Say <span>hello...</span></h1>

<p>
    We would love to hear from you.
</p>
<p>
    <b>email: </b>hello@rubyrate.com
</p>
            
	
<form action="${save_url}" method="post">
    <label>Name</label>
    <input name="name" type="text"/>

    <label>Email</label>
    <input name="email" type="text"/>

    <label>Message</label>
    <textarea name="message"></textarea>

    <input type="submit" name="submit" class="button" value="Send"/>
</form>	

