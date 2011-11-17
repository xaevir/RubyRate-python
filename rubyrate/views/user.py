from pyramid.view import view_config
from pyramid.url import resource_url
from pyramid.renderers import render
from pyramid.httpexceptions import HTTPFound
from pyramid.security import remember
from pyramid.security import forget

from pyramid.renderers import render
from pyramid.response import Response


from pyramid_mailer import get_mailer
from pyramid_mailer.message import Message

from rubyrate.my_deform.form import Button
from rubyrate.my_deform.form import Form

import colander
import deform


from pymongo.objectid import ObjectId

from rubyrate import resources
from rubyrate import models 
from rubyrate import schemas 

import logging
from pprint import pprint
log = logging.getLogger(__name__)

from mako.template import Template

def unique_username(node, value):
    users = models.Users()
    user = users.by_username(value)
    if user:
        raise colander.Invalid(node, 'That username already exists')

@view_config(name='activate', context=resources.User, renderer='form.mako')
def activate_buyer(user, request):
    if hasattr(user, 'username'):
        #already activated
        html = '<h1>Already Activated</h1>'
        tmp = render('writeable.mako', {'html':html}, request)
        return Response(tmp)
    heading = 'Please activate your account, so you can respond to your messages'
    schema = schemas.Buyer()
    if hasattr(user, 'email'):
        del schema['email']
    form = Form(schema, buttons=(Button(title="Activate Account", css_class='btn'),)) 
    if request.method == "GET": 
        return {'form':form.render(),
                'heading': heading}
    try:
        controls = request.POST.items()
        # add unique username validation
        username = schema['username']
        username.validator = colander.All(colander.Length(min=2, max=50), unique_username)
        captured = form.validate(controls)
    except deform.ValidationFailure, e:
        return {'form':e.render(),
                'heading': heading}
    # passed validation
    for key, value in captured.items():
        setattr(user, key, value)
    user.save()
    request.session.flash('Thank you for activating your account.')
    wish = models.Wishes().by_user_id(user._id)
    url = '/wishes/%s/messages'%wish._id
    headers = remember(request, user.username)
    return HTTPFound(location = url, headers = headers)


@view_config(name='create-buyer', context=resources.Users, renderer='form.mako')
def create_buyer(context, request):
    schema = schemas.Buyer()
    form = Form(schema,
        buttons=(Button(title="Create Account", css_class='btn'),)) 
    if request.method == "GET": 
        return {'form':form.render()}
    # validate      
    try:
        controls = request.POST.items()
        # bind unique username
        username = schema['username']
        username.validator = colander.All(colander.Length(min=2, max=50), unique_username)
        captured = form.validate(controls)
    except deform.ValidationFailure, e:
        return {'form':e.render()}
    # passed valication
    user = models.User(captured)
    user.insert()
    request.session.flash('Thank you for signing up')
    headers = remember(request, user.username)
    return HTTPFound(location = '/', headers = headers)
    
@view_config(name='create-seller', context=resources.Users, renderer='/users/create_seller.mako')
def create_seller(context, request):
    heading = 'Please create an account so that you can reply to this wish'
    wish = models.Wishes().by_id(request.subpath[0])
    schema = schemas.Seller()
    form = Form(schema,
        buttons=(Button(title="Create Account", css_class='btn'),)) 
    if request.method == "GET": 
        return {'form':form.render(),
                'heading': heading,
                'wish': wish}
    # validate      
    try:
        controls = request.POST.items()
        # bind unique username
        username = schema['username']
        username.validator = colander.All(colander.Length(min=2, max=50), unique_username)
        captured = form.validate(controls)
    except deform.ValidationFailure, e:
        return {'form':e.render(),
                'heading': heading,
                'wish': wish}
    # passed valication
    user = models.User(captured)
    user.insert()
    request.session.flash('Thank you for signing up')
    headers = remember(request, user.username)
    try:
        url = '/wishes/%s/messages/create'%request.subpath[0]
    except:
        url = '/wishes' 
    return HTTPFound(location = url, headers = headers)



@view_config(name='', context=resources.User, permission='view')
def view_user(user, request):
    return Response('You are viewing the user' + user.username) 

@view_config(name='edit', context=resources.User, permission='edit')
def edit_user(user, request):
    return Response('This page is secret' + user.username) 


def match_user_password(node, value):
    user = models.Users().by_username(value['username'])
    if user and user.check_password(value['password']):
        return True
    raise colander.Invalid(node, 'Please check your username or password')

@view_config(name='login', context=resources.Users, renderer="form.mako")
@view_config(context='pyramid.exceptions.Forbidden', renderer="form.mako")
def login(context, request):
    # context prior to forbidden being throw is in request.context
    login_url = request.application_url+'/users/login'
    referrer = request.url
    if referrer == login_url:
        referrer = '/' # never use the login form itself as came_from
    came_from = request.params.get('came_from', referrer)
    schema = schemas.Login(
        validator = match_user_password).bind(came_from = came_from)
    form = Form(schema, buttons=(
        Button(title='Login', css_class='btn'),))
    heading = 'Kindly, sign in'            
    if request.method == "GET": 
        return {'form':form.render(),
                'heading': heading}
    # validate        
    try:
        controls = request.POST.items()
        captured = form.validate(controls)
    except deform.ValidationFailure, e:
        return {'form': e.render(), 
                'heading': heading}
    # passed validation
    headers = remember(request, captured['username'])
    request.session.flash('Welcome.')
    ## redirect
    return HTTPFound(location = came_from, headers = headers)


@view_config(name='logout', context=resources.Root)
def logout(context, request):
    headers = forget(request)
    return HTTPFound(location = request.application_url, headers = headers)

