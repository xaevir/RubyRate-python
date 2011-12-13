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

@view_config(name="", context=resources.Root, renderer='home_page.mako')
def create_wish_homepage(context, request):
    schema = schemas.WishNoAccount()
    # if a person is already logged in:
    if request.user:
        if 'admin' in request.user.groups:
            schema = schemas.WishNoAccount()
            schema['email'].missing=''
        if 'member' in request.user.groups:
            schema = schemas.WishNoAccount()
            del schema['email']
            if hasattr(request.user, 'zip_code'):
                del schema['zip_code']
    else:
        schema = schemas.WishNoAccount()
    form = Form(schema, buttons=(Button(title='Make Wish', css_class='btn'),))
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
                                           sender=settings['to'],
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

@view_config(context=resources.Wish, renderer='/wishes/show.mako')
def show_wish(context, request):
    parent_id = str(context._id)
    cursor = models.Messages().messages_of_parent(parent_id)
    return dict(wish = context,
                messages = cursor)

@view_config(context=resources.Wishes, renderer='/wishes/list.mako') 
def list_wishes(context, request):
    cursor = context.get_wishes()
    return dict(wishes = cursor,
                url = request.resource_url)


@view_config(name='edit', context=resources.Wish, renderer='form.mako',
             permission='edit')
def edit_wish(context, request):
    schema = schemas.Wish()
    return render_form(schema, request, appstruct=context.__dict__)

@view_config(name='delete', context=resources.Wish, renderer='form.mako', permission='edit')
def delete_wish(context, request):
    context.remove()
    request.session.flash('Deleted')
    root = resources.Root(request)
    url = resource_path(root['admin'])
    return HTTPFound(location = url)

@view_config(name="create-first", context=resources.Messages, renderer='/messages/create.mako')
def create_first_message(context, request):
    if not request.loggedin:
        href = '/users/create-seller/%s'% context.__parent__.__name__
        return HTTPFound(href)            

    # check if they already sent message
    result = context.already_sent_message(context.__parent__.__name__, request.user.username)
    if result is not None:
        notice = 'We do not want to burden this person, so we wait for them to respond before you can send more messages'
        tmp = render('notice.mako', {'notice': notice}, request)
        return Response(tmp)

    schema = schemas.Message()
    schema['content'].title = 'Kindly add your message'
    schema['parent'].default = context.__parent__.__name__
    form = Form(schema, buttons=(Button(title='Send Message', css_class='btn'),))
    if request.method == 'GET': 
        return {'form': form.render(), 
                'wish': context.__parent__}
    try:
        controls = request.POST.items()
        captured = form.validate(controls)
    except deform.ValidationFailure, e:
        return {'form': e.render(),
                'wish': context.__parent__}
    # passed validation
    message = models.Message()
    message.username = request.user.username 
    message.content = captured['content'] 
    message.parent = captured['parent']
    message.ancestors = [captured['parent']]
    message.insert()
    thank_you = 'This customer has been contacted with your message'
    request.session.flash(thank_you)
    # redirect
    href = request.resource_url(context)
    return HTTPFound(href)             


@view_config(name='is-new', context=resources.Chats, xhr=True, renderer='json', 
             request_method='GET')
def is_new_chat(context, request):
    subject = context.__parent__._id
    chat = models.Chats().exists(request.user._id, subject)
    if chat is None:
        return {}        
    return {'id':str(chat['_id']) }


@view_config(name='reply', context=resources.Wish, renderer='/chats/reply.mako')
def reply(context, request):
    # is new 
    chat = models.Chats().exists(request.user._id, context._id)
    #if chat is not None: 
        #load previous messages
    #    raise Exception('load previous chats')
    return {'wish': context}



class ChatSchema(formencode.Schema):
    allow_extra_fields = True
    filter_extra_fields = True
    subject = validators.String(not_empty=True)
    content = validators.String(not_empty=True)

@view_config(context=resources.Chats, xhr=True, renderer='json', 
             request_method='POST')
def chats(context, request):
    schema = ChatSchema()
    try:
        captured = schema.to_python(request.json_body)
    except formencode.Invalid, error:
        request.response.status_int = 400
        return error.unpack_errors()
    # passed validation
    wish = models.Wishes().by_id(str(captured['subject']))
    chat = models.Chat()
    chat.user_data = [{'_id': wish.user_id, 'new': 1},
                     {'_id': request.user._id, 'new': 0}]
    chat.shared_by = [request.user._id, wish.user_id]
    chat.subject_id = ObjectId(captured['subject'])
    chat.subject_content = wish.content 
    chat.insert()  
    messages = [{'content' : wish.content},
               {'username': request.user.username,
                'content' : captured['content']} ]
    chat.push_all(messages)
    return {'id': str(chat._id), 
            'subject': captured['subject'],
            'content': captured['content']}


@view_config(context=resources.Chats, xhr=True, renderer='json', 
             request_method='GET', permission='view')
def get_chats(context, request):
    cursor = context.get_chats()
    x = {} 
    for doc in cursor:
        for key, value in doc.items():
            if not isinstance(value, str):
                x[key] = str(value)
    return x 


@view_config(name="nav", context=resources.Chats, xhr=True, renderer='json', 
             request_method='GET', permission='view')
def chats_nav(context, request):
    return context.nav()




