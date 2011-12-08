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

import formencode
from formencode import validators
from formencode import htmlfill

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

class UniqueUsername(formencode.FancyValidator):
    def _to_python(self, value, state):
        user = state.by_username(value)
        if user:
            raise formencode.Invalid(
                'That username already exists',
                 value, state)
        return value


class BuyerSchema(formencode.Schema):
    allow_extra_fields = True
    filter_extra_fields = True
    username = formencode.All(validators.PlainText(not_empty=True),
                              validators.MinLength(2),
                              validators.MaxLength(60),
                              UniqueUsername())
    email = validators.Email(resolve_domain=True, not_empty=True)
    password = validators.MinLength(5, not_empty=True)


@view_config(name='activate', context=resources.User, permission='activate')
def activate_buyer(user, request):
    tpl = '/users/activate.mako'
    if hasattr(user, 'username'):
        #already activated
        html = '<h1>Already Activated</h1>'
        tmp = render('writeable.mako', {'html':html}, request)
        return Response(tmp)
    schema = BuyerSchema()
    if request.method == "GET": 
         return Response(render(tpl, {}, request))
    try:
        params = schema.to_python(request.params, user.__parent__)
    except formencode.Invalid, e:
        html = htmlfill.render(render(tpl, {}, request),
                                          defaults=e.value,
                                          errors=e.error_dict)
        return Response(html)
    # passed validation
    for key, value in params.items():
        setattr(user, key, value)
    user.save()
    request.session.flash('Thank you for activating your account.')
     
    wish = models.Wishes().by_user_id(user._id) 
    wish.update_with_username(user) 
    models.Chats().update_with_username(wish._id, user)
    url = '/users/%s/chats'%user.username
    headers = remember(request, user.username)
    return HTTPFound(location = url, headers = headers)


@view_config(name='create', context=resources.Users, renderer='form.mako')
def create_user(context, request):
    heading = 'Kindly Sign Up'
    schema = schemas.User()
    form = Form(schema,
        buttons=(Button(title="Create Account", css_class='btn'),)) 
    if request.method == "GET": 
        return {'form':form.render(), 'heading': heading}
    # validate      
    try:
        controls = request.POST.items()
        # bind unique username
        username = schema['username']
        username.validator = colander.All(colander.Length(min=2, max=50), unique_username)
        captured = form.validate(controls)
    except deform.ValidationFailure, e:
        return {'form':e.render(), 'heading': heading}
    # passed valication
    user = models.User(captured)
    user.insert()
    request.session.flash('Thank you for signing up')
    headers = remember(request, user.username)
    return HTTPFound(location = '/', headers = headers)
    
@view_config(name='create-reply', context=resources.Users, renderer='/users/create_seller.mako')
def create_reply_user(context, request):
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
        url = '/wishes/%s/reply'%request.subpath[0]
    except:
        url = '/wishes' 
    return HTTPFound(location = url, headers = headers)


@view_config(context=resources.MyWishes, renderer='/my_wishes/list.mako', permission='view') 
def list_wishes(context, request):
    cursor = context.get_wishes()
    return dict(wishes = cursor,
                url = request.resource_url)




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

