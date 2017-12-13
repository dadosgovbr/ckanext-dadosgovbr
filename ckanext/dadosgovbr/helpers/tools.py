# -*- coding: utf-8 -*-
from ckan.lib.base import c, g, h, model
import ckan.logic
from ckan.logic import get_action
from random import shuffle
from copy import deepcopy

# Cache
import hashlib, pickle, os, errno, time


def trim_string(s, tamanho):
    s = unicode(s)
    return s if (len(s) < tamanho) else s[:(tamanho - 5)].rsplit(u" ", 1)[0] + u"..."

def trim_letter(s, tamanho):
    s = unicode(s)
    return s if (len(s) < tamanho) else s[:(tamanho)] + u"..."

def eouv_is_avaliable ():
    from ckan.common import config
    if 'eouv.url' in config:
        return True
    return False

def eouv_check_tags (tags):
    for x in tags:
        if (x['name'].lower() == 'pgi'):
            return False
    return True

def helper_get_contador_eouv (package_name):
    out = {}
    error=0
    exist_tuple=None
    exist_table_eouv=None

    # Verificar se a tabela exist
    query_revision = "select exists (select * from pg_tables where tablename = 'package_eouv') as exist"
    result_exist_table_eouv = model.Session.execute(query_revision)
    for row in result_exist_table_eouv:
        exist_table_eouv = row['exist']
    if not(exist_table_eouv): error=1
    print('exist_table_eouv', error)

    # Verifica se possui a tupla com like/dislike
    if exist_table_eouv:
        query_posit = "SELECT EXISTS (SELECT 1 FROM package_eouv WHERE package_name = '"+str(package_name)+"') as positivo"
        exist_tupla_positiva = model.Session.execute(query_posit)
        for row in exist_tupla_positiva:
            exist_tuple = row['positivo']
    if not(exist_tuple): error=1
    print('exist_tuple', error)

    # Obtém valor do like/dislike se a tupla existir
    if exist_tuple:
        query_nro_dislike = "SELECT nro_like, nro_dislike FROM package_eouv WHERE package_name = '"+str(package_name)+"'"    
        num_dislike_array = model.Session.execute(query_nro_dislike)
        count=0
        for row in num_dislike_array:
            count += 1
            out['nro_dislikes'] = row['nro_dislike']
            out['nro_likes'] = row['nro_like']
        if count == 0: error=1
            
    # Se houve algum erro, então valores iguais a zero
    if error == 1:
        out['nro_dislikes'] = 0
        out['nro_likes'] = 0

    return out


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

def resource_count():
    ''' Return total number of resources on current CKAN platform

        @return int
    '''
    try:
        # resource search
        context = {'model': model, 'session': model.Session,
                   'user': c.user or c.author}
        data_dict = {
            'query':{},
            'facet.field':g.facets,
            'offset':0,
            'limit':0,
            'order_by': None,
        }
        query = ckan.logic.get_action('resource_search')(context,data_dict)
        return query['count']
    except Exception as e:
        return 0


def most_recent_datasets(limit_of_datasets=5):
    """ Return most recent datasets
    """

    # Get cache if exist
    # or is older than 5 minutes
    most_recent_datasets = cache_load('most_recent_datasets', 5)

    # Get from database if cache doesn't exist or expirate
    if(most_recent_datasets == None):

        import ckan.lib.dictization as d
        from ckan.logic import get_action
        from sqlalchemy import desc

        context = {'model': model, 'session': model.Session,
                   'user': c.user or c.author}

        query = model.Session.query(model.Package, model.Activity)
        query = query.filter(model.Activity.object_id==model.Package.id)
        query = query.filter(model.Activity.activity_type == 'new package')
        query = query.filter(model.Package.state == 'active')
        query = query.order_by(desc(model.Activity.timestamp))
        query = query.limit(limit_of_datasets)
        most_recent_from_bd = query.all()
        most_recent_datasets = [
            (
                g.site_url + '/dataset/' + dataset.name,
                dataset.title,
                dataset.author,
                activity.timestamp.isoformat(),
            )   for dataset, activity in most_recent_from_bd]

        most_recent_datasets = []
        for dataset, activity in most_recent_from_bd:
            dataset.link = 'dataset/' + dataset.name
            dataset.time = activity.timestamp.strftime("%d/%m/%Y")
            dataset.organization = h.get_organization(dataset.owner_org)
            most_recent_datasets.append(dataset)

        # Create cache
        cache_create(most_recent_datasets, 'most_recent_datasets')

    return most_recent_datasets