@view_config(context=resources.User, permission='view', renderer="app.mako")
def user_home(context, request):
    #request.subpath[0]
    cursor = models.Chats().get_chats()
    count = cursor.count() 
    if count:
        recent_chat = cursor[0] 
        messages = recent_chat['messages']
    else:
        recent_chat = {} 
        messages = {} 
    return {'chats': cursor, 
            'messages': messages,
            'count': count}


@view_config(context=resources.Messages, xhr=True, renderer='json', 
             request_method='GET')
def messages(context, request):
    chat = context.__parent__
    x = {} 
    for doc in chat.messages:
        for key, value in doc.items():
            if not isinstance(value, str):
                x[key] = str(value)
    return x 



class MessageForm(formencode.Schema):
    allow_extra_fields = True
    filter_extra_fields = True
    content = validators.String(not_empty=True)

@view_config(context=resources.Messages, xhr=True, renderer='json', 
             request_method='POST')
def _messages(context, request):
    schema = MessageForm()
    try:
        captured = schema.to_python(request.json_body)
    except formencode.Invalid, error:
        request.response.status_int = 400
        return error.unpack_errors()
    # passed validation
    message = {'username': request.user.username,
               'content' : captured['content']}
    chat = context.__parent__  
    chat.push(message)
    return {'content': captured['content']} 
    


@view_config(context=resources.Message, renderer='/messages/show.mako')
def show_message(context, request):
    return dict(message = context.content,
                replies = {},
                page = 'show-message',
                create_link = request.resource_url(context))


@view_config(name='contact', context=resources.Root, renderer="form.mako")
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


@view_config(context=resources.Admin, renderer='/admin/home.mako', permission='view')  
def admin(context, request):
    wishes = models.Wishes()
    cursor = wishes.get_wishes()

    return {'wishes': cursor,
           'get_wish_owner': wishes.get_wish_owner}


"""
@view_config(name='summary', context=Wish, renderer='/wish/summary.mako')
def summary_wish(context, request):
    replies = context['replies']
    str_id = str(context.model._id)
    cursor = replies.Model.all_by_parent(str_id, replies.Model)
    return dict(
        wish = context.model,
        replies = cursor,
        page = 'summary',
        create_link = request.resource_url(context['replies'], 'create')
        )




@view_config(context=Wishes, renderer='/wish/list.mako')
def list_wishes(context, request):
    wishes = context.Model.get_all_without_email(context.Model)
    return {'wishes': wishes}


@view_config(name="create", context=Emails, renderer='form.mako',
             custom_predicates=(allowed_methods('GET', 'POST'),))
def create_email(context, request):
    parent_name = context.__parent__.__name__
    schema = context.schema(after_bind=context.schema.on_create)
    schema = schema.bind(parent_name=parent_name)
    form = Form(
        schema, 
        buttons=(Button(title='Submit Reply', css_class='btn'),))
    return render_form(form, request)


@view_config(name="create", context=Replies, renderer='form.mako',
             custom_predicates=(allowed_methods('GET', 'POST'),))
def create_reply(context, request):
    parent_name = context.__parent__.__name__
    schema = context.schema(after_bind=context.schema.on_create)
    schema = schema.bind(parent_name=parent_name)
    form = Form(
        schema, 
        buttons=(Button(title='Submit Reply', css_class='btn'),))
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
    if request.method == 'POST': 
        #initialize model
        message = {} 
        message['content'] = captured.pop('message')
        message['parent'] = captured.pop('parent')
        half_user = models.HalfUser(captured)
        half_user.insert()

        
        

    return render_form(form, request)



@view_config(context=Reply, renderer='/replies/show.mako')
def show_reply(context, request):
    return {'message': context.model.message, 
            'company': context.model.company,
            'company_href': context.model._id}

@view_config(context=Replies, renderer='form.mako')
def list_replies(answers, request):
    settings = request.registry.settings
    orig = settings['deform.searchpath'] 
    specific = settings['deform.searchpath'] + '/table'
    renderer = ZPTRendererFactory((specific ))

    cursor = answers.get_answers_of_parent()

    lst = []
    for doc in cursor:
        doc['companylink'] = (doc['_id'], doc['company'])   
        lst.append(doc)

    class thWidget(Widget):
        def serialize(self, field, cstruct, readonly=True):
            html = '<tr>'
            for item in cstruct:
                html += '<th>%s</th>' % item 
            return html + '</tr>' 

    class AnswersSeq(SequenceSchema):
        answer = AnswerSchema(after_bind=AnswerSchema.show_list).bind()


    headers = [] 
    children = AnswersSeq.answer.children
    for child in children:
        headers.append(child.title)

    class Headers(SequenceSchema):
        header = colander.SchemaNode(
                colander.String())

    appstruct={'headers': headers, 'answers':lst}


    class Composed(Schema):
        headers = Headers(widget=thWidget())
        answers = AnswersSeq()

    schema = Composed()

    form = Form(schema, renderer=renderer, formid="list" )
    readonly = form.render(appstruct, readonly=True)
    dct = {'form': readonly, 
           'heading': 'Recent items that need pricing'}
    return dct





class SupplierSchema(MappingSchema):
    company_name = SchemaNode(String())
    phone_number = SchemaNode(String())
    locations = SchemaNode(String())
    products_you_sell = SchemaNode(String())
    area_you_serve = SchemaNode(String())
    email = SchemaNode(
        String(),
        validator = colander.Email())


@view_config(name='supplier', context=Root, renderer="supplier.mako")
def supplier(context, request):
    schema = SupplierSchema()
    myform = Form(schema, 
                buttons=(Button(title='Send', css_class='btn'),))
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


"""
