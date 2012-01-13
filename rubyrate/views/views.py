from pyramid.view import view_config
from pyramid.response import Response
from pyramid.renderers import render
from pyramid.traversal import resource_path

import pyramid_mailer
from pyramid.url import resource_url
from pyramid.httpexceptions import HTTPFound

import transaction

from pymongo.objectid import ObjectId

import colander
import deform

from rubyrate.my_deform.form import Button
from rubyrate.my_deform.form import Form
from pkg_resources import resource_filename
from deform import ZPTRendererFactory

from pprint import pprint
p = pprint


import formencode
from formencode import validators

from rubyrate import resources
from rubyrate import models 
from rubyrate import schemas 

from rubyrate.utility import allowed_methods
from rubyrate.utility import render_form
from rubyrate.utility import id_generator

import urllib
import urllib2

import json

from pyramid.security import remember
from pyramid.security import forget


@view_config(name='create-reply.html', context=resources.Forms, renderer='string', http_cache=0 , permission='public')
def create_reply_form(context, request):    
    schema = schemas.Reply()
    form = Form(schema, css_class='reply-form form-stacked', buttons=(Button(title='Reply', css_class='btn'),))
    return form.render() 



@view_config(name='create-wish.html', context=resources.Forms, renderer='string', http_cache=0 , permission='public')
def create_wish_form(context, request):    
    schema = schemas.Wish()
    if request.user and hasattr(request.user, 'groups'):
        if 'admin' in request.user.groups:
            schema['email'].missing=''
    if request.user: 
        del schema['email']
        if hasattr(request.user, 'zip_code'):
            schema['zip_code'].default= request.user.zip_code
    form = Form(schema, formid="bobby", buttons=(Button(title='Make Wish', css_class='btn large primary'),))
    if context.__name__ ==  'forms':    
        return form.render() 
    return form 


@view_config(context=resources.Messages, xhr=True, renderer='json', 
             request_method='POST', permission='public',  )#request_param='label'
def wishes_(context, request):
    form = create_wish_form(context, request)
    try:
        controls = request.json_body.items()
        captured = form.validate(controls)
    except deform.ValidationFailure, e:
        return {'form': e.render()}
    # passed validation
    user = request.user
    if user:
        captured['author'] = {'name': user.username, '_id': user._id}

    label = captured.pop('labels')
    message = models.Message(captured)
    message.labels = ['wish'] 
    message.insert()
    return {'success': True} 


@view_config(context=resources.Messages, renderer='app_container.mako', permission='public' ) 
def list_wishes(context, request):
    cursor = context.get_wishes()
    arr = []
    for wish in cursor: 
        for key, value in wish.items():
            if not isinstance(value, str):
                wish[key] = str(value)
        arr.append(wish)
    return dict(load_module = 'wishes', 
                json_data = json.dumps(arr),
                page_name = 'Wishes',
                tagline = 'by area code')



@view_config(context=resources.App, http_cache=0 )
def app(context, request):
    return Response('this is the app homepage') 
    #nav = {'action': 'reply', 'title': 'Create Chat'}
    #return dict(js_module = 'nav', 
    #            json_data = json.dumps(nav),
    #            )


@view_config(name='login', context=resources.Root, xhr=True, renderer='json', 
             request_method='POST')
def login(context, request):
    #{"status":"okay","email":"bobby.chambers33@gmail.com","audience":"localhost","expires":1324075564937,"issuer":"browserid.org"}
    assertion = request.POST['assertion']
    args = {'assertion': assertion,
            'audience': 'localhost'}
    encoded_args = urllib.urlencode(args)
    url = 'https://browserid.org/verify'
    response = urllib2.urlopen(url, encoded_args)
    response = json.loads(response.read())
    if response['status'] == 'okay':
        headers = remember(request, response['email'])
        tup = headers[1]
        cookie = tup[1] 
        return {'cookie':cookie, 'email': response['email'] }
    else: 
        return None

@view_config(name='whoami', context=resources.Root, xhr=True, renderer='json', 
             request_method='GET')
def whoami(context, request):
    if request.user:
        return {'email': request.user.email}
    return None 

@view_config(name="scraper", context=resources.Root, renderer='write.mako')
def scraper(context, request):
    from BeautifulSoup import BeautifulSoup
    html = open("/home/bobby/Desktop/scraper.html", "r").read()
    soup = BeautifulSoup(html)
    chiros = soup.findAll('div', {'class' : "contact vcard"})
    raise Exception
    for chiro in chiros:
        #name = chiro.div.h2.a.string    
        address = chiro.find('div', {'class': 'bizAddr'})
        print address
        #address = address.findAll(text=True) 
        #address = ''.join(address)       
        #print name, address


@view_config(renderer='home_page.mako', http_cache=0)
def visitor_home(context, request):
    form  = create_wish_form(context, request)
    if request.method == 'GET': 
        html = form.render()
        return {'form': html}
    # validate 
    try:
        controls = request.POST.items()
        captured = form.validate(controls)
    except deform.ValidationFailure, e:
        return {'form': e.render()}
    # passed validation
    content = captured.pop('content')
    zip_code = captured.get('zip_code', '')
    email = captured.get('email', '')

    if 'member' in request.user.groups:
        user = request.user 
        if hasattr(user, 'zip_code'):
            zip_code = user.zip_code
        email = user.email
    else:
        user = models.User()
        user.zip_code = zip_code
        user.email = email
        user.groups = ['seller']
        user.groups.append('member')
        user.has_wish = True
        user.insert()


    wish = models.Wish()
    wish.user_id = user._id
    wish.content = content 
    wish.zip_code = zip_code 
    wish.insert()
    # email notification
    settings = request.registry.settings
    email = pyramid_mailer.message.Message(subject='New Request',

                                           recipients=[settings['to']],
                                           body=' ')
    mailer = pyramid_mailer.get_mailer(request) 
    mailer.send(email)
    transaction.commit()
    # show modal message
    # redirect
    #resource = context['wishes'][wish._id]
    href = request.resource_url(context, 'thanks-for-wish')
    return HTTPFound(href)             


