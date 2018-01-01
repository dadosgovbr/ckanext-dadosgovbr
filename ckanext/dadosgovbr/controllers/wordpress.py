# -*- coding: utf-8 -*-

import ckan.plugins as p
from ckan.lib.base import c, render
from pylons import request, response
from pylons.controllers.util import redirect
import requests

# Wordpress integration
import ckanext.dadosgovbr.helpers.wordpress as wp


class NoticiasController(p.toolkit.BaseController):

    def redirect (ctrl, slug):
        return redirect(b'/noticia/'+slug)

    def show (ctrl, slug):
        c.wp_post = wp.post(slug)
        return render('wordpress/post_single.html')

    def list (ctrl):
        if ('page' in request.GET):
            c.wp_page_number = int(request.GET['page'])
        else:
            c.wp_page_number = int(1)

        c.title = "Notícias".decode('utf8')
        c.wp_posts = wp.posts(10, c.wp_page_number)
        c.total_of_posts = wp.getTotalPages()

        return render('wordpress/posts.html')

    def feed (ctrl):
        # Get content from feed URL
        url     = "http://dados.gov.br/wp/feed"
        feed    = requests.get(url)
        content = feed.content

        # Update URL to mask Wordpress path
        #content = content.replace("dados.gov.br/wp", "dados.gov.br/noticias")

        # Set header for XML content
        response.headers['Content-Type'] = (
            b'text/xml; charset=utf-8')

        return content


class PaginasController(p.toolkit.BaseController):
    def index (ctrl, slug):
        c.wp_page = wp.page(slug)
        return render('wordpress/page_single.html')

    def redirect (ctrl, slug):
        return redirect(b'/pagina/'+slug)

