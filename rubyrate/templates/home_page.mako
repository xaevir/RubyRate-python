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
        <h1>What if you could compare prices 
            to get the best product for the best price in the World?</h1>
        <p style="font-size: 16px; color: #626262">Here you can do it.
           Just enter your information in the form and we will send you an easy
           to read email so you can compare quotes from the US and world 
           suppliers.</p>
    </div>
    <div class="col_2">
        ${literal(form)}
    </div>
</%def>

<div class="col_1" style="padding-top: 20px">
    <ul class="arrows">
        <li><h3>We negotiate the prices for you.</h3>
            We are in the business to get you the best possible product at the
            best possible price.
        </li>

        <li><h3>Its 100% free</h3>
            Its 100 percent free to receive a quote.
        </li>

        <li><h3>Must be a bulk purchase</h3>
            In order for our service to work quotes for Bulk orders are only
            accepted. What is a bulk order: an order of 30 or more of the same
            units.
        </li>
    </ul>
</div>
<div class="col_2">

    <h3>More about our service</h3>
    <p>
        We specialize  Eco-friendly building products ie water saving
        products, Eco-friendly flooring, stainless steel products, kitchens,
        tiles. However we are not just limited to building supplies. You name
        we can can quote it. If you need assistance with purchasing of a
        product to importing we are here to help. We believe you should be
        getting the best product for the best price.
    </p>
    <p> 
        If you are not ready for a bulk purchase yet. Sign up to recieve
        <a href="/price-alerts">price alerts.</a>    
    </p>

</div>

