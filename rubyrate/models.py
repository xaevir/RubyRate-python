from pyramid.threadlocal import get_current_request 
from pymongo.objectid import ObjectId
import datetime
from cryptacular import bcrypt 
from rubyrate.utility import DictDiffer
from rubyrate.utility import slugify
from bson.code import Code

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
            cls = self.__model__
            obj = cls.__new__(cls)
            obj.__dict__ = doc
            return obj
   

class Model(object):
    __collection__ = None

    def __init__(self, doc = None):
        if doc:
            for key, value in doc.iteritems():
                setattr(self, key, value)

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

class Wish(Model):
    __collection__ = 'messages'

    def update_with_username(self, user):
        collection = get_current_request().db[self.__collection__]
        collection.update({'user_id': user._id}, 
                          {'$set': {'username':user.username}})


class Wishes(Collection):
    __collection__ = 'messages'
    __model__ = Wish 

    def get_wishes(self):
        collection = get_current_request().db[self.__collection__]
        return collection.find({'labels': 'wish'}).sort('created', -1)

    def by_user_id(self, _id):
        collection = get_current_request().db[self.__collection__]
        doc = collection.find_one({'user_id': _id})
        if doc:
            cls = self.__model__
            obj = cls.__new__(cls)
            obj.__dict__ = doc
            return obj

    def get_wish_owner(self, _id):
        db = get_current_request().db
        doc = db.users.find_one({'_id': _id})
        return doc
        

class MyWish(Model):
    __collection__ = 'wishes'


class MyWishes(Collection):
    __collection__ = 'wishes'
    __model__ = MyWish 

    def get_wishes(self):
        request = get_current_request()
        user = request.user  
        collection = request.db[self.__collection__]
        return collection.find({'user_id':user._id}).sort('created', -1)


class Chat(Model):
    __collection__ = 'chats'

    def push(self, message):
        collection = get_current_request().db[self.__collection__]
        now = datetime.datetime.utcnow()
        message['created'] = now 
        request = get_current_request()
        for _id in self.shared_by:
            if request.user._id != _id:
                other_id = _id
        
        collection.update({'_id': self._id, 'user_data._id': other_id}, 
                          {'$push': {'messages': message},
                           '$set': {'date_modified': now },
                           '$inc': {'user_data.$.new' : 1},  
                           })

    def push_all(self, messages):
        collection = get_current_request().db[self.__collection__]
        now = datetime.datetime.utcnow()
        messages[1]['created'] = now 
        collection.update({'_id': self._id}, 
                          {'$pushAll': {'messages': messages},
                           '$set': {'date_modified': now }})
                                     

class Chats(Collection):
    __collection__ = 'chats'
    __model__ = Chat

    def exists(self, user_id, subject_id):
        collection = get_current_request().db[self.__collection__]
        doc = collection.find_one({'shared_by': user_id, 'subject_id': subject_id})
        return doc

    def get_chats(self):
        request = get_current_request()
        user = request.user  
        collection = request.db[self.__collection__]
        return collection.find({'shared_by':user._id}).sort('created', -1)

    def update_with_username(self, subject_id, user):
        request = get_current_request()
        collection = request.db[self.__collection__]
        collection.update({'subject_id': subject_id}, 
                          {'$set': {'messages.0.username':user.username}}, 
                          upsert=False, multi=True, safe=True)

    def nav(self):
        request = get_current_request()
        user = request.user  
        collection = get_current_request().db[self.__collection__]

        map = Code("function() {"
                "if (!this.messages) {"
                     " this.messages = new Array();"
                 "}"
                   "    var msg_total = this.messages.length;"
                   "    var key = {wish_id: this._id, subject_id: this.subject_id," 
                                  "content: this.subject_content,};"
                   "    emit( key, {msg_total: msg_total});"
                   "}")

        reduce = Code("function(key, values) {"
                      "    var total = 0;"
                      "    values.forEach(function(doc) {"
                      "        total += doc.msg_total;"
                      "    });"
                      "    return {msg_total: total};"
                      "}")
        result = collection.map_reduce(map, reduce, "nav", query={"shared_by": user._id} )
        arr = []
         
        for doc in result.find():
            x = {} 
            x.update(doc['_id'])
            x.update(doc['value'])
            for key, value in x.items():
                if not isinstance(value, str):
                    x[key] = str(value)
            #doc['_id'].extend( ) 
            #doc['_id'] = str(doc['_id'])
            arr.append(x)
        return arr            

class Message(Model):
    __collection__ = 'messages'
    def init(self, args):
        for key, value in args.iteritems():
            setattr(self, key, value)

