# -*- coding: utf-8 -*-
import datetime

from pylons import config

from ckan.logic import get_action, check_access
from ckan.lib.helpers import date_str_to_datetime
from ckan.logic import NotFound, NotAuthorized
from ckan.lib.base import request, _, c, BaseController, model, abort, h, g, render
from ckan.lib.base import response, redirect, gettext
import ckan.lib.package_saver as package_saver
from ckan.lib.helpers import json
import ckan.logic.action.get

from ckan.controllers.package import PackageController

class DadosGovBrDatasetController(PackageController):
    """A customized controller for the dataset related views on the
    ckanext-dadosgovbr theme.
    """
    def read(self, id, format='html'):

        if not format == 'html':
            ctype, extension, loader = \
                self._content_type_from_extension(format)
            if not ctype:
                # An unknown format, we'll carry on in case it is a
                # revision specifier and re-constitute the original id
                id = "%s.%s" % (id, format)
                ctype, format, loader = "text/html; charset=utf-8", "html", \
                    MarkupTemplate
        else:
            ctype, format, loader = self._content_type_from_accept()

        response.headers['Content-Type'] = ctype

        package_type = self._get_package_type(id.split('@')[0])
        context = {'model': model, 'session': model.Session,
                   'user': c.user or c.author, 'for_view': True,
                   'auth_user_obj': c.userobj}
        data_dict = {'id': id}

        # interpret @<revision_id> or @<date> suffix
        split = id.split('@')
        if len(split) == 2:
            data_dict['id'], revision_ref = split
            if model.is_id(revision_ref):
                context['revision_id'] = revision_ref
            else:
                try:
                    date = h.date_str_to_datetime(revision_ref)
                    context['revision_date'] = date
                except TypeError, e:
                    abort(400, _('Invalid revision format: %r') % e.args)
                except ValueError, e:
                    abort(400, _('Invalid revision format: %r') % e.args)
        elif len(split) > 2:
            abort(400, _('Invalid revision format: %r') %
                  'Too many "@" symbols')

        # check if package exists
        try:
            c.pkg_dict = get_action('package_show')(context, data_dict)
            c.pkg = context['package']
        except NotFound:
            abort(404, _('Dataset not found'))
        except NotAuthorized:
            abort(401, _('Unauthorized to read package %s') % id)

        # used by dadosgovbr_dataset plugin
        import re
        extras = c.pkg.extras
        subject = extras.get("VCGE", None)
        vcge_re = r"([^[]+)\s*\[(http://[^[\]]+)\]\s?[,;]?\s?"
        c.pkg_dict["subjects"] = []
        if subject:
            for name, url in re.findall(vcge_re, subject):
                c.pkg_dict["subjects"].append((name,url))
            #try:
            #    del c.pkg_dict["extras"]["VCGE"]
            #except KeyError:
            #    pass
        
        # used by disqus plugin
        c.current_package_id = c.pkg.id
        c.related_count = c.pkg.related_count

        # can the resources be previewed?
        for resource in c.pkg_dict['resources']:
            resource['can_be_previewed'] = self._resource_preview(
                {'resource': resource, 'package': c.pkg_dict})

        self._setup_template_variables(context, {'id': id},
                                       package_type=package_type)

        package_saver.PackageSaver().render_package(c.pkg_dict, context)

        template = self._read_template(package_type)
        template = template[:template.index('.') + 1] + format

        try:
            return render(template, loader_class=loader)
        except ckan.lib.render.TemplateNotFound:
            msg = _("Viewing {package_type} datasets in {format} format is "
                    "not supported (template file {file} not found).".format(
                    package_type=package_type, format=format, file=template))
            abort(404, msg)

        assert False, "We should never get here"
        
