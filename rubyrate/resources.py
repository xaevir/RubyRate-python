import datetime
from pyramid.threadlocal import get_current_request 
from pyramid.security import authenticated_userid
from pyramid.security import Allow
from pyramid.security import Deny
from pyramid.security import ALL_PERMISSIONS
from pyramid.security import Everyone
from pyramid.security import Authenticated
from pyramid.traversal import resource_path

from pprint import pprint
from pprint import pformat
p = pprint
import logging
from pprint import pprint
log = logging.getLogger(__name__)

from pymongo.objectid import ObjectId
from pymongo.errors import InvalidId


from rubyrate import schemas 

from rubyrate import models

from pytz import timezone
import pytz
eastern = timezone('US/Eastern')

def check_id(_id):
    try: 
        ObjectId(_id)
        return True
    except InvalidId:
        raise KeyError


class Root(dict):
    __name__ = None
    __parent__ = None

    def __init__(self, request):
        self.request = request
        self['users'] = Users(self) 
        self['admin'] = Admin(self) 
        self['wishes'] = Wishes(self) 
        self['chats'] = Chats(self)
        self['chats'].__acl__ = [ (Allow, Authenticated, ('admin', 'edit'))]
        

class Wishes(models.Wishes):
    __acl__ = [ (Allow, 'group:admin', ('admin', 'edit'))]

    def __init__(self, parent):
        self.__name__ = 'wishes'
        self.__parent__ = parent 

    def __getitem__(self, key):
        check_id(key)
        model = self.by_id(key)
        if not model:
            raise KeyError
        resource = Wish(key, self)
        resource.__dict__.update(model.__dict__) 
        resource.__acl__ = [ (Allow, Everyone, 'view'),
                             (Allow, 'group:admin', 'edit') ]
        return resource


class Wish(models.Wish, dict):
    def __init__(self, key, parent):
        self.__name__   = key
        self.__parent__ = parent
        self['chats'] = Chats(self)


class Chats(models.Chats):
    def __init__(self, parent):
        self.__name__ = 'chats'
        self.__parent__ = parent 

    def __getitem__(self, key):
        check_id(key)
        model = self.by_id(key)
        if not model:
            raise KeyError
        resource = Chat(key, self)
        resource.__dict__.update(model.__dict__) 
        return resource

class Chat(models.Chat, dict):
    def __init__(self, name, parent):
        self.__name__   = name 
        self.__parent__ = parent 
        self['messages'] = Messages(self)

class Messages(models.Messages):
    __acl__ = [ (Allow, Authenticated, ('add'))]
    def __init__(self, parent):
        self.__name__ = 'messages'
        self.__parent__ = parent 


class Message(models.Message):
    def __init__(self, name, parent):
        self.__name__   = name
        self.__parent__ = parent 


class Admin(models.Admin, dict):
    __name__ = 'admin'
    __acl__ = [ (Allow, 'group:admin', ('view', 'edit'))]

    def __init__(self, parent):
        self.__parent__ = parent 


class Users(models.Users):
    def __init__(self, parent):
        self.__name__ = 'users'
        self.__parent__ = parent 
        self.request = get_current_request() 

    def __getitem__(self, key):
        try: 
            ObjectId(key)
            # it must be an objectId so retrieve from db
            model = self.by_id(key)
        except InvalidId:
            model = self.by_username(key)
        if not model:
            raise KeyError

        resource = User(key, self)
        resource.__dict__.update(model.__dict__) 
        resource.__acl__ = [ (Allow, Everyone, 'activate'),    
                             (Allow, 'group:admin', 'view'), 
                             (Deny, Everyone, ALL_PERMISSIONS)]
        if hasattr(resource, 'username'):
            resource.__acl__.insert(0, (Allow, resource.username, 'view'))                                
        return resource


class User(models.User, dict):
    def __init__(self, name, parent):
        self.__name__   = name
        self.__parent__ = parent 
        self['chats'] = Chats(self) 
        self['wishes'] = MyWishes(self) 

class MyWishes(models.MyWishes):
    def __init__(self, parent):
        self.__name__ = 'my-wishes'
        self.__parent__ = parent 
        self.request = get_current_request() 

    def __getitem__(self, key):
        try: 
            ObjectId(key)
            # it must be an objectId so retrieve from db
            model = self.by_id(key)
        except InvalidId:
            model = self.by_username(key)
        if not model:
            raise KeyError
        resource = MyWish(key, self)
        resource.__dict__.update(model.__dict__) 
        return resource


class MyWish(models.MyWish):
    def __init__(self, name, parent):
        self.__name__   = name
        self.__parent__ = parent 
