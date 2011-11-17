<%def name="message_block(content, author, shorten=False, tip='right')">
<% url = request.resource_url%>

    <blockquote class="bubble tip-${tip}">
        <p>
            ${content}
        </p>
    </blockquote>
    <a class="title" href="/users/${author}"
                style="font-size: 12px">${author}</a>

</%def>

