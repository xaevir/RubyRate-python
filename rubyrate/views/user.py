from pyramid.view import view_config
from pyramid.url import resource_url
from pyramid.renderers import get_renderer
from pyramid.renderers import render
from pyramid.httpexceptions import HTTPFound
from pyramid.response import Response
from pyramid.traversal import resource_path
from pyramid.security import remember
from pyramid.security import forget

from pyramid_mailer import get_mailer
from pyramid_mailer.message import Message

from colander import MappingSchema
from colander import Mapping
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
from colander import All
from colander import deferred

from deform import ValidationFailure
from deform import widget
from deform.widget import PasswordWidget

from rubyrate.my_deform.form import Button
from rubyrate.my_deform.form import Form

from rubyrate.resources import Root
from rubyrate.resources import Users
from rubyrate.resources import User

import logging
from pprint import pprint
log = logging.getLogger(__name__)


@view_config(name='create', context=Users, renderer='/user/create.mako')
def create_user(context, request):
    myform = Form(CreateUser(),
        buttons=(Button(title="Create Account", css_class='blue'),)) 

    if request.method == "GET": 
        return {'form':myform.render()}
      
    if request.method == "POST": 
        try:
            user_details = myform.validate(request.POST.items())
            User.insert(user_details)
            request.session.flash('Thank you for signing up')
            headers = remember(request, user_details['username'])
            return HTTPFound(location = request.path_url, headers = headers)

        except ValidationFailure, e:
            return {'form':e.render()}


@view_config(name='', context=User, permission='view')
def view_user(user, request):
    return Response('You are viewing the user' + user.username) 

@view_config(name='edit', context=User, permission='edit')
def edit_user(user, request):
    return Response('This page is secret' + user.username) 


#_____________________________________________________________________Login___

@deferred
def deferred_came_from_default(node, kw):
   came_from = kw.get('came_from')
   return came_from

class LoginSchema(MappingSchema):
    username = SchemaNode(
        String())
    password = SchemaNode(
        String(), 
        widget = widget.PasswordWidget())
    came_from = SchemaNode(
        String(),
        widget = widget.HiddenWidget(), 
        default = deferred_came_from_default)

def matching_username_password(node, value):
    from rubyrate import models
    doc = models.User.by_username(value['username'])
    if doc and models.User.check_password(value['password'], doc['password']):
        return True
    raise Invalid(node, 'Please check your username or password')


@view_config(name='login', context=Users, renderer="form.mako")
@view_config(context='pyramid.exceptions.Forbidden', renderer="form.mako")
def login(context, request):
    # context prior to forbidden being throw is in request.context
    login_url = request.application_url+'/users/login'
    referrer = request.url
    if referrer == login_url:
        referrer = '/' # never use the login form itself as came_from
    came_from = request.params.get('came_from', referrer)
    schema = LoginSchema(validator = matching_username_password).bind(
        came_from = came_from)
    myform = Form(schema, buttons=('login',), css_class="deform medium-form")
    if request.method == "GET": 
        return {'form':myform.render()}
    controls = request.POST.items()
    try:
        appstruct = myform.validate(controls)
        headers = remember(request, appstruct['username'])
        return HTTPFound(location = came_from, headers = headers)
    except ValidationFailure, e:
        return {'form':e.render()}


@view_config(name='logout', context=Root)
def logout(context, request):
    headers = forget(request)
    return HTTPFound(location = request.application_url, headers = headers)
