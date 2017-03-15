# -*- coding: utf-8 -*-

import ckan.plugins as p
from ckan.lib.base import c, render
from pylons import request
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

    def feed (ctrl):
        return "Not available... try again later..."

        url = "https://blog.thenets.org/feed"
        response = requests.get(url)

        return response.content