#    def post(self):
#        db = get_current_request().db
#        db.messages.insert(self.__dict__)
                

class Messages(object):



    def send(self, subject_id, body, recipient):
        db = get_current_request().db
        user = request.user  

        message = Message(subject, body)   
        message.labels = [{'name':'sent'}]
        message.recipient = recipient

        Chat = Chats().get_if_exists(message)

        if chat is None:
            chat = Chat(message) 
            chat.insert()
        else:
            db.chats.update({'_id': chat._id}, 
                      {'$push': {'messages': message.__dict__},
                       '$set': {'modified': message._id.generation_time()},
                       '$inc': {'total' : 1},  
                       })

        self.receive(subject_id, body, recipient, sender)


    def receive(message):
        db = get_current_request().db
        user = request.user  
        chat = Chats().get_if_exists(user, subject_id, recipient)

        if chat is None:
            chat = Chat() 
            chat._id = ObjectId()
            chat.user_id = user._id 
            chat.username = user.username 

        message = Message()   
        message._id = ObjectId()
        message.subject_id = subject_id
        message.body = body
        message.labels = [{'name':'inbox'}]
        message.sent_by = 'jose'
        db.mailboxes.update({'username': recipient}, {'$push': {'messages': message.__dict__ }})

    


class Chat(Model):
    def init(self, message):
        user = get_current_request().user
        self.modified = message._id.generation_time() 
        self.user_id = user._id 
        self.username = user.username 
        self.msg_total = 1  
        self.messages = [message._dict__] 

    def insert(self):
        request = get_current_request()
        user = request.user  
        db = request.db
        db.chats.insert(self.__dict__)

    

class Chats(object):
    # collection = mailboxes    
    def get_if_exists(self, subject_id, user, recipient=None, sender=None):
        request = get_current_request()
        db = request.db
        if sender:
            doc = db.chats.find_one({'subject_id': subject_id , 'user_id': user._id,
                                             '$or': [{'messages.recipient': sender} , 
                                                     {'messages.sender': sender}]})
        if recipient:
            doc = db.chats.find_one({'subject_id': subject_id , 'user_id': user._id,
                                             '$or': [{'messages.recipient': recipient},
                                                     {'messages.sender': recipient}]})
        if doc:
            cls = self.__model__
            obj = cls.__new__(cls)
            obj.__dict__ = doc
            return obj

         
"""    


class MessagesOld(Collection):
    __collection__ = 'messages'

    def messages_of_parent(self, parent_id):
        collection = get_current_request().db[self.__collection__]
        result = collection.find( { 'parent' : parent_id } ).sort('created', -1)
        return result
            
    def already_sent_message(self, parent, username):                 
        collection = get_current_request().db[self.__collection__]
        result = collection.find_one({'parent': parent, 'username': username})  
        return result

    def chat(self, ancestor_id, user):
        collection = get_current_request().db[self.__collection__]
        result = collection.find( { 'ancestor' : ancestor_id,  } ).sort('created', -1)
        return result



class MessageOld(Model):
    __collection__ = 'messages'

    def __init__(self, doc):
        self.created  = datetime.datetime.utcnow()
        self.username = doc['username']
        self.content = doc['content'] 

"""
class Admin(object):
    pass


class User(Model):
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
        elif name == 'username':
            object.__setattr__(self, 'slug', slugify(value))
            object.__setattr__(self, name, value)
        else:
            object.__setattr__(self, name, value)

    def check_password(self, freshly_submitted):
        crypt = bcrypt.BCRYPTPasswordManager()
        result =  crypt.check(self.password, freshly_submitted)
        return result

    def get_nav(self):
        pass 


class Users(Collection):
    __collection__ = 'users'
    __model__ = User 


    def by_login(self, name):
        collection = get_current_request().db[self.__collection__]
        doc = collection.find_one({'username': name})
        if doc is None:
            doc = collection.find_one({'email': name})
        if doc:
            cls = self.__model__
            obj = cls.__new__(cls)
            obj.__dict__ = doc
            return obj
       


    def by_username(self, name):
        collection = get_current_request().db[self.__collection__]
        doc = collection.find_one({'username': name})
        if doc:
            cls = self.__model__
            obj = cls.__new__(cls)
            obj.__dict__ = doc
            return obj

    def by_email(self, name):
        collection = get_current_request().db[self.__collection__]
        doc = collection.find_one({'email': name})
        if doc:
            cls = self.__model__
            obj = cls.__new__(cls)
            obj.__dict__ = doc
            return obj
