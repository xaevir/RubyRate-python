from pyramid.view import view_config
from pyramid.response import Response
from pyramid.renderers import render

from pyramid_mailer import get_mailer
from pyramid_mailer.message import Message
from pyramid.url import resource_url
from pyramid.httpexceptions import HTTPFound

import transaction

import formencode
from formencode.schema import Schema
from formencode.validators import String, PlainText, MaxLength, MinLength, Email
from formencode.validators import Invalid, FancyValidator 
from formencode import htmlfill


import smtplib

from rubyrate.resources import Root

@view_config(name="", context=Root, renderer='home_page.mako')
def home_page(context, request):
    return {} 


class Quote(Schema):
    allow_extra_fields = True
    filter_extra_fields = True
    name = formencode.All(String(not_empty=True),
                              MaxLength(200),
                              MinLength(2))
    email = formencode.All(Email(not_empty=True),
                              MaxLength(200))
    product              = String()
    specs                = String()
    quantity             = String()
    lead_time            = String()
    shipping_destination = String()
    payment_terms        = String()


@view_config(name="quote", context=Root)
def quote(context, request):
    tpl = 'quote.mako'
    tpl_vars = {'save_url': request.path_url}
    if request.method == "GET": 
        html =  render(tpl, tpl_vars, request)
        return Response(html)
    schema = Quote() 
    try:
        params = schema.to_python(request.params, request)
        # get the email's body
        quote_email_tpl = render('/email/quote.mako', params)
        message = Message(subject='Quote page',
                          sender='RubyRate_QuotePage@rubyrate.com',
                          recipients=['bobby.chambers33@gmail.com'],
                          html=quote_email_tpl)
        mailer = get_mailer(request)
        mailer.send(message)
        transaction.commit()
        request.session.flash('Thank you!')
        this_page =  resource_url(context, request, 'quote')
        return HTTPFound(location = this_page)                           
    except formencode.Invalid, e:
        html =  render(tpl, tpl_vars, request)
        html = htmlfill.render(html, defaults=e.value, errors=e.error_dict)
        return Response(html)


#____________________________________________________________________Contact__


class ContactForm(formencode.Schema):
    allow_extra_fields = True
    filter_extra_fields = True
    name = formencode.All(String(not_empty=True),
                              MaxLength(200),
                              MinLength(2))
    email = formencode.All(Email(not_empty=True),
                              MaxLength(200))
    message = formencode.All(String(not_empty=True),
                              MaxLength(3000))

@view_config(name='contact', context=Root)
def contact(context, request):
    tpl = 'contact.mako'
    tpl_vars = {'save_url': request.path_url}
    if request.method == "GET": 
        html =  render(tpl, tpl_vars, request)
        return Response(html)
    schema = ContactForm() 
    try:
        params = schema.to_python(request.params, request)
        # get the email's body
        contact_email_tpl = render('/email/contact.mako', params)
        message = Message(subject='Contact page',
                          sender='RubyRate_ContactPage@rubyrate.com',
                          recipients=['bobby.chambers33@gmail.com'],
                          html=contact_email_tpl)
        mailer = get_mailer(request)
        mailer.send(message)
        transaction.commit()
        request.session.flash('Thank you!')
        this_page =  resource_url(context, request, 'contact')
        return HTTPFound(location = this_page)                           
    except formencode.Invalid, e:
        html =  render(tpl, tpl_vars, request)
        html = htmlfill.render(html, defaults=e.value, errors=e.error_dict)
        return Response(html)


