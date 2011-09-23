from copy import deepcopy
from rubyrate.utility import DictDiffer
from pyramid.threadlocal import get_current_request 
from pprint import pprint
#write later as list comprehension

def remove_empty(dct):
    non_empty = dict((key, dct[key]) for key,value in dct.iteritems() 
        if value != '')
    return non_empty

def remove_traversal(dct):
    cleaned = dict((key, dct[key]) for key,value in dct.iteritems() 
        if not key.startswith('__'))
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
    try:
        obj.__uses_descriptor__
        # check for intersection of class properties and database keys 
        # Using a property decorator, the function name would be the same as 
        # the database key
        a = set(dir(obj))
        b = set(attrs.keys())
        intersect = a.intersection(b)
        if intersect:
            attrs = mangle_keys(intersect, attrs, obj.__class__.__name__) 
    except AttributeError: 
        pass
    obj.__dict__ = attrs
    return obj

def mongosave(self, dct = None):
    attrs = dct or self.__dict__
    collection = self.__collection__
    db = get_current_request().db
    non_empty = remove_empty(attrs)
    cleaned = remove_traversal(non_empty)
    if not hasattr(self, '_id'):
        return db.collection.insert(cleaned)
    # record already exists so check for altered
    changed, removed = get_altered(cleaned, self.__origdict__) 
    if changed: #cld be calling save on obj not changed so not need for db   
        db.collection.update({'_id': self._id}, {'$set': changed})  # safe = True
    if removed:
        db.collection.update({'_id': self._id}, {'$unset': removed})

def remove(self):
    db = get_current_request().db
    db.collection.remove({'_id':self._id})


