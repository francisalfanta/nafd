import autocomplete_light
autocomplete_light.autodiscover()

from django.contrib import admin
from django.contrib.admin import widgets, helpers
from django.contrib.admin.options import csrf_protect_m

from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.admin import UserAdmin
from django.contrib.admin import SimpleListFilter

from django.http import HttpResponseRedirect, HttpResponse
from django.core import serializers

from .models import *
from .forms import *
from .pdf_license import *

from django.shortcuts import redirect
from django.conf.urls import patterns, include, url

from django.forms.formsets import all_valid
from django.forms.models import BaseInlineFormSet
from django.forms import MediaDefiningClass

from django.utils.translation import ugettext as _
from django.utils.encoding import force_unicode

from django.db.models import Q
from django.db import transaction

import logging
log = logging.getLogger(__name__)

from datetime import timedelta, datetime
from functools import partial

from noconflict import classmaker

from .admin_helpers import *
from .admin_helpers import admin_site
from .utils.import_csv import *


##############################################################
# TESTING
'''
import django_filters
class DirUserFilter(django_filters.FilterSet):
    #group = django_filters.ModelChoiceFilter(lookup_type='Director')
    class Meta:
        model = NAFD_USER_GROUPS
        fields = ['nafd_user__code_name']
'''
## another test ##
## Action buttion ##
def download_csv(modeladmin, request, queryset):
    if not request.user.is_staff:
        raise PermissionDenied
    opts = queryset.model._meta
    model = queryset.model
    response = HttpResponse(mimetype='text/csv')
    # force download.
    response['Content-Disposition'] = 'attachment;filename=export.csv'
    # the csv writer
    writer = csv.writer(response)
    field_names = [field.name for field in opts.fields]
    # Write a first row with header information
    writer.writerow(field_names)
    # Write data rows
    for obj in queryset:
        writer.writerow([getattr(obj, field) for field in field_names])
    return response
download_csv.short_description = "Download selected as csv"

# END TEST MODULE
###############################################################
'''
Foreign keys in django admin list display
'''
class ModelAdminWithForeignKeyLinksMetaclass(MediaDefiningClass):

    def __getattr__(cls, name):

        def foreign_key_link(instance, field):           
            # Django 1.6
            ##Model._meta.module_name was renamed to model_name
            #target._meta.app_label, target._meta.module_name, target.id, unicode(target))
            #print 'app_label: ', target._meta.app_label 
            #print 'model_name: ', target._meta.model_name
            #print 'id: ', target.id
            #print 'target: ', unicode(target)
            target = getattr(instance, field)
            if target:
                return u'<a href="../../%s/%s/%d">%s</a>' % (             
                    target._meta.app_label, target._meta.model_name, target.id, unicode(target)) 

        if name[:8] == 'link_to_':
            method = partial(foreign_key_link, field=name[8:])
            method.__name__ = name[8:]
            method.allow_tags = True
            setattr(cls, name, method)
            return getattr(cls, name)
        raise AttributeError
###### end ######################################################
### ListFilter ###
#ok!
class ApprovedbyListFilter(SimpleListFilter):
    title = _('Approved by')
    parameter_name = 'signatory'
    
    def lookups(self, request, model_admin):
        final_list = dict()
        director_list = NAFD_USER_GROUPS.objects.select_related().filter(group__name='Director')
        for x in director_list:
            final_list[x.nafd_user.id] = x.nafd_user.code_name
        return final_list.items()
    
    def queryset(self, request, queryset):
        if self.value() > 0:           
            return queryset.filter(approved_by=self.value())                    
        if self.value() == 'All':            
            return queryset 

class IssuedbyListFilter(SimpleListFilter):
    title = _('Issued by')
    parameter_name = 'engr'
    
    def lookups(self, request, model_admin):
        final_list = dict()
        evaluator_list = NAFD_USER_GROUPS.objects.select_related().filter(group__name='Engr')
        for x in evaluator_list:
            final_list[x.nafd_user.id] = x.nafd_user.code_name
        return final_list.items()
    
    def queryset(self, request, queryset):
        if self.value() > 0:          
            return queryset.filter(issued_by=self.value())
        if self.value() == 'All':            
            return queryset    
#ok!
class DirectorListFilter(SimpleListFilter):
    title = _('Director')
    parameter_name = 'signatory'
    
    def lookups(self, request, model_admin):
        final_list = dict()
        director_list = NAFD_USER_GROUPS.objects.select_related().filter(group__name='Director')
        for x in director_list:
            final_list[x.nafd_user.id] = x.nafd_user.code_name
        return final_list.items()
    
    def queryset(self, request, queryset):
        if self.value() > 0:           
            return queryset.filter(signatory=self.value())                    
        if self.value() == 'All':            
            return queryset        
        '''
        if self.value() > 0:
            print 'dumaan s zero', self.value()
            for x in director_list:
                l = [x.nafd_user.id]
            return queryset.filter(signatory__in=self.value())
        if self.value() == 'All':
            return queryset
        '''
#ok!
class EncoderListFilter(SimpleListFilter):
    title = _('Encoder')
    parameter_name = 'encoder'
    
    def lookups(self, request, model_admin):
        final_list = dict()
        encoder_list = NAFD_USER_GROUPS.objects.select_related().filter(group__name='Encoder')
        for x in encoder_list:
            final_list[x.nafd_user.id] = x.nafd_user.code_name
        return final_list.items()
    
    def queryset(self, request, queryset):
        if self.value() > 0:          
            return queryset.filter(encoder=self.value())
        if self.value() == 'All':            
            return queryset    
#ok!
class EngrListFilter(SimpleListFilter):
    title = _('Evaluator')
    parameter_name = 'engr'
    
    def lookups(self, request, model_admin):
        final_list = dict()
        evaluator_list = NAFD_USER_GROUPS.objects.select_related().filter(group__name='Engr')
        for x in evaluator_list:
            final_list[x.nafd_user.id] = x.nafd_user.code_name
        return final_list.items()
    
    def queryset(self, request, queryset):
        if self.value() > 0:          
            return queryset.filter(evaluator=self.value())
        if self.value() == 'All':            
            return queryset    

