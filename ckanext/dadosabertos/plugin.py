# -*- coding: utf-8 -*-

import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from ckan.lib.base import c, g, h, model

from ckan.plugins import implements, SingletonPlugin
from ckan.plugins import IConfigurer
from ckan.plugins import IRoutes

# Wordpress integration
import ckanext.dadosabertos.helpers.wordpress as wp

# Custom helper tools
import ckanext.dadosabertos.helpers.tools as tools


class DadosabertosPlugin(plugins.SingletonPlugin):
    ''' Plugin Dados Abertos

        Classe principal.
        - Define diretórios para imagens, CSS e JS
        - Define mapeamento para novas rotas
        - Define novos helpers
    '''

    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.ITemplateHelpers)
    implements(IConfigurer, inherit=True)
    implements(IRoutes, inherit=True)

    # Diretórios para templates e arquivos estáticos
    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic', 'dadosabertos')

    # Mapeamento das URLs
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
                    controller='ckanext.dadosabertos.controllers.scheming:AplicativosController',
                    action='index')
        map.connect('/aplicativos_busca/{title}',
                    controller='ckanext.dadosabertos.controllers.scheming:AplicativosController',
                    action='single')
        map.connect('/inventarios',
                    controller='ckanext.dadosabertos.controllers.scheming:InventariosController',
                    action='index')
        map.connect('/concursos',
                    controller='ckanext.dadosabertos.controllers.scheming:ConcursosController',
                    action='index')
                    
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
            'dadosgovbr_get_featured_group': tools.get_featured_group,
            'dadosgovbr_cache_create': tools.cache_create,
            'dadosgovbr_cache_load': tools.cache_load
        }
