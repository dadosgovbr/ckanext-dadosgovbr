# -*- coding: utf-8 -*-
from logging import getLogger
import urlparse

import requests

from ckan.common import config

import ckan.logic as logic
import ckan.lib.base as base
from ckan.common import _
from ckan.plugins.toolkit import asint


class NoticiasController(base.BaseController):