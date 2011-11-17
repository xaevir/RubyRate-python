import datetime
from pyramid.threadlocal import get_current_request 
from pyramid.security import authenticated_userid
from pyramid.security import Allow, Everyone
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
        user = request.user
        if 'visitor' in request.user.groups:
            self.request.loggedin = False
        else:
            self.request.loggedin = True
        self['users'] = Users(self) 
        self['admin'] = Admin(self) 
        self['wishes'] = Wishes(self) 


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
        self['messages'] = Messages(self) 
        self['convo'] = Convo(self) 

class Convo(models.Convo):
    def __init__(self, parent):
        self.__name__   = 'convo' 
        self.__parent__ = parent 



class Messages(models.Messages, dict):
    def __init__(self, parent):
        self.__name__ = 'messages'
        self.__parent__ = parent 

    def __getitem__(self, key):
        if not check_id(key):
            raise KeyError
        doc = models.Message.by_id(key, models.Message)
        if not doc:
            raise KeyError
        resource = Message(key, self)
        for key, value in doc.iteritems():
            setattr(resource, key, value)
        resource.__acl__ = [ (Allow, Everyone, 'view'),
                         (Allow, 'group:admin', 'edit') ]
        return resource


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
        resource.__acl__ = [ (Allow, Everyone, 'view'),
                             (Allow, 'group:admin', 'edit') ]
        return resource


class User(models.User):
    def __init__(self, name, parent):
        self.__name__   = name
        self.__parent__ = parent 
