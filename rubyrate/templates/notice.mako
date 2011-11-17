<%inherit file="/base.mako"/>
<%namespace file="/partials/heading_block.mako" import="heading_block"/>

<%def name="body_id()">${page or 'general'}</%def>

<div id="notice">
    <h1>${notice}</h1>
</div>



