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
from deform.widget import TextInputWidget
from deform.widget import TextAreaWidget
from deform.widget import Widget
from deform.widget import RadioChoiceWidget

from rubyrate.my_deform.form import Button
from rubyrate.my_deform.form import Form
from pkg_resources import resource_filename
from deform import ZPTRendererFactory


from rubyrate.resources import Root
from rubyrate.resources import Items
from rubyrate.resources import Item
from rubyrate.resources import Users
from rubyrate.resources import User
from rubyrate.resources import Admin


import smtplib

from mako.template import Template

class ItemSchema(MappingSchema):
    email = SchemaNode(
        String(),
        validator = Email())
    product = SchemaNode(
        String(),
        widget= TextAreaWidget())
    quantity = SchemaNode(String())
    by_when = SchemaNode(
        String(),
        title="When would you like to buy this product/service")
    zip_code = SchemaNode(String())
    price_range = SchemaNode(
        String(),
        missing = '',
        title= 'Price Range (optional)')
    choices = (('yes', 'Yes'), )                      
    international = SchemaNode(
        String(),
        missing='',
        validator = OneOf([x[0] for x in choices]),
        widget = RadioChoiceWidget(values=choices, css_class='reg-position'),
        title = 'Would you like pricing from international suppliers?')
        

@view_config(name="", context=Root, renderer='home_page.mako')
def create_item_on_home_page(context, request):
    schema = ItemSchema()
    form = Form(schema, 
        buttons=(Button(title='Get Pricing',css_class='button blue'),), 
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


@view_config(context=Items, renderer='/item/list.mako')
def list_items(items, request):
    items = items.get_recent() 
    return {'items': items}

@view_config(context=Item, renderer='/item/view.mako')
def view_item(item, request):
    #something going on with how python stores the vars in this func
    form = Form(ItemSchema())
    node = form.children.pop(0)
    if node.name != 'email':
        raise Exception
    readonly = form.render(item.__dict__, readonly=True)
    return {'form': readonly}

@view_config(name='edit', context=Item, renderer='form.mako')
def edit_item(item, request):
    schema = ItemSchema()
    form = Form(schema, 
        buttons=(Button(title='Update'),),)
    if request.method == "GET": 
        return {'form':form.render(item.__dict__)}
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


@view_config(name='', context=Admin, renderer='/admin/home.mako', 
    permission='view')
def item_admin(admin, request):
    items = admin.get_items()
    return {'items': items}

