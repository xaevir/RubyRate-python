from deform.widget import TextInputWidget
from deform.widget import TextAreaWidget
from deform.widget import Widget
from deform.widget import HiddenWidget 

from markdown import markdown
from colander import null

from rubyrate.utility import pretty_date

class Markdown(TextAreaWidget):
    def serialize(self, field, cstruct, readonly=False):
        if cstruct is null:
            cstruct = ''
        if readonly is True:
            cstruct = markdown(cstruct)
            return super(Markdown, self).serialize(field, cstruct, readonly=True)
        return super(Markdown, self).serialize(field, cstruct, readonly=False)


class Link(TextInputWidget):
    def serialize(self, field, cstruct, readonly=False):
        if cstruct is null:
            cstruct = ''
        if readonly is True:
            cstruct = '<a href="http://%s">%s</a>' % (cstruct, cstruct)
            return super(Link, self).serialize(field, cstruct, readonly=True)
        return super(Link, self).serialize(field, cstruct, readonly=False)


class PrettyDate(Widget):
    def serialize(self, field, cstruct, readonly=False):
        if cstruct is null:
            cstruct = ''
        date = pretty_date(cstruct)
        if date is None:
            raise Exception
        return '<td>%s</td>' % date

    def deserialize(self, field, cstruct, readonly=False):
        # TODO should I implement this?
        return cstruct


class LinkFromId(Widget):
    def serialize(self, field, cstruct, readonly=False):
        if cstruct is null:
            cstruct = ''
        request = get_current_request()
        url = resource_path(request.context, cstruct[0])
        return '<td><a href="%s">%s</a></td>' % (url, cstruct[1])

    def deserialize(self, field, cstruct, readonly=False):
        # TODO should I implement this?
        return cstruct


class PassThru(Widget):
    def serialize(self, field, cstruct, readonly=False):
        return cstruct
    def deserialize(self, field, cstruct, readonly=False):
        if cstruct is null:
            cstruct = ''
        return cstruct

class NoShowWidget(HiddenWidget):
    def serialize(self, field, cstruct=None, readonly=False):
        return ''
    def deserialize(self, field, cstruct, readonly=False):
        return cstruct

class thWidget(Widget):
    def serialize(self, field, cstruct, readonly=True):
        if cstruct is colander.null:
            cstruct = u''
        html = '<tr>'
        for item in cstruct:
            html += '<th>%s</th>' % item 
        return html + '</tr>' 

class Blockquote(Widget):
    def serialize(self, field, cstruct, readonly=True):
        if cstruct is colander.null:
            cstruct = u''
        html = '<blockquote class="rectangle-speech-border">%s' % cstruct
        return html + '</blockquote>'
