import datetime
from pyramid.threadlocal import get_current_request 
from pyramid.security import authenticated_userid
from pyramid.security import Allow
from pyramid.security import Deny
from pyramid.security import ALL_PERMISSIONS
from pyramid.security import Everyone
from pyramid.security import Authenticated
from pyramid.traversal import resource_path

from pyramid.httpexceptions import HTTPForbidden

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
"""
    __acl__ = [ (Allow, Everyone, 'public'),    
                (Deny, Everyone, ALL_PERMISSIONS)]
"""

def appmaker(request):
    if self.request.user: 
       return App 
    if not 'app_root' in zodb_root:
        app_root = MyModel()
        zodb_root['app_root'] = app_root
        import transaction
        transaction.commit()
    return zodb_root['app_root']



class App(object):
    __name__ = None
    __parent__ = None

    def __init__(self, request):
        self.request = request 

    def __getitem__(self, key):
        if key == 'messages': return Messages(key, self) 
        if key == 'forms': return Forms(self) 
        else:
            raise KeyError

class Forms(dict):
    def __init__(self, parent):
        self.__name__ = 'forms'
        self.__parent__ = parent 


class My(object):
    __acl__ = [ (Allow, Authenticated, ('view', 'add'))]   
    __name__ = 'my'
    def __init__(self, parent, request):
        self.__parent__ = parent
        self.__dict__.update(request.user.__dict__)


class Users(models.Users):
    __acl__ = [ (Allow, Authenticated, 'view')]   

    def __init__(self, parent):
        self.__name__ = 'users'
        self.__parent__ = parent

    def __getitem__(self, user):
        if user is None:
            raise KeyError

        resource = User(request.user.username, self)
        resource.__dict__.update(model.__dict__)
        return resource


class User(models.User, dict):
    def __init__(self, name, parent):
        self.__name__ = name
        self.__parent__ = parent
        self['chats'] = Chats(self)


class Message(models.Message):
    def __init__(self, name, parent):
        self.__name__   = name
        self.__parent__ = parent


class Messages(models.Messages):
    def __init__(self, name, parent):
        self.__name__ = name
        self.__parent__ = parent 

    def __getitem__(self, key):
        check_id(key)
        model = self.by_id(key)
        if not model:
            raise KeyError
        resource = Wish(key, self)
        resource.__dict__.update(model.__dict__) 
        return resource
