<%inherit file="/base.mako"/>
<%def name="page_name()">summary</%def>
<% from rubyrate.utility import pretty_date %>

<div id="letter" class="clearfix">
    ${literal(conclusion)}
</div>


<div id="bizcard" class="clearfix">
    ${literal(answers)}
</div>
    
