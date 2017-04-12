# -*- coding: utf-8 -*-
from ckan.lib.base import c, g, h, model
import ckan.logic
from ckan.logic import get_action
from random import shuffle
from copy import deepcopy


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


def cache_dict (d, lifetime=600):
    """ Return a list of mainly datasets from a group

        @params group_name:string (group name)
                number_of_datasets:int (number of datasets to be returned)
        @return list<packages> (list of datasets)
    """
    # Cache
    cache_dir = '/tmp/ckan_cache/'
    f_name = 'featured_group'

    # Remove old cache file
    # 14400 = 10 minutes
    now = time.time()
    file_is_old = False
    if (os.path.isfile(f_name)):
        if (os.stat(f_name).st_mtime < (now - 14400)):
            file_is_old = True

    # Check if cached file exists
    if (os.path.isfile(f_name) and not file_is_old):
        # Get JSON from cache
        f       = open(f_name, 'r')
        posts   = json.loads(f.read())
        f.close()

    # with open(cache_dir+f_name, 'wb') as f:
    #     var = {1 : 'a' , 2 : 'b'}
    #     pickle.dump(var, f)
    # with open('filename','rb') as f:
    #     var = pickle.load(f)


def get_featured_group(group_name='dados-em-destaque', number_of_datasets=3):
    """ Return a list of mainly datasets from a group

        @params group_name:string (group name)
                number_of_datasets:int (number of datasets to be returned)
        @return list<packages> (list of datasets)
    """
    from ckan.logic import get_action
    context = {'model': model, 'session': model.Session,
               'user': c.user or c.author}

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

    return group
