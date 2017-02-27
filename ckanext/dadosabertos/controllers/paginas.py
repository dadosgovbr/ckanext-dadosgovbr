# -*- coding: utf-8 -*-

import ckan.plugins as p
from ckan.lib.base import c, render
from pylons import request

# Wordpress integration
import ckanext.dadosabertos.helpers.wordpress as wp


class PaginasController(p.toolkit.BaseController):
    def index (ctrl, slug):
        c.wp_page = wp.page(slug)
        return render('paginas/index.html')
