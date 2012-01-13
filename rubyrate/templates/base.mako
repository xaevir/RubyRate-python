<%namespace file="/partials/admin_nav.mako" import="admin_nav"/>
<%namespace file="/partials/heading_block.mako" import="heading_block"/>

<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>${self.title()}</title>

    <!-- HTML5 shim, for IE6-8 support of HTML elements -->
    <!--[if lt IE 9]>
      <script src="http://html5shim.googlecode.com/svn/trunk/html5.js"></script>
    <![endif]-->

    <link rel="shortcut icon" href="/static/favicon.png"/>

    <link rel="stylesheet/less" type="text/css" href="/static/css/bootstrap.less">
    <script src="/static/js/libs/less/less-1.2.0.min.js" type="text/javascript"></script>

    <%doc>
    <script>
      if (less.env === "development")
          less.watch();
    </script>
    <%doc>
    <%doc>
    <link rel="stylesheet" type="text/css" href="/static/bootstrap.css">
    <link rel="stylesheet" type="text/css" href="/static/main.css">
    </%doc>


    <script>
        % if json_data is not UNDEFINED:
            var json_data =  ${literal(json_data)};
        % endif 

        
        % if load_module is not UNDEFINED: 
            var load_module = '${load_module}';
        % endif

        <%doc>
        require(['app', 
            % if js_module is not UNDEFINED: 
                'views/${js_module}'
                % endif
        ]);
        </%doc>
    </script>

    <script data-main="/static/js/main" src="/static/js/libs/require/require.js"></script>



   ${self.styles()} 
</head>

<body>
  <div class="topbar">
     <div class="fill"> 
        <div class="container">
          <a class="brand" href="/">
              <span class="ir">ruby<b>rate</b></span>
          </a>
          <ul class="nav">
            <li class="active"><a href="#">Home</a></li>
                % if request.user:
                    <li><a href="/my/messages">My Messages</a></li>
                    <li><a href="#" class="action-create-wish">Create Wish</a></li>
                % endif
                <li><a href="/messages/wish">All Wishes</a></li>

          </ul>
              <p class="pull-right">
                % if request.user:
                    <a href="/logout">Logout
                        (${request.user.username})</a>
                % else:
                    <a href="/users/create">Create Account</a>
                    <a href="/users/login">Login</a>
                % endif
              </p>
        </div>
    </div>
  </div>

    <div class="container">
      ${next.body()}

      <footer>
        <div class="horizontal-rule ">
            <span class="first"></span>
            <span class="second"></span>
            <span class="third"></span>
        </div>

        <li><a href="/contact">Contact</a></li>
        <p> &copy; Ruby Rate 2011</p>
      </footer>

    </div> <!-- /container -->

</body>
</html>

<%def name="styles()"></%def>
<%def name="title()">Ruby Rate</%def>
<%def name="heading_caller()"></%def>
