from rubyrate.mongobase import mongosave
from rubyrate.mongobase import remove
from rubyrate.mongobase import restore
import datetime
from pyramid.threadlocal import get_current_request 
from cryptacular import bcrypt 
from pyramid.security import authenticated_userid
from pyramid.security import Allow, Everyone
from pymongo.objectid import ObjectId
from pyramid.traversal import resource_path
from pymongo.errors import InvalidId

from pprint import pprint
from pprint import pformat
p = pprint
import logging
from pprint import pprint
log = logging.getLogger(__name__)


from markdown import markdown

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
import colander

import deform
from deform.widget import TextInputWidget
from deform.widget import TextAreaWidget
from deform.widget import Widget
from deform.widget import RadioChoiceWidget
from deform.widget import HiddenWidget 

from colander import null

from rubyrate.utility import pretty_date
from rubyrate.mongobase import get_altered

from pytz import timezone
import pytz
eastern = timezone('US/Eastern')

def check_id(_id):
    try: 
        ObjectId(_id)
        return True
    except InvalidId:
        raise KeyError


class Markdown(TextAreaWidget):
    def serialize(self, field, cstruct, readonly=False):
        if cstruct is null:
            cstruct = ''
        if readonly is True:
            cstruct = markdown(cstruct)
            return super(Markdown, self).serialize(field, cstruct, readonly=True)
        return super(Markdown, self).serialize(field, cstruct, readonly=False)


class Link(String):
    def serialize(self, node, appstruct):   
        cstruct = super(Link, self).serialize(node, appstruct)
        return '<a href="http://%s">%s</a>' % (cstruct, cstruct)


class PrettyDate(Widget):
    def serialize(self, field, cstruct, readonly=False):
        if cstruct is null:
            cstruct = ''
        date = pretty_date(cstruct)
        if date is None:
            raise Exception
        return '<td>%s</td>' % date

    def deserialize(self, field, cstruct, readonly=False):
        # TODO should I implement this?
        return cstruct


class LinkFromId(Widget):
    def serialize(self, field, cstruct, readonly=False):
        request = get_current_request()
        url = resource_path(request.context, cstruct[0])
        return '<td><a href="%s">%s</a></td>' % (url, cstruct[1])



class PassThru(Widget):
    def serialize(self, field, cstruct, readonly=False):
        return cstruct
    def deserialize(self, field, cstruct, readonly=False):
        return cstruct

class NoShowWidget(HiddenWidget):
    def serialize(self, field, cstruct=None, readonly=False):
        return ''

def remove_empty(dct):
    non_empty = dict((key, dct[key]) for key,value in dct.iteritems() 
        if value != '')
    return non_empty

def mongosave(collection, dct = None):
    attrs = dct or self.__dict__
    collection = self.__class__.__name___
    db = get_current_request().db
    non_empty = remove_empty(attrs)
    cleaned = remove_traversal(non_empty)
    if not hasattr(self, '_id'):
        return db.collection.insert(cleaned)
    # record already exists so check for altered
    changed, removed = get_altered(cleaned, self.__origdict__) 
    if changed: #cld be calling save on obj not changed so not need for db   
        db.collection.update({'_id': self._id}, {'$set': changed})  # safe = True
    if removed:
        db.collection.update({'_id': self._id}, {'$unset': removed})



class Root(object):
    __name__ = None
    __parent__ = None
    def __init__(self, request):
        self.request = request
        self.request.loggedin = authenticated_userid(request)

    def __getitem__(self, key):
        if key == 'wishes':
            return Wishes(key, self)
        elif key == 'users':
            return Users(key, self)
        elif key == 'admin':
            return Admin(key, self)
        elif key == 'answers':
            return Answers(key, self)
        else:
            raise KeyError


class Admin(object):
    __acl__ = [ (Allow, 'group:admin', 'view')]

    def __init__(self, name, parent):
        self.__name__   = name
        self.__parent__ = parent 

    def get_items(self):
        db = get_current_request().db
        return db.wishes.find()


class Wishes(object):
    def __init__(self, name, parent):
        self.__name__   = name
        self.__parent__ = parent 

    def get_without_email(self):
        db = get_current_request().db
        return db.wishes.find( {}, { 'email' : 0 } )

    def __getitem__(self, key):
        check_id(key)
        wish = Wish.by_id(key)
        if not wish:
            raise KeyError
        wish.__name__   = key
        wish.__parent__ = self
        wish.__acl__ = [ (Allow, Everyone, 'view'),
                         (Allow, 'group:admin', 'edit') ]
        return wish



