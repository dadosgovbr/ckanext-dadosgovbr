# -*- coding: utf-8 -*-

import ckan.plugins as p
from ckan.lib.base import c, g, render, model
from pylons import request, response
from pylons.controllers.util import redirect
import requests


class ConcursosController(p.toolkit.BaseController):
    def index (ctrl):
        import ckan.lib.dictization as d
        from ckan.logic import get_action
        from sqlalchemy import desc
        import json

        context = {'model': model, 'session': model.Session,
                   'user': c.user or c.author}

        # 
        from pprint import pprint

        c.concursos = model.Session.execute("select * from package pk join package_extra pke on pk.id = pke.package_id where pk.type = 'aplicativo' and pke.key = 'image'")
        
        pprint(c.concursos)
        
        if request.method == 'GET' and 's' in request.GET:
            c.s_result    = request.GET['s']
        else:
            c.s_result    = ""

        return render('concursos.html')