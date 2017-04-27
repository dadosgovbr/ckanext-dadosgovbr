import os
from ckan.plugins import implements, SingletonPlugin
from ckan.plugins import IRoutes

class DadosGovBrNewsSection(SingletonPlugin):
    '''The feed reader for the dados.gov.br site.

    Uses CKAN's IRoutes plugin interface to call the feed reader feature from this plugin
    package.

    '''
    implements(IRoutes, inherit=True)

    def before_map(self, map):
        map.connect('home', '/',
                    controller='ckanext.dadosgovbr.controllers.home:DadosGovBrHomeController',
                    action='index')
        return map

