<%inherit file="/base.mako"/>
<%def name="body_id()">wish</%def>
<%def name="page_width()">900px</%def>
<%namespace file="/partials/wish_block.mako" import="wish_block"/>

${wish_block(wish)}

