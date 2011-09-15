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

from rubyrate.resources import Items
from rubyrate.resources import Item
from rubyrate.resources import Root

import smtplib


class QuoteSchema(MappingSchema):
    email = SchemaNode(
        String(),
        validator = Email())
    product = SchemaNode(String())
    quantity = SchemaNode(String())
    lead_time = SchemaNode(String())
    area_code = SchemaNode(String())
    price_range = SchemaNode(
        String(),
        missing = '',
        title= 'Price Range (optional)')
    choices = (('yes', 'Yes'), ('no', 'No'))                      
    international = SchemaNode(
        String(),
        validator = OneOf([x[0] for x in choices]),
        widget = RadioChoiceWidget(values=choices, css_class='reg-position'),
        title = 'Would you like pricing from international suppliers?')
        

@view_config(name="", context=Root, renderer='home_page.mako')
def home_page(context, request):
    schema = QuoteSchema()
    form = Form(schema, 
        buttons=(Button(title='Get Pricing',css_class='button blue'),), 
        renderer=request.registry.settings['deform.renderer'],
        formid='product_needed_form')
    if request.method == "GET": 
        return {'form':form.render()}
    try:
        pricing_data = form.validate(request.POST.items())
        item = Item(pricing_data)
        item.save()
        # email notification
        settings = request.registry.settings
        email = Message(subject='Pricing Needed',
            sender=settings['to'],
            recipients=[settings['to']],
            body=' ')
        mailer = get_mailer(request)
        mailer.send(email)
        transaction.commit()

        # show message
        thank_you = render('mini/thankyou_homepage.mako', request)    
        request.session.flash(thank_you)
        return HTTPFound(location = request.path_url)             
    except ValidationFailure, e:
        return {'form':e.render()}

@view_config(name='', context=Items, renderer='need_pricing.mako')
def need_pricing(items, request):
    items = items.get_recent() 
    return {'items': items}
    

class ContactSchema(MappingSchema):
    name = SchemaNode(String(),
        validator = Length(min=2, max=200))
    email = SchemaNode(String(),
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
        settings = request.registry.settings
        email = Message(subject='Contact page',
                        sender=settings['from'],
                        recipients=[settings['to']],
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
                        recipients=[request.registry.settings['to']],
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
                        sender='ruby_robot@rubyrate.com',
                        recipients=[request.registry.settings['email_forms_send_to']],
                        html=readonly_form)
        mailer = get_mailer(request)
        mailer.send(email)
        transaction.commit()
        request.session.flash('Thank you!')
        return HTTPFound(location = request.path_url)             
    except ValidationFailure, e:
        return {'form':e.render()}

