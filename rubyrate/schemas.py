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
from colander import Regex
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


class PlainText(Regex):
    def __init__(self, msg=None):
        if msg is None:
            msg = 'Enter only letters, numbers, or _ (underscore)'
        super(PlainText, self).__init__(
            u'^[a-zA-Z_\-0-9]*$', msg=msg)

class Base(MappingSchema):
    @staticmethod
    def on_create(node, kw):
        del node['_id']
        del node['created']

    @staticmethod
    def on_update(node, kw):
        del node['_id']
        del node['created']


class Reply(Base):
    body = SchemaNode(
        String(),
        title= '',
        widget= TextAreaWidget(css_class='required'))
    parent = SchemaNode(String(), widget=HiddenWidget())
    labels = SchemaNode(String(), widget=HiddenWidget(), default='reply')



class Wish(Base):
    body = SchemaNode(
        String(),
        widget= TextAreaWidget(css_class='xlarge required'),
        title= 'What would you like help buying...')
    email = SchemaNode(
        String(),
        title= 'Email (never shared)',
        validator = Email(),
        widget = TextInputWidget(css_class='xlarge required email'))
    zip_code = SchemaNode(String(),
        title= 'Zip Code or Relevant Location',
        widget = TextInputWidget(css_class='span2 required'))
    labels = SchemaNode(String(), widget=HiddenWidget(), default='wish')


class User(MappingSchema):
    username = SchemaNode(
        String(),
        validator = Length(min=2, max=60) )
    email = SchemaNode(
        String(),
        validator = Email())
    password = SchemaNode(
        String(), 
        validator = Length(min=5),
        widget = PasswordWidget())


class Seller(MappingSchema):
    username = SchemaNode(
        String(),
        validator = Length(min=3, max=50)) 
    email = SchemaNode(
        String(),
        validator = Email())
    password = SchemaNode(
        String(), 
        validator = Length(min=5, max=100),
        widget = PasswordWidget())
    company = SchemaNode(String(),  
                         widget = TextInputWidget(css_class='name'),
                         missing='')
    website = SchemaNode(String(), missing='')
    phone = SchemaNode(String(), missing='')

@colander.deferred
def deferred_came_from_default(node, kw):
    came_from = kw.get('came_from')
    return came_from

class Login(MappingSchema):
    login = SchemaNode(
        String())
    password = SchemaNode(
        String(), 
        widget = PasswordWidget())
    came_from = SchemaNode(
        String(),
        widget = HiddenWidget(), 
        default = deferred_came_from_default)




class Contact(MappingSchema):
    name = SchemaNode(String(),
        validator = Length(min=2, max=200),
        widget = TextInputWidget(css_class='span2 required'))
        
    email = SchemaNode(String(),
        validator = colander.Email())
    message = SchemaNode(String(),
        validator = Length(max=2000),
        widget=TextAreaWidget())

class SpecialUrl(MappingSchema):
    wish_id = SchemaNode(String())


class SupplierSchema(MappingSchema):
    company_name = SchemaNode(String())
    phone_number = SchemaNode(String())
    locations = SchemaNode(String())
    products_you_sell = SchemaNode(String())
    area_you_serve = SchemaNode(String())
    email = SchemaNode(
        String(),
        validator = colander.Email())

