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


    <div class="col_1">
        <h1>We do your product pricing research</h1>
        <h2>Here is how it works</h2>
        <p style="font-size: 16px; color: #626262">
            After you fill in the form on the right, we contact suppliers for 
            pricing, find out if they have any sales, coupons, or 
            discounts. We will than email you with pricing 
            infromation regarding your product. We want to keep you 
            informed if you can get better pricing for your product. Thats it. 
        </p>

        <h2>Benefits to you</h2>
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
    <h3>More about our service</h3>
    <p>
        Our service is ideal for those that plan ahead or know they will need 
        a particular item in the future. Allowing us to perform the research 
        as well as notify you of the sales, that approaching or discounts 
        for that product.     
    </p>

    </div>
    <div class="col_2">
        ${literal(form)}
    </div>

<div class="col_1">
</div>
<div class="col_2">


</div>

