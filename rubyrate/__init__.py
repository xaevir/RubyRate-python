from pyramid.config import Configurator
from pyramid_beaker import session_factory_from_settings
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy

from pyramid.security import authenticated_userid

from pyramid.httpexceptions import HTTPUnauthorized

from rubyrate.resources import groupfinder
from rubyrate.resources import Root

from pyramid.events import subscriber
from pyramid.events import BeforeRender
from pyramid.events import NewRequest
from pyramid.url import static_url

from pkg_resources import resource_filename
from deform import ZPTRendererFactory
from rubyrate.my_deform.form import Form

from gridfs import GridFS
import pymongo

import os

import logging
log = logging.getLogger(__name__)

here = os.path.dirname(os.path.abspath(__file__))

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    # email to send forms
    settings['from'] = 'ruby_robot@rubyrate.com'
    settings['to'] = 'ruby@rubyrate.com'

    settings['session.secret'] = 'u3wawf7jmvypAz8hpE8Yfu7J4fGZzbkg'
    settings['session.key'] = 'rubyrate' 
    settings['session.auto'] = True 
    settings['session.cookie_expires'] = True 
    settings['session.type'] = 'file' 

    settings['session.data_dir'] = here + '/data/sessions/data'     
    settings['session.lock_dir'] = here + '/data/sessions/lock' 

    settings['mako.directories'] = 'rubyrate:templates'
    settings['mako.module_directory'] = 'rubyrate:data/templates'
    settings['mako.imports'] = ['from webhelpers.html import escape',
                                'from webhelpers.html import literal']
    settings['mako.default_filters'] = ['escape']

    # adding the renderer to my own version of form
    deform_templates = resource_filename('deform', 'templates')
    search_path = (here + '/templates/deform') #, deform_templates
    #settings['deform.renderer'] = ZPTRendererFactory(search_path)
    settings['deform.searchpath'] = here + '/templates/deform'

    Form.set_zpt_renderer(search_path)

    authn_policy = AuthTktAuthenticationPolicy(
        secret='u3wawf7jmvypAz8hpE8Yfu7J4fGZzbkg',          
        callback=groupfinder)
    authz_policy = ACLAuthorizationPolicy()

    config = Configurator(root_factory=Root,
        settings=settings,
        authentication_policy=authn_policy,
        authorization_policy=authz_policy)

    config.set_session_factory(session_factory_from_settings(settings))

    # Mongo Setup
    conn = pymongo.Connection('mongodb://localhost/')
    config.registry.settings['db_conn'] = conn

    config.include('pyramid_mailer')

    config.add_static_view('static', 'rubyrate:static')
    config.scan('rubyrate')

    return config.make_wsgi_app()


@subscriber(NewRequest)
def add_mongo_db(event):
    settings = event.request.registry.settings
    db = settings['db_conn'][settings['db_name']]
    event.request.db = db
    event.request.fs = GridFS(db)  


@subscriber(NewRequest)
def csrf_validation_event(event):
    request = event.request
    user = authenticated_userid(request)
    csrf = request.params.get('csrf_token')
    if (request.method == 'POST' or request.is_xhr) and \
       (user) and \
       (csrf != unicode(request.session.get_csrf_token())):
        raise HTTPUnauthorized
