<%inherit file="/base.mako"/>
<%def name="body_id()">messages</%def>
<%def name="page_width()">900px</%def>
<%namespace file="/partials/message_block.mako" import="message_block"/>
<%namespace file="/partials/wish_block.mako" import="wish_block"/>

<div id="wish">
    <blockquote class="bubble tip-left">
        <p>
            ${wish.content}
        </p>
        % if request.user._id != wish.user_id:
            <a href="/wishes/${wish._id}/messages/create-first" class="btn-reply btn-reply-large"
                >reply</a>
        % endif
        <div class="zip-code">
            ${wish.zip_code}
        </div>
    </blockquote>
</div>


% if messages:
<ul id="isotope" class="clearfix">
    % for message in messages:
    <li class="isotope-item">
        <blockquote class="bubble tip-right">
            <p>
                ${message['content']}
            </p>
            % if wish.user_id == request.user._id: 
                <a href="/wishes/${wish._id}/messages/create" class="btn-reply btn-reply-small"
                    >reply</a>
            % endif
        </blockquote>
        <a class="title" href="/users/${message['username']}"
                    style="font-size: 12px">${message['username']}</a>
    </li>

    % endfor
</ul>
% endif
