<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
  "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en">
<head>
    <title>${self.title()}</title>

    <meta http-equiv="Content-Type" content="text/html;charset=UTF-8"/>
        
    <link rel="shortcut icon" href=${request.static_url('rubyrate:static/favicon.png')} />
    <link rel="stylesheet" type="text/css" href="${request.static_url('rubyrate:static/main.css')}"/>
    <meta name="google-site-verification" content="FEhVgca4t1L-9-6SYatkLmhXwd4TtlapTRDh7h4qQtM" />
    ${self.head()}
</head>

<body id="${self.page_name()}" >
<div id="doc2" class="clearfix">

    <div id="hd" class="clearfix">
        <a id="logo" href="/">
            <img src="${request.static_url('rubyrate:static/rubyrate_logo.png')}" />
        </a>
        <ul id="nav" class="clearfix">
            <li><a href="/items">Items Needing Pricing</a></li>
            <li>|</li>
            <li><a href="/supplier">Suppliers</a></li>
            <li>|</li>
            <li><a href="/contact">Contact</a></li>
        </ul>
        <ul id="login-nav" class="clearfix">
            % if request.loggedin:
                <li><a href="/logout">Logout</a></li>
            % else:
                <li><a href="/users/create">Create Account</a></li>
                <li><a href="/users/login">Login</a></li>
            % endif
        </ul>
    </div>

    <div id="bd">
        % if request.session.peek_flash():
        <div id="flash">
            <% flash = request.session.pop_flash() %>
                % for message in flash:
                ${literal(message)}<br>
                % endfor
        </div>
        % endif

        ${next.body()}

        <div class="clear"></div>
    </div>

    <div id="ft">
        <%doc>
            <ul id="ft-nav">
                <li><a href="contact">Contact</a></li>
            </ul>
        </%doc>
        <p>
            &copy; Ruby Rate 2011
        </p>
    </div>

</div>

${self.js()}
</body>
</html>

<%def name="title()">Ruby Rate</%def>
<%def name="head()"></%def>
<%def name="js()">
</%def>
<%def name="page_name()">regular</%def>
<%def name="bd_hd()"></%def>
