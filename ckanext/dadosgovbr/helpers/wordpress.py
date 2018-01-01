# -*- coding: utf-8 -*-

# Dependence for Wordpress_Post
from ckan.plugins import implements, SingletonPlugin
from ckan.plugins import IConfigurer
from ckan.plugins import IRoutes
import requests, hashlib, os, json, time, re
import datetime
import dateutil.parser as dp

# Logging
import logging
log = logging.getLogger(__name__)



def get_domain():
    ''' Return Wordpress domain URL
        Define your Wordpress domain here

        @return string
    '''
    #return "https://blog.thenets.org"
    return 'http://dados.gov.br/wp'




def cache_json(url):
    ''' Return JSON from URL
        If exist a cached file, create JSON from cache.

        @return dict
    '''
    # Check cache dir exists
    cache_dir = '/tmp/ckan_cache/'
    if(not os.path.isdir(cache_dir)):
        os.makedirs(cache_dir)

    # Cached file
    f_key  = hashlib.md5(url).hexdigest()
    f_name = cache_dir+'ckan_'+f_key

    # Remove old cache file
    # 600 = 10 minutes
    now = time.time()
    file_is_old = False
    if (os.path.isfile(f_name)):
        if (os.stat(f_name).st_mtime < (now - 600)):
            file_is_old = True

    # Check if cached file exists
    if (os.path.isfile(f_name) and not file_is_old):
        # Get JSON from cache
        f       = open(f_name, 'r')
        posts   = json.loads(f.read())
        f.close()

    # If cache file not exist or has expired
    else:
        triesCount=0
        while True and triesCount < 10:
            # Try to get JSON from URL
            try:
                request = requests.get(url, timeout=3)  # Request of URL
                posts   = request.json()
                if(request.status_code > 400):
                    raise

                # Remove old cache file
                if (os.path.isfile(f_name)):
                    os.remove(f_name)

                # Write cache file
                f       = open(f_name, 'w')
                f.write(request.text)
                f.close()

            # Try again if got some error
            except Exception as e:
                triesCount+=1
                log.error('Wordpress API | Error getting url: %s', url)
                log.info ('Wordpress API | trying again')
                continue

            break


    return posts # Convert JSON to Python object


def post(post_slug):
    ''' Return post by slug

        @param post_slug:string
        @return dict
    '''
    url = get_domain()+"/wp-json/wp/v2/posts?filter[name]="+str(post_slug)+"&_embed"
    return cache_json(url)[0]

def getTotalPages():
    ''' Return the total number of pages

        @return int
    '''
    # URL
    url = get_domain()+"/wp-json/wp/v2/posts"
    try:
        n_pages = requests.get(url, timeout=10).headers['X-WP-TotalPages']
    except Exception as e:
        log.error('Wordpress API | Error getting url: %s', url)
        n_pages = 10

    return int(n_pages)


def posts(posts_per_page=10, page_number=1):
    ''' Return a list of latest posts

        @return list<dict>
    '''
    # URL
    url   = get_domain()+"/wp-json/wp/v2/posts?per_page="+str(posts_per_page)+"&page="+str(page_number)
    json  = cache_json(url)

    # Remove <a> tags from excerpt
    for post in json:
        post['excerpt']['rendered'] = re.sub("<a(.*?)<\/a>", "", post['excerpt']['rendered'])

    # Get posts and return
    return json



def page(page_slug):
    ''' Return page by slug

        @param page_slug:string
        @return dict
    '''

    # Get single post
    url = get_domain()+"/wp-json/wp/v2/pages?filter[name]="+str(page_slug)+"&_embed"

    # Check error
    j = cache_json(url)
    if ('error' in j):
        return j
    else:
        return j[0]



def format_timestamp(timestamp,timeFormat='%d/%m/%Y %H:%M'):
    ''' Return a formated datetime

        Example: format_timestamp('2005-08-15T15:52:01', '%d/%m/%Y %H:%M')

        @params timestamp:string (ISO 8601)
                timeFormat:string (Python datetime sintax)
        @return formated:string
    '''
    posix_time = float(dp.parse(timestamp).strftime('%s'))
    formated = datetime.datetime.utcfromtimestamp(posix_time).strftime(timeFormat)
    return formated
