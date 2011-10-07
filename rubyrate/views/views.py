from pyramid.view import view_config
from pyramid.response import Response
from pyramid.renderers import render

from pyramid_mailer import get_mailer
from pyramid_mailer.message import Message
from pyramid.url import resource_url
from pyramid.httpexceptions import HTTPFound

import transaction

from mako.template import Template

from colander import MappingSchema
from colander import SequenceSchema
from colander import TupleSchema
from colander import SchemaNode
from colander import Schema
from colander import String
from colander import Boolean
from colander import Integer
from colander import Length
from colander import OneOf
from colander import Function
from colander import Invalid
import colander

from markdown import markdown

import deform
from deform.widget import TextInputWidget
from deform.widget import TextAreaWidget
from deform.widget import Widget
from deform.widget import RadioChoiceWidget
from deform import ValidationFailure

from rubyrate.my_deform.form import Button
from rubyrate.my_deform.form import Form
from pkg_resources import resource_filename
from deform import ZPTRendererFactory

from pprint import pprint
p = pprint

from rubyrate.resources import Root
from rubyrate.resources import Wishes
from rubyrate.resources import Wish
from rubyrate.resources import Users
from rubyrate.resources import User
from rubyrate.resources import Admin
from rubyrate.resources import Replies
from rubyrate.resources import Reply
from rubyrate.resources import Emails
from rubyrate.resources import Email

import smtplib

from mako.template import Template

from rubyrate.resources import del_autos


def render_form(form, request, appstruct=colander.null, redirect=True,
                success=None, readonly=False):
    captured = None
    url = request.resource_url(request.context.__parent__)
    if request.method == 'GET': 
        html = form.render(appstruct, readonly=readonly)
    else:
        try:
            controls = request.POST.items()
            captured = form.validate(controls)
            if success:
                response = success(captured, request)
                if response is not None:
                    return response
            if request.method == 'PUT': 
                request.context.model.update(captured)
                request.session.flash('Updated')
            if request.method == 'POST': 
                #initialize model
                model = request.context.Model(captured)
                _id = model.insert()
                request.session.flash('Created')
            if redirect:
                raise HTTPFound(url)  
            else:
                html = form.render(captured)
        except deform.ValidationFailure, e:
            html = e.render()
    return {'form': html}


def allowed_methods(*allowed):
    '''Custom predict checking if the HTTP method in the allowed set.
    It also changes the request.method according to "_method" form parameter
    and "X-HTTP-Method-Override" header
    '''
    def predicate(info, request):
        if request.method == 'POST':
            request.method = (
                request.str_POST.get('_method', '').upper() or
                request.headers.get('X-HTTP-Method-Override', '').upper() or
                request.method)
 
        return request.method in allowed
    return predicate


def change_context(context, request):
    if isinstance(context, Root):
        request.context = context['wishes']
    return True 

@view_config(name="", context=Root, renderer='home_page.mako', 
             custom_predicates=(allowed_methods('GET', 'POST'),change_context))
def create_wish(context, request):
    context = request.context # actual context
    schema = context.schema(after_bind=context.schema.on_create).bind()
    form = Form(schema, buttons=(
        Button(title='Get Replies', css_class='button'),))
    def success(captured, request):
        model = request.context.Model(captured)
        _id = model.insert()
        # email notification
        settings = request.registry.settings
        email = Message(subject='New Wish',
            sender=settings['to'],
            recipients=[settings['to']],
            body=' ')
        mailer = get_mailer(request) 
        mailer.send(email)
        transaction.commit()
        # show modal message
        thank_you = 'Thank you. We are working on your wish.'    
        request.session.flash(thank_you)
        href = request.resource_url(context[_id])
        raise HTTPFound(href)             
    return render_form(form, request, success=success)


@view_config(context=Wish, renderer='/wish/show.mako')
def show_wish(context, request):
    replies = context['replies']
    str_id = str(context.model._id)
    cursor = replies.Model.all_by_parent(str_id, replies.Model)
    return dict(
        wish = context.model,
        replies = cursor,
        page = 'show-wish',
        create_link = request.resource_url(context['replies'], 'create')
        )

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



@view_config(name='update', context=Reply, renderer='form.mako',
             custom_predicates=(allowed_methods('GET', 'PUT'),))
@view_config(name='update', context=Wish, renderer='form.mako',
             custom_predicates=(allowed_methods('GET', 'PUT'),))
def update_context(context, request):
    schema = context.schema(after_bind=del_autos).bind()
    form = Form(schema, 
                _method='PUT', 
                buttons=(Button(title='Update', css_class='button'),))
    return render_form(form, request, appstruct=context.__dict__)

@view_config(context=Wishes, renderer='/wish/list.mako')
def list_wishes(context, request):
    wishes = context.Model.get_all_without_email(context.Model)
    return {'wishes': wishes}

@view_config(name='delete', context=Wish, renderer='form.mako',
             custom_predicates=(allowed_methods('DELETE'),))
def delete_wish(context, request):
    context.remove()
    request.session.flash('Deleted')
    return HTTPFound(location = '/admin')

@view_config(name="create", context=Emails, renderer='form.mako',
             custom_predicates=(allowed_methods('GET', 'POST'),))
@view_config(name="create", context=Replies, renderer='form.mako',
             custom_predicates=(allowed_methods('GET', 'POST'),))
def create_reply(context, request):
    parent_name = context.__parent__.__name__
    schema = context.schema(after_bind=context.schema.on_create)
    schema = schema.bind(parent_name=parent_name)
    form = Form(
        schema, 
        buttons=(Button(title='Submit Reply', css_class='button'),))
    return render_form(form, request)



@view_config(context=Reply, renderer='form.mako')
def show_reply(context, request):
    schema = context.schema(after_bind=del_autos).bind()
    form = Form(schema, 
                buttons=(Button(title='Update', css_class='button'),))
    form_dct = render_form(form, request, appstruct=context.model.__dict__, 
                       readonly=True, redirect=False)
    return {'form': form_dct['form'], 
            'page_name': 'show-reply'}

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


class ContactSchema(MappingSchema):
    name = SchemaNode(String(),
        validator = Length(min=2, max=200))
    email = SchemaNode(String(),
        validator = colander.Email())
    message = SchemaNode(String(),
        validator = Length(max=2000),
        widget=TextAreaWidget())

@view_config(name='contact', context=Root, renderer="contact.mako")
def contact(context, request):
    schema = ContactSchema()
    myform = Form(schema, 
                buttons=(Button(title='Send', css_class='button'),))
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
                        recipients=['bobby.chambers33@gmail.com'], #settings['to']
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
        validator = colander.Email())


@view_config(name='supplier', context=Root, renderer="supplier.mako")
def supplier(context, request):
    schema = SupplierSchema()
    myform = Form(schema, 
                buttons=(Button(title='Send', css_class='button'),))
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


@view_config(context=Admin, renderer='/admin/home.mako', 
    permission='view')
def item_admin(admin, request):
    items = admin.get_items()
    return {'items': items,
            'give_pricing': '/prices/create'}

