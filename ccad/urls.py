from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.conf.urls.static import static
#from django.views.generic import DetailView, FormView

#from autocomplete.views import autocomplete
from django.contrib.auth.decorators import permission_required, user_passes_test
from import_excel.views import import_excel
from ccad.forms import RSLImportForm, PPPImportForm
from ccad.models import SOA_detail, LatestRsl, Equipment
from ccad.forms import *


def staff_required(login_url=None):
    return user_passes_test(lambda u: u.is_staff, login_url=login_url)

urlpatterns = patterns('',    
    url(r'^logbook_manual', 'ccad.views.logbook_manual'),
    url(r'^user-kpi', 'ccad.views.kpi_data', name='user_kpi'),
    url(r'^province', 'ccad.views.provincedetails', name='province'),
    url(r'^sitename', 'ccad.views.sitenamedetails', name='site_details'),
    url(r'^equipment', 'ccad.views.equipdetails', name='equip_details'),
    url(r'^natureofservice', 'ccad.views.natureofservice', name='nos'),   
    url(r'^soa_detail/import-ppp-rsl/', staff_required(login_url='../admin')(import_excel), {
             'FormClass': SOA_detail_ppprsl_ImportForm, 'next_url': '', 'with_good': True, 'template_name': 'import_excel/soa_ppp_rsl_import.html',
      }, name='SOAdetail-ppp-rsl'), 
    url(r'^soa_detail/import-demo-dup/', staff_required(login_url='../admin')(import_excel), {
             'FormClass': SOA_detail_demodup_ImportForm, 'next_url': '', 'with_good': True, 'template_name': 'import_excel/soa_demo_dup_import.html',
      }, name='SOAdetail-demo-dup'), 

    url(r'^ppp/import-from-excel/', staff_required(login_url='../admin')(import_excel), {
             'FormClass': PPPImportForm, 'next_url': '', 'with_good': True, 'template_name': 'import_excel/ppp_import_excel.html',
      }, name='PPP-import-excel'), 

    url(r'^latestrsl/import-from-excel/', staff_required(login_url='../admin')(import_excel), {
             'FormClass': RSLImportForm, 'next_url': '', 'with_good': True, 'template_name': 'import_excel/rsl_import_excel.html',
      }, name='RSL-import-excel'), 

    url(r'^engr/undo/(?P<pk>\d+)', 'ccad.views.for_correction'),    # former name: undolink_engr # working
    url(r'^detail/(?P<detail>\w+)/(?P<pk>\d+)', 'ccad.views.app_detail', name='info_detail'),    # working
    url(r'^engr/upload/(?P<pk>\d+)', 'ccad.views.upload_endorsementfile', name='upload_endorsementfile'), # former name: engr_uploadwindow # working
    url(r'^ccad/ajax-upload$', 'ccad.views.import_uploader', name="ajax_upload"), # working
    url(r'^engr/del_endo/(?P<pk>\d+)/(?P<rb_filterby>\w+)', 'ccad.views.delete_endorsementfile', name="delete_endorsementfile"), # former name: del_endorementfile  # working
    
    url(r'^encoder/undo/(?P<pk>\d+)', 'ccad.views.undolink',),         
    url(r'^encoder/upload/(?P<pk>\d+)', 'ccad.views.uploadwindow', name='uploadwindow'),
    url(r'^(?P<rb_filterby>\w+)', 'ccad.views.logbook', name="logs"), # working     
)
urlpatterns += staticfiles_urlpatterns()