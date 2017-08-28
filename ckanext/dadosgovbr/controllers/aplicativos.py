# -*- coding: utf-8 -*-

import ckan.plugins as p
from ckan.lib.base import c, g, render, model
from pylons import request, response
from pylons.controllers.util import redirect
import requests

# Wordpress integration
import ckanext.dadosgovbr.helpers.wordpress as wp

# ============================================================
# Aplicativos
# ============================================================
class AplicativosController(p.toolkit.BaseController):
    def index (ctrl):
        # Query
        from ckan.logic import get_action
        context = {'model': model, 'session': model.Session,
                'user': c.user or c.author}

        # Get "aplicativos"
        data_dict = {'fq': 'type:aplicativo'}
        c.aplicativos = get_action('package_search')(context, data_dict)['results']

        # Get page content from Wordpress
        wp_page_slug = 'scheming_aplicativos'
        c.wp_page = type('Nothing', (object,), {})  
        c.wp_page.content = type('Nothing', (object,), {})  
        c.wp_page.content.rendered = "Conteudo da pagina nao encontrado..."
        try:
            c.wp_page = wp.page(wp_page_slug)
        except:
            pass

        # DEBUG
        # from pprint import pprint
        # pprint(c.aplicativos)


        # Get search params from URL
        if request.method == 'GET' and 's' in request.GET:
            c.s_result    = request.GET['s']
        else:
            c.s_result    = ""


        return render('scheming/aplicativo/search_bkp.html')


    
    def single (ctrl, title):
        from ckan.logic import get_action
        context = {'model': model, 'session': model.Session,
                'user': c.user or c.author}

        # Get app
        data_dict = {'id': title, 'include_extras': 'True'}
        app = get_action('package_show')(context, data_dict)
        c.app_dict = app

        # DEBUG
        from pprint import pprint
        pprint(app)

        c.app_title = title
        return render("scheming/aplicativo_modal.html")
