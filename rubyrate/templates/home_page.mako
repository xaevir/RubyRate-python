<%inherit file="/base.mako"/>
<%def name="page_name()">home</%def>
<%def name="js()">
    <script type="text/javascript" src="${request.static_url('rubyrate:static/jquery-1.6.2.min.js')}"></script>
    <script type="text/javascript" src="${request.static_url('rubyrate:static/main.js')}"></script>
</%def>


<div id="chunk_1" class="clearfix">
    <div class="gray-to-white"></div>
    <div class="content">
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
    </div>

</div>



<%doc>
The following is an example of quote for water saving dual flush toilets:


Mixing a container. Want to save on shipping costs mix a container
with either other goods you interested in ie, Kitchen cabinets and pex
tubing.
</%doc>
