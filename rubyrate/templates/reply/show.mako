<%inherit file="/base.mako"/>
<%def name="body_id()">reply</%def>


    <blockquote class="rectangle-speech-border">
        <p>${wish.wish}</p>
    </blockquote>
    <div class="button-wrap blue">
        <a href="${create_link}" class="button">Reply</a>
    </div>