class RBUserListFilter(SimpleListFilter):
    title = _('Assign to')
    parameter_name = 'current_user'
    
    def lookups(self, request, model_admin):
        final_list = dict()
        rbuser_list = NAFD_USER_GROUPS.objects.select_related().filter(group__name='Regulation Branch Personnel')
        for x in rbuser_list:
            final_list[x.nafd_user.id] = x.nafd_user.code_name
        return final_list.items()
    
    def queryset(self, request, queryset):
        if self.value() > 0:          
            return queryset.filter(current_user=self.value())
        if self.value() == 'All':            
            return queryset 

class RBUserListFilter2(SimpleListFilter):
    title = _('Created by')
    parameter_name = 'current_user'
    
    def lookups(self, request, model_admin):
        final_list = dict()
        rbuser_list = NAFD_USER_GROUPS.objects.select_related().filter(group__name='Regulation Branch Personnel')
        for x in rbuser_list:
            final_list[x.nafd_user.id] = x.nafd_user.code_name
        return final_list.items()
    
    def queryset(self, request, queryset):
        if self.value() > 0:          
            return queryset.filter(current_user=self.value())
        if self.value() == 'All':            
            return queryset 
### END ListFilter ###
### Inline ####
#ok!
class RequiredInlineFormSet(BaseInlineFormSet):
    """
    Generates an inline formset that is required
    """

    def _construct_form(self, i, **kwargs):
        """
        Override the method to change the form attribute empty_permitted
        """
        form = super(RequiredInlineFormSet, self)._construct_form(i, **kwargs)
        form.empty_permitted = True
        return form
#ok!
class SOAdetailInline(admin.TabularInline):
    model   = SOA_detail
    #form   = SoadetailForm
    form    = autocomplete_light.modelform_factory(SOA_detail, form=SoadetailForm)    
    extra   = 0
    formset = RequiredInlineFormSet
    classes = ('grp-collapse grp-open',)
    inline_classes = ('grp-collapse grp-open',)

    class Media:
        css = { 'all': ['css/soainline.css'],}
        js = ('admin/js/soainline.js',)
#OK!
class RSLInline(InlineEditLinkMixin, admin.TabularInline): 
    fields  = ['edit_details', 'issued', 'rslno', 'status', 'sitename', 'class_of_station', 'ptsvc', 'form_serial', 'evaluator', 'encoder']   
    form    = RslInlineForm
    model   = LatestRsl_v2

    extra   = 0
    classes = ('grp-collapse grp-open',)
    inline_classes = ('grp-collapse grp-open',)
#OK!
class PPPInline(InlineEditLinkMixin, admin.TabularInline):
    #readonly_fields = ['id']
    extra   = 0
    fields  = ['edit_details', 'makemodel', 'freqrange_low', 'freqrange_high', 'bwe', 'power', 'serialno', 'sitename']
    form    = PPPInlineForm
    model   = Equipment
    classes = ('grp-collapse grp-open',)
    inline_classes = ('grp-collapse grp-open',)

    def save_model(self, request, obj, form, change): 
        if request.user.groups.filter(name='Engr').exists():
            print 'Savin Inline Equipment - Engr View LogBook'
#OK!   
class Official_ReceiptInline(admin.TabularInline):
    model   = LatestRsl_v2_Official
    form    = RSL_ORForm
    extra   = 0
    #classes = ('grp-collapse grp-open',)
    #inline_classes = ('grp-collapse grp-open',)
#OK!
class StatementsInline(admin.TabularInline):
    model   = Statements
    #form    = autocomplete_light.modelform_factory(Statements)
    form    = StatementForm
    extra   = 0
    classes = ('grp-collapse grp-open',)
    inline_classes = ('grp-collapse grp-open',)

### for testing
class EquipRackInline(admin.TabularInline):
    model   = EquipRack
    #form    = autocomplete_light.modelform_factory(Statements)
    form    = EquipRackForm
    extra   = 0
    classes = ('grp-collapse grp-open',)
    inline_classes = ('grp-collapse grp-open',)
### end
#OK!
class EquipmentInline(admin.TabularInline):   
    extra = 0
    fields = [ 'equipment', 'equip_freqrange', 'equip_txrx', 'equip_callsign', 
              'equip_powerbwe', 'equip_purchase', 'equip_possess', 'equip_storage', 'equip_usagepolarity', 'ant_details']
    model = LatestRsl_v2_Equipment
    form  = LatestRsl_v2_EquipmentForm    
    verbose_name_plural = "Related Equipments"
    verbose_name        = "Equipment for RSL"
    classes = ('grp-collapse grp-open',)
    inline_classes = ('grp-collapse grp-open',)

