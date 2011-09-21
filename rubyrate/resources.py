from rubyrate.mongobase import mongosave
from rubyrate.mongobase import remove
from rubyrate.mongobase import restore
import datetime
from pyramid.threadlocal import get_current_request 
from cryptacular import bcrypt 
from pyramid.security import authenticated_userid
from pyramid.security import Allow, Everyone
from pymongo.objectid import ObjectId

from pprint import pprint
p = pprint
import logging
from pprint import pprint
log = logging.getLogger(__name__)


from colander import MappingSchema
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
import colander

import deform
from deform.widget import TextInputWidget
from deform.widget import TextAreaWidget
from deform.widget import Widget
from deform.widget import RadioChoiceWidget
from deform.widget import HiddenWidget 



class Root(object):
    __name__ = None
    __parent__ = None
    def __init__(self, request):
        self.request = request
        self.request.loggedin = authenticated_userid(request)

    def __getitem__(self, key):
        if key == 'items':
            return Items(key, self)
        elif key == 'users':
            return Users(key, self)
        elif key == 'admin':
            return Admin(key, self)
        else:
            raise KeyError

class Admin(object):
    __acl__ = [ (Allow, 'group:admin', 'view')]

    def __init__(self, name, parent):
        self.__name__   = name
        self.__parent__ = parent 

    def get_items(self):
        db = get_current_request().db
        return db.item.find()




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


class Item(MappingSchema):
    _id = SchemaNode(String()) 
    created = SchemaNode(String())
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
   
    def insert(self, dct):
        db = get_current_request().db
        clean = remove_empty(dct)
        db.item.insert(clean)

    def save(self, dct):
        mongosave(self, dct)
        

    @staticmethod
    def on_creation(node, kw):
        del node['_id']
        node['created'].widget=NoShowWidget()
        node['created'].missing = datetime.datetime.utcnow()

    @staticmethod
    def safe_show(node, kw):
        del node['email']

    @staticmethod
    def by_id(_id):
        """Restore the user from DB or return None"""
        db = get_current_request().db
        doc = db.item.find_one({'_id': ObjectId(_id)})
        if doc is None:
            return 
        return restore(Item, doc)


class Items(object):
    def __init__(self, name, parent):
        self.__name__   = name
        self.__parent__ = parent 

        
        self.ItemsSeq = ItemsSeq

    def get_without_email(self):
        db = get_current_request().db
        return db.item.find( {}, { 'email' : 0 } )

    def __getitem__(self, key):
        raise Exception
        item = Item.by_id(key)
        if not item:
            raise KeyError
        item.__name__   = key
        item.__parent__ = self
        item.__acl__ = [ (Allow, Everyone, 'view'),
                         (Allow, 'group:admin', 'edit') ]
        return item



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
    __collection__ = 'user'
    __uses_descriptor__ = True
    def __init__(self, data):
        self.created  = datetime.datetime.now()
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
        doc = db.user.find_one({'username': name})
        if doc is None:
            return 
        return restore(User, doc)
        
    @staticmethod
    def exists(name):
        """check if user exists"""
        db = get_current_request().db
        doc = db.user.find_one({'username': name})
        if doc is None:
            return 
        return True



