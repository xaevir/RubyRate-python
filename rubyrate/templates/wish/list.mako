<%inherit file="/base.mako"/>
<%def name="body_id()"></%def>
<%def name="page_width()">900px</%def>

<ul id="wishes" class="clearfix">
% if wishes:
    % for wish in wishes:
    <li style="position: relative" class="wish">
        <blockquote class="rectangle-speech-border">
            <p>
                <a href="/wishes/${wish['_id']}">${wish['wish']}</a>
            </p>
            <b class="a1"></b>
            <b class="a2"></b>
            <b class="a3"></b>
            <b class="a4"></b>
        </blockquote>
            <span style="position: absolute; 
                        right: 30px;
                        bottom: 50px;
                        color: #666;
                        ">
                        zip: ${wish['zip_code']}
            </span>
    </li>
    % endfor
% else:
  <li>There are no open wishes</li>
% endif
</ul>
