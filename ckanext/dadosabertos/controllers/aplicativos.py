# -*- coding: utf-8 -*-

import ckan.plugins as p
from ckan.lib.base import c, g, render, model
from pylons import request, response
from pylons.controllers.util import redirect
import requests


class AplicativosController(p.toolkit.BaseController):
    def index (ctrl):
        # Query
        schema_name = "aplicativo"
        sql = "select pk.name as name, pk.title as title,(select pEx.value as author from package_extra pEx where pk.id = pEx.package_id and pEx.key = 'author_name'),pk.author_email as author_email,(select pExt.value as description from package_extra pExt where pk.id = pExt.package_id and pExt.key = 'description'),(select g.title as group_title from public.group g where g.id = pk.owner_org),pke.value as image  from package pk join package_extra pke on pk.id = pke.package_id where pk.type = '"+schema_name+"' and pke.key = 'image' and pk.state = 'active' and pk.private = FALSE"

        # Get "aplicativos"
        c.aplicativos = model.Session.execute(sql)

        # DEBUG
        from pprint import pprint
        pprint(model.Session.execute(sql).keys())


        # Get search params from URL
        if request.method == 'GET' and 's' in request.GET:
            c.s_result    = request.GET['s']
        else:
            c.s_result    = ""

        return render('scheming/aplicativos.html')