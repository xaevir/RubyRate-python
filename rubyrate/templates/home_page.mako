<%inherit file="/base.mako"/>
<%def name="page_name()">home</%def>
<%def name="js()">
    <script type="text/javascript" src="${request.static_url('rubyrate:static/fancybox/jquery.fancybox-1.3.4.pack.js')}"></script>
    <script type="text/javascript" src="${request.static_url('rubyrate:static/fancybox/jquery.easing-1.3.pack.js')}"></script>
</%def>
<%def name="head()">
    <link rel="stylesheet" type="text/css" href="${request.static_url('rubyrate:static//fancybox/jquery.fancybox-1.3.4.css')}"/>
</%def>


    <div class="col_1">
        <h1>We do your product pricing research</h1>
        <h2>How it works</h2>

        <ul class="how-works">
            <li>
                <span class="circle">1</span>
                <h3>We do your product researching</h3>
                <p>
                After you fill in the form on the right, we contact  
                national, local, or internationl suppliers for prices, promotions, 
                and discounts.
                </p>
            </li>
            <li>
                <span class="circle">2</span>
                <h3>Report the research</h3>
                <p>
                We then email you this collected information in an easy to digest
                email with pictures and prices of each supplier's product. 
                </p>
            </li>
            <li> 
                <span class="circle">3</span>
                <h3>Monitor for prices changes</h3>
                <p>
                Within your lead time, we continue to check in with the suppliers 
                to see if anything about their prices have changed.
                </p>
            </li>
        </ul>

    </div>
    <div class="col_2">
        ${literal(form)}
    </div>
    <div class="clear"></div>
    <h2>How it benefits you</h2>
    <ul id="points" class="clearfix">
        <li>
            <h3>Save Time</h3>
            Saves you the time and hassle it takes to shop around for your
            product.
        </li>
        <li>
            <h3>Save Work</h3>
            Saves you the work of organizing the pricing info with a pen and 
            pad.  
        </li>
        <li>
            <h3>Save Money</h3>
            Saves you money. Your time is money and our service is free
            for now. 
        </li>
    </ul>

    <h2 style="margin-top: 1em;">If you have questions?</h2>
    <p><b>Email:</b> ruby@rubyrate.com</p>
    <p><b>Phone:</b> 484.452.4064</p>
    <p>Or you can fill out the form on the <a href="/contact">contact page</a></p>

            


