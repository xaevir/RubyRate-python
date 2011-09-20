<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
  "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en">
<head>
    <title>${self.title()}</title>

    <meta http-equiv="Content-Type" content="text/html;charset=UTF-8"/>
        
    <link rel="shortcut icon" href=${request.static_url('rubyrate:static/favicon.png')} />
    <link rel="stylesheet" type="text/css" href="${request.static_url('rubyrate:static/main.css')}"/>
    <!--[if lt IE 7]>
    <script src="http://ie7-js.googlecode.com/svn/version/2.1(beta4)/IE7.js"></script>
    <![endif]-->
    ${self.head()}
</head>

<body id="${self.page_name()}" >
<div id="doc2" class="clearfix">

    <div id="hd" class="clearfix">
        <a href="/" class="clearfix" style="float: left">
            <h2 id="logo" class="ir">Ruby Rate</h2>
        </a>
        <ul id="login-nav" class="clearfix">
            % if request.loggedin:
                <li><a href="/logout">Logout</a></li>
            % else:
                <li><a href="/users/create">Create Account</a></li>
                <li><a href="/users/login">Login</a></li>
            % endif
        </ul>
        <div class="clear"></div>
        <ul id="nav" class="clearfix">
            <li><a href="/items">Items Needing Pricing</a></li>
            <li>|</li>
            <li><a href="/supplier">Suppliers</a></li>
            <li>|</li>
            <li><a href="/contact">Contact</a></li>
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

<a title="Real Time Web Analytics" href="http://getclicky.com/66480413"><img alt="Real Time Web Analytics" src="//static.getclicky.com/media/links/badge.gif" border="0" /></a>
<script src="//static.getclicky.com/js" type="text/javascript"></script>
<script type="text/javascript">try{ clicky.init(66480413); }catch(e){}</script>
<noscript><p><img alt="Clicky" width="1" height="1" src="//in.getclicky.com/66480413ns.gif" /></p></noscript>

<script type="text/javascript" src="${request.static_url('rubyrate:static/jquery-1.6.2.min.js')}"></script>
${self.js()}
<script type="text/javascript" src="${request.static_url('rubyrate:static/main.js')}"></script>
</body>
</html>

<%def name="title()">Ruby Rate</%def>
<%def name="head()"></%def>
<%def name="js()">
</%def>
<%def name="page_name()">regular</%def>
<%def name="bd_hd()"></%def>
