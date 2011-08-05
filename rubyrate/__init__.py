from pyramid.config import Configurator
from rubyrate.resources import Root

from pyramid.events import subscriber
from pyramid.events import BeforeRender
from pyramid.url import static_url


import os

from pyramid_beaker import session_factory_from_settings

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """

    settings['session.secret'] = os.urandom(32)
    settings['session.key'] = 'rubyrate' 
    settings['session.auto'] = True 

    settings['mako.directories'] = 'rubyrate:templates'
    settings['mako.module_directory'] = 'rubyrate:data/templates'
    settings['mako.imports'] = ['from webhelpers.html import escape',
                                'from webhelpers.html import literal']
    settings['mako.default_filters'] = ['escape']

    config = Configurator(root_factory=Root, settings=settings)

    config.set_session_factory(session_factory_from_settings(settings))

    config.add_static_view('static', 'rubyrate:static')
    config.scan('rubyrate')
    config.include('pyramid_mailer')
    return config.make_wsgi_app()


#@subscriber(BeforeRender)
#def add_global(event):
    #event['h'] = static_url
#    eventt['literal'] = 
