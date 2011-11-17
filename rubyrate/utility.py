import re
import colander
from pyramid.httpexceptions import HTTPFound

from rubyrate.my_deform.form import Button
from rubyrate.my_deform.form import Form


import string
import random
def id_generator(size=6, chars=string.ascii_uppercase + string.digits + 
                 string.ascii_lowercase):
    return ''.join(random.choice(chars) for x in range(size))


def create_form(request, schema):
    action = request.view_name
    if action == 'create': 
        button_title = 'Create'
        method = 'POST'
    if action == 'edit': 
        button_title = 'Update'
        method = 'PUT'
    form = Form(schema, 
                _method = method, 
                buttons = (Button(
                               title= button_title, 
                               css_class='btn'),))
    return form


def render_form(schema, request, appstruct=colander.null, form=None,redirect=True,
                success=None, readonly=False, flash=True):
    if not form:
        form = create_form(request, schema)

    if request.method == 'GET': 
        html = form.render(appstruct, readonly=readonly)
        return {'form': html}
    # validate 
    try:
        controls = request.POST.items()
        captured = form.validate(controls)
    except deform.ValidationFailure, e:
        return {'form': e.render()}
    # passed validation
    if request.POST['_method'] == 'PUT':
        request.context.update(captured)
        flash_msg = 'Updated'
        url = request.resource_url(request.context.__parent__.__parent__)
    if request.POST['_method'] == 'POST':
        #initialize model
        raise Exception('have to add specific model as a parameter')
        request.context = request.context.Model(captured)
        request.context.model.insert()
        flash_msg = 'Created'
    if success:
        return success(request)
    if flash:
        request.session.flash(flash_msg)
    if redirect:
        url = request.resource_url(request.context)
        raise HTTPFound(url)  
    else:
        return form.render(captured)



def allowed_methods(*allowed):
    '''Custom predict checking if the HTTP method in the allowed set.
    It also changes the request.method according to "_method" form parameter
    and "X-HTTP-Method-Override" header
    '''
    def predicate(info, request):
        if request.method == 'POST':
            request.method = (
                request.POST.get('_method', '').upper() or
                request.headers.get('X-HTTP-Method-Override', '').upper() or
                request.method)
 
        return request.method in allowed
    return predicate


def slugify(name):
    filter = { 
        '&+' : 'and', # replace & with 'and'              
        '[^a-zA-Z0-9]+' : '_', # non-alphanumeric characters with a hyphen
        '-+' : '_' # replace multiple hyphens with a single hyphen
    }
    for k, v in filter.items():
        name = re.sub(k, v, name)
    name = name.strip('_') 
    return name	


class DictDiffer(object):
    """
    Calculate the difference between two dictionaries as:
    (1) items added
    (2) items removed
    (3) keys same in both but changed values
    (4) keys same in both and unchanged values
    """
    def __init__(self, current_dict, past_dict):
        self.current_dict, self.past_dict = current_dict, past_dict
        self.set_current, self.set_past = set(current_dict.keys()), set(past_dict.keys())
        self.intersect = self.set_current.intersection(self.set_past)
    def added(self):
        return self.set_current - self.intersect 
    def removed(self):
        return self.set_past - self.intersect 
    def changed(self):
        return set(o for o in self.intersect if self.past_dict[o] != self.current_dict[o])
    def unchanged(self):
        return set(o for o in self.intersect if self.past_dict[o] == self.current_dict[o])


def pretty_date(time=False):
    """
    Get a datetime object or a int() Epoch timestamp and return a
    pretty string like 'an hour ago', 'Yesterday', '3 months ago',
    'just now', etc
    """
    from datetime import datetime
    from pytz import timezone
    import pytz
    now = datetime.utcnow()
    #now = datetime.now()
    if type(time) is int:
        diff = now - datetime.fromtimestamp(time)
    elif isinstance(time,datetime):
        diff = now - time 
    elif not time:
        diff = now - now
    second_diff = diff.seconds
    day_diff = diff.days

    if day_diff < 0:
        return ''

    if day_diff == 0:
        if second_diff < 10:
            return "just now"
        if second_diff < 60:
            return str(second_diff) + " seconds ago"
        if second_diff < 120:
            return  "a minute ago"
        if second_diff < 3600:
            return str( second_diff / 60 ) + " minutes ago"
        if second_diff < 7200:
            return "an hour ago"
        if second_diff < 86400:
            return str( second_diff / 3600 ) + " hours ago"
    if day_diff == 1:
        return "Yesterday"
    if day_diff < 7:
        return str(day_diff) + " days ago"
    if day_diff < 31:
        return str(day_diff/7) + " weeks ago"
    if day_diff < 365:
        return str(day_diff/30) + " months ago"
    return str(day_diff/365) + " years ago"

