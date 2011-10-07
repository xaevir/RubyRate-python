#write later as list comprehension


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


