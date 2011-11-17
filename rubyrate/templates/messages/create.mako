<%inherit file="/base.mako"/>
<%def name="body_id()">messages-create</%def>
<%def name="page_width()">900px</%def>
<%namespace file="/partials/wish_block.mako" import="wish_block"/>


${wish_block(wish, reply=False)}


${literal(form)}



   
