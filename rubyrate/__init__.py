from pyramid.config import Configurator
from rubyrate.resources import Root

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(root_factory=Root, settings=settings)
    config.add_view('rubyrate.views.my_view',
                    context='rubyrate:resources.Root',
                    renderer='rubyrate:templates/mytemplate.pt')
    config.add_static_view('static', 'rubyrate:static')
    return config.make_wsgi_app()