@view_config(name="thanks-for-wish", context=resources.Root, 
             renderer='/mini/thankyou_homepage.mako')
def thankyou(context, request):
    return {}

@view_config(context=resources.Message, renderer='/wishes/show.mako')
def show_wish(context, request):
    parent_id = str(context._id)
    cursor = models.Messages().messages_of_parent(parent_id)
    return dict(wish = context,
                messages = cursor)


@view_config(name='edit', context=resources.Message, renderer='form.mako',
             permission='edit')
def edit_wish(context, request):
    schema = schemas.Wish()
    return render_form(schema, request, appstruct=context.__dict__)

@view_config(name='delete', context=resources.Message, renderer='form.mako', permission='edit')
def delete_wish(context, request):
    context.remove()
    request.session.flash('Deleted')
    root = resources.Root(request)
    url = resource_path(root['admin'])
    return HTTPFound(location = url)


@view_config(name='is-new', context=resources.Message, xhr=True, renderer='json', 
             request_method='GET')
def is_new_chat(context, request):
    subject = context.__parent__._id
    chat = models.Chats().exists(request.user._id, subject)
    if chat is None:
        return {}        
    return {'id':str(chat['_id']) }



@view_config(context=resources.Messages, xhr=True, renderer='json', 
             request_method='GET')
def messages_get(context, request):
    chat = context.__parent__
    x = {} 
    for doc in chat.messages:
        for key, value in doc.items():
            if not isinstance(value, str):
                x[key] = str(value)
    return x 


class MessageFirstWishSchema(formencode.Schema):
    allow_extra_fields = True
    filter_extra_fields = True
    body = validators.String(not_empty=True)
    email = validators.String(not_empty=True)
    username = validators.String(not_empty=True)
    zip_code = validators.String(not_empty=True)
    



class MessageSendSchema(formencode.Schema):
    allow_extra_fields = True
    filter_extra_fields = True
    body = validators.String(not_empty=True)
    recipient = validators.String(not_empty=True)

@view_config(name='at', context=resources.Messages, xhr=True, renderer='json', 
             request_method='POST', permission='send')
def messages_at(context, request):
    schema = MessageSendSchema()
    try:
        captured = schema.to_python(request.json_body)
    except formencode.Invalid, error:
        request.response.status_int = 400
        return error.unpack_errors()
    user = request.user
    message = models.Message({'body': captured['body'], 
                              'author': {'name': user.username, '_id': user._id},
                              'recipient': captured['recipient'],
                              'labels': ['at', 'kickoff']})
    message.send()
    return {'body': captured['body']} 


class MessageReplySchema(formencode.Schema):
    allow_extra_fields = True
    filter_extra_fields = True
    body = validators.String(not_empty=True)
    recipient = validators.String(not_empty=True)
    parent = validators.String(not_empty=True)


@view_config(name='reply',context=resources.Messages, xhr=True, renderer='json', 
             request_method='POST', permission='send')
def messages_reply(context, request):
    schema = MessageSendSchema()
    try:
        captured = schema.to_python(request.json_body)
    except formencode.Invalid, error:
        request.response.status_int = 400
        return error.unpack_errors()
    user = request.user
    message = models.Message({'body': captured['body'], 
                              'author': {'name': user.username, '_id': user._id},
                              'recipient': captured['recipient'],
                              'labels': ['reply']})
    user = request.user
    message.reply()
    return {'body': captured['body']} 



"""
the number of people responded would be the number of c
message with my username and a chat.id    
find where has chat ids and my username
unread = recipient is me and status is unread

add orginal chat.id to user model for each new chat
find all 

push a common id onto ancestor

get all messages where username is me and subthreads  

find chats
how
find all where ancestor id is wish_id 

find the chats the a replier sent as a seller
    
find all messages sent
then check if there are subs

find all messages label is chat
stamp it with id

get all leafs by checking no ancestor is zero

get all chats : message where username is me and ancestor is one    



push chat onto message original

how to get get all chats
how do you know if a sub has a replies

message reply username = bobby 

replies has the original in ancestors

"""

@view_config(name='contact', renderer="form.mako")
def contact(context, request):
    tpl_vars = {'heading'  : 'Say Hello...',
                'content'  : '<p><b>email: </b>ruby@rubyrate.com</p>',
                'page_name': 'contact'}  
    
    schema = schemas.Contact()
    myform = Form(schema, 
                buttons=(Button(title='Send', css_class='btn'),))
    if request.method == "GET": 
        tpl_vars['form'] = myform.render()
        return tpl_vars
    # validate            
    try:
        controls = request.POST.items()
        captured = myform.validate(controls)
    except deform.ValidationFailure, e:
        tpl_vars['form'] = e.render()
        return tpl_vars
    # passed validation
    # email the data
    readonly_form = myform.render(captured, readonly=True)
    settings = request.registry.settings
    email = pyramid_mailer.message.Message(subject='Contact Page',
                                           sender=settings['from'],
                                           recipients=[settings['to']],
                                           body=readonly_form)
    mailer = pyramid_mailer.get_mailer(request) 
    mailer.send(email)
    transaction.commit()

    request.session.flash('Thank you!')
    return HTTPFound(location = request.path_url)             
