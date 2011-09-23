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
from colander import TupleSchema
from colander import SchemaNode
from colander import Schema
from colander import String
from colander import Boolean
from colander import Integer
from colander import Length
from colander import OneOf
from colander import Email
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
from rubyrate.resources import WishSchema
from rubyrate.resources import Users
from rubyrate.resources import User
from rubyrate.resources import Admin
from rubyrate.resources import Answers
from rubyrate.resources import Answer
from rubyrate.resources import AnswerSchema
from rubyrate.resources import ConclusionSchema
from rubyrate.resources import Conclusion
from rubyrate.resources import Conclusions


import smtplib

from mako.template import Template

from rubyrate.resources import del_autos


def render_form(form, request, appstruct=colander.null, submitted='submit',
                success=None, readonly=False, rest=None, just_get_form=None):
    captured = None
    if submitted in request.POST:
        try:
            controls = request.POST.items()
            captured = form.validate(controls)
            if success:
                response = success(captured)
                if response is not None:
                    return response
            elif rest == 'PUT':
                request.context.update(captured)
                request.session.flash('Updated')
                if just_get_form is not None:
                    url = request.resource_url(request.context)
                    return HTTPound(location = url)  
            elif rest == 'POST':
                request.context.update(captured)
                request.session.flash('Created')
                if just_get_form is not None:
                    url = request.resource_url(request.context)
                    return HTTPFound(location = url)  
            html = form.render(captured)
        except deform.ValidationFailure, e:
            # the submitted values could not be validated
            html = e.render()
    else:
        # the request requires a simple form rendering
        html = form.render(appstruct, readonly=readonly)
    return {'form': html}



@view_config(context=Wish, renderer='/form.mako')
def show_wish(wish, request):
    specific = request.registry.settings['deform.searchpath'] + '/table'
    renderer = ZPTRendererFactory((specific ))

    class thWidget(Widget):
        def serialize(self, field, cstruct, readonly=True):
            if cstruct is colander.null:
                cstruct = u''
            html = '<tr>'
            for item in cstruct:
                html += '<th>%s</th>' % item 
            return html + '</tr>' 

    wish_schema = WishSchema(after_bind=WishSchema.show_single).bind()

    heads = [] 
    children = wish_schema.children
    for child in children:
        heads.append(child.title)

    appstruct={'headers': heads, 'wish_schema':wish.__dict__}

    class Headers(SequenceSchema):
        header = colander.SchemaNode(
                    colander.String())

    class Composed(Schema): 
        headers = Headers(widget=thWidget())
        wish_schema = WishSchema(after_bind=WishSchema.show_single).bind()

    composed = Composed()

    form = Form(composed, renderer=renderer, formid="list")
    readonly = form.render(appstruct, readonly=True)

    href = request.resource_url(wish, 'answers', 'create')
    button = '<div class="button-wrap blue"><a href="%s" class="button">Answer</a></div>' % href

    return {'form': readonly, 
            'heading': wish.product,
            'button': button,
            'page': 'answer',
            }




@view_config(name='update', context=Wish, renderer='form.mako')
def update_wish(context, request):
    schema = WishSchema(after_bind=del_autos).bind()
    form = Form(schema, buttons=(Button(title='Update'),))
    return render_form(form, request, appstruct=context.__dict__, rest='PUT')
   
@view_config(name="", context=Root, renderer='home_page.mako')
def homepage(root, request):
    actual_context = root['wishes'] 
    return create_wish(actual_context, request) 


def create_wish(context, request):
    schema = WishSchema(after_bind=WishSchema.on_creation).bind()
    def succeed(captured):
        context.insert(captured)
        # email notification
        settings = request.registry.settings
        email = Message(subject='Pricing Needed',
            sender=settings['to'],
            recipients=[settings['to']],
            body=' ')
        mailer = get_mailer(request)
        mailer.send(email)
        transaction.commit()

        # show modal message
        thank_you = render('mini/thankyou_homepage.mako', request)    
        request.session.flash(thank_you)
        return HTTPFound(location = request.path_url)             

    form = Form(schema, 
        buttons=(Button(title='Get Pricing', css_class='button blue'),), 
        formid='wish_form')
    return render_form(form, request, success=succeed)

    


