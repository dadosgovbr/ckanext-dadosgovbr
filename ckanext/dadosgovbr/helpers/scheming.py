# -*- coding: utf-8 -*-
from ckan.lib.base import h, g

def get_schema_name(dataset_name=None):
    ''' Return schema name '''
    if(dataset_name == None):
        schema_name = str(h.full_current_url()).replace(g.site_url, '').split('/')[1].split('?')[0]
        if(schema_name[-1:]=='s'):
            schema_name=schema_name[:-1]
        # print(schema_name)
        return schema_name
    return 'dataset'

def get_schema_title(schema_name=None, plural=False):
    ''' Return schema title '''
    schema_titles = {}
    schema_titles['aplicativo']         = u"aplicativo"
    schema_titles['aplicativo_plural']  = u"aplicativos"
    schema_titles['concurso']           = u"concurso"
    schema_titles['concurso_plural']    = u"concursos"
    schema_titles['inventario']         = u"item de inventário"
    schema_titles['inventario_plural']  = u"itens de inventário"
    schema_titles['dataset']            = u"conjunto de dados"
    schema_titles['dataset_plural']     = u"conjuntos de dados"
    if(schema_name==None):
        schema_name=get_schema_name()
    if(schema_name in schema_titles):
        if(plural):
            return schema_titles[schema_name+'_plural']
        else:
            return schema_titles[schema_name]
    return u'resultado(s)'
