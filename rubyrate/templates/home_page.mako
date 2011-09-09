<%inherit file="/base.mako"/>
<%def name="page_name()">home</%def>
<%def name="js()">
    <script type="text/javascript" src="${request.static_url('rubyrate:static/jquery-1.6.2.min.js')}"></script>
    <script type="text/javascript" src="${request.static_url('rubyrate:static/fancybox/jquery.fancybox-1.3.4.pack.js')}"></script>
    <script type="text/javascript" src="${request.static_url('rubyrate:static/fancybox/jquery.easing-1.3.pack.js')}"></script>
    <script type="text/javascript" src="${request.static_url('rubyrate:static/main.js')}"></script>
</%def>
<%def name="head()">
    <link rel="stylesheet" type="text/css" href="${request.static_url('rubyrate:static//fancybox/jquery.fancybox-1.3.4.css')}"/>
</%def>


<%def name="bd_hd()">
    <div class="col_1">
        <h1>We will do your product  pricing research</h1>
        <p style="font-size: 16px; color: #626262">
            Enter information about a specific product in the form. We will 
            then perform pricing research for that specific item. After we 
            have compiled our results we will send you an email with the 
            pricing information.
        </p>
    </div>
    <div class="col_2">
        ${literal(form)}
    </div>
</%def>

<div class="col_1" style="padding-top: 20px">
    <ul class="arrows">
        <li><h3>Make you sure are getting the best price</h3>
            We price many suppliers to ensure you are getting the best 
            prices.
        </li>

        <li><h3>Make sure you are not missing out on any discounts</h3>
            We send you notifications if there are sales or discounts for your item.
        </li>

        <li><h3>Saves you time and its free</h3>       
            We will do all the research for you for free
        </li>
    </ul>
</div>
<div class="col_2">

    <h3>More about our service</h3>
    <p>
        Our service is ideal for those that plan ahead or know they will need 
        a particular item in the future. Allowing us to perform the research 
        as well as notify you of the sales, that approaching or discounts 
        for that product.     
    </p>

</div>

