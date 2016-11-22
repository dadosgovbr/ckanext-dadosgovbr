import os
from ckan.plugins import implements, SingletonPlugin
from ckan.plugins import IRoutes
from ckan.config.routing import SubMapper

class DadosGovBrDatasetView(SingletonPlugin):
    '''The customized dataset view screen.
    '''
    implements(IRoutes, inherit=True)

    def before_map(self, map):
        # Default mappings copied from ckan/config/routing.py that we want to preserve.
        with SubMapper(map, controller='package') as m:
            m.connect('/dataset/{action}',
                requirements=dict(action='|'.join([
                    'list',
                    'new',
                    'autocomplete',
                    'search'
                    ]))
            )
            m.connect('/dataset/{action}/{id}/{revision}', action='read_ajax',
                requirements=dict(action='|'.join([
                    'read',
                    'edit',
                    'authz',
                    'history',
                ]))
            )
            m.connect('/dataset/{action}/{id}',
                requirements=dict(action='|'.join([
                    'edit',
                    'editresources',
                    'authz',
                    'history',
                    'read_ajax',
                    'history_ajax',
                ]))
            )
            m.connect('/dataset/{id}.{format}', action='read')
            m.connect('/dataset/{id}/resource/{resource_id}', action='resource_read')
            
        # Our new custom mapping.
        map.connect('/dataset/{id}',
            controller='ckanext.dadosgovbr.controllers.package:DadosGovBrDatasetController',
            action='read')
        return map

