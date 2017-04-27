# -*- coding: utf-8 -*-

import ckan.plugins as p
from ckan.lib.base import c, g, render, model
from pylons import request, response
from pylons.controllers.util import redirect
import requests


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

        # DEBUG
        # from pprint import pprint
        # pprint(c.aplicativos)


        # Get search params from URL
        if request.method == 'GET' and 's' in request.GET:
            c.s_result    = request.GET['s']
        else:
            c.s_result    = ""


        return render('scheming/aplicativos.html')
    


    
    def single (ctrl, title):
        from ckan.logic import get_action
        context = {'model': model, 'session': model.Session,
                'user': c.user or c.author}

        # Get group
        data_dict = {'id': title, 'include_extras': 'True'}
        app = get_action('package_show')(context, data_dict)


        # DEBUG
        from pprint import pprint
        pprint(app)

        c.app_title = title
        return render("scheming/aplicativo_single.html")





# ============================================================
# Concursos
# ============================================================
class ConcursosController(p.toolkit.BaseController):
    def index (ctrl):
        # Query
        from ckan.logic import get_action
        context = {'model': model, 'session': model.Session,
                'user': c.user or c.author}
        
        # Get "concursos"
        data_dict = {'fq': 'type:concurso'}
        c.concursos = get_action('package_search')(context, data_dict)['results']

        # DEBUG
        # from pprint import pprint
        # pprint(c.concursos)


        # Get search params from URL
        if request.method == 'GET' and 's' in request.GET:
            c.s_result    = request.GET['s']
        else:
            c.s_result    = ""

        return render('scheming/concursos.html')





# ============================================================
# Inventários
# ============================================================
class InventariosController(p.toolkit.BaseController):
    def index (ctrl):
        # Query
        from ckan.logic import get_action
        context = {'model': model, 'session': model.Session,
                'user': c.user or c.author}
        
        # Get "inventarios"
        data_dict = {'fq': 'type:inventario'}
        c.concursos = get_action('package_search')(context, data_dict)['results']

        # DEBUG
        # from pprint import pprint
        # pprint(c.concursos)


        # Get search params from URL
        if request.method == 'GET' and 's' in request.GET:
            c.s_result    = request.GET['s']
        else:
            c.s_result    = ""

        return render('scheming/inventarios.html')
