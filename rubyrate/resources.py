from rubyrate.mongobase import Base
from rubyrate.mongobase import restore
import datetime
from pyramid.threadlocal import get_current_request 
from cryptacular import bcrypt 
from pyramid.security import authenticated_userid
from pyramid.security import Allow, Everyone
from pymongo.objectid import ObjectId

from pprint import pprint

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


class Items(object):
    def __init__(self, name, parent):
        self.__name__   = name
        self.__parent__ = parent 

    def get_recent(self):
        db = get_current_request().db
        return db.item.find()

    def __getitem__(self, key):
        item = Item.by_id(key)
        if not item:
            raise KeyError
        item.__name__   = key
        item.__parent__ = self
        item.__acl__ = [ (Allow, Everyone, 'view'),
                         (Allow, 'group:admin', 'edit') ]
        return item

class Item(Base):
    __collection__ = 'item'
    def __init__(self, data):
        self.created = datetime.datetime.utcnow()
        for key, value in data.iteritems():
            setattr(self, key, value)

    @staticmethod
    def by_id(_id):
        """Restore the user from DB or return None"""
        db = get_current_request().db
        doc = db.item.find_one({'_id': ObjectId(_id)})
        if doc is None:
            return 
        return restore(Item, doc)



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

class User(Base):
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