### END Inline ####
#ok!            
class MasterRslAdmin(admin.ModelAdmin):
    list_display        = ['rslno','issued','carrier','site','validity_to','encoder']
    search_fields       = ['=rslno','=issued','carrier','validity_to','encoder','form_serial', 
                           'sn1', 'sn2', 'sn3', 'sn4', 'sn5', 'sn6', 'sn7', 'sn8',
                           'sn9', 'sn10', 'sn11', 'sn12', 'sn13', 'sn14', 'sn15',
                           'sn16', 'sn17', 'sn18', 'sn19', 'sn20', 'sn21', 'sn22',
                           'sn23', 'sn24']
    fieldsets           = [
        (None,              {'fields'  : [('status', 'rslno', 'validity_from', 'validity_to','extension','form_serial'),]}),
        ('Site Info',       {'fields'  : ('issued', 'carrier', 'site', ('street', 'city'),('province', 'region'), 'longitude', 'latitude')}),
        ('Remarks',         {'fields'  : ('remarks','remarks_2')}),
        ('Antenna Info',    {'classes' : ('grp-collapse grp-closed',),
                             'fields'  : ('lic_to_operate',('class_of_station', 'nature_of_service'), 'ptsvc',
                                          'dir', 'h', 'gn', 't')}),
        ('Equipment Info',  {'classes' : ('grp-collapse grp-closed',),
                             'fields'  : ('make','freqrange','bwe_1','power','callsign','spare_equip_serial',
                                         ('polarity1','tx1_min','tx1','tx1_max'),
                     ('sn1','rx1_min','rx1','rx1_max'),
                     ('polarity2','tx2_min','tx2','tx2_max'),
                     ('sn2','rx2_min','rx2','rx2_max'),
                     ('polarity3','tx3_min','tx3','tx3_max'),
                     ('sn3','rx3_min','rx3','rx3_max'),
                     ('polarity4','tx4_min','tx4','tx4_max'),
                     ('sn4','rx4_min','rx4','rx4_max'),
                                         ('polarity5','tx5_min','tx5','tx5_max'),
                                         ('sn5','rx5_min','rx5','rx5_max'),
                                         ('polarity6','tx6_min','tx6','tx6_max'),
                                         ('sn6','rx6_min','rx6','rx6_max'),
                                         ('polarity7','tx7_min','tx7','tx7_max'),
                     ('sn7','rx7_min','rx7','rx7_max'),
                                         ('polarity8','tx8_min','tx8','tx8_max'),
                                         ('sn8','rx8_min','rx8','rx8_max'),
                                         ('polarity9','tx9_min','tx9','tx9_max'),
                     ('sn9','rx9_min','rx9','rx9_max'),
                                         ('polarity10','tx10_min','tx10','tx10_max'),
                                         ('sn10','rx10_min','rx10','rx10_max'),
                                         ('polarity11','tx11_min','tx11','tx11_max'),
                                         ('sn11','rx11_min','rx11','rx11_max'),
                                         ('polarity12','tx12_min','tx12','tx12_max'),
                     ('sn12','rx12_min','rx12','rx12_max'))}),
        ('Other Serial No', {'classes'  : ('grp-collapse grp-closed',),
                             'fields'   : ('sn13','sn14','sn15','sn16','sn17',
                                          'sn18','sn19','sn20','sn21','sn22','sn23','sn24')
                                          }),
        ('Cashier Stamp',   {'classes' : ('grp-collapse grp-closed',),
                             'fields'  : (('or_no', 'or_no2'),
                                          ('amount', 'amount2'),
                                          ('date_paid','date_paid2'),'dst',
                                          )}),
        ('Control Info',    {'classes' : ('grp-collapse grp-closed',),
                             'fields'  : (('encoder','evaluator','signatory'),)}),
        ]
#ok!
class LatestRslAdmin(admin.ModelAdmin):
    form                = autocomplete_light.modelform_factory(LatestRsl)
    list_display        = ['rslno','issued','carrier','site', 'tx1','rx1', 'validity_to','longitude', 'latitude', 'encoder']
    save_as             = True
    search_fields       = ['=rslno','=issued','longitude', 'latitude','site','carrier','validity_to','encoder','form_serial','callsign',
				   'sn1','sn2','sn3','sn4','sn5','sn6','sn7','sn8','sn9','sn10','sn11','sn12','sn13',
				   'sn14','sn15','sn16','sn17','sn18','sn19','sn20','sn21','sn22','sn23','sn24']
    fieldsets           = [
        ('Site Info',       {'fields'  : ( 'carrierFK', 'site', ('street'),('philaddress'), ('deg_long', 'min_long', 'sec_long'),
                                           ('deg_lat', 'min_lat', 'sec_lat'),)}),
        ('For Update',      {'fields'  : [('status', 'rslno', 'issued'),('validity_from', 'validity_to','extension'),'form_serial',]}),
	    ('Cashier Stamp',   {'classes' : ('grp-collapse grp-open',),
                             'fields'  : (('or_no', 'or_no2'),
                                          ('amount', 'amount2'),
                                          ('date_paid','date_paid2'),'dst',
                                          )}),
	    ('Control Info',    {'classes' : ('grp-collapse grp-open',),
                             'fields'  : (('updater', 'encoder'),('evaluator','signatory'),)}),
 	    ('Equipment Info',  {'classes' : ('grp-collapse grp-closed',),
                             'fields'  : ('make','freqrange','bwe_1','power','callsign','spare_equip_serial',
                    					 ('polarity1','tx1_min','tx1','tx1_max'),
                    					 ('sn1','rx1_min','rx1','rx1_max'),
                    					 ('polarity2','tx2_min','tx2','tx2_max'),
                    					 ('sn2','rx2_min','rx2','rx2_max'),
                    					 ('polarity3','tx3_min','tx3','tx3_max'),
                    					 ('sn3','rx3_min','rx3','rx3_max'),
                     					 ('polarity4','tx4_min','tx4','tx4_max'),
                    					 ('sn4','rx4_min','rx4','rx4_max'),
                                         ('polarity5','tx5_min','tx5','tx5_max'),
                                         ('sn5','rx5_min','rx5','rx5_max'),
                                         ('polarity6','tx6_min','tx6','tx6_max'),
                                         ('sn6','rx6_min','rx6','rx6_max'),
                                         ('polarity7','tx7_min','tx7','tx7_max'),
                    					 ('sn7','rx7_min','rx7','rx7_max'),
                                         ('polarity8','tx8_min','tx8','tx8_max'),
                                         ('sn8','rx8_min','rx8','rx8_max'),
                                         ('polarity9','tx9_min','tx9','tx9_max'),
                    					 ('sn9','rx9_min','rx9','rx9_max'),
                                         ('polarity10','tx10_min','tx10','tx10_max'),
                                         ('sn10','rx10_min','rx10','rx10_max'),
                                         ('polarity11','tx11_min','tx11','tx11_max'),
                                         ('sn11','rx11_min','rx11','rx11_max'),
                                         ('polarity12','tx12_min','tx12','tx12_max'),
                    					 ('sn12','rx12_min','rx12','rx12_max'))}),
        ('Other Serial No', {'classes'  : ('grp-collapse grp-closed',),
                             'fields'   : ('sn13','sn14','sn15','sn16','sn17',
                                          'sn18','sn19','sn20','sn21','sn22','sn23','sn24')
                                          }),                       
        ('Remarks',         {'fields'  : ('remarks','remarks_2')}),
        ('Antenna Info',    {'classes' : ('grp-collapse grp-closed',),
                             'fields'  : ('lic_to_operate',('class_of_station', 'nature_of_service'), 'ptsvc',
                                          'dir', 'h', 'gn', 't')}),       
        ]
    actions = [print_preview, preview_data]

    def response_change(self, request, obj):
        res = super(LatestRslAdmin, self).response_change(request, obj)
        if "next" in request.GET:
            return HttpResponseRedirect(request.GET['next'])
        else:
            return res

    def response_add(self, request, obj):
        res = super(LatestRslAdmin, self).response_add(request, obj)
        if "next" in request.GET:
            return HttpResponseRedirect(request.GET['next'])
        else:
            return res         
