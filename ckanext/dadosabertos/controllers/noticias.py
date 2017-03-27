# -*- coding: utf-8 -*-

import ckan.plugins as p
from ckan.lib.base import c, render
from pylons import request, response
from pylons.controllers.util import redirect
import requests

# Wordpress integration
import ckanext.dadosabertos.helpers.wordpress as wp


class NoticiasController(p.toolkit.BaseController):

    def show (ctrl, slug):
        c.wp_post = wp.post(slug)
        return render('noticias/show.html')

    def list (ctrl):
        if ('page' in request.GET):
            c.wp_page_number = int(request.GET['page'])
        else:
            c.wp_page_number = int(1)

        c.title = "Notícias".decode('utf8')
        c.wp_posts = wp.posts(10, c.wp_page_number)
        return render('noticias/list.html')

    def redirect (ctrl, slug):
        return redirect(b'/noticias/'+slug)

    def feed (ctrl):
        # Get content from feed URL
        url     = "http://dados.gov.br/wp/feed"
        feed    = requests.get(url)
        content = feed.content

        # Filters
        # Update URL to mask Wordpress path
        #content = content.replace("dados.gov.br/wp", "dados.gov.br/noticias")

        # Set header for XML content
        response.headers['Content-Type'] = (
            b'text/xml; charset=utf-8')

        return content
