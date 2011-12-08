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

        <a href="/wishes/${wish['_id']}">
            <blockquote class="bubble tip-left">
                <p>
                        % if len(wish['content']) > 160:
                                ${wish['content'][0:160]} 
                                <span class="more"> ...</span>
                        % else:
                            ${wish['content']}
                        % endif
                </p>
                <div class="zip-code">
                    ${wish['zip_code']}
                </div>
            </blockquote>
        </a>

    </li>
    % endfor
% endif
</ul>
