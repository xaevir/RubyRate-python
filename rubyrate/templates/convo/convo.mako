<%inherit file="/base.mako"/>
<%def name="body_id()">convo</%def>
<%namespace file="/partials/wish_block.mako" import="wish_block"/>

<ul id="convo-messages"> 
    <li>
        <blockquote class="bubble tip-left">
            <p>
                ${wish.content}
            </p>
            <div class="zip-code">
                ${wish.zip_code}
            </div>
        </blockquote>
    </li>

</ul>

    <div id="convo-bottom">
            ${literal(form)}
    </div>




