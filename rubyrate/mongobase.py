from copy import deepcopy
from rubyrate.utility import DictDiffer
from pyramid.threadlocal import get_current_request 
#write later as list comprehension
def remove_empty(dct):
    cleaned = {}
    for key, value in dct.items():
        if not value:
            continue 
    cleaned[key] = value
    return cleaned

def remove_extra(dct):
    cleaned = {}
    # the value cld be empty from form submit of non required field
    for key, value in dct.items():
        if not value:
            continue 
        # traversal needs the __name__, __parent__ attrs
        if key.startswith('__'):
            continue
        cleaned[key] = value
    return cleaned

def unmangle(dct, classname):
    """undo mangling of private vars"""
    private_var_beginning = '_%s__' % classname 
    for key, value in dct.items():
        if key.startswith(private_var_beginning):
            private_var = dct.pop(key) 
            key = key.replace(private_var_beginning, '')  
            dct[key] = private_var 
    return dct

def mangle_keys(intersect, dct, classname):
    """replace private var with its mangled name"""
    for key in intersect:
        dct['_'+classname+'__'+key] = dct[key]
        dct.pop(key)
    return dct

def get_altered(dct, origdict):
    differ  = DictDiffer(dct, origdict)
    changed = differ.changed()
    added   = differ.added()
    removed = differ.removed()
    # combine changed and added
    changed.update(added) 
    changed = dict((key, dct[key]) for key in changed)
    removed = dict((key, 1) for key in removed)
    return changed, removed 

def restore(cls, attrs):
    cls.__origdict__ = deepcopy(attrs) #otherwise its getting updated by shallow copy     
    obj = cls.__new__(cls)
    # chk if propery name same as class name 
    # which wld be a property decorator
    a = set(dir(obj))
    b = set(attrs.keys())
    intersect = a.intersection(b)
    if intersect:
        attrs = mangle_keys(intersect, attrs, obj.__class__.__name__) 
    obj.__dict__ = attrs
    return obj


class Base(object):
    def save(self):
        db = get_current_request().db
        collection = db[self.__collection__]
        dct = remove_extra(self.__dict__)
        dct = unmangle(dct, self.__class__.__name__)
        if not hasattr(self, '_id'):
            return collection.insert(dct)
        changed, removed = get_altered(dct, self.__origdict__) 
        if changed: #cld be calling save on obj not changed so not need for db   
            collection.update({'_id': self._id}, {'$set': changed})  # safe = True
        if removed:
            collection.update({'_id': self._id}, {'$unset': removed})
    def remove(self):
        db = get_db()
        collection = db[self.__collection__]
        collection.remove({'_id':context._id})
    

