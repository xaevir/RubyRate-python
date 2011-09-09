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
from deform.widget import RadioChoiceWidget

from rubyrate.form.form import Button

import smtplib

from rubyrate.resources import Root

class QuoteSchema(MappingSchema):
    email = SchemaNode(
        String(),
        validator = Email())
    product = SchemaNode(String())
    quantity = SchemaNode(String())

@view_config(name="", context=Root, renderer='home_page.mako')
def home_page(context, request):
    schema = QuoteSchema()
    myform = Form(schema, 
                  buttons=(Button('get quote',css_class='button blue center'),), 
                  renderer=request.registry.settings['deform.renderer'])
    if request.method == "GET": 
        return {'form':myform.render()}
    controls = request.POST.items()
    try:
        appstruct = myform.validate(controls)
        # email the controls
        readonly_form = myform.render(appstruct, readonly=True)
        email = Message(subject='Home Page',
                        sender='HomePage@rubyrate.com',
                        recipients=[request.registry.settings['email_forms_send_to']],
                        html=readonly_form)
        mailer = get_mailer(request)
        mailer.send(email)
        transaction.commit()

        thank_you = render('mini/thankyou_homepage.mako', request)    
        request.session.flash(thank_you)
        return HTTPFound(location = request.path_url)             
    except ValidationFailure, e:
        return {'form':e.render()}


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
    myform = Form(schema, buttons=('send',))
    if request.method == "GET": 
        return {'form':myform.render()}
    controls = request.POST.items()
    try:
        appstruct = myform.validate(controls)
        # email the controls
        readonly_form = myform.render(appstruct, readonly=True)
        email = Message(subject='Contact page',
                        sender='ContactPage@rubyrate.com',
                        recipients=[request.registry.settings['email_forms_send_to']],
                        html=readonly_form)
        mailer = get_mailer(request)
        mailer.send(email)
        transaction.commit()
        request.session.flash('Thank you!')
        return HTTPFound(location = request.path_url)             
    except ValidationFailure, e:
        return {'form':e.render()}



class PriceAlertSchema(MappingSchema):
    name               = SchemaNode(String(),
                             validator = Length(min=2, max=200))
    email              = SchemaNode(String(),
                             validator = Email())
    zip                = SchemaNode(Integer())

    specified_products = SchemaNode(String(),
                             validator = Length(max=1000),
                             widget=TextAreaWidget())

    choices            = (('new', 'New'), ('used', 'Used'))                      
    condition          = SchemaNode(String(),
                            widget = RadioChoiceWidget(values=choices),
                            validator = OneOf([x[0] for x in choices]))
    how_long           = SchemaNode(String(),
                            title = 'How long would you like to recieve alerts for this product?')


@view_config(name='price-alert', context=Root, renderer="price_alert.mako")
def price_alert(context, request):
    schema = PriceAlertSchema()
    myform = Form(schema, buttons=('send',))
    if request.method == "GET": 
        return {'form':myform.render()}
    controls = request.POST.items()
    try:
        appstruct = myform.validate(controls)
        # email the controls
        readonly_form = myform.render(appstruct, readonly=True)
        email = Message(subject='Price Alert Page',
                        sender='PriceAlertPage@rubyrate.com',
                        recipients=[request.registry.settings['email_forms_send_to']],
                        html=readonly_form)
        mailer = get_mailer(request)
        mailer.send(email)
        transaction.commit()
        request.session.flash('Thank you!')
        return HTTPFound(location = request.path_url)             
    except ValidationFailure, e:
        return {'form':e.render()}


class SupplierSchema(MappingSchema):
    company_name = SchemaNode(String())
    phone_number = SchemaNode(String())
    locations = SchemaNode(String())
    products_you_sell = SchemaNode(String())
    area_you_serve = SchemaNode(String())
    email = SchemaNode(
        String(),
        validator = Email())


@view_config(name='supplier', context=Root, renderer="supplier.mako")
def supplier(context, request):
    schema = SupplierSchema()
    myform = Form(schema, buttons=('send',))
    if request.method == "GET": 
        return {'form':myform.render()}
    controls = request.POST.items()
    try:
        appstruct = myform.validate(controls)
        # email the controls
        readonly_form = myform.render(appstruct, readonly=True)
        email = Message(subject='Supplier Page',
                        sender='SupplierPage@rubyrate.com',
                        recipients=[request.registry.settings['email_forms_send_to']],
                        html=readonly_form)
        mailer = get_mailer(request)
        mailer.send(email)
        transaction.commit()
        request.session.flash('Thank you!')
        return HTTPFound(location = request.path_url)             
    except ValidationFailure, e:
        return {'form':e.render()}

