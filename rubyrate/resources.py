from rubyrate.mongobase import Base
import datetime
from pyramid.threadlocal import get_current_request 

def get_db():
    request = get_current_request()
    return request.db

class Root(object):
    __name__ = None
    __parent__ = None
    def __init__(self, request):
        self.request = request
    def __getitem__(self, key):
        if key == 'need-pricing':
            return Items(key, self)
        else:
            raise KeyError

class Items(object):
    __collection__ = 'item'
    def __init__(self, name, parent):
        self.__name__   = name
        self.__parent__ = parent 

    def get_recent(self):
        db = get_db()
        collection = db[self.__collection__]
        return collection.find()
       

class Item(Base):
    __collection__ = 'item'
    def __init__(self, data):
        self.created = datetime.datetime.now()
        self.setFlexAttrs(data)

    @staticmethod
    def by_username(name):
        """Restore the user from DB or return None"""
        db = get_db()
        doc = db.user.find_one({'username': name})
        if doc is None:
            return 
        return restore(User, doc)