def get_organization_extra(org_name, extra_name):

    # Get cache if exist
    # or is older than 2 minutes
    extra = cache_load(str(org_name)+'/'+str(extra_name) , 1)

    # Check if has nothing
    if(extra == 'nothing'):
        return None

    # Tyr to get from database if cache doesn't exist or expirate
    try:
        if(extra == None):
            # Get extras from org
            extras = h.get_organization(org_name)['extras']

            # Search for organization extra by "extra_name"
            for extra in extras:
                if(extra['key'] == extra_name):
                    # Create cache
                    cache_create(extra, str(org_name)+'/'+str(extra_name) )        
                    return extra
            
            # Create cache
            cache_create('nothing', str(org_name)+'/'+str(extra_name) )
            return None
    except:
        return None

    return extra



def cache_create (d, name):
    """ Create a cache for 'd' dict.

        @params d:dict
                name:string (to identify cache)
    """

    # Cache path and file name
    cache_checksum  = hashlib.sha256(name).hexdigest() 	# Create checksum by name
    cache_file_path = '/tmp/ckan/dict_'+cache_checksum  # /tmp/ckan/dict_$cache_name

    # Create cache dir, if not exist
    if not os.path.exists('/tmp/ckan/'):
        os.makedirs('/tmp/ckan/')

    # Delete cached file, if exist
    try:
        os.remove(cache_file_path)
    except OSError:
        pass

    # Create 'd' as a cache
    with open(cache_file_path, 'wb') as handle:
        pickle.dump(d, handle, protocol=pickle.HIGHEST_PROTOCOL)


def cache_load (name, lifetime=10):
    """ Return a dict cached.

        @params name:string (to identify cache)
                lifetime:int (in minutes. Default: 10)
        @return d:dict
    """

    # Cache path and file name
    cache_checksum  = hashlib.sha256(name).hexdigest() 	# Create checksum by name
    cache_file_path = '/tmp/ckan/dict_'+cache_checksum  # /tmp/ckan/dict_$cache_name

    # Check if file is old
    now = time.time()
    file_old = False
    if (os.path.isfile(cache_file_path)):
        if (os.stat(cache_file_path).st_mtime < (now - 60 * lifetime)):
            file_old = True

    # Open and load cached 'd' dict if file exist and not expirate
    if(os.path.exists(cache_file_path) and not file_old):
        with open(cache_file_path, 'rb') as handle:
            d = pickle.load(handle)
        return d
    
    # Return none if no cache found or expirate
    else:
        return None
    


def get_featured_group(group_name='dados-em-destaque', number_of_datasets=3):
    """ Return a list of mainly datasets from a group

        @params group_name:string (group name)
                number_of_datasets:int (number of datasets to be returned)
        @return list<packages> (list of datasets)
    """
    from ckan.logic import get_action
    context = {'model': model, 'session': model.Session,
               'user': c.user or c.author}
    

    # Get cache if exist
    # or is older than 2 minutes
    group = cache_load('dados_em_destaque', 2)

    # Get from database if cache doesn't exist or expirate
    if(group == None):
        # Get group
        data_dict = {'id': group_name, 'include_datasets': 'True'}
        group = get_action('group_show')(context, data_dict)

        # Shuffle datasets list
        import random
        random.shuffle(group['packages'])

        # Limit number of datasets
        limit = number_of_datasets
        if (len(group['packages']) < limit):
            limit = len(group['packages'])
        group['packages'] = group['packages'][:limit]
        
        # Create cache
        cache_create(group, 'dados_em_destaque')
        

    return group



def get_package(package_id):
    ''' Return package by name/id '''

    from ckan.logic import get_action
    context = {'model': model, 'session': model.Session,
               'user': c.user or c.author}

    # Get package
    data_dict = {'id': package_id}
    package  = get_action('package_show')(context, data_dict)
    
    return package

