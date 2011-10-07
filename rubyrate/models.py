from pyramid.threadlocal import get_current_request 
from pymongo.objectid import ObjectId
import datetime
from cryptacular import bcrypt 

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

class Crud(object):
    __collection__ = None

    def __init__(self, doc):
        for key, value in doc.iteritems():
            setattr(self, key, value)
        self.created = datetime.datetime.utcnow()

    @staticmethod
    def by_id(_id, cls):
        collection = get_current_request().db[cls.__collection__]
        doc = collection.find_one({'_id': ObjectId(_id)})
        if doc is None:
            return 
        return doc 

    def insert(self):
        clean = prepare_for_db(self.__dict__)
        collection = get_current_request().db[self.__collection__]
        _id = collection.insert(clean)
        return _id

    def update(self):
        clean = prepare_for_db(self.__dict__)
        collection = get_current_request().db[self.__collection__]
        collection.update({'_id': self._id}, {'$set': clean})  # safe = True


    def remove(self):
        collection = self.__db__[self.__collection__]
        self.collection.remove({'_id':self._id})

class Wish(Crud):
    __collection__ = 'wishes'

    @staticmethod
    def get_all_without_email(cls):
        collection = get_current_request().db[cls.__collection__]
        return collection.find( {}, { 'email' : 0 }).sort('created', -1)


class Reply(Crud):
    __collection__ = 'replies'


    @staticmethod
    def all_by_parent(_id, cls):
        if not isinstance(_id, str):
            raise Exception
        collection = get_current_request().db[cls.__collection__]
        return collection.find({'parent': _id})


class Email(Crud):
    __collection__ = 'emails'


class User(Crud):
    __collection__ = 'users'
    __uses_descriptor__ = True

    def __init__(self, data):
        password = data.pop('password')
        self.set_password(password)
        self.created  = datetime.datetime.utcnow()
        for key, value in data.iteritems():
            setattr(self, key, value)

    def set_password(self, value):
        crypt = bcrypt.BCRYPTPasswordManager()
        self.password =  crypt.encode(value)

    @staticmethod
    def check_password(freshly_submitted, from_db):
        crypt = bcrypt.BCRYPTPasswordManager()
        return crypt.check(from_db, freshly_submitted)

    @staticmethod
    def by_username(name):
        collection = get_current_request().db[User.__collection__]
        doc = collection.find_one({'username': name})
        if doc is None:
            return 
        return doc 
        
