<%inherit file="/base.mako"/>
<%def name="body_id()">wishes</%def>
<%def name="page_width()">900px</%def>
<%namespace file="/partials/wish_block.mako" import="wish_block"/>

<ul id="isotope" class="clearfix">

% if not wishes:
    <li>There are no wishes</li>
% else:
    % for wish in wishes:
    <li class="isotope-item">

        <blockquote class="bubble tip-left">
            <p>
                <a href="/wishes/${wish['_id']}/messages">
                    % if len(wish['content']) > 160:
                            ${wish['content'][0:160]} 
                            <span class="more"> ...</span>
                    % else:
                        ${wish['content']}
                    % endif
                </a>
            </p>
            <div class="zip-code">
                ${wish['zip_code']}
            </div>
        </blockquote>


    </li>
    % endfor
% endif
</ul>