# ok
class CarrierAdmin(admin.ModelAdmin):
    list_display        = ['companyname','contactperson', 'street',  'c_initial']
    search_fields       = ['companyname','contactperson', 'c_initial', ]  
    #exclude             = ['address_id']
    form                = autocomplete_light.modelform_factory(Carrier, form=CarrierForm)
    actions              = [export_as_csv]
#### Statement of Accounts ####
#ok!
class SOAAdmin(admin.ModelAdmin):
    #change_list_template = "admin/change_list_filter_sidebar.html"
    # to display horizontally --seems not working   
    list_display        = ['soa_code', 'date_issued', 'carrier', 'service_type', 'issued_by', 'approved_by', 'no_years', 
                           'validity_from', 'validity_to', 'official_receipt']
    search_fields       = ['soa_code', 'official_receipt__or_no' ]
    fieldsets           = [(None, {'fields': ('soa_code',  'date_issued', 'carrier', 'app_type', ('service_type', 'no_years'), 
                                             ('validity_from', 'validity_to'))}),
                           ('Official Receipt', {'fields': ('official_receipt',)}),  
        ] # for manual soa code
    #fieldsets           = [('', {'fields': ('carrier', 'app_type', ('service_type', 'no_years'), ('validity_from', 'validity_to'))}),] # for auto soa code
    #exclude             = ['soa_code']
    inlines             = (SOAdetailInline,)                              
    form                = SoaForm
    list_filter         = ['date_issued', 'validity_from', 'validity_to', 'carrier', 'service_type', IssuedbyListFilter, ApprovedbyListFilter , 'app_type']
    date_hierarchy      = 'date_issued'
    actions              = [export_as_csv]
    
    class Media:
        js = ('admin/js/soa.js',)

    def response_change(self, request, obj):        
        res = super(SOAAdmin, self).response_change(request, obj)
        if "next" in request.GET:
            return HttpResponseRedirect(request.GET['next'])
        else:
            return res 
       
    def response_add(self, request, obj):  
        res = super(SOAAdmin, self).response_add(request, obj)
        if "next" in request.GET:
            return HttpResponseRedirect(request.GET['next'])       
        else:
            return res 

    def get_urls(self):
        urls = super(SOAAdmin, self).get_urls()
        my_urls = patterns('',
            (r'^my_view/$', self.my_view)
        )
        return my_urls + urls

    def my_view(self,request,pk):
        from django.shortcuts import render_to_response
        from django.template import RequestContext

        object = Model.objects.get(pk=pk)
        model_dict = model_object.__dict__
        return render_to_response('admin/ccad/soa/model_view.html',locals(),context_instance=RequestContext(request))
    
    @csrf_protect_m
    @transaction.commit_on_success
    def add_view(self, request, form_url='', extra_context=None):
        "The 'add' admin view for this model."
        model = self.model
        opts = model._meta

        if not self.has_add_permission(request):
            raise PermissionDenied

        ModelForm = self.get_form(request)
        formsets = []
        inline_instances = self.get_inline_instances(request)
        if request.method == 'POST':
            form = ModelForm(request.POST, request.FILES)
            if form.is_valid():
               new_object = self.save_form(request, form, change=False)
               form_validated = True
            else:
               form_validated = False
               new_object = self.model()
            prefixes = {}
            for FormSet, inline in zip(self.get_formsets(request), inline_instances):
               prefix = FormSet.get_default_prefix()
               prefixes[prefix] = prefixes.get(prefix, 0) + 1
               if prefixes[prefix] != 1 or not prefix:
                  prefix = "%s-%s" % (prefix, prefixes[prefix])
               formset = FormSet(data=request.POST, files=request.FILES,
                              instance=new_object,
                              save_as_new="_saveasnew" in request.POST,
                              prefix=prefix, queryset=inline.queryset(request))
               formsets.append(formset)
            if all_valid(formsets) and form_validated:
               self.save_model(request, new_object, form, False)
               self.save_related(request, form, formsets, False)
               self.log_addition(request, new_object)
               log.info('The new object has %s id' % new_object.id)
               ## added
               print 'entered response_add soa'
                # saving soa id to LogBook
               if "log_id" in request.GET:
                   next    = request.GET.get('next')
                   log_id  = request.GET.get('log_id')       
                   logbk   = LogBook.objects.get(pk=log_id)
                   soa     = SOA.objects.get(pk=new_object.id)                   
                   print 'saving new log id and soa id'
                   payment = Statements.objects.create(logbook=logbk, soa=soa)
                   payment.save()
               print 'save successful for new payment'
               print ' Saving SOA in group Engr' 
               ### end add
               print 'inside what i want', new_object.id
               return HttpResponseRedirect('/admin/ccad/soa/%s' % new_object.id) #<-- changed to my new one
        else:
            # Prepare the dict of initial data from the request.
            # We have to special-case M2Ms as a list of comma-separated PKs.
            initial = dict(request.GET.items())
            for k in initial:
                try:
                    f = opts.get_field(k)
                except models.FieldDoesNotExist:
                    continue
                if isinstance(f, models.ManyToManyField):
                    initial[k] = initial[k].split(",")
            form = ModelForm(initial=initial)
            prefixes = {}
            for FormSet, inline in zip(self.get_formsets(request), inline_instances):
                prefix = FormSet.get_default_prefix()
                prefixes[prefix] = prefixes.get(prefix, 0) + 1
                if prefixes[prefix] != 1 or not prefix:
                    prefix = "%s-%s" % (prefix, prefixes[prefix])
                formset = FormSet(instance=self.model(), prefix=prefix,
                                  queryset=inline.queryset(request))
                formsets.append(formset)

        adminForm = helpers.AdminForm(form, list(self.get_fieldsets(request)),
            self.get_prepopulated_fields(request),
            self.get_readonly_fields(request),
            model_admin=self)
        media = self.media + adminForm.media

        inline_admin_formsets = []
        for inline, formset in zip(inline_instances, formsets):
            fieldsets = list(inline.get_fieldsets(request))
            readonly = list(inline.get_readonly_fields(request))
            prepopulated = dict(inline.get_prepopulated_fields(request))
            inline_admin_formset = helpers.InlineAdminFormSet(inline, formset,
                fieldsets, prepopulated, readonly, model_admin=self)
            inline_admin_formsets.append(inline_admin_formset)
            media = media + inline_admin_formset.media

        context = {
            'title': _('Add %s') % force_unicode(opts.verbose_name),
            'adminform': adminForm,
            'is_popup': "_popup" in request.REQUEST,
            'show_delete': False,
            'media': media,
            'inline_admin_formsets': inline_admin_formsets,
            'errors': helpers.AdminErrorList(form, formsets),
            'app_label': opts.app_label,
        }
        context.update(extra_context or {})
        return self.render_change_form(request, context, form_url=form_url, add=True)
   
    def save_model(self, request, obj, form, change):          
        if request.user.groups.filter(name='Encoder').exists():         # not verified
            pass
        elif request.user.groups.filter(name='Engr').exists():            # not verified 
            #print 'ENGR: obj.suf_fees :', obj.suf_fees
            return super(SOAAdmin, self).save_model(request, obj, form, change)
        elif request.user.groups.filter(name='RB Secretary').exists():    # not verified
            pass
        else:
            #print 'ELSE - obj.suf_fees :', obj.suf_fees
            return super(SOAAdmin, self).save_model(request, obj, form, change)
