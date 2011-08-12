from pyramid.view import view_config
from pyramid.response import Response
from pyramid.renderers import render

from pyramid_mailer import get_mailer
from pyramid_mailer.message import Message
from pyramid.url import resource_url
from pyramid.httpexceptions import HTTPFound

import transaction

from colander import MappingSchema
from colander import SequenceSchema
from colander import SchemaNode
from colander import String
from colander import Boolean
from colander import Integer
from colander import Length
from colander import OneOf
from colander import Email
from colander import Function
from colander import Invalid
from colander import null

from deform import ValidationFailure
from deform import Form
from deform.widget import TextInputWidget
from deform.widget import TextAreaWidget
from deform.widget import Widget

import smtplib

from rubyrate.resources import Root

class CheckPlaceholder(TextAreaWidget):
    def serialize(self, field, cstruct, readonly=False):
        if cstruct is null:
            cstruct = field.widget.placeholder
            field.widget.css_class = 'ui-placeholder' 
        # sets the css_class above if I dont write this if statement
        # maybe its in deform template.py there is a cache 
        if cstruct != field.widget.placeholder:
            field.widget.css_class = '' 
        template = readonly and self.readonly_template or self.template
        return field.renderer(template, field=field, cstruct=cstruct)

    def deserialize(self, field, pstruct):
        if pstruct is null or pstruct == field.widget.placeholder:
            return null
        if self.strip:
            pstruct = pstruct.strip()
        if not pstruct:
            return null
        return pstruct


class QuoteSchema(MappingSchema):
    email = SchemaNode(
        String(),
        validator = Email())

    product = SchemaNode(
        String(),
        widget = CheckPlaceholder(placeholder='example: \r\nkitchen sink with dimensions'),
        )

    quantity = SchemaNode(
        String(),
        widget = TextInputWidget())


@view_config(name="", context=Root, renderer='home_page.mako')
def home_page(context, request):
    schema = QuoteSchema()
    settings = request.registry.settings
    myform = Form(schema, buttons=('get quote',), renderer=settings['deform.renderer'])
    if request.method == "GET": 
        return {'form':myform.render()}
    controls = request.POST.items()
    try:
        appstruct = myform.validate(controls)
        # email the controls
        readonly_form = myform.render(appstruct, readonly=True)
        email = Message(subject='Quote page',
                        sender='RubyRate_QuotePage@rubyrate.com',
                        recipients=['bobby.chambers33@gmail.com'],
                        html=readonly_form)
        mailer = get_mailer(request)
        mailer.send(email)
        transaction.commit()
        request.session.flash('Thank you!')
        return HTTPFound(location = request.path_url)             
    except ValidationFailure, e:
        return {'form':e.render()}
#____________________________________________________________________Contact__

class ContactSchema(MappingSchema):
    name    = SchemaNode(String(),
                         validator = Length(min=2, max=200))
    email   = SchemaNode(String(),
                         validator = Email())
    message = SchemaNode(String(),
                         validator = Length(max=2000),
                         widget=TextAreaWidget())


@view_config(name='contact', context=Root, renderer="contact.mako")
def contact(context, request):
    schema = ContactSchema()
    myform = Form(schema, buttons=('submit',))
    if request.method == "GET": 
        return {'form':myform.render()}
    controls = request.POST.items()
    try:
        appstruct = myform.validate(controls)
        # email the controls
        readonly_form = myform.render(appstruct, readonly=True)
        email = Message(subject='Contact page',
                        sender='RubyRate_ContactPage@rubyrate.com',
                        recipients=['bobby.chambers33@gmail.com'],
                        html=readonly_form)
        mailer = get_mailer(request)
        mailer.send(email)
        transaction.commit()
        request.session.flash('Thank you!')
        return HTTPFound(location = request.path_url)             
    except ValidationFailure, e:
        return {'form':e.render()}