class Wish(object):
    collection = 'wishes'

    @staticmethod
    def insert(dct):
        db = get_current_request().db
        clean = remove_empty(dct)
        db[self.collection].insert(clean)


    def update(self, dct):
        from rubyrate.mongobase import get_altered
        db = get_current_request().db
        clean = remove_empty(dct)
        changed, removed = get_altered(clean, self.__origdict__) 
        if changed: #cld be calling save on obj not changed so not need for db   
            db[self.collection].update({'_id': self._id}, {'$set': changed}, safe = True)  # safe = True
        #if removed:
        #    db[collection].update({'_id': self._id}, {'$unset': removed})


    @staticmethod
    def by_id(_id):
        """Restore the user from DB or return None"""
        db = get_current_request().db
        doc = db.wishes.find_one({'_id': ObjectId(_id)})
        if doc is None:
            return 
        return restore(Wish, doc)

    def __getitem__(self, key):
        if key == 'answers':
            return Answers(key, self)
        if key == 'conclusions':
            return Conclusions(key, self)
        if key == 'summary':
            return Summary(key, self)
        else:
            raise KeyError

class Summary(object):
    def __init__(self, name, parent):
        self.__name__    = name
        self.__parent__  = parent 
        self._id         = parent.__name__
        self.answers     = Answers(self._id, parent)
        self.conclusions = Conclusions(self._id, parent)
        self.answrs      = self.answers.get_answers_of_parent()
        self.db          = get_current_request().db
        self.conclusion  = self.db.conclusion.find_one({'parent': self._id})


def del_autos(node, kw):
    if kw=='just_id':
        del node['_id']
    else: 
        del node['_id']
        del node['created']

class thWidget(Widget):
    def serialize(self, field, cstruct, readonly=True):
        if cstruct is colander.null:
            cstruct = u''
        html = '<tr>'
        for item in cstruct:
            html += '<th>%s</th>' % item 
        return html + '</tr>' 

class WishSchema(MappingSchema):
    _id = SchemaNode(String()) 
    email = SchemaNode(
        String(),
        validator = Email())
    product = SchemaNode(
        String(),
        widget= TextAreaWidget())
    quantity = SchemaNode(String())
    when = SchemaNode(
        String(),
        title="When would you like this")
    zip_code = SchemaNode(String())
    price_range = SchemaNode(
        String(),
        missing = '',
        title= 'Price Range (optional)')
    created = SchemaNode(PassThru(), widget = PrettyDate())
   
    @staticmethod
    def on_creation(node, kw):
        del node['_id']
        node['created'].widget=NoShowWidget()
        node['created'].missing = datetime.datetime.utcnow()

    @staticmethod
    def on_update(node, kw):
        del node['_id']
        del node['created']

    @staticmethod
    def show_list(node, kw):
        del node['email']
        del node['price_range']
        _id = node['_id']
        del node['_id']
        product = node['product']
        del node['product']
        prodlink = SchemaNode(PassThru(), name='prodlink', widget=LinkFromId())
        node.children.insert(0,prodlink)

    @staticmethod
    def show_single(node, kw):
        del node['_id']
        del node['email']
        del node['product']
        

class Answers(object):
    def __init__(self, name, parent):
        self.__name__   = name
        self.__parent__ = parent 

    def __getitem__(self, key):
        check_id(key)
        answer = Answer.by_id(key)
        if not answer:
            raise KeyError
        answer.__name__   = key
        answer.__parent__ = self
        answer.__acl__ = [ (Allow, Everyone, 'view'),
                         (Allow, 'group:admin', 'edit') ]
        return answer

    def get_answers_of_parent(self, id = None):
        _id = self.__parent__.__name__
        db = get_current_request().db
        return db.answers.find({'parent': _id})

class Answer(object):
    @staticmethod
    def insert(dct):
        db = get_current_request().db
        clean = remove_empty(dct)
        db.answers.insert(clean)

    def save(self, dct):
        mongosave(self, dct)

    @staticmethod
    def by_id(_id):
        """Restore the user from DB or return None"""
        db = get_current_request().db
        doc = db.answers.find_one({'_id': ObjectId(_id)})
        if doc is None:
            return 
        return restore(Answer, doc)


