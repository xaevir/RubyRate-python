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


def del_autos(node, kw):
    if kw=='just_id':
        del node['_id']
    else: 
        del node['_id']
        del node['created']

def just_key(node, kw):
    message = kw.get('message')
    keep = node[message]
    node.children = [keep]


class Root(dict):
    __name__ = None
    __parent__ = None

    def __init__(self, request):
        self.request = request
        self.request.loggedin = authenticated_userid(request)
        self['wishes'] = Wishes(self) 
        self['users'] = Users(self) 
        self['admin'] = Admin(self) 


class Wishes(object):
    __name__ = 'wishes'
    schema = schemas.Wish

    def __init__(self, parent):
        self.__parent__ = parent 
        self.request    = parent.request
        self.Model      = models.Wish

    def __getitem__(self, key):
        check_id(key)
        doc = self.Model.by_id(key, self.Model)
        if not doc:
            raise KeyError
        # set obj attrs 
        self.model   = self.Model(doc)
        wish         = Wish(key, self)
        wish.schema  = self.schema
        wish.model   = self.model
        wish.__acl__ = [ (Allow, Everyone, 'view'),
                         (Allow, 'group:admin', 'edit') ]
        return wish

class Wish(dict):
    def __init__(self, name, parent):
        self.__name__   = name
        self.__parent__ = parent 
        self.request    = parent.request
        self['replies'] = Replies(self)
        self['emails']  = Emails(self)

class Replies(object):
    __name__ = 'replies'
    schema = schemas.Reply

    def __init__(self, parent):
        self.__parent__ = parent 
        self.request    = parent.request
        self.Model      = models.Reply

    def __getitem__(self, key):
        check_id(key)
        doc = self.Model.by_id(key, self.Model)
        if not doc:
            raise KeyError
        self.model   = self.Model(doc)
        reply        = Reply(key, self)
        reply.schema = self.schema
        reply.model  = self.model
        reply.__acl__ = [ (Allow, Everyone, 'view'),
                         (Allow, 'group:admin', 'edit') ]
        return reply


class Reply(object):
    def __init__(self, name, parent):
        self.__name__   = name
        self.__parent__ = parent 


class Emails(object):
    __name__ = 'emails'
    schema = schemas.Email

    def __init__(self, parent):
        self.__parent__ = parent 
        self.request    = parent.request
        self.Model      = models.Email

    def __getitem__(self, key):
        check_id(key)
        doc = self.Model.by_id(key, self.Model)
        if not doc:
            raise KeyError
        self.model   = self.Model(doc)
        email        = Email(key, self)
        email.schema = self.schema
        email.model  = self.model
        email.__acl__ = [ (Allow, Everyone, 'view'),
                         (Allow, 'group:admin', 'edit') ]
        return email

class Email(object):
    def __init__(self, name, parent):
        self.__name__   = name
        self.__parent__ = parent 


class Admin(object):
    __name__ = 'admin'
    __acl__ = [ (Allow, 'group:admin', 'view')]

    def __init__(self, parent):
        self.__parent__ = parent 

    def get_items(self):
        db = self.request.db
        return db.wishes.find()



def groupfinder(name, request):
    user = models.User.by_username(name)
    # If the user is in the db then they have passed validation and are 
    # a member. Since every user will be a member it does not make sense to
    # add this field to the db. I will only add it if they are admins, etc...
    # If down the road, I add an email verification, then I will alter this.
    if user:
        groups = getattr(user, 'groups', ['member'])
        return ['group:%s'%group for group in groups]


class Users(object):
    __name__ = 'users'
    schema = schemas.User

    def __init__(self, parent):
        self.__parent__ = parent 
        self.request    = parent.request
        self.Model      = models.User

    def __getitem__(self, key):
        check_id(key)
        doc = self.Model.by_username(key)
        if not doc:
            raise KeyError
        self.model  = self.Model(doc)
        user        = User(key, self)
        user.schema = self.schema
        user.model  = self.model
        user.__acl__ = [ (Allow, Everyone, 'view'),
                         (Allow, 'group:admin', 'edit') ]
        return user


class User(object):
    def __init__(self, name, parent):
        self.__name__   = name
        self.__parent__ = parent 



