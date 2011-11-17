<%inherit file="/base.mako"/>
<%def name="page_name()">create-account</%def>
<%namespace file="/partials/wish_block.mako" import="wish_block"/>
<%namespace file="/partials/heading_block.mako" import="heading_block"/>

<%def name="heading_caller()">
    ${heading_block(heading)}
</%def>



<div class="col_1">
    ${literal(form)}
</div>


<div class="col_2">
    ${wish_block(wish, reply=False)}
</div>

