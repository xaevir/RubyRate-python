<%inherit file="/base.mako"/>
<%def name="page_segment()">wishes</%def>
<%def name="scripts()">
    <script src="/static/js/libs/LABjs/LAB.js"></script>
    <script>
       $LAB
       .script("/static/js/libs/jquery/jquery.js")
       .script("/static/js/libs/underscore/underscore.js").wait()
       .script("/static/js/libs/backbone/backbone.js")
       .script("/static/js/libs/jquery-validation/jquery.validate.js")
       .script("/static/js/libs/raphael-min.js").wait()
       .script("/static/js/libs/isotope.min.js")
       .wait(function(){
          myplugin.init();
          framework.init();
          framework.doSomething();
       });

    </script>
</%def>




<%namespace file="/partials/wish_block.mako" import="wish_block"/>


<%text>
    <script type="text/template" id="wish-item">
        <blockquote class="bubble tip-right">
            <p>
                <%= content %>     
            </p>
        </blockquote>
    </script>

</%text>

<%doc>
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
</%doc>

</ul>


