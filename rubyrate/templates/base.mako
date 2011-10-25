<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
  "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en">
<head>
    <title>${self.title()}</title>
    <meta http-equiv="Content-Type" content="text/html;charset=UTF-8"/>
    <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">
    <link rel="shortcut icon" href=${request.static_url('rubyrate:static/favicon.png')} />
    <link rel="stylesheet" type="text/css" href="${request.static_url('rubyrate:static/main.css')}"/>
    <!--[if lt IE 8]>
    <script src="http://ie7-js.googlecode.com/svn/version/2.1(beta4)/IE8.js"></script>
    <![endif]-->   
    ${self.header_css()}
    ${self.header_js()}
</head>

<body id="${self.body_id()}" >


    <div id="hd" class="clearfix">
        <div class="content clearfix">
            <a href="/" id="logo" class="ir">rubyrate</a>
            <ul id="nav" class="clearfix">
                <li><a href="/wishes">Open Wishes</a></li>
                <li><a href="/supplier">Suppliers</a></li>
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
    </div>

<div id="doc2" class="clearfix" style="width: ${self.page_width()}">


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
${self.footer_js()}
</body>
</html>

<%def name="title()">Ruby Rate</%def>

<%def name="footer_js()">
    <a title="Web Analytics" href="http://getclicky.com/66480413"><img alt="Web Analytics" src="//static.getclicky.com/media/links/badge.gif" border="0" /></a>
    <script type="text/javascript">
    var clicky_site_ids = clicky_site_ids || [];
    clicky_site_ids.push(66480413);
    (function() {
      var s = document.createElement('script');
      s.type = 'text/javascript';
      s.async = true;
      s.src = '//static.getclicky.com/js';
      ( document.getElementsByTagName('head')[0] || document.getElementsByTagName('body')[0] ).appendChild( s );
    })();
    </script>
    <noscript><p><img alt="Clicky" width="1" height="1" src="//in.getclicky.com/66480413ns.gif" /></p></noscript>
</%def>

<%def name="header_js()">
    <script src="http://cdnjs.cloudflare.com/ajax/libs/labjs/2.0.3/LAB.min.js"></script>
    <script>
       $LAB
       .setOptions({AlwaysPreserveOrder:true})
       .script("http://cdnjs.cloudflare.com/ajax/libs/jquery/1.6.4/jquery.min.js").wait()
       .script("http://cdnjs.cloudflare.com/ajax/libs/raphael/1.5.2/raphael-min.js")
       .script("http://cdnjs.cloudflare.com/ajax/libs/json2/20110223/json2.js")
       .script("http://cdnjs.cloudflare.com/ajax/libs/underscore.js/1.1.7/underscore-min.js")
       .script("http://cdnjs.cloudflare.com/ajax/libs/backbone.js/0.5.3/backbone-min.js").wait()

       .script("/static/js/main.js")
    </script>
    <script>
    </script>

</%def>

<%def name="body_id()">regular</%def>
<%def name="page_width()"></%def>
<%def name="bd_hd()"></%def>
<%def name="header_css()"></%def>
