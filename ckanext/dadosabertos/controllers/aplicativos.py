# -*- coding: utf-8 -*-

import ckan.plugins as p
from ckan.lib.base import c, g, render, model
from pylons import request, response
from pylons.controllers.util import redirect
import requests


class AplicativosController(p.toolkit.BaseController):
    def index (ctrl):
        import ckan.lib.dictization as d
        from ckan.logic import get_action
        from sqlalchemy import desc

        context = {'model': model, 'session': model.Session,
                   'user': c.user or c.author}

        query = model.Session.query(model.Package, model.Activity)
        query = query.filter(model.Activity.object_id==model.Package.id)
        query = query.filter(model.Package.state == 'active')
        query = query.filter(model.Package.type.like('aplicativo'))
        aplicativos_query = query.all()

        aplicativos = [
            (
                g.site_url + '/dataset/' + dataset.name,
                #cls.limita_tamanho(dataset.title, 46),
                dataset.title,
                #cls.limita_tamanho(dataset.author, 28),
                dataset.author,
                #cls.tempo_atras(activity.timestamp),
                activity.timestamp.isoformat(),
            )   for dataset, activity in aplicativos_query]

        aplicativos = []
        for dataset, activity in aplicativos_query:
            dataset.link = 'dataset/' + dataset.name
            dataset.time = activity.timestamp.strftime("%d/%m/%Y")
            aplicativos.append(dataset)

        # Remove duplicados
        aplicativos_clean = []
        for app in aplicativos:
            if app not in aplicativos_clean:
                aplicativos_clean.append(app)
                


        c.aplicativos = aplicativos_clean



        return render('aplicativos/list.html')