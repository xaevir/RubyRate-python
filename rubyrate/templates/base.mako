<%namespace file="/partials/admin_nav.mako" import="admin_nav"/>
<%namespace file="/partials/heading_block.mako" import="heading_block"/>

<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
  "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en">
<head>
    <title>${self.title()}</title>
    <meta http-equiv="Content-Type" content="text/html;charset=UTF-8"/>
    <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1"/>
    <link rel="shortcut icon" href="/static/favicon.png"/>
    <link rel="stylesheet" type="text/css" href="${request.static_url('rubyrate:static/main.css')}"/>
    <link rel="stylesheet" type="text/css" href="${request.static_url('rubyrate:static/js/libs/fancybox/jquery.fancybox-1.3.4.css')}"/>
    <!--[if lt IE 8]>
    <script src="http://ie7-js.googlecode.com/svn/version/2.1(beta4)/IE8.js"></script>
    <![endif]-->   
    ${self.header_css()}
    ${self.header_js()}
</head>



<body id="${self.body_id()}" >

<div id="hd" class="clearfix">
    <div class="content clearfix">
        <a href="/" id="logo">
            <span class="ir">rubyrate</span>
        </a>
        <ul id="nav" class="clearfix">
            % if request.user:
                <li><a href="/users/${request.user.username}">My Chats</a></li>
            % endif
            % if hasattr(request.user, 'has_wish'):
                <li><a href="/users/${request.user.username}/wishes">My Wishes</a></li>
            % endif
            <li><a href="/wishes">All Wishes</a></li>
            <li><a href="/contact">Contact</a></li>
        </ul>
        <ul id="login-nav" class="clearfix">
            % if request.user:
                <li><a href="/logout">Logout <span style="font-weight: normal">
                    (<span id="username">${request.user.username}</span>)</span></a></li>
            % else:
                <li><a href="/users/create">Create Account</a></li>
                <li><a href="/users/login">Login</a></li>
            % endif
        </ul>
    </div>             
</div>

${self.heading_caller()}

<div id="bd" class="clearfix">
    <div id="flash">
    % if request.session.peek_flash():
        <div class="success">
                <% flash = request.session.pop_flash() %>
                % for message in flash:
                ${literal(message)}<br>
                % endfor
        </div>
    % endif
    </div>
    <div id="${self.page_segment()}">
        ${next.body()}
    </div>
    <div class="clear"></div>
</div>

<div id="footer">
    <%doc>
        <ul id="ft-nav">
            <li><a href="contact">Contact</a></li>
        </ul>
    </%doc>
    <p>
        &copy; Ruby Rate 2011
    </p>
${self.footer_js()}
<%text>
<script type="text/template" id="message-form">
    <form action="#" class="deform" id="convo-form">
        <textarea name="content"></textarea>
        <button name="submit" type="submit" class="btn" value="submit">
            <span>Send Message</span>
        </button>
    </form>
</div>
</script>

<script type="text/template" id="message-item">
        <li class="${css_class}">
            <blockquote class="bubble tip-${tip}">
                <p>
                ${message['content']}     
                </p>

            </blockquote>
            % if author == 'me':
                <span class="title">me</span>
            % else:
            <a class="title" href="/users/${author}"
                        style="font-size: 12px">${author}</a>
            % endif
        </li>
</script>

</%text>
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
    <script src="/static/js/libs/LABjs/LAB.js"></script>
    <script>
       $LAB
       .setOptions({AlwaysPreserveOrder:true})
       .script("/static/js/libs/jquery/jquery.js").wait()
       //.script("http://cdnjs.cloudflare.com/ajax/libs/raphael/1.5.2/raphael-min.js")
       //.script("http://cdnjs.cloudflare.com/ajax/libs/json2/20110223/json2.js")
       .script("/static/js/libs/underscore/underscore.js")
       .script("/static/js/libs/doTimeout.js")
       .script("/static/js/libs/backbone/backbone.js").wait()
       .script("http://ajax.aspnetcdn.com/ajax/jquery.validate/1.9/jquery.validate.min.js")
       //.script("/static/js/libs/fancybox/jquery.fancybox-1.3.4.pack.js")
       .script("/static/js/libs/pinfooter.js")
       .script("/static/js/libs/isotope.min.js").wait()
       .script("/static/js/app.js").wait()
       .script("/static/js/modules/nav.js").wait()
       .script("/static/js/main.js").wait()
    </script>
    <script>
    </script>

</%def>

<%def name="body_id()">regular</%def>
<%def name="page_width()"></%def>
<%def name="page_segment()"></%def>
<%def name="heading_caller()"></%def>
<%def name="bd_hd()"></%def>
<%def name="header_css()"></%def>
