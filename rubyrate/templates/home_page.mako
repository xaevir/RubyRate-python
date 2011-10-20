<%inherit file="/base.mako"/>
<%def name="body_id()">home</%def>
<%def name="js()">
    <script type="text/javascript" src="${request.static_url('rubyrate:static/fancybox/jquery.fancybox-1.3.4.pack.js')}"></script>
    <script type="text/javascript" src="${request.static_url('rubyrate:static/fancybox/jquery.easing-1.3.pack.js')}"></script>
</%def>
<%def name="header_css()">
    <link rel="stylesheet" type="text/css" href="${request.static_url('rubyrate:static//fancybox/jquery.fancybox-1.3.4.css')}"/>
</%def>


    <blockquote class="rectangle-speech-border light-yellow right-tip" id="main-headline">
        <h1>We connect you to people who want your business</h1>
        <div id="arc-tip"></div>
    
    </blockquote>
    <div class="col_1" id="how-it-works">
        <h2>How it works</h2>
            <blockquote class="rectangle-speech-border">
            <table>
                <tr>
                    <td class="num">
                        <span>1</span>
                    </td>
                    <td>
                        <p>You enter the product or service that 
                        you are looking to buy</p>
                    </td>
                </tr>
                <tr>
                    <td class="num">
                        <span>2</span>
                    </td>
                    <td>
                        <p>
                        We find companies in your area who 
                        can help because they want your business</p>
                    </td>
                </tr>
                <tr class="no-border">
                    <td class="num">
                        <span>3</span>
                    </td>
                    <td>
                        <p>
                        In return you get helpful replies and 
                        maybe even discount</p>
                    </td>
                </tr>
            </table>
                <b class="a1"></b>
                <b class="a2"></b>
                <b class="a3"></b>
                <b class="a4"></b>
            </blockquote>
    </div>
  
 



<%doc>
        <ul class="how-works">
            <li>
                <span class="circle">1</span>
                <p>
                    You enter the product or service you are looking to find.
                </p>
            </li>
            <li>
                <span class="circle">2</span>
                <p>
                    We spend several days finding the companies in your area who 
                    can help you simply because they want your business.
                </p>
            </li>
            <li> 
                <span class="circle">3</span>
                <p>
                    When the first reply comes in, you get receive an email.
                </p>
            </li>
        </ul>
</%doc>
    <div class="col_2">
        <h2>Give it a try</h2>
        ${literal(form)}
    </div>
    <div class="clear"></div>
    <h2>Why its helpful</h2>
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

            