#ok!
class SOAdetailAdmin(admin.ModelAdmin):
    __metaclass__ = classmaker(right_metas=(ModelAdminWithForeignKeyLinksMetaclass,))
    list_display        = ['sitename', 'link_to_soa', 'site_addr', 'call_sign', 'old_chan', 'channel', 'freq', 'bw', 'ppp_units', 'rsl_units', 'mod_units', 'stor_units']
    search_fields       = ['call_sign', 'sitename', 'site_addr', 'city', 'band']        
    form = autocomplete_light.modelform_factory(SOA_detail)
    actions              = [export_as_csv]
 
#### end Statement of Accounts ####
#### Logbook #### OK!
class LetterLogBookAdmin(admin.ModelAdmin):
    list_display        = ['controlNo', 'dateEntry', 'letter_from', 'letter_to', 'subject']
    verbose_name_plural = 'Letter Logbook'
    date_hierarchy      = 'dateEntry'
    search_fields       = ['controlNo', 'letter_from', 'letter_to', 'subject']
    actions              = [export_as_csv]

    def get_readonly_fields(self, request, obj=None):
        return ['controlNo']

    def response_change(self, request, obj):
        res = super(LetterLogBookAdmin, self).response_change(request, obj)
        if "next" in request.GET:
            return HttpResponseRedirect(request.GET['next'])
        else:
            return res

    def response_add(self, request, obj):
        res = super(LetterLogBookAdmin, self).response_add(request, obj)
        if "next" in request.GET:
            return HttpResponseRedirect(request.GET['next'])
        else:
            return res  
#OK!
class Pending_descAdmin(admin.ModelAdmin):
    list_display        = ['pend_description']
    actions              = [export_as_csv]   
#OK!
class PPPfilesAdmin(admin.ModelAdmin):
    list_display        = ['logbook', 'user', 'docfile']
    search_fields       = ['logbook__controlNo', 'user__code_name', 'user__username', 'user__first_name', 'user__last_name', 'docfile']
    list_filter         = ['user', 'logbook']
    actions             = [export_as_csv]
    exclude             = ['user']

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        return super(PPPfilesAdmin, self).save_model(request, obj, form, change)

    def get_changelist(self, request, **kwargs):
        """Returning change list by requested user Only."""
        from django.contrib.admin.views.main import ChangeList

        class ActiveChangeList(ChangeList):
            def get_query_set(self, *args, **kwargs):
                qs = super(ActiveChangeList, self).get_query_set(*args, **kwargs)
                return qs.filter(Q(user=request.user))

        return ActiveChangeList
    '''
    def render_change_form(self, request, context, add=False, change=False, form_url='', obj=None):
    #def add_view(self, request, form_url='', extra_context=None):        
        if request.method == 'GET':
            print 'request.method = GET : ', request.GET.get('logbook__id__exact')
            if request.GET.get('logbook__id__exact'):
                print '*** PPP request key found ***'
        return super(PPPfilesAdmin, self).render_change_form(request, context, add=False, change=False, form_url='', obj=None)
    '''
#OK!
class Official_ReceiptAdmin(admin.ModelAdmin):
    list_display        = ['or_no', 'date_paid', 'amount', 'validity_from', 'validity_to', 'carrier' ]
    #form                = autocomplete_light.modelform_factory(Official_Receipt)
    form                = Official_ReceiptForm
    search_fields       = ['or_no', 'amount']
    list_filter         = ['date_paid', 'validity_from', 'validity_to', 'carrier']
    date_hierarchy      = 'date_paid'
    actions              = [export_as_csv]
    #save_as             = True
