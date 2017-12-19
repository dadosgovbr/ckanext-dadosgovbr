# -*- coding: utf-8 -*-

import ckan.plugins as p
from ckan.lib.base import c, g, h, render, model
import ckan.lib.base as base
from pylons import request, response
from pylons.controllers.util import redirect

from ckan.common import OrderedDict, config

# Common pages

class CommonController(base.BaseController):
    def error(self):

        return render('error/403.html')