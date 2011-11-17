from pyramid.threadlocal import get_current_request 
from pymongo.objectid import ObjectId
import datetime
from cryptacular import bcrypt 
from rubyrate.utility import DictDiffer

def remove_empty(dct):
    non_empty = dict((key, dct[key]) for key,value in dct.iteritems() 
        if value != '')
    return non_empty

def remove_private(dct):
    cleaned = dict((key, dct[key]) for key,value in dct.iteritems()
        if not key.startswith('__'))
    return cleaned

def prepare_for_db(dct):
    dct = remove_empty(dct)
    dct = remove_private(dct)
    return dct


class Collection(object):

     def by_id(self,_id):
        collection = get_current_request().db[self.__collection__]
        doc = collection.find_one({'_id': ObjectId(_id)})
        if doc:
            cls = self.__contains__
            obj = cls.__new__(cls)
            obj.__dict__ = doc
            return obj
   

class Crud(object):
    __collection__ = None

    def __init__(self, doc = None):
        if doc:
            for key, value in doc.iteritems():
                setattr(self, key, value)
        self.created = datetime.datetime.utcnow()

    def insert(self):
        clean = prepare_for_db(self.__dict__)
        collection = get_current_request().db[self.__collection__]
        _id = collection.insert(clean)
        self._id = _id

    def save(self):
        clean = prepare_for_db(self.__dict__)
        collection = get_current_request().db[self.__collection__]
        collection.save(clean)


#    def update(self, dct):
#        # first get orginal values ready 
#        original = prepare_for_db(self.__dict__)
#        # clean the new values for empties
#        new = prepare_for_db(dct)
#        # check original vs new values for changes
#        changed, removed = self.get_altered(new, original) 
#        collection = get_current_request().db[self.__collection__]
#        collection.update({'_id': self._id}, {'$set': changed})  # safe = True
#        #set the obj values
#        for key, value in changed.iteritems():
#            setattr(self, key, value)"""

    def remove(self):
        collection = get_current_request().db[self.__collection__]
        collection.remove({'_id':self._id})


    def get_altered(self, dct, origdict):
        differ  = DictDiffer(dct, origdict)
        changed = differ.changed()
        added   = differ.added()
        removed = differ.removed()
        # combine changed and added
        changed.update(added) 
        changed = dict((key, dct[key]) for key in changed)
        removed = dict((key, 1) for key in removed)
        return changed, removed 

class Wish(Crud):
    __collection__ = 'wishes'


class Wishes(Collection):
    __collection__ = 'wishes'
    __contains__ = Wish 

    def get_wishes(self):
        collection = get_current_request().db[self.__collection__]
        return collection.find().sort('created', -1)

    def by_user_id(self, _id):
        collection = get_current_request().db[self.__collection__]
        doc = collection.find_one({'user_id': _id})
        if doc:
            cls = self.__contains__
            obj = cls.__new__(cls)
            obj.__dict__ = doc
            return obj

    def get_wish_owner(self, _id):
        db = get_current_request().db
        doc = db.users.find_one({'_id': _id})
        return doc
        

class Convo(Collection):
    __collection__ = 'messages'



class Messages(Collection):
    __collection__ = 'messages'

    def get_messages(self, _id):
        collection = get_current_request().db[self.__collection__]
        result = collection.find( { 'ancestors' : _id } ).sort('created', -1)
        return result
            
    def already_sent_message(self, parent, username):                 
        collection = get_current_request().db[self.__collection__]
        result = collection.find_one({'parent': parent, 'username': username})  
        return result


class Message(Crud):
    __collection__ = 'messages'

    def __init__(self, doc = None, parent={}):
        self.ancestors = parent.get('ancestors', '')
        self.parent = parent.get('_id', '')
        self.created  = datetime.datetime.utcnow()
        if doc: 
            for key, value in doc.iteritems():
                setattr(self, key, value)


class Admin(object):
    pass


class User(Crud):
    __collection__ = 'users'

    def __init__(self, data=None):
        self.created  = datetime.datetime.utcnow()
        if data:
            for key, value in data.iteritems():
                setattr(self, key, value)

    def __setattr__(self, name, value):
        if name == 'password': 
            crypt = bcrypt.BCRYPTPasswordManager()
            object.__setattr__(self, name, crypt.encode(value))
        else:
            object.__setattr__(self, name, value)

    def check_password(self, freshly_submitted):
        crypt = bcrypt.BCRYPTPasswordManager()
        result =  crypt.check(self.password, freshly_submitted)
        return result


class Users(Collection):
    __collection__ = 'users'
    __contains__ = User 

    def by_username(self, name):
        collection = get_current_request().db[self.__collection__]
        doc = collection.find_one({'username': name})
        if doc:
            cls = self.__contains__
            obj = cls.__new__(cls)
            obj.__dict__ = doc
            return obj