#OK!
class LogBookAdmin(admin.ModelAdmin):
    #change_list_template = "admin/change_list_filter_sidebar.html"
    list_filter         = ['due_date', 'acceptancedate', 'carrier', 'status', 'transtype', 'service', RBUserListFilter, 'pending_desc']
    search_fields       = ['controlNo', 'permitNo', 'first_stn', 'last_stn', 'soa__soa_code']#,  'official_receipt__or_no']
    date_hierarchy      = 'acceptancedate'
    list_display        = ['controlNo','acceptancedate','due_date',  'carrier', 'status', 'permitNo','units',
                           'noofstation','first_stn', 'last_stn', 'transtype']#, 'official_receipt']    
    exclude             = ['encoder_status', 'engr_status', 'chief_status', 'ischecked', 'pend_at', 'engrchoice']    
    
    fieldsets           = [
        ('Logbook Detail',      {   'classes'   : ('grp-collapse grp-open',),
                                    'fields'    : (('current_user', 'controlNo', 'status'),('acceptancedate', 'due_date'), 'carrier',                                                   
                                               'permitNo')}),        
        ## for TESTING
        #('Official Receipts',   {   'classes'   : ('placeholder statements_set-group',),
        #                            'fields'    : ()}),
        ('Statement of Account Info', {'classes':('grp-collapse grp-open',),
                                       'fields' :(('transtype', 'service'),'units','noofstation','first_stn','last_stn')}),
        
        ('Remarks',             {   'classes'   : ('grp-collapse grp-open',),
                                    'fields'    : ('logbook_remarks',)}),
        
        ('Read Only fields',    {   'classes'   : ('grp-collapse grp-open',),
                                    'fields'    : ('fas_data',
                                                   'endorsementfile','pending_desc')}),
    ]
    inlines             = (StatementsInline, EquipRackInline, RSLInline,)
    form                = LogBookForm
    actions             = [export_as_csv]

    class Media:
        js = (
            'js/jquery-1.9.1.js',
            'js/jquery.min.js',
            'js/jquery-ui.js',          
            )
        css = { 'all' : ['css/logbook_css.css'], }

    def save_model(self, request, obj, form, change):
        print 'entered LogbookAdmin save model'          
        added = 0     
        ext_added = 0
        ext = 0
        start_ext = 0
        ## value for due date
        if obj.units < 20 and obj.transtype in 'DEMO':
            print 'obj.units < 20 and obj.transtype in DEMO'
            ext = 3
            start_ext = 4
        elif obj.units >= 20 and obj.transtype in 'DEMO':
            print 'obj.units >= 20 and obj.transtype in DEMO'
            ext = 10
            start_ext = 11
        elif obj.units < 20 and obj.transtype in 'PPP':
            print 'obj.units < 20 and obj.transtype in PPP'
            ext = 1
            start_ext = 2
        elif obj.units >= 20 and obj.transtype in 'PPP':
            print 'obj.units >= 20 and obj.transtype in PPP'
            ext = 10
            start_ext = 11
        elif obj.units < 20 and obj.transtype in 'RECALL':
            print 'obj.units < 20 and obj.transtype in RECALL'
            ext = 1
            start_ext = 2
        elif obj.units >= 20 and obj.transtype in 'RECALL':
            print 'obj.units >= 20 and obj.transtype in RECALL'
            ext = 10
            start_ext = 11
        elif obj.noofstation+obj.units < 20 and obj.transtype in 'REN / MODPPPRECALL': 
            print 'object less than 3: REN / MODPPPRECALL'               
            ext = 3
            start_ext = 4
        elif obj.noofstation+obj.units >= 20 and obj.transtype in 'REN / MODPPPRECALL': 
            print 'obj.noofstation+obj.units >= 20 and and obj.transtype in REN / MODPPPRECALL:'                             
            ext = 10
            start_ext = 11        
        elif obj.noofstation < 20 and obj.transtype in 'RENNEWDUPREN / DUPDUP / REN':  
            print 'obj.noofstation < 20 and obj.transtype in RENNEWDUP:'               
            ext = 3
            start_ext = 4
        elif obj.noofstation >= 20 and obj.transtype in 'RENNEWDUPREN / DUPDUP / REN':  
            print 'obj.noofstation >= 20 and obj.transtype in RENNEWDUP:'               
            ext = 10
            start_ext = 11
        #elif obj.units < 3 and obj.transtype in 'PPP':

        # loop thru the days
        for i in range(1, ext+1):
            due = obj.acceptancedate+timedelta(days=i)
            # check holidays in no_work table
            holiday_instance = no_work.objects.filter(Q(nowork_day__month=due.month) & Q(nowork_day__day=due.day))  
            if due.isoweekday() == 6 or due.isoweekday() == 7 or holiday_instance.exists():                    
                added +=1
                print 'no work days found: ', added
        # range up to 30 days set can be extended as needed
        for i in range(start_ext, 30):                                    
            due = obj.acceptancedate+timedelta(days=i)
            ext_hol_instance = no_work.objects.filter(Q(nowork_day__month=due.month) & Q(nowork_day__day=due.day))
            # checking beyond 3 days if its weekend
            if not (ext_hol_instance.exists() or (due.isoweekday() == 6 or due.isoweekday() == 7)) and not (added == 0):                
                # days left to add
                added = added -1
                print '30 files more added: ', added
                # the day is working day                
                ext_added = i                    
                print '30 files ext_added', ext_added                
        print 'ext_added :', ext_added
        print 'added :', added
        if ext_added == 0:
            obj.due_date = obj.acceptancedate+timedelta(days=ext+added)
        else:     
            obj.due_date = obj.acceptancedate+timedelta(days=ext_added)     
        
        if request.user.groups.filter(name='Encoder').exists():         # not verified
            pass
        elif request.user.groups.filter(name='Engr').exists():            # verified
            print 'Saved by Engr.'
        #elif request.user.groups.filter(name='RB Secretary').exists():    # not verified
        #    pass
        #else:        
        return super(LogBookAdmin, self).save_model(request, obj, form, change)
   
    def get_readonly_fields(self, request, obj=None):  
        user_id = NAFD_User.objects.get(code_name=request.user)
        print 'Request User: ', request.user
        # NAFD_USER_GROUPS.objects.filter(Q(nafd_user=user_id) & Q(group__name='Engr'))      
        if NAFD_USER_GROUPS.objects.filter(Q(nafd_user=user_id) & Q(group__name='Engr')).exists():
            print 'Engr View LogBook'            
            return ['permitNo', 'logbook_remarks',  'acceptancedate', 'controlNo', 'docfile', 'endorsementfile', 'fas_data',  'pending_desc', 'due_date', 'units', 'noofstation','first_stn','last_stn', 'service', 'status', 'transtype']
        elif NAFD_USER_GROUPS.objects.filter(Q(nafd_user=user_id) & Q(group__name='NAFD Secretary')).exists():
            print 'NAFD Secretary View'
            #return ['controlNo', 'docfile', 'endorsementfile', 'fas_data', 'status', 'pending_desc', 'due_date', 'units', 'noofstation','first_stn','last_stn', 'transtype', 'service']
            return ['controlNo', 'docfile', 'endorsementfile', 'fas_data', 'pending_desc', 'due_date', 'units', 'noofstation','first_stn','last_stn',  'service']
        elif NAFD_USER_GROUPS.objects.filter(Q(nafd_user=user_id) & Q(group__name='Encoder')).exists():
            print 'Encoder View'
            #return ['current_user', 'permitNo', 'logbook_remarks',  'acceptancedate', 'controlNo', 'docfile', 'endorsementfile', 'fas_data', 'status', 'pending_desc', 'due_date', 'units', 'noofstation','first_stn','last_stn', 'transtype', 'service']
            return [ 'logbook_remarks',  'acceptancedate', 'controlNo', 'docfile', 'endorsementfile', 'fas_data', 'pending_desc', 'due_date', 'units', 'noofstation','first_stn','last_stn', 'service']
        else:
            print 'Admin View'
            return ['current_user', 'permitNo', 'logbook_remarks',  'acceptancedate', 'controlNo', 'docfile', 'endorsementfile', 'fas_data', 'status', 'pending_desc', 'due_date', 'units', 'noofstation','first_stn','last_stn', 'transtype', 'service']
    
    def response_change(self, request, obj):
        res = super(LogBookAdmin, self).response_change(request, obj)
        if "next" in request.GET:
            return HttpResponseRedirect(request.GET['next'])
        else:
            return res
    
    def response_add(self, request, obj):
        res = super(LogBookAdmin, self).response_add(request, obj)
        if "next" in request.GET:
            return HttpResponseRedirect(request.GET['next'])
        else:
            return res

    #def has_add_permission(self, request):
    #    return False

    #def __init__(self, *args, **kwargs):
    #    super(LogBookAdmin, self).__init__(*args, **kwargs)
    #    self.list_display_links = (None,)

    # to hide change and add buttons on main page:
    #def get_model_perms(self, request): 
    #    return {'view': True}
