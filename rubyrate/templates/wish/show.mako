<%inherit file="/base.mako"/>
<%def name="body_id()">wish</%def>
<%def name="page_width()">900px</%def>

    <blockquote id="main-bubble" class="bubble tip-left">
        <p>${wish.wish}</p>

        <span id="reply">
            <a href="${create_link}" class="btn">
                <div id="reply-sign"></div>Reply
            </a>

        </span>
        <div class="tip-left-green"></div>
    </blockquote>
   
    <div class="clear" style="margin-bottom: 30px;"></div>

<ul id="replies" class="clearfix">
% if replies:
    % for reply in replies:
    <li class="reply clearfix">
        <div class="title">
            <a href="${request.resource_url(request.context['replies'], reply['_id'])}"
                    style="font-size: 12px">${reply['company']}</a>
        </div>
        <blockquote class="bubble tip-right ">
            <p>
                % if len(reply['message']) > 160:
                    ${reply['message'][0:160]} 
                    <a href="${request.resource_url(request.context['replies'], reply['_id'])}"
                        style="font-size: 10px">...more</a>
                % else:
                    ${reply['message']}
                % endif
            </p>
            <a href="${create_link}" class="create-message">
                reply
            </a>
        </blockquote>

    </li>
    % endfor
% endif
</ul>
