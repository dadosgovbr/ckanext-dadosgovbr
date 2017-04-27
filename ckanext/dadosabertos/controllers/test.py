# -*- coding: utf-8 -*-

import ckan.plugins as p
from ckan.lib.base import c, g, render, model
from pylons import request, response
from pylons.controllers.util import redirect
import requests

class TestController(p.toolkit.BaseController):
    def index (ctrl):
        return render("test.html")