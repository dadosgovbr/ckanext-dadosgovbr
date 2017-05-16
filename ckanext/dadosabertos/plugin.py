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
    def after_map(self, map):
        # Wordpress feed redirect (if load balancer fail)
        map.connect('/feed',
                    controller='ckanext.dadosabertos.controllers.noticias:NoticiasController',
                    action='feed')

        # ckanext-scheming
        map.connect('/test',
                    controller='ckanext.dadosabertos.controllers.test:TestController',
                    action='index')
        map.connect('/aplicativos',
                    controller='ckanext.dadosabertos.controllers.aplicativos:AplicativosController',
                    action='index')
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
        map.connect('/eouv/new_negative',
                    controller='ckanext.dadosabertos.controllers.eouv:EouvController',
                    action='new_negative')
                    
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

            # Generict tools
            'dadosgovbr_trim_string': tools.trim_string,
            'dadosgovbr_trim_letter': tools.trim_letter,
            'dadosgovbr_resource_count': tools.resource_count,
            'dadosgovbr_get_organization_extra': tools.get_organization_extra,
            'dadosgovbr_get_featured_group': tools.get_featured_group,
            'dadosgovbr_cache_create': tools.cache_create,
            'dadosgovbr_cache_load': tools.cache_load
        }