#OK!
class SitenameAdmin(admin.ModelAdmin):
    list_display        = ['site', 'street', 'address', 'longitude', 'latitude', 'carrier']    
    form                = SitenameForm
    readonly_fields     = ['longitude', 'latitude']
    search_fields       = ['site', 'street', 'longitude', 'latitude']
    list_filter         = ['carrier', 'address']
    fieldsets = [
        (None,              {'fields': ['site', 'street', 'address', 'carrier', ('deg_long', 'min_long', 'sec_long', 'longitude'),
                                        ('deg_lat', 'min_lat', 'sec_lat', 'latitude')]}),
        ]
    actions              = [export_as_csv]

    #class Media:
        #js = ['admin/js/longlat.js', ]
        #css = { 'all' : ['css/latestrsl_v2_css.css'], } 
#OK!
class ClassofstationAdmin(admin.ModelAdmin):
    list_display        = ['class_name', 'description']
    actions              = [export_as_csv]
#OK!
class EquipModelAdmin(admin.ModelAdmin):
    list_display        = ['make']
    search_fields       = ['make']
    actions              = [export_as_csv]
#OK!
class AntennaAdmin(admin.ModelAdmin):
    form                = autocomplete_light.modelform_factory(Antenna)
    list_display        = ['id', 'antenna_type','directivity', 'height', 'gain' ]  
    search_fields       = ['id', 'antenna_type', 'directivity', 'height', 'gain']
    actions              = [export_as_csv]
#### end Logbook ####
#### Support Documents ####
class SuggestionboxAdmin(admin.ModelAdmin):
    form                = SuggestionboxForm
    list_display        = ['title', 'remark', 'username']
    list_filter         = [RBUserListFilter2]
    search_fields       = ['title', 'remark', 'username']
    fieldsets           = [(None, {'fields': ['title', 'remark']}),]  
    actions             = [export_as_csv]

    def save_model(self, request, obj, form, change):  
        obj.username = request.user        
        return super(SuggestionboxAdmin, self).save_model(request, obj, form, change)

class DocFormatsAdmin(admin.ModelAdmin):
    form                = DocFormatsForm
    list_display        = ['title', 'docfile', 'username']
    list_filter         = [RBUserListFilter2]
    search_fields       = ['title', 'docfile', 'username']
    fieldsets           = [(None, {'fields': ['title', 'docfile']}),]
    actions             = [export_as_csv]

    def save_model(self, request, obj, form, change):  
        obj.username = request.user        
        return super(DocFormatsAdmin, self).save_model(request, obj, form, change)
#### End Documents ####
#OK!
class EquipmentAdmin(admin.ModelAdmin):
    #form                = autocomplete_light.modelform_factory(Equipment)#, form=EquipmentForm)
    form                = EquipmentForm
    search_fields       = ['tx_min', 'tx', 'tx_max', 'rx_min', 'rx', 'rx_max', 'power',
                           'freqrange_low', 'freqrange_high', 'callsign', 'usages', 'serialno', 'polarity', 'p_purchase', 'p_possess', 'p_storage', 'makemodel__make',
                           'antenna__antenna_type','sitename__street', 'sitename__address__city', 'sitename__address__province']
    list_display        = ['makemodel', 'serialno', 'callsign', 'equip_txrx', 'equip_powerbwe', 
                           'equip_freqrange', 'equip_usagepolarity', 'p_purchase', 'p_possess', 'p_storage', 'carrier', 'antenna']
    list_filter         = ['carrier', 'makemodel', 'bwe']
    fieldsets = [
        (None,              {'fields': [('callsign', 'status'),]}),
        ('Make/Type/Model', {'fields': ['makemodel', 'serialno',('power', 'unit'),'bwe','usages']}),
        ('Frequency Range',       {'classes' : ('grp-collapse grp-open',),
                                    'fields': [('freqrange_low','freqrange_high'), ('freqrange_low2','freqrange_high2')]}),
        ('Transmit / Received',    {'classes' : ('grp-collapse grp-open',),
                                    'fields': [('tx_min', 'tx', 'tx_max'), ('rx_min', 'rx', 'rx_max')]}),
        ('Permits',         {'classes' : ('grp-collapse grp-open',),
                                'fields': ['p_purchase', 'p_possess', 'p_storage']}),
        ('Related to',      {'fields': [('carrier', 'antenna'),]})
    ]
    actions              = [export_as_csv]

    def response_change(self, request, obj):
        res = super(EquipmentAdmin, self).response_change(request, obj)
        if "next" in request.GET:
            return HttpResponseRedirect(request.GET['next'])
        else:
            return res

    def response_add(self, request, obj):
        res = super(EquipmentAdmin, self).response_add(request, obj)
        if "next" in request.GET:
            return HttpResponseRedirect(request.GET['next'])
        else:
            return res     
