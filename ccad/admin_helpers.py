from django.core.urlresolvers import reverse
from django.contrib.admin import AdminSite
from django.views.decorators.cache import never_cache

from functools import update_wrapper
from django.http import Http404, HttpResponseRedirect
from django.contrib.admin import ModelAdmin, actions
from django.contrib.admin.forms import AdminAuthenticationForm
from django.contrib.auth import logout as auth_logout, REDIRECT_FIELD_NAME
from django.contrib.contenttypes import views as contenttype_views
from django.views.decorators.csrf import csrf_protect
from django.db.models.base import ModelBase
from django.core.exceptions import ImproperlyConfigured
from django.core.urlresolvers import reverse, NoReverseMatch
from django.template.response import TemplateResponse
from django.utils import six
from django.utils.text import capfirst
from django.utils.translation import ugettext as _
from django.views.decorators.cache import never_cache

class InlineEditLinkMixin(object):
    readonly_fields = ['edit_details']
    edit_label = "Edit"
    def edit_details(self, obj):
        if obj.id:
            opts = self.model._meta
            return "<a href='%s' target='_blank'>%s</a>" % (reverse(
                'admin:%s_%s_change' % (opts.app_label, opts.object_name.lower()),
                args=[obj.id]
            ), self.edit_label)
        else:
            return "(save to edit details)"
    edit_details.allow_tags = True

class NAFDAdminSite(AdminSite):
    @never_cache
    def index(self, request, extra_context=None):
        """
        Displays the main admin index page, which lists all of the installed
        apps that have been registered in this site.
        """
        app_dict = {}
        user = request.user
        for model, model_admin in self._registry.items():
            app_label = model._meta.app_label
            has_module_perms = user.has_module_perms(app_label)

            if has_module_perms:
                perms = model_admin.get_model_perms(request)

                # Check whether user has any perm for this module.
                # If so, add the module to the model_list.
                if True in perms.values():
                    info = (app_label, model._meta.model_name)
                    model_dict = {
                        'name': capfirst(model._meta.verbose_name_plural),
                        'object_name': model._meta.object_name,
                        'perms': perms,
                    }
                    if perms.get('change', False):
                        try:
                            model_dict['admin_url'] = reverse('admin:%s_%s_changelist' % info, current_app=self.name)
                        except NoReverseMatch:
                            pass
                    if perms.get('add', False):
                        try:
                            model_dict['add_url'] = reverse('admin:%s_%s_add' % info, current_app=self.name)
                        except NoReverseMatch:
                            pass
                    ## added
                    if perms.get("encoder_view_logbook", False):
                        try:
                            print 'Contains this encoder view permissions'
                        except NoReverseMatch:
                            print 'No Reverse Match'
                    if app_label in app_dict:
                        app_dict[app_label]['models'].append(model_dict)
                    else:
                        app_dict[app_label] = {
                            'name': app_label.title(),
                            'app_label': app_label,
                            'app_url': reverse('admin:app_list', kwargs={'app_label': app_label}, current_app=self.name),
                            'has_module_perms': has_module_perms,
                            'models': [model_dict],
                        }

        # Sort the apps alphabetically.
        app_list = list(six.itervalues(app_dict))
        app_list.sort(key=lambda x: x['name'])

        # Sort the models alphabetically within each app.
        for app in app_list:
            app['models'].sort(key=lambda x: x['name'])

        context = {
            'title': _('Site administration'),
            'app_list': app_list,
        }
        context.update(extra_context or {})
        return TemplateResponse(request, self.index_template or
                                'admin/index.html', context,
                                current_app=self.name)
    def get_urls(self):
        from django.conf.urls import patterns, url

        urls = super(NAFDAdminSite, self).get_urls()
        urls += patterns('',
            url(r'^my_view/$', self.admin_view(some_view))
        )
        return urls

admin_site = NAFDAdminSite()