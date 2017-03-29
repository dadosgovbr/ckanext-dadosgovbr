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
        map.connect('/feed',
                    controller='ckanext.dadosabertos.controllers.noticias:NoticiasController',
                    action='feed')
        map.connect('/noticias',
                    controller='ckanext.dadosabertos.controllers.noticias:NoticiasController',
                    action='list')
        map.connect('/noticias/{slug}',
                    controller='ckanext.dadosabertos.controllers.noticias:NoticiasController',
                    action='show',
                    slug=0)
        map.connect('/noticia/{slug}', # Legacy from dados.gov.br 2015 version
                    controller='ckanext.dadosabertos.controllers.noticias:NoticiasController',
                    action='redirect',
                    slug=0)
        map.connect('/paginas/{slug}',
                    controller='ckanext.dadosabertos.controllers.paginas:PaginasController',
                    action='index')
        return map



    def get_helpers(self):
        '''Register all functions

        '''
        # Template helper function names should begin with the name of the
        # extension they belong to, to avoid clashing with functions from
        # other extensions.
        return {
            'dadosabertos_most_recent_datasets': tools.most_recent_datasets,
            'dadosabertos_wordpress_posts': wp.posts,
            'dadosabertos_trim_string': tools.trim_string,
            'dadosabertos_trim_letter': tools.trim_letter,
            'dadosabertos_resource_count': tools.resource_count,
            'dadosabertos_get_featured_group': tools.get_featured_group,
            'dadosabertos_format_timestamp': wp.format_timestamp }