#OK!            
class LatestRsl_v2Admin(admin.ModelAdmin):
    #change_list_template = "admin/change_list_filter_sidebar.html"
    __metaclass__ = classmaker(right_metas=(ModelAdminWithForeignKeyLinksMetaclass,))
    inlines             = (EquipmentInline, Official_ReceiptInline)  
    form                = LatestRsl_v2Form
    search_fields       = ['=rslno','=issued','logbook__controlNo', 'official_receipt__or_no', 'carrier__companyname', 'equipment__makemodel__make', 'form_serial', 
                           'evaluator__code_name', 'encoder__code_name', 'signatory__code_name', 'sitename__street', 'sitename__site', 'sitename__address__city',
                           'sitename__address__province', 'sitename__address__regioncode', 'equipment__serialno', 'equipment__callsign'] 
                           
    list_display        = ['rslno', 'status', 'issued', 'link_to_carrier', 'link_to_sitename', 'sitename_street', 'sitename_province', 'link_to_logbook',      
                           'form_serial', 'class_of_station', 'nature_of_service', 'ptsvc', 'remarks']
    date_hierarchy      = 'issued'   
    list_filter         = ['carrier', 'class_of_station', 'status', DirectorListFilter, EngrListFilter, EncoderListFilter]
    fieldsets           = [
        ('Logbook Info',       {'fields' : (('logbook'), 'carrier')}),
        ('License Info',       {'classes' : ('grp-collapse grp-open',),
                                'fields' : (('status', 'issued'), ('rslno', 'form_serial', 'capacity'), ('class_of_station', 'lic_to_operate', 'nature_of_service'), 'ptsvc')}), 
        ('Site',               {'classes' : ('grp-collapse grp-open',),
                                'fields' : ('sitename', 'sitename_street', ('sitename_city', 'sitename_province', 'sitename_region'), ('sitename_longitude', 'sitename_latitude')
                                )}),               
        ('Remarks Info',       {'classes' : ('grp-collapse grp-open',),
                                'fields' : ('remarks', ('encoder', 'evaluator'), 'signatory')})        
        ]
    actions              = [export_as_csv]
    # when readonly_fields on saving is not possible
    #readonly_fields     = ('sitename_street', 'sitename_province', 'sitename_region',  'lic_to_operate', 'sitename_city', 'sitename_latitude', 'sitename_longitude')
    
    def response_change(self, request, obj):
        res = super(LatestRsl_v2Admin, self).response_change(request, obj)
        if "next" in request.GET:
            return HttpResponseRedirect(request.GET['next'])
        else:
            return res  

    def response_add(self, request, obj):
        res = super(LatestRsl_v2Admin, self).response_add(request, obj)
        if "next" in request.GET:
            return HttpResponseRedirect(request.GET['next'])
        else:
            return res

    class Media:
        #js = ['js/latestrsl_v2.js', ]
        css = { 'all' : ['css/latestrsl_v2_css.css'], }
#### end RSL required table ####
#ok!
# Define an inline admin descriptor for UserProfile model
# which acts a bit like a singleton
''' Depreciated in Django 1.5
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'profile'
'''
# Define a new User admin
#class UserAdmin(UserAdmin):
#    model = NAFD_User
    #inlines = (UserProfileInline, )

class PhilAddressAdmin(admin.ModelAdmin):
    list_display = ['city', 'province', 'region', 'regioncode']
    search_fields= ['city', 'province', 'region', 'regioncode']
    list_filter  = ['city', 'province', 'region', 'regioncode']
    form         = PhilAddressForm  
    actions              = [export_as_csv]    

class no_workAdmin(admin.ModelAdmin):
    list_display = ['nowork_day', 'tframe', 'description']
    search_fields= ['nowork_day', 'tframe', 'description']
    actions      = [export_as_csv]
    
admin.site.register(no_work, no_workAdmin)
admin.site.register(PhilAddress, PhilAddressAdmin)
#admin.site.register(MasterRsl, MasterRslAdmin)
#admin.site.register(LatestRsl, LatestRslAdmin)
admin.site.register(Carrier, CarrierAdmin)

admin.site.register(SOA, SOAAdmin)
admin.site.register(SOA_detail, SOAdetailAdmin)

admin.site.register(Letter_LogBook, LetterLogBookAdmin)
admin.site.register(Pending_desc, Pending_descAdmin)
admin.site.register(PPPfiles, PPPfilesAdmin)
admin.site.register(Official_Receipt, Official_ReceiptAdmin)
admin.site.register(LogBook, LogBookAdmin)
admin.site.register(Sitename, SitenameAdmin)                           
admin.site.register(Classofstation, ClassofstationAdmin)
admin.site.register(EquipModel, EquipModelAdmin)
admin.site.register(Antenna, AntennaAdmin)
admin.site.register(Equipment, EquipmentAdmin)
admin.site.register(LatestRsl_v2, LatestRsl_v2Admin)

admin.site.register(Suggestion_box, SuggestionboxAdmin)
admin.site.register(DocFormats, DocFormatsAdmin)
# Re-register UserAdmin
''' Depreciated in Django 1.5
admin.site.unregister(User)
'''
class MyUserAdmin(UserAdmin):  
    form     = MyUserChangeForm   
    add_form = MyUserCreationForm 
    fieldsets = (
        (None, {'fields': ('code_name', 'kpi_target', 'foryear')}),
    ) +UserAdmin.fieldsets
admin.site.register(NAFD_User, MyUserAdmin)

class KPIAdmin(admin.ModelAdmin):
    list_display = ['current_year', 'target']
    search_fields= ['current_year', 'target']
    actions      = [export_as_csv]

admin.site.register(KPI, KPIAdmin)




