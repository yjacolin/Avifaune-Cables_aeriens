# -*- coding: utf-8 -*-
from pyramid.config import Configurator
import sqlalchemy
import sqlahelper

from pyramid_beaker import session_factory_from_settings

PROFILES = {}


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    for p in ['rte', 'enedis', 'ogm']:
        PROFILES[settings['profile.%s' % p]] = p

    session_factory = session_factory_from_settings(settings)
    config = Configurator(settings=settings, session_factory=session_factory)

    config.include('pyramid_mako')

    # initialize database
    engine = sqlalchemy.engine_from_config(settings, 'sqlalchemy.')
    sqlahelper.add_engine(engine)

    # add the "geojson" renderer
    config.add_renderer(name='csv', factory='cables.renderers.CSVRenderer')

    # add routes to the entry view class
    config.add_route('export_zonessensibles', '/export/zonessensibles')
    config.add_route('export_communes', '/export/communes')
    config.add_route('export_departements', '/export/departements')
    config.add_route('profile', '/profile')
    config.scan()

    # add the static view (for static resources)
    config.add_static_view('static', 'cables:static')

    return config.make_wsgi_app()

