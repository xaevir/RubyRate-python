from colander import MappingSchema
from colander import SequenceSchema
from colander import TupleSchema
from colander import SchemaNode
from colander import String
from colander import Boolean
from colander import Integer
from colander import Length
from colander import OneOf
from colander import Email
from colander import Function
from colander import Invalid
from colander import DateTime
from colander import All
import colander

import deform
from deform.widget import TextInputWidget
from deform.widget import TextAreaWidget
from deform.widget import Widget
from deform.widget import RadioChoiceWidget
from deform.widget import HiddenWidget 
from deform.widget import PasswordWidget 


from rubyrate.my_deform.widgets import Markdown
from rubyrate.my_deform.widgets import Link
from rubyrate.my_deform.widgets import PrettyDate
from rubyrate.my_deform.widgets import LinkFromId
from rubyrate.my_deform.widgets import PassThru
from rubyrate.my_deform.widgets import NoShowWidget


import datetime

class Base(MappingSchema):

    @staticmethod
    def on_create(node, kw):
        del node['_id']
        del node['created']

    @staticmethod
    def on_update(node, kw):
        del node['_id']
        del node['created']
   

class Wish(Base):
    _id = SchemaNode(String()) 
    wish = SchemaNode(
        String(),
        widget= TextAreaWidget(),
        title= 'What would you like help buying...',
        )
    email = SchemaNode(
        String(),
        validator = Email())
    zip_code = SchemaNode(String())
    created = SchemaNode(PassThru(), widget = PrettyDate())
   
    @staticmethod
    def show_list(node, kw):
        del node['email']
        _id = node['_id']
        del node['_id']
        product = node['wish']
        del node['wish']
        prodlink = SchemaNode(PassThru(), name='prodlink', widget=LinkFromId())
        node.children.insert(0,prodlink)


class Reply(Base):
    _id = SchemaNode(String()) 
    company = SchemaNode(String(),  
                widget = TextInputWidget(css_class='name'))
    website = SchemaNode(String(), widget = Link())
    email = SchemaNode(
        String(),
        validator = Email())
    phone = SchemaNode(String())
    message = SchemaNode(
        String(),
        widget= Markdown())
    created = SchemaNode(PassThru(), widget=PrettyDate())
    parent = SchemaNode(String(), widget=HiddenWidget())

    @staticmethod
    def on_create(node, kw):
        parent_name = kw.get('parent_name')
        del node['_id']
        del node['created']
        node['parent'].default = parent_name 


    @staticmethod
    def show_list(node, kw):
        del node['created']
        del node['message']
        _id = node['_id']
        del node['_id']
        company = node['company']
        del node['company']
        companylink = SchemaNode(PassThru(), name='companylink', 
            title = 'Company', widget=LinkFromId())
        node.children.insert(0,companylink)


class Email(Base):
    _id = SchemaNode(String()) 
    body = SchemaNode(String(),  
        widget= TextAreaWidget())
    sender = SchemaNode(String()) 
    to = SchemaNode(String()) 
    created = SchemaNode(PassThru(), widget=PrettyDate())

class User(MappingSchema):
    def unique_username(node, value):
        user = User.by_username(value)
        if user:
            raise Invalid(node, 'That username already exists')
    username = SchemaNode(
        String(),
        validator = All( Length(min=3, max=50), unique_username ) )
    email = SchemaNode(
        String(),
        validator = Email())
    password = SchemaNode(
        String(), 
        validator = Length(min=5, max=100),
        widget =PasswordWidget())


