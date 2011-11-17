<%inherit file="/base.mako"/>
<%def name="body_id()">wish</%def>
<%def name="page_width()">900px</%def>


    <blockquote id="main" class="rectangle-speech-border">
        <p>${wish.wish}</p>
    <div id="reply" class="blue">
        <a href="${create_link}" class="button blue">
            <div id="reply-sign"></div>Reply
        </a>
    </div>

    </blockquote>
    
    <div class="clear" style="margin-bottom: 30px;"></div>

<ul id="replies" class="clearfix">
% if replies:
    % for reply in replies:
    <li>
        <blockquote class="rectangle-speech-border light-yellow right-tip">
            <p>
                <b>${reply['company']}</b> <br />
                <% 
                from markdown import markdown
                import re
                brief = reply['message'][0:160]
                brief = markdown(brief)
                %>
                ${literal(brief)} 
            </p>
            <div style="text-align: right; position: relative;">
                <a 
                style="border-radius: 20px;
                       position: absolute;
                       bottom: -25px;
                       right: 0;
                       background: #fff;
                       padding: 5px;
                       font-size: 11px;
                       text-decoration: underline;
                "
                href="${request.resource_url(request.context['replies'], reply['_id'])}">more</a></div>
        </blockquote>
    </li>
    % endfor
% endif
</ul>