@view_config(context=Wishes, renderer='list.mako')
def list_wishes(wishes, request):
    settings = request.registry.settings
    orig = settings['deform.searchpath'] 
    specific = settings['deform.searchpath'] + '/table'
    renderer = ZPTRendererFactory((specific ))

    cursor = wishes.get_without_email()
    lst = []
    for doc in cursor:
        doc['prodlink'] = (doc['_id'], doc['product'])   
        lst.append(doc)


    class thWidget(Widget):
        def serialize(self, field, cstruct, readonly=True):
            html = '<tr>'
            for item in cstruct:
                html += '<th>%s</th>' % item 
            return html + '</tr>' 

    class inputWidget(Widget):
        def serialize(self, field, cstruct, readonly=True):
            return '<input type="text" value="%s">' % cstruct


    class NeedSeq(SequenceSchema):
        wish = WishSchema(after_bind=WishSchema.show_list).bind()

    headers = [] 
    children = NeedSeq.wish.children
    for child in children:
        headers.append(child.title)
    headers[0] = 'Product'

    class Headers(SequenceSchema):
        header = colander.SchemaNode(
                    colander.String())

    appstruct={'headers': headers, 'need_seq':lst}


    class Composed(Schema):
        headers = Headers(widget=thWidget())
        need_seq = NeedSeq()

    schema = Composed()

    from pprint import pformat
    form = Form(schema, renderer=renderer, pformat=pformat, formid="list" )
    readonly = form.render(appstruct, readonly=True)
    dct = {'form': readonly, 
           'header': 'Recent items that need pricing'}
    return dct



@view_config(name='delete', context=Wish, renderer='form.mako')
def delete_item(wish, request):
    wish.remove()
    request.session.flash('Deleted')
    return HTTPFound(location = '/admin')


@view_config(name="create", context=Answers, renderer='form.mako')
def create_answer(context, request):
    schema = AnswerSchema(after_bind=AnswerSchema.on_creation).bind()
    answer = show_wish(context.__parent__, request)
    form = Form(schema, 
        buttons=(Button(title='Submit Answer', css_class='button blue'),), 
        formid='create_form')
    if request.method == "GET": 
        return {'form': form.render(),
                'answer': answer['form'],
                'heading': answer['heading'],
                'answer_heading':'Your Answer'}
    controls = request.POST.items()
    try:
        appstruct = form.validate(controls)
        appstruct['parent'] = context.__parent__.__name__
        request.context.insert(appstruct)
        request.session.flash('Thank you!')
        return HTTPFound(location = request.path_url)             

    except ValidationFailure, e:
        return {'form': e.render(),
                'answer': answer['form'],
                'heading': answer['heading'],
                'answer_heading':'Your Answer'}




@view_config(context=Answers, renderer='form.mako')
def list_answers(answers, request):
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


@view_config(name="create", context=Conclusions, renderer='form.mako')
def create_conclusion(conclusion, request):
    heading = 'Closing Remarks/Conclusion'
    schema = ConclusionSchema(after_bind=ConclusionSchema.on_creation).bind()
    form = Form(schema, 
        buttons=(Button(title='Submit Conclusion', css_class='button blue'),), 
        formid='create_form')
    if 'submit' not in request.POST:
        return {'form': form.render(),
                'heading': heading,
                'page': 'conclusion'}
    controls = request.POST.items()
    try:
        appstruct = form.validate(controls)
        appstruct['parent'] = conclusion.__parent__.__name__

        Conclusion.insert(appstruct)
        request.session.flash('Thank you!')

        url = request.resource_url(request.context.__parent__)
        return HTTPFound(location = url)             

    except ValidationFailure, e:
        return {'form': e.render(),
                'heading':heading,
                'page': 'conclusion'}


@view_config( context=Conclusion, renderer='form.mako')
def update_conclusion(context, request):
    schema = ConclusionSchema(after_bind=del_autos).bind()
    form = Form(schema, buttons=(Button(title='Update'),),just_get_form=True )
    html =  render_form(form, request, appstruct=context.__dict__, rest='PUT')
    return {'page': 'conclusion',
            'form': html['form']}

from rubyrate.resources import Summary

@view_config(context=Summary, renderer='summary.mako')
def summary(context, request):
    settings = request.registry.settings
    orig = settings['deform.searchpath'] 
    specific = settings['deform.searchpath'] + '/list'
    renderer = ZPTRendererFactory((specific ))

    conclusion = context.conclusion['message']
    conclusion = markdown(conclusion)

    cursor = context.answrs

    lst = []
    for doc in cursor:
        lst.append(doc)
  
    appstruct={'answers':lst}

    class A(SequenceSchema):
        x = AnswerSchema(after_bind=AnswerSchema.show_for_summary).bind()

    class Composed(MappingSchema):
        answers = A()

    schema = Composed()
    form = Form(schema, renderer=renderer, formid="list" )
    readonly = form.render(appstruct, readonly=True)
    return {'heading': context.__parent__.product,
            'answers':readonly,
            'conclusion':conclusion }

    """
    index = 0
    total = cursor.count()

    while index < total:
        try:
           x = cursor[index] 
        except:
            x = {} #has to be iterable
        try:
            y = cursor[index+1]
        except:
            y = {} 
        first = {'x': x} 
        second = {'y': y} 
        lst.append(first)
        lst.append(second)
        index += 2
    """


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


@view_config(context=Admin, renderer='/admin/home.mako', 
    permission='view')
def item_admin(admin, request):
    items = admin.get_items()
    return {'items': items,
            'give_pricing': '/prices/create'}