class AnswerSchema(MappingSchema):
    _id = SchemaNode(String()) 
    company = SchemaNode(String(),  
                widget = TextInputWidget(css_class='name'))
    website = SchemaNode(Link())
    email = SchemaNode(
        String(),
        validator = Email())
    phone = SchemaNode(String())
    message = SchemaNode(
        String(),
        widget= Markdown())
    created = SchemaNode(PassThru(), widget=PrettyDate())

    @staticmethod
    def on_creation(node, kw):
        del node['_id']
        node['created'].widget=NoShowWidget()
        node['created'].missing = datetime.datetime.utcnow()

    @staticmethod
    def show_list(node, kw):
        del node['created']
        del node['_id']



class Conclusions(object):

    def __init__(self, name, parent):
        self.__name__   = name
        self.__parent__ = parent 

    def __getitem__(self, key):
        if key == 'update':
            key = self.__parent__.__name__
            check_id(key)
            conclusion = Conclusion.by_parent(key)
            if not conclusion:
                raise KeyError
            conclusion.__name__   = key
            conclusion.__parent__ = self
            conclusion.__acl__ = [ (Allow, Everyone, 'view'),
                             (Allow, 'group:admin', 'edit') ]
            return conclusion
        else:
            raise KeyError



class Conclusion(object):

    @staticmethod
    def by_parent(_id):
        db = get_current_request().db
        doc = db.conclusion.find_one({'parent': _id})
        if doc is None:
            return 
        return restore(Conclusion, doc)

    @staticmethod
    def insert(dct):
        db = get_current_request().db
        clean = remove_empty(dct)
        db.conclusion.insert(clean)

    def update(self, dct):
        db = get_current_request().db
        clean = remove_empty(dct)
        changed, removed = get_altered(clean, self.__origdict__) 
        if changed: #cld be calling save on obj not changed so not need for db   
            db.conclusion.update({'_id': self._id}, {'$set': changed}, safe = True)  # safe = True

def just_key(node, kw):
    message = kw.get('message')
    keep = node[message]
    node.children = [keep]


class ConclusionSchema(MappingSchema):
    _id = SchemaNode(String()) 
    message = SchemaNode(
        String(),
        widget= Markdown())
    created = SchemaNode(PassThru(), widget=PrettyDate())
    parent = SchemaNode(String(), widget=HiddenWidget())

    @staticmethod
    def on_creation(node, kw):
        del node['_id']
        node['created'].widget=NoShowWidget()
        node['created'].missing = datetime.datetime.utcnow()




def groupfinder(name, request):
    user = User.by_username(name)
    # If the user is in the db then they have passed validation and are 
    # a member. Since every user will be a member it does not make sense to
    # add this field to the db. I will only add it if they are admins, etc...
    # If down the road, I add an email verification, then I will alter this.
    if user:
        groups = getattr(user, 'groups', ['member'])
        return ['group:%s'%group for group in groups]

class Users(object):
    def __init__(self, name, parent):
        self.__name__   = name
        self.__parent__ = parent 

    def __getitem__(self, key):
        user = User.by_username(key)
        if not user:
            raise KeyError
        user.__name__   = key
        user.__parent__ = self
        user.__acl__ = [ (Allow, Everyone, 'view'),
                         (Allow, user.username, 'edit'),
                         (Allow, 'group:admin', 'edit') ]

        return user

class User(object):
    __collection__ = 'users'
    __uses_descriptor__ = True
    def __init__(self, data):
        self.created  = datetime.datetime.utcnow()
        for key, value in data.iteritems():
            setattr(self, key, value)

    @property
    def password(self):
        return self.__password

    @password.setter
    def password(self, value):
        crypt = bcrypt.BCRYPTPasswordManager()
        self.__password =  crypt.encode(value)

    def check_password(self, unencrypted):
        crypt = bcrypt.BCRYPTPasswordManager()
        return crypt.check(self.password, unencrypted)

    @staticmethod
    def by_username(name):
        """Restore the user from DB or return None"""
        db = get_current_request().db
        doc = db.users.find_one({'username': name})
        if doc is None:
            return 
        return restore(User, doc)
        
    @staticmethod
    def exists(name):
        """check if user exists"""
        db = get_current_request().db
        doc = db.users.find_one({'username': name})
        if doc is None:
            return 
        return True

    @staticmethod
    def insert(dct):
        db = get_current_request().db
        clean = remove_empty(dct)
        db.users.insert(clean)




