# -*- coding: utf-8 -*-

import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from ckan.lib.base import c, g, h, model
from ckan.common import OrderedDict

from ckan.plugins import implements, SingletonPlugin
from ckan.plugins import IConfigurer
from ckan.plugins import IRoutes

# Wordpress integration
import ckanext.dadosabertos.helpers.wordpress as wp

# Custom helper tools
import ckanext.dadosabertos.helpers.tools as tools


class DadosabertosPlugin(plugins.SingletonPlugin, toolkit.DefaultDatasetForm):
    ''' Plugin Dados Abertos

        Classe principal.
        - Define recriação do schema do Solr
        - Define diretórios para imagens, CSS e JS
        - Define mapeamento para novas rotas
        - Define novos helpers
    '''
    plugins.implements(plugins.IPackageController)
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.ITemplateHelpers)
    implements(IConfigurer, inherit=True)
    implements(IRoutes, inherit=True)



    # Recriação do schema (Solr)
    # =======================================================
    def read(self, entity):
        pass

    def create(self, entity):
        pass

    def edit(self, entity):
        pass

    def authz_add_role(self, object_role):
        pass

    def authz_remove_role(self, object_role):
        pass

    def delete(self, entity):
        pass

    def before_search(self, search_params):
        # Redirect for search page
        schemas = ['concurso', 'aplicativo', 'inventario']
        url_current = h.full_current_url()
        if(url_current.replace(g.site_url+'/','') in schemas):
            from pylons.controllers.util import redirect
            redirect(url_current.replace(g.site_url,'')+'s')
        return search_params

    def after_search(self, search_results, search_params):
        return search_results

    def before_index(self, data_dict):
        import json, pprint

        # All multiValue fields from ckanext-scheming
        multiValue = ['dados_abertos_base', 'atualizacoes_base', 'informacoes_publicas_base']

        for i, value in enumerate(multiValue):
            # If package has "multiValue"
            if('extras_'+value in data_dict):
                # Add to Solr schema
                data_dict[multiValue[i]] = []

                # If package has multi value for multiValue field
                try:
                    for item in json.loads(data_dict['extras_'+value]):
                        data_dict[multiValue[i]].append(item)
                    #print(data_dict[multiValue[i]])
                
                # If package has just one value for multiValue field
                except:
                    data_dict[multiValue[i]].append(data_dict['extras_'+value])
                    #print(data_dict['extras_'+value])
        return data_dict

    def before_view(self, pkg_dict):
        # Redirect to correct URL based on schema name
        actions_accepted = ['read','edit','new']
        if (c.action in actions_accepted and c.controller=='package'):
            schema_expected = pkg_dict['type']
            schema_current  = str(h.full_current_url()).replace(g.site_url, '').split('/')[1]
            if (schema_current != schema_expected):
                from pylons.controllers.util import redirect
                url_current = h.full_current_url()
                url_current = str(url_current).replace(g.site_url+'/'+schema_current, g.site_url+'/'+schema_expected)
                # print('redir_to',url_current)
                # print(schema_expected)
                # print(schema_current)
                redirect(url_current.replace(g.site_url,''))
        return pkg_dict

    def after_create(self, context, data_dict):
        return data_dict

    def after_update(self, context, data_dict):
        return data_dict

    def after_delete(self, context, data_dict):
        return data_dict

    def after_show(self, context, data_dict):
        return data_dict

    def update_facet_titles(self, facet_titles):
        return facet_titles


    # Diretórios para templates e arquivos estáticos
    # =======================================================
    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        #toolkit.add_resource('fanstatic', 'dadosabertos')

    
    
    # Mapeamento das URLs
    # =======================================================
    def before_map(self, map):
        map.connect('/organization/{id}',
                    controller='ckanext.dadosabertos.controllers.scheming_organization:TestController',
                    action='read_dataset',
                    id=0)
        map.connect('/organization/aplicativos/{id}',
                    controller='ckanext.dadosabertos.controllers.scheming_organization:TestController',
                    action='read_aplicativo',
                    id=0)
        map.connect('/organization/concursos/{id}',
                    controller='ckanext.dadosabertos.controllers.scheming_organization:TestController',
                    action='read_concurso',
                    id=0)
        return map



    # Mapeamento das URLs
    # =======================================================
    def after_map(self, map):
        # Testing
        map.connect('/test',
                    controller='ckanext.dadosabertos.controllers.test:TestController',
                    action='index')

        map.connect('/test/{id}',
                    controller='ckanext.dadosabertos.controllers.test:TestController',
                    action='read',
                    id=0)

        # ckanext-scheming
        map.connect('/aplicativos',
                    controller='ckanext.dadosabertos.controllers.scheming:SchemingPagesController',
                    action='search')
        # map.connect('/aplicativos',
        #             controller='ckanext.dadosabertos.controllers.aplicativos:AplicativosController',
        #             action='index')
        map.connect('/aplicativos_busca/{title}',
                    controller='ckanext.dadosabertos.controllers.aplicativos:AplicativosController',
                    action='single')
        map.connect('/inventarios',
                    controller='ckanext.dadosabertos.controllers.scheming:SchemingPagesController',
                    action='search')
        map.connect('/concursos',
                    controller='ckanext.dadosabertos.controllers.scheming:SchemingPagesController',
                    action='search')
                    
        # e-Ouv
        map.connect('/eouv/new_positive',
                    controller='ckanext.dadosabertos.controllers.eouv:EouvController',
                    action='new_positive')
        map.connect('/eouv/new_negative',
                    controller='ckanext.dadosabertos.controllers.eouv:EouvController',
                    action='new_negative')
                    
        # Wordpress feed redirect (if load balancer fail)
        map.connect('/feed',
                    controller='ckanext.dadosabertos.controllers.noticias:NoticiasController',
                    action='feed')

        # Wordpress
        map.connect('/noticias',
                    controller='ckanext.dadosabertos.controllers.wordpress:NoticiasController',
                    action='list')
        map.connect('/noticias/{slug}', # Legacy from dados.gov.br 2017 version
                    controller='ckanext.dadosabertos.controllers.wordpress:NoticiasController',
                    action='redirect',
                    slug=0)
        map.connect('/noticia/{slug}',
                    controller='ckanext.dadosabertos.controllers.wordpress:NoticiasController',
                    action='show',
                    slug=0)
        map.connect('/noticias/{id}/{slug}', # Legacy from dados.gov.br 2016 version
                    controller='ckanext.dadosabertos.controllers.wordpress:NoticiasController',
                    action='redirect',
                    slug=0)
        map.connect('/pagina/{slug}', 
                    controller='ckanext.dadosabertos.controllers.wordpress:PaginasController',
                    action='index')
        map.connect('/paginas/{slug}', # Legacy from dados.gov.br 2016 version
                    controller='ckanext.dadosabertos.controllers.wordpress:PaginasController',
                    action='redirect')
        return map




    # Registro dos helpers
    # =======================================================
    def get_helpers(self):
        '''Register all functions

        '''
        # Template helper function names should begin with the name of the
        # extension they belong to, to avoid clashing with functions from
        # other extensions.
        return {
            # Homepage
            'dadosgovbr_most_recent_datasets': tools.most_recent_datasets,

            # Wordpress
            'dadosgovbr_wordpress_posts': wp.posts,
            'dadosgovbr_format_timestamp': wp.format_timestamp,

            # Scheming
            'dadosgovbr_get_schema_name': tools.get_schema_name,
            'dadosgovbr_get_schema_title': tools.get_schema_title,

            # Generict tools
            'dadosgovbr_trim_string': tools.trim_string,
            'dadosgovbr_trim_letter': tools.trim_letter,
            'dadosgovbr_resource_count': tools.resource_count,
            'dadosgovbr_get_featured_group': tools.get_featured_group,
            'dadosgovbr_get_organization_extra': tools.get_organization_extra,
            'dadosgovbr_get_package': tools.get_package,
            'dadosgovbr_cache_create': tools.cache_create,
            'dadosgovbr_cache_load': tools.cache_load,

            # e-Ouv
            'dadosgovbr_eouv_is_avaliable': tools.eouv_is_avaliable,
            'dadosgovbr_get_contador_eouv': tools.helper_get_contador_eouv
        }
        