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
            most_recent_datasets.append(dataset)


        return most_recent_datasets


def get_organization_extra(org_name, extra_name):
    extras = h.get_organization(org_name)['extras']

    # Search for organization extra by "extra_name"
    for extra in extras:
        if(extra['key'] == extra_name):
            return extra
    
    return None



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
