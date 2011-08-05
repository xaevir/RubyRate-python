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

from deform import ValidationFailure
from deform import Form
from deform import widget

import smtplib

from rubyrate.resources import Root

@view_config(name="", context=Root, renderer='home_page.mako')
def home_page(context, request):
    return {} 


class QuoteSchema(MappingSchema):
    name                 = SchemaNode(String(),
                                      validator = Length(min=2, max=200))
    email                = SchemaNode(String(),
                                      validator = Email())
    product              = SchemaNode(String(), missing='')
    specs                = SchemaNode(String(), missing='')
    quantity             = SchemaNode(String(), missing='')
    lead_time            = SchemaNode(String(), missing='')
    shipping_destination = SchemaNode(String(), missing='')
    payment_terms        = SchemaNode(String(), missing='')

@view_config(name="quote", context=Root, renderer="quote.mako")
def quote(context, request):
    schema = QuoteSchema()
    myform = Form(schema, buttons=('submit',))
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
                         widget=widget.TextAreaWidget())


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

