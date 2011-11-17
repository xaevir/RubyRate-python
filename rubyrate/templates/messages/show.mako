<%inherit file="/base.mako"/>
<%def name="body_id()">message</%def>
<%def name="page_width()">900px</%def>

    <blockquote id="main-bubble" class="bubble tip-left">
        <p>${message}</p>
        <div class="tip-left-green"></div>
    </blockquote>
   
