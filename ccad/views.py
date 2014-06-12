import os
from datetime import date
from django.conf import settings

from django.core.urlresolvers import reverse
from django.core.context_processors import csrf
from django.core.files.uploadhandler import FileUploadHandler
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.exceptions import ObjectDoesNotExist

from django.contrib import messages
from django.contrib.auth.models import Group
from django.contrib.auth import authenticate
from django.contrib.admin.widgets import AdminFileWidget
from django.contrib.auth.decorators import login_required

from django.db.models import Max, Q

from django.utils.safestring import SafeString

from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseBadRequest, Http404, HttpResponseNotAllowed, StreamingHttpResponse
from django.template import RequestContext
from django.template import loader, Context
from django.forms.models import modelformset_factory, BaseModelFormSet, inlineformset_factory
from django import forms

from ccad.forms import *
from ccad.models import *
from ccad.serializers import *

import logging, json

from django.middleware.csrf import get_token
from ajaxuploader.views import AjaxFileUploader
from ajaxuploader.backends.local import LocalUploadBackend
from django.core.files.base import File, ContentFile

from datetime import datetime

from django.views.decorators.csrf import csrf_exempt

from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
#ok!
class myAjaxFileUploader(AjaxFileUploader):
    def _ajax_upload(self, request, *args, **kwargs):
        print  'ajax_upload started'
        if request.method == "POST":
            if request.is_ajax():
                # the file is stored raw in the request
                upload = request
                is_raw = True
                # AJAX Upload will pass the filename in the querystring if it
                # is the "advanced" ajax upload
                try:
                    filename = request.GET['qqfile']
                    pk = request.GET['pk']

                    # added 06/27/2013 10:23pm
                    # fully working 06/30/2013 3:00pm                 
                    instance = LogBook.objects.get(id=pk)                    
                    file_content = ContentFile(upload.read())                    
                    instance.endorsementfile.save(filename, file_content)         
                    print 'instance.endorsementfile', instance.endorsementfile          
                    instance.save()                    
                    # next problem double file save --> solved by placing different folder
                    # next is subclassing this part --> solved by placing return super at the end while removing all return line
                    # next problem attaching the upload element to the parent html  --> scrap for now 06/30/2013 (too difficult :)                   
                except KeyError:
                    return HttpResponseBadRequest("AJAX request not valid")
            # not an ajax upload, so it was the "basic" iframe version with
            # submission via form
            else:
                is_raw = False
                if len(request.FILES) == 1:
                    # FILES is a dictionary in Django but Ajax Upload gives
                    # the uploaded file an ID based on a random number, so it
                    # cannot be guessed here in the code. Rather than editing
                    # Ajax Upload to pass the ID in the querystring, observe
                    # that each upload is a separate request, so FILES should
                    # only have one entry. Thus, we can just grab the first
                    # (and only) value in the dict.
                    upload = request.FILES.values()[0]
                else:
                    raise Http404("Bad Upload")
                filename = upload.name                

            backend = self.get_backend()

            # custom filename handler
            filename = (backend.update_filename(request, filename, *args, **kwargs)
                        or filename)
            # save the file
            backend.setup(filename, *args, **kwargs)
            print 'setup complete!'
            success = backend.upload(upload, filename, is_raw, *args, **kwargs)
            print 'success: ', success     
            print 'filename: ' + filename
            # callback
            extra_context = backend.upload_complete(upload, filename, *args, **kwargs)
            print 'extra context complete! ', extra_context           
            # let Ajax Upload know whether we saved it or not
            ret_json = {'success': success, 'filename': filename}
            print 'ret_json', ret_json
            if extra_context is not None:
                ret_json.update(extra_context)
            
            return HttpResponse(json.dumps(ret_json, cls=DjangoJSONEncoder), content_type='application/json; charset=utf-8')
        else:
            print 'Error: Only Post allowed'
            response = HttpResponseNotAllowed(['POST'])
            response.write("ERROR: Only POST allowed")
            return response
        #super(myAjaxFileUploader, self)._ajax_upload(request, *args, **kwargs)
#ok!    
import_uploader = myAjaxFileUploader(UPLOAD_DIR='endorsement/tmp')
#ok!
class LogBookBaseFormSet(BaseModelFormSet):

    def __init__(self, *args, **kwargs):
        super(LogBookBaseFormSet,self).__init__(*args, **kwargs)
        # check seems not working 06/22/2013
        self.widget = {'docfile': AdminFileWidget(), 'engrchoice':forms.RadioSelect() }

    def clean(self):
        if any(self.errors):
            return
        for form in self.forms:
            status = form['status'].data
            if not status:
                raise forms.ValidationError, "Please Complete the Required Fields"
#ok!
def log_status(request):
    #print 'request.http : ', request.META.get('HTTP_REFERER','/')
    http_referer = request.META.get('HTTP_REFERER','/')
    slice_from = http_referer.rfind('/', 1)    
    rb_filterby = http_referer[slice_from+1:]
    #print 'rb_filterby : ', rb_filterby
    return rb_filterby
## used in app_detail view
#ok!
def modeldict(instance):
    # snippet for model dict
    data = {}
    choice_value = ''
    docfile      = 'docfile'

    for field in instance._meta.fields:
        fname = field.name        
        # resolve picklists/choices, with get_xyz_display() function
        get_choice = 'get_'+fname+'_display'        

        if hasattr( instance, get_choice):
            choice_value = getattr( instance, get_choice)()
        
        # Check field value for content
        if field.value_from_object(instance) == None or not choice_value:
            data[field.name] = 'unknown'
        else:
            data[field.name] = field.value_from_object(instance)
            if field.name == 'docfile':        
                # Get only file name
                data[field.name] = docname(str(getattr(instance, docfile)))            

    return data
#ok!
def docname(full_path_filename):
    f = str(full_path_filename)                
    find_slash = f.rfind('/',1)        
    docfile = f[find_slash+1:len(f)]

    return docfile
#ok!
def checkprogress(status_type):
    if status_type == 'CHECKING REQUIREMENTS': # by User
        val = 10
    elif status_type == 'ISSUANCE OF SOA':  # by User
        val = 20
    elif status_type == 'PAYMENT':
        val = 30
    elif status_type == 'EVALUATION': # by User
        val = 40
    elif status_type == 'ENDORSEMENT': # by User
        val = 50
    elif status_type == 'ENCODING': # by User
        val = 60 
    elif status_type == 'REVIEW': # by User
        val = 70
    elif status_type == 'SIGNATURE': # by User
        val = 90
    elif status_type == 'CHIEF SIGNATURE': # by User
        val = 92
    elif status_type == 'DIRECTOR SIGNATURE': # by User
        val = 94
    elif status_type == 'CASHIER STAMP': # by User
        val = 96
    elif status_type == 'RELEASE TO SECRETARIAT':
        val = 98
    elif status_type == 'TASK COMPLETED':
        val = 100
    else:
        val = 0

    return val
## for editing specific rsl
#OK!
def edit_rsl(request, pk):
    rec_id = request.GET.get('pk','')    
    instance = LogBook.objects.get(id=pk)

    return render_to_response (reverse('admin:ccad_logbook_change', args=(pk,)))
#OK!
def uploadwindow(request, pk):
    if 'pk' in request.GET and request.GET['pk']:
        pk = request.GET['pk']

    data        ={}
    instance    = LogBook.objects.get(id=pk)
    status_value= checkprogress(instance.status)        
    docfileform = PPPfilesForm(request.POST, request.FILES)
    #print 'Entered UploadWindow with pk:', pk
    #print 'docfileform :', docfileform
    if request.method == "POST":        
        if docfileform.is_valid():
            #print 'docfileform is valid'        
            f = request.FILES['docfile']            
            # easy upload hander
            #instance.docfile.save(f._name, f, True)
            pppfiles = PPPfiles.objects.create(logbook=instance, user=request.user)
            pppfiles.docfile.save(f._name, f, True)
            # check for no value
            pppfiles.save()        
            #print 'ppp file save'
        # Redirect to the document list after POST
        #print 'Doc is valid with file name :', f
        return HttpResponseRedirect(reverse('ccad.views.uploadwindow', args=(instance.id,)))               
    else:
        docfileform = PPPfilesForm() # A empty, unbound form      
        #print 'Empty Doc'
    # model dictionary snippet
    data = modeldict(instance)
    #print 'data: ', data
    # Render list page with the documents and the form    
    #print 'Doc File form : ', docfileform
    ctx = {'data': data, 'instance': instance, 'status_value': status_value, 'docfileform': docfileform}
    ctx.update(csrf(request))

    return render_to_response('upload.html', ctx, context_instance=RequestContext(request))
#OK!
#from django.db import transaction
#@transaction.autocommit
@login_required
def logbook(request, rb_filterby=None): 
    # initialize    
    #print 'Entered logbook', request.user.groups.filter(name='NAFD Secretary').exists()
    #print 'request.user: ', request.user
    LogBookFormSet = modelformset_factory(LogBook, extra=0, fields = ('controlNo','status','ischecked','id','engrchoice', 'pending_desc', 'current_user'))       
    site_url = 'admin/logbook.html'   
    task_list = None
    sec_task = ['PAYMENT', 'ENDORSEMENT', 'DIRECTOR SIGNATURE', 'CASHIER STAMP', 'RELEASE TO SECRETARIAT']

    encoder_list = NAFD_User.objects.filter(groups__name='Encoder', is_active=1)    ## for engr action choosing an encoder
    engr_list = NAFD_User.objects.filter(groups__name='Engr',is_active=1)           ## for chief action choosing an engr
    rb_group = Group.objects.filter(user__username__startswith=request.user)        ## for choosing template between groups    
    try:
        chief = NAFD_User.objects.get(Q(groups__name='NAFD Chief', is_active=1))    ## check who's NFD Chief
        #print 'chief: ', chief
    except NAFD_User.MultipleObjectsReturned:
        chief_list = NAFD_User.objects.filter(Q(groups__name='NAFD Chief', is_active=1)).order_by('date_joined')
        for record in chief_list[1:]:           
            print 'update the other chief found to set inactive :', record.id
            record.is_active = False
            record.save()        
        chief = NAFD_User.objects.get(Q(groups__name='NAFD Chief', is_active=1))   ## check who's NFD Chief
    if request.user.groups.filter(name='Engr').exists():
        #print 'order_in engr'
        order_in = 'engr_status'
    elif request.user.groups.filter(name='NAFD Secretary').exists():
        order_in = 'chief_status'
        #print 'order in chief'
        task_list = LogBook.objects.order_by(order_in, 'controlNo').filter(status__in=sec_task)           
    elif request.user.groups.filter(name='Encoder').exists():                
        #print 'order in encoder'
        order_in = 'encoder_status'    
        task_list = LogBook.objects.order_by(order_in, 'controlNo').filter(Q(current_user=request.user) | Q(status='REVIEW'))           
    else:
        #print 'order in controlno'
        order_in = 'controlNo'
        task_list = LogBook.objects.order_by('controlNo').filter(status='CHIEF SIGNATURE')

    ### filterby ###
    logbook         = LogBook.objects.all().order_by(order_in, 'controlNo').filter(~Q(status='TASK COMPLETED'))                 # verified correct and running smoothly
    processing      = LogBook.objects.all().order_by('controlNo').filter(~Q(status='TASK COMPLETED'))                      # verified correct and running smoothly
    assign_task     = logbook.filter(Q(current_user=request.user))                                                              # verified correct and running smoothly    
    non_assign_task = logbook.filter(current_user__isnull=True)                                                                 # verified correct and running smoothly    
    pending_task    = logbook.filter(Q(pend_at__gt=0))                                                                          # verified correct and running smoothly            
    task_completed  = LogBook.objects.all().order_by(order_in, 'controlNo').filter(Q(status='TASK COMPLETED'))                  # verified correct and running smoothly  

    ### check for query string and add to rb_filterby param
    if "page" in request.GET:
        second_args = request.GET['page']
        url_args = rb_filterby +'?page='+ second_args
    else:
        url_args = rb_filterby

    if rb_filterby == 'new':            # verified correct and running smoothly        
        if not task_list:
            task_list = assign_task                 
    elif rb_filterby == 'unassign':     # verified correct and running smoothly
        task_list = non_assign_task
    elif rb_filterby == 'processing':   # verified correct and running smoothly
        task_list = processing        
    elif rb_filterby == 'pending':      # verified correct and running smoothly
        task_list = pending_task        
    elif rb_filterby == 'taskdone':     # verified correct and running smoothly            
        task_list = task_completed      
    else:
        if not task_list:    
            task_list = assign_task         # verified correct and running smoothly
    
    ### seperating  
    paginator   = Paginator(task_list, 5) # Show 5 log per page

    page = request.GET.get('page')
    try:
        logs = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        logs = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        logs = paginator.page(paginator.num_pages)      

    i = 1   
    max_record  = task_list.count()        
    pbar_kvalue = dict()    
    instance    = ''   

    for task in task_list:
        try:
            audit = LogBook_audit.objects.filter(logbook=task.id, status='ENCODING').order_by('id').latest('id')        
            recent_encoder = audit.username
        except ObjectDoesNotExist:
            recent_encoder = None
        #print 'recent_encoder: ', recent_encoder
        if task.pend_at:
            #pbar_kvalue[i]      = task.status + '-' + str(task.pend_at) + '-' +task.transtype  + '~' + str(task.current_user) + ':' + str(request.user.username) + '|' + str(recent_encoder)
            pbar_kvalue[i]      = task.status + '-' + str(task.pend_at) + '-' +"tasktranstype"  + '~' + str(task.current_user).upper() + ':' + str(request.user.username).upper() + '|' + str(recent_encoder).upper()
        else:
            #pbar_kvalue[i]      = task.status + '-' + task.transtype + '~' + str(task.current_user)  + ':' + str(request.user.username) + '|' + str(recent_encoder)
            pbar_kvalue[i]      = task.status + '-' + "tasktranstype" + '~' + str(task.current_user).upper()  + ':' + str(request.user.username).upper() + '|' + str(recent_encoder).upper()
        i += 1
    
    page_query = task_list.filter(id__in=[log.id for log in logs])    

    if request.method == 'POST': # If the form has been submitted...
        formset = LogBookFormSet(request.POST, request.FILES, queryset=page_query) # A form bound to the POST data
        #print 'Entered POST: ', formset.errors 
        if formset.is_valid(): # All validation rules pass 
            formset.save(commit=False)
            print 'Entered formset.is_valid'
            for form in formset.forms:
                pend_desc   = form.cleaned_data['pending_desc']  
                status      = form.cleaned_data['status']
                ischecked   = form.cleaned_data['ischecked']
                record_id   = form.cleaned_data['id']          # fetch field is controlNo instead of ID    
                engrchoice  = form.cleaned_data['engrchoice']  
                encoder_user= form.cleaned_data['current_user']                    
                instance    = LogBook.objects.get(controlNo=record_id) # get record with respect to POST['id']

                if ischecked == True: 
                    #print 'ischecked True'
                    if request.user.groups.filter(name='Engr').exists(): #### Engr
                        print 'Entered Engr'
                        if status == 'CHECKING REQUIREMENTS':
                            # instance.current_user = '' #?? no fields yet logbook will be in charge of placing the user                      
                            if engrchoice == 'PENDING':
                                instance.pend_at = 10
                                instance.current_user = request.user
                            else:
                                instance.status = 'ISSUANCE OF SOA'
                                instance.current_user = request.user
                        if status == 'ISSUANCE OF SOA': 
                            # logbook will be in charge of placing the user                       
                            if engrchoice == 'PENDING':                                                   
                                instance.pend_at = 20  
                                instance.current_user = request.user
                            else:
                                # security check for uploaded SOA
                                if instance.stm_count > 0:
                                    instance.status = 'PAYMENT'
                                    instance.current_user = request.user
                                else:
                                    msg = 'Please upload applicable Statement of Account for CN: %s' %(instance.controlNo)
                                    messages.error(request, msg)                  
                        if status == 'EVALUATION':                            
                            instance.status = engrchoice                            
                            if engrchoice == 'PENDING':
                                instance.pend_at = 40                         # verified correct and running smoothly  
                                instance.pending_desc = pend_desc          
                            if engrchoice == 'ENCODING':
                                instance.current_user = encoder_user          # verified correct and running smoothly 
                            if engrchoice == 'ENDORSEMENT':
                                instance.current_user = request.user          # verified correct and running smoothly                  
                        if status == 'PENDING':
                            if instance.pend_at == 40:
                                instance.status = 'EVALUATION'
                            elif instance.pend_at == 10:
                                instance.status = 'CHECKING REQUIREMENTS'
                            elif instance.pend_at == 20:
                                instance.status = 'ISSUANCE OF SOA'
                            elif instance.pend_at == 70:
                                instance.status = 'REVIEW'
                            instance.current_user = request.user               # verified correct and running smoothly
                            instance.pend_at = None                            # verified correct and running smoothly 
                        if status == 'ENDORSEMENT':
                            instance.current_user = request.user
                            instance.status = 'ENCODING'                    
                        if status == 'REVIEW':
                            if engrchoice == 'PENDING':                           
                               instance.pend_at = 70
                            else:
                                instance.status = 'SIGNATURE'                  # verified correct and running smoothly 
                            instance.current_user = request.user               # verified correct and running smoothly 
                        if status == 'SIGNATURE':
                            instance.status = 'CHIEF SIGNATURE'
                            instance.current_user = chief           # to be forwarded to RB Secretary                   
                    
                    elif request.user.groups.filter(name='RB Secretary').exists(): ### Director Secretary
                        print 'Entered RB Secretary'
                        if status == 'CHIEF SIGNATURE':
                            print 'RB Secretary'
                            instance.status = 'DIRECTOR SIGNATURE'
                            instance.current_user = request.user    # to be forwarded to NAFD Secretary
                        if status == 'DIRECTOR SIGNATURE':
                            instance.status = 'CASHIER STAMP'
                            instance.current_user = request.user
                        if status == 'CASHIER STAMP':
                            instance.status = 'RELEASE TO SECRETARIAT'
                            instance.current_user = request.user

                    elif request.user.groups.filter(name='NAFD Secretary').exists(): ### NAFD Secretary
                        print 'Entered Elif NAFD Secretary'
                        engr_user   = form.cleaned_data['current_user']  
                        if status == 'PAYMENT':  
                            print 'Entered Payment'
                            instance.status = 'EVALUATION'
                            instance.current_user = engr_user       # to be forwarded to engr
                        if status == 'ENDORSEMENT':
                            instance.status = 'EVALUATION'                 
                            instance.current_user = engr_user       # to be forwarded to engr
                        if status == 'DIRECTOR SIGNATURE':
                            instance.status = 'CASHIER STAMP'
                            instance.current_user = request.user
                        if status == 'CASHIER STAMP':
                            instance.status = 'RELEASE TO SECRETARIAT'
                            instance.current_user = request.user
                        if status == 'RELEASE TO SECRETARIAT':
                            instance.status = 'TASK COMPLETED'                 # verified correct and running smoothly
                            instance.current_user = request.user               # verified correct and running smoothly
                        #if status == 'RELEASE TO SECRETARIAT':
                            # upload received doc from secretariat rec

                    elif request.user.groups.filter(name='Encoder').exists():   ### Encoder  
                        #print 'Entered Encoder Secretary'        
                        #instance.status = 'REVIEW'  
                        try:                                                                                             
                            assign_engr = LogBook_audit.objects.filter(logbook_id=instance.id, status='EVALUATION').latest('log_in')       # verified correct and running smoothly
                            currentuser = NAFD_User.objects.get(id=assign_engr.username.id)                                                  # verified correct and running smoothly
                            ## security check for correctiveness of uploaded rsl                           
                            log_stn_count = instance.noofstation
                            #print 'log_stn_count: ', log_stn_count
                            log_unit_count = instance.units
                            #print 'log_unit_count: ', log_unit_count
                            rsl_list = LatestRsl_v2.objects.filter(logbook=instance.id)
                            ## self.noofstation vs rsl stns
                            rsl_stn_count = LatestRsl_v2.objects.filter(logbook=instance.id).count()
                            #print 'soa_list', rsl_stn_count
                            ## self.units vs equipments units                            
                            ## test
                            #eq_unit_count = Equipment.objects.filter(logbook=instance.id).count() # original
                            eq_unit_count = EquipRack.objects.filter(logbook=instance.id).count()
                            ## end test
                            #print 'eq_unit_count: ', eq_unit_count
                            instance.status = 'REVIEW'
                            instance.current_user = currentuser
                            ## by checking no. of station between rsl and soa stn                            
                            '''if log_stn_count == rsl_stn_count and log_unit_count == eq_unit_count:
                                #proceed
                                instance.status = 'REVIEW'
                                instance.current_user = currentuser
                            else:
                                msg = 'Please upload applicable RSL for CN: %s' % (instance.controlNo)
                                messages.error(request, msg)
                                print msg
                            '''
                            ## also no. of equipment between equipment and soa ppp or license or channel
                        except ObjectDoesNotExist:
                            print "Either the LogBook_audit or User doesn't exist."
                            currentuser = None
                        #instance.current_user = currentuser                                                                           # verified correct and running smoothly                                
                    instance.save()
                    ## checking for task completeness
                    if instance.status == 'TASK COMPLETED':
                        log_audit = LogBook_audit.objects.get(logbook=instance, status='TASK COMPLETED')
                        if log_audit:
                            #print 'Status is Task Completed.'
                            if log_audit.log_in < instance.due_date:
                                #print 'Is Ontime'
                                log_audit.is_ontime = True
                            else:
                                #print 'Is not Ontime'
                                log_audit.is_ontime = False
                        log_audit.save()                    
                    print 'Done instance save'                    
            return HttpResponseRedirect(reverse('ccad.views.logbook', args=[url_args])) # Redirect after POST
        #print 'After POST'
    else:
        formset = LogBookFormSet(queryset=page_query) # An unbound form
        #print 'Not POST'
    task_and_formset = zip(logs, formset)    
        
    ctx = {'requestuser':request.user, 'url_args': url_args, 'rb_group': rb_group, 'engr_list': engr_list, 'encoder_list': encoder_list, 'logs': logs, 'task_and_formset': task_and_formset, 'formset': formset, 'max_record': max_record, 
           'pbar_kvalue': SafeString(json.dumps(pbar_kvalue)),  'pbar_kvalue2': json.dumps(pbar_kvalue),}
    ctx.update(csrf(request))    

    return render_to_response(site_url, ctx, context_instance=RequestContext(request))
#OK!
def for_correction(request, pk):        # same with undolink_engr
    print 'inside for_correction'
    # only the assign engr for such logbook can undo command
    undo_rec  = LogBook.objects.get(pk=pk)  
    rb_filterby = 'new' 
    # undo ENCODING by returning the status to EVALUATION
    if undo_rec.status == 'ENCODING':
        print 'inside undo encoding'
        undo_rec.current_user = request.user         # verified correct and running smoothly
        undo_rec.status = 'EVALUATION'               # verified correct and running smoothly
     # undo ENDORSEMENT by returning the status to EVALUATION
    if undo_rec.status == 'ENDORSEMENT' or undo_rec.status == 'EVALUATION': 
        undo_rec.current_user = request.user         # verified correct and running smoothly   
        undo_rec.status = 'EVALUATION'               # verified correct and running smoothly
        undo_rec.endorsementfile = None              # verified correct and running smoothly
    if undo_rec.status == 'REVIEW':  
        #assign_encoder = top_or_none(LogBook_audit.objects.filter(logbook_id=pk, status='ENCODING').order_by('log_in'))     # verified correct and running smoothly      
        assign_encoder = LogBook_audit.objects.filter(logbook_id=pk, status='ENCODING').latest('log_in')
        currentuser = NAFD_User.objects.get(pk=assign_encoder.username.id)                                                    # verified correct and running smoothly  
        undo_rec.current_user = currentuser                                                                                 # verified correct and running smoothly  
        undo_rec.status = 'ENCODING'                                                                                        # verified correct and running smoothly  
    undo_rec.save()
    return HttpResponseRedirect(reverse('ccad.views.logbook', args=['new'])) 
#OK!
def delete_endorsementfile(request, pk, rb_filterby):
    instance = LogBook.objects.get(id=pk)
    instance.endorsementfile = "" or None
    instance.save()   
    
    url_args = json.dumps(rb_filterby, ensure_ascii=True, check_circular=False).replace('"','')    ### remove unnecessary string ###
    
    return HttpResponseRedirect(reverse('ccad.views.logbook', args=[url_args]))# same with del_endorsementfile
#OK!
def upload_endorsementfile(request, pk):        
    if 'pk' in request.GET and request.GET['pk']:
        pk = request.GET['pk']    

    #if 'next' in request.GET and request.GET['next']:
    #    rb_filterby = request.GET['next']

    instance    = LogBook.objects.get(id=pk)
    #url_args = json.dumps(rb_filterby, ensure_ascii=True, check_circular=False).replace('"','')     ### remove unnecessary string ###
    
    csrf_token = get_token(request)

    ctx = RequestContext(request, {'csrf_token': csrf_token, 'instance': instance})#, 'rb_filterby': rb_filterby})#'url_args': url_args, 
    ctx.update(csrf(request))
  
    return render_to_response('admin/import.html', ctx)
#OK!
def undolink(request, pk):
    undo_rec  = LogBook.objects.get(pk=pk)    
    # undo submit by returning the status to ENCODING
    if undo_rec.status == 'REVIEW':        
        undo_rec.status = 'ENCODING'                # verified correct and running smoothly
        undo_rec.current_user = request.user        # verified correct and running smoothly
        undo_rec.save()                             # verified correct and running smoothly
    return HttpResponseRedirect(reverse('ccad.views.logbook', args=(log_status(request),)))
#ok!
def undolink_engr(request, pk):
    # only the assign engr for such logbook can undo command
    undo_rec  = LogBook.objects.get(pk=pk)   
    # undo ENCODING by returning the status to EVALUATION
    if undo_rec.status == 'ENCODING':
        undo_rec.current_user = request.user         # verified correct and running smoothly
        undo_rec.status = 'EVALUATION'               # verified correct and running smoothly
     # undo ENDORSEMENT by returning the status to EVALUATION
    if undo_rec.status == 'ENDORSEMENT': 
        undo_rec.current_user = request.user         # verified correct and running smoothly   
        undo_rec.status = 'EVALUATION'               # verified correct and running smoothly
    if undo_rec.status == 'REVIEW':  
        #assign_encoder = top_or_none(LogBook_audit.objects.filter(logbook_id=pk, status='ENCODING').order_by('log_in'))     # verified correct and running smoothly      
        assign_encoder = LogBook_audit.objects.filter(logbook_id=pk, status='ENCODING').latest('log_in')
        currentuser = User.objects.get(username=assign_encoder.username)                                                    # verified correct and running smoothly  
        undo_rec.current_user = currentuser                                                                                 # verified correct and running smoothly  
        undo_rec.status = 'ENCODING'                                                                                        # verified correct and running smoothly  
    undo_rec.save()
    return HttpResponseRedirect(reverse('ccad.views.logbook', args=(log_status(request),))) 
#ok!
def app_detail(request, detail, pk):    # for showing 'More Details'
    #print 'inside app_detail under :', detail
    ### Initialize ###
    instance     = LogBook.objects.get(pk=pk)
    #print 'instance: ', instance
    #print 'instance.permitNo: ', instance.permitNo    
    rsl_list     = LatestRsl_v2.objects.none()
    equip_list   = Equipment.objects.none()
    
    rsl_dict     = {'sitename':'', 'rslid': None}
    rslinfo_list = []
    ## added
    equip_sn_list= []
    equip_id_list= []
    equip_txrx_list = []
    equip_callsign_list = []
    equip_dict   = {'antenna_id':'', 'eq_id':'', 'callsign':'', 'make':'', 'serialno':'', 'antenna':'', 'txrx':''}
    eqinfo_list  = []
    ##################
    # Get Sitename in LatestRsl ## using LatestRsl_v2
    try:
        rsl_list     = LatestRsl_v2.objects.filter(logbook=pk)    # one posibilities
    except ObjectDoesNotExist:                                      # it can be any logbook id
        rsl_list     = LatestRsl_v2.objects.all()     # all() for now
    # Get equipment list per logbook
    try:
        equiprack_list   = EquipRack.objects.select_related().filter(logbook=pk)
        #print 'try equip_list: ', equip_list
    except ObjectDoesNotExist:
        equiprack_list   = Equipment.objects.none()
        #print 'No equip list'

    # consider value for pending first
    if instance.pend_at:
        status_value = instance.pend_at
    else:        
        status_value = checkprogress(instance.status)     
    # model dictionary snippet
    data         = modeldict(instance)        
    site_url     = ''
    cashier_stamp = dict()  
    ## added 04/10/2014
    ## check OR No. table
    try:
        statement = Statements.objects.select_related().filter(logbook=pk)
        #print 'logbook id: ', pk
        #print 'statement count: ', statement.count()
        for s in statement:
            #print 's.soa.official_receipt :', s.soa.official_receipt
            try:
                if cashier_stamp and s.soa.official_receipt.or_no:
                    cashier_stamp['or_no'] = str(cashier_stamp['or_no']) +' / '+ str(s.soa.official_receipt)                    
                    #print 'with cashier_stamp already: ', cashier_stamp                        
                else:
                    cashier_stamp['or_no'] = s.soa.official_receipt
                    #print 'cashier_stamp : ', cashier_stamp
                if s.soa.official_receipt:                
                    cashier_stamp['amount'] = s.soa.official_receipt.amount
                    #print 'cashier_stamp[amount] :', cashier_stamp['amount']                
                    cashier_stamp['date_paid'] = s.soa.official_receipt.date_paid
                    #print 'cashier_stamp[date_paid] :', cashier_stamp['date_paid']

            except ObjectDoesNotExist:
                pass
    except ObjectDoesNotExist:
        pass
    ## end add
    if detail == 'ppp':
        eq_id = []        
        if 'PPP' in instance.transtype or 'NEW' in instance.transtype:                       
            if instance.permitNo:
                eq_filter_list = equiprack_list.filter(equipment__p_purchase=instance.permitNo)                
                #print 'PPP equip list: ', equip_list
            else:
                eq_filter_list = equiprack_list
                #print 'Default eq_filter_list: ', eq_filter_list
                pass
        elif 'STO' in instance.transtype:            
            if instance.permitNo:
                eq_filter_list = equiprack_list.filter(equipment__p_storage=instance.permitNo)           
                #print 'STO equip list: ', equip_list
            else:
                eq_filter_list = equiprack_list
                #print 'Default eq_filter_list: ', eq_filter_list
                pass
        for e in eq_filter_list:
            eq_id.append(e.equipment.id)
            #print 'eq_id: ', eq_id        
        
        equip_list = Equipment.objects.filter(pk__in=eq_id)
        #print 'ppp-equip list: ', equip_list 
        i = 0 # counter for equip set per rsl
        sitename = ''             
        rslid = ''
        for eq in equip_list:            
            #print 'equip: ', equip 
            try:            
                rsl_queryset = LatestRsl_v2_Equipment.objects.select_related().filter(equipment=eq.id)
                #print 'rsl queryset: ', rsl_queryset
                old_entry = date(2000,1,1)
                
                for rsl_object in rsl_queryset:
            
                    if rsl_object.latestrsl_v2.sitename:
                        if rsl_object.latestrsl_v2.sitename.site:
                            #print 'sitename exist for: %s-%s' % (eq.makemodel.make, eq.serialno)
                            new_entry = rsl_object.latestrsl_v2.issued
                            #print 'new entry: ', new_entry
                            if new_entry > old_entry:                       ## get the latest issued RSL for the mention Equipment                                   
                                old_entry = rsl_object.latestrsl_v2.issued                           
                                sitename  = rsl_object.latestrsl_v2.sitename.site     ## specify the Sitename
                                rslid     = rsl_object.latestrsl_v2                   ## specify latest rsl id 
                                #print 'rsl id: ', rslid
                        else:
                            #print 'NO sitename for: %s-%s' % (eq.makemodel.make, eq.serialno)
                            pass
            except ObjectDoesNotExist:
                rsl_queryset = LatestRsl_v2_Equipment.objects.none()
                print 'No rsl_queryset'
                rslid = ''
                sitename = ''
            
            rsl_dict.update(sitename=sitename, rslid=rslid)         ## update dictionary
            rslinfo_list.insert(i, rsl_dict)                        ## add to the list            
            i = i + 0 
        site_url = 'detail_page_ppp.html'
        equip_zip = zip(equip_list, rslinfo_list)
        ctx = { 'cashier_stamp': cashier_stamp, 
                'equip_zip': equip_zip,  
                'instance': instance, 
                'status_value': status_value}
        ctx.update(csrf(request))

        return render_to_response (site_url, ctx, context_instance=RequestContext(request))       
    elif detail == 'cprsl':
        #rsl_list = LatestRsl_v2.objects.filter(logbook=instance.id)                           ## need to be verified for multiple entry
        #print 'rsl list', rsl_list
        i = 0 # counter for equip set per rsl
       
        for rsl in rsl_list:
            #print 'rsl id: ', rsl.id 
            equip_set = LatestRsl_v2_Equipment.objects.select_related().filter(latestrsl_v2=rsl)
            #print 'rsl_equip ', equip_set
            sn_i = 0 # counter for equip serial per equip            
            for eq in equip_set: 
                ### add serial to equip_sn_dict  
                ### need to add equipment ID              
                equip_sn_list.append(eq.equipment.serialno)                          
                #print 'equip serialno', eq.equipment.serialno
                #print 'equip_sn_list[sn_%s]: %s' % (sn_i, equip_sn_list[sn_i])
                equip_id_list.append(eq.equipment.id)    
                #print 'equip id', eq.equipment.id
                #print 'equip_id_list[%s]: %s' % (sn_i, equip_id_list[sn_i])

                ## do not add same callsign            
                if eq.equipment.callsign not in equip_callsign_list:
                    #print 'NOT EQUAL'
                    equip_callsign_list.append(eq.equipment.callsign)            
                    #print 'equip callsign', eq.equipment.callsign
                    #print 'equip_callsign[%s]: %s' % (sn_i, equip_callsign_list[sn_i])
                
                ### end add
                if eq.equipment.tx and eq.equipment.rx:
                    txrx = str(eq.equipment.tx) +'/'+ str(eq.equipment.rx)
                elif eq.equipment.tx_min and eq.equipment.rx_min:
                    txrx = u'%s-%s/%s-%s' % (eq.equipment.tx_min, eq.equipment.tx_max, eq.equipment.rx_min, eq.equipment.rx_max)
                else:
                    txrx = ''

                equip_txrx_list.append(txrx)                
                equip_dict={'antenna_id': eq.equipment.antenna.id, 'make':eq.equipment.makemodel.make, 
                            'antenna':eq.equipment.antenna.antenna_type,
                            # eq.equipment.id will be use to check if equipment exist only
                            'eq_id':eq.equipment.id}             
                sn_i = sn_i + 1                              
            equip_id_sn_zip = zip(equip_sn_list, equip_id_list)           
            equip_dict['callsign'] = equip_callsign_list
            equip_dict['serialno'] = equip_id_sn_zip
            equip_dict['txrx']     = equip_txrx_list

            eqinfo_list.insert(i,equip_dict)
            #print 'BEFORE: equinfo_list', eqinfo_list
            # empty list
            equip_sn_list = []
            equip_txrx_list=[]
            equip_callsign_list = []
            equip_id_list = []
            ### end empty
            i = i + 1                   
        #print 'eqinfo list: ', eqinfo_list      
        site_url = 'detail_page_cprsl.html'
        #print 'eqinfor_list: ', eqinfo_list
        #else 
            ## write error handling here 
        #print 'rsl_list: ', rsl_list
        #print 'eqinfo_list: ', eqinfo_list
        #print 'equip_list : ', equip_list
        #print 'rslinfo_list: ', rslinfo_list
        #print 'cashier_stamp: ', cashier_stamp
        #print 'data: ', data
        #print 'instance: ', instance
        #print 'status_value: ', status_value

        rsl_zip   = zip(rsl_list, eqinfo_list)    
        #equip_zip = zip(equip_list, rslinfo_list)    
        ctx = { 'cashier_stamp': cashier_stamp,           
                'rsl_zip': rsl_zip, 
                #'equip_zip': equip_zip,  
                'instance': instance, 
                'status_value': status_value}
        ctx.update(csrf(request))

        return render_to_response (site_url, ctx, context_instance=RequestContext(request))
#ok!
@csrf_exempt
def natureofservice(request):    
    #responsedata= classtation.description
    #responsedata = 'a public'
    if request.is_ajax():
        if request.method == 'GET':
            #message = "This is an XHR GET request"
            combo1val   = request.GET.get('combo1val')
            try:
                if type(combo1val) == 'str':
                    classtation = Classofstation.objects.get(class_name=combo1val)                    
                else:
                    classtation = Classofstation.objects.get(id=combo1val)
                desc     = classtation.description
                cname    = classtation.class_name
                message  = (desc,',', cname)#json.dumps(desc, cname)
            except (ValueError, ObjectDoesNotExist):                  
                message     = "unknown class of station"
        elif request.method == 'POST':
            #message = "This is an XHR POST request"
            message = ""
            # Here we can access the POST data
            #print request.POST
    else:
        message = "No XHR"
    return HttpResponse(message)    

class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)
#ok!
#@csrf_exempt
def sitenamedetails(request):   
    template = loader.get_template('admin/ccad/latestrsl_v2/change_form.html')
    sitename = ''
    if request.is_ajax():
        if request.method == 'GET':
            #message = "This is an XHR GET request"
            combo1val   = request.GET.get('combo1val')
            try:
                if type(combo1val) == 'str':
                    sitename = Sitename.objects.select_related().get(site=combo1val)                    
                else:
                    sitename = Sitename.objects.select_related().get(id=combo1val)
                                          
                serializer = SitenameSerializer(sitename)
            except (ValueError, ObjectDoesNotExist):                  
                message     = "unknown Site"
        elif request.method == 'POST':
            #message = "This is an XHR POST request"
            message = ""
            # Here we can access the POST data
            #print request.POST
    else:
        message = "No XHR"
    
    if sitename:        
        return JSONResponse(serializer.data)        
    else:    
        return HttpResponse(message)        
#ok!
#@csrf_exempt
def equipdetails(request):   
    template = loader.get_template('admin/ccad/latestrsl_v2/change_form.html')
    equipment = ''
    message   = 'x'
    serializer = ''
    if request.is_ajax():
        if request.method == 'GET':
            #message = "This is an XHR GET request"
            combo1val   = request.GET.get('combo1val')
            equipment = Equipment.objects.get(id=combo1val)    
            serializer = EquipmentSerializer(equipment)           
        elif request.method == 'POST':
            #message = "This is an XHR POST request"
            message = ""
            # Here we can access the POST data
            #print request.POST
    else:
        message = "No XHR"
        #print message
    if serializer:         
        return JSONResponse(serializer.data)        
    else:
        return HttpResponse(message)        

def provincedetails(request):
    if request.is_ajax():
        if request.method == 'GET':
            #message = "This is an XHR GET request"
            combo1val   = request.GET.get('combo1val')         
            try:    
                prov_queryset = Province.objects.get(id=combo1val)
                philadd = PhilAddress.objects.order_by('province').filter(province=prov_queryset.province).latest('id')                    
    
                serializer = PhilAddressSerializer(philadd)                
            except (ValueError, ObjectDoesNotExist):                  
                message     = "unknown Site"
        elif request.method == 'POST':
            #message = "This is an XHR POST request"
            message = ""
            # Here we can access the POST data
            #print request.POST
    else:
        message = "No XHR"
    
    if philadd:         
        return JSONResponse(serializer.data)        
    else:        
        return HttpResponse(message)

@login_required
def kpi_data(request):
    #print 'Initialize values'    
    message = ''    
    prev_type = ''    
    prev_count = 0

    include_only = ['PPP', 'CP', 'RSL', 'MOD', 'RECALL', 'TP', 'DEMO', 'DUP']  
    export_data = {} 
    for i in include_only:            
        export_data[i] = 0
        export_data[i+'_ontime'] = 0
        export_data[i+'_due'] = 0
    
    # tabledata JavaScript Literal Initializer
    c, v = '', ''
    id, label, type = '', '', ''
    cols, rows = '', ''
    rows_input, cols_input = [], []
    data = {}    
              
    if request.is_ajax():        
        show_user   = int(request.GET.get('user_stat'))    
        apt = App_type.objects.all()

        try:
            apt2 = apt.extra(select={'units':"""SELECT 
                                          nvl(SUM( \
                                          CASE \
                                            WHEN appt.trans_type LIKE 'PPP' \
                                            THEN sappt.ppp_units \
                                            WHEN appt.trans_type LIKE 'CP' \
                                            THEN (sappt.const_fee/360) \
                                            WHEN appt.trans_type LIKE 'MOD' \
                                            THEN sappt.mod_units \
                                            WHEN appt.trans_type LIKE 'RECALL' \
                                            THEN sappt.stor_units \
                                            WHEN appt.trans_type LIKE 'RSL' \
                                            THEN sappt.rsl_units \
                                            WHEN appt.trans_type LIKE 'TP' \
                                            THEN sappt.rsl_units \
                                            WHEN appt.trans_type LIKE 'DUP' \
                                            THEN (sappt.duplicate_fee/120) \
                                            WHEN appt.trans_type LIKE 'DEMO' \
                                            THEN sappt.ppp_units \
                                          END),0) "items" \
                                        FROM ccad_app_type appt, \
                                          ( SELECT DISTINCT(sl.controlNo), \
                                            sappt_apptid, \
                                            sl.ppp_units, \
                                            sl.const_fee, \
                                            sl.rsl_units, \
                                            sl.mod_units, \
                                            sl.stor_units, \
                                            sl.duplicate_fee \
                                          FROM \
                                            (SELECT la.id laid, \
                                              l.controlNo, \
                                              s.*, \
                                              sappt.app_type_id sappt_apptid \
                                            FROM ccad_logbook l, \
                                              ccad_logbook_audit la, \
                                              ccad_soa s, \
                                              ccad_statements st, \
                                              ccad_soa_app_type sappt, \
                                              ccad_nafd_user au \
                                            WHERE l.ID = la.logbook_id \
                                            AND s.id = st.soa_id     \
                                            AND l.id = st.logbook_id  \
                                            AND s.ID   = sappt.soa_id \
                                            AND au.ID  = la.username_id \
                                            AND au.id = %s \
                                            ) sl \
                                          ) sappt \
                                        WHERE appt.ID = sappt.sappt_apptid \
                                        AND appt.id = ccad_app_type.id \
                                        GROUP BY appt.trans_type, appt.id"""},
                            select_params=(show_user,))
            # possible queryset translation -- unfinished
            # for i in include_only:
            #     sappt_list = SOA_App_type.objects.select_related().filter(app_type__trans_type=i)
            #     for sappt in sappt_list:
            #         print sappt.app_type.trans_type # username transaction type             
            #         logbook_list = sappt.soa.logbook_set.all()
            #         for logbook in logbook_list:
            #            logbook_audit_list = logbook.logbook_audit_set.filter(username__id=show_user)
            #            if logbook_audit_list.count() > 0            
            #                print 'Type: ', sappt.app_type.trans_type
            #                if sappt.app_type.trans_type == 'PPP':
            #                    print 'Units: ', sappt.soa.ppp_units
            #                elif sappt.app_type.trans_type == 'CP':
            #                    print 'Units: ', sappt.soa.const_fee/360 # 360 should be a parameter
            #                elif sappt.app_type.trans_type == 'RSL':
            #                    print 'Units: ', sappt.soa.rsl_units
            #                elif sappt.app_type.trans_type == 'MOD':
            #                    print 'Units: ', sappt.soa.mod_units
            #                elif sappt.app_type.trans_type == 'RECALL':
            #                    print 'Units: ', sappt.soa.stor_units
            #                elif sappt.app_type.trans_type == 'TP':
            #                    print 'Units: ', sappt.soa.rsl_units
            #                elif sappt.app_type.trans_type == 'DUP':
            #                    print 'Units: ', sappt.soa.duplicate_fee/120
            #                elif sappt.app_type.trans_type == 'DEMO':
            #                    print 'Units: ', sappt.soa.ppp_units

            # for getting on time completed task
            for i in include_only:
                sappt_list = SOA_App_type.objects.select_related().filter(app_type__trans_type=i)
                ontime_count = 0          # resetting variables                         
                current_type = i
                for sappt in sappt_list:
                    logbook_list = sappt.soa.logbook_set.all()
                    for logbook in logbook_list:
                        logbook_audit_list = logbook.logbook_audit_set.filter(username__id=show_user)
                        ontime_count = logbook_audit_list.filter(is_ontime=1).count() 
                
                        if current_type == prev_type:
                            export_data[i+'_ontime']=ontime_count + prev_count
                        else:
                            export_data[i+'_ontime']=ontime_count
                        prev_type = i
                        prev_count = ontime_count                                    

        except  (ValueError, ObjectDoesNotExist):
            print 'Error in evaluating apt2.'        
    
        for rec in apt2:            
            if rec.trans_type in include_only:
                export_data[rec.trans_type]=rec.units            
        # computing for include trans_type items completed beyond due date
        for i in include_only:
            if export_data[i] ==None:
                export_data[i] = 0 
            export_data[i+'_due']= export_data[i] - export_data[i+'_ontime']          
    
    else:
        message = "No XHR"
    
    if export_data:                                                 
        return JSONResponse(export_data)                   
    else:     
        return HttpResponse(message) 


@login_required
def logbook_manual(request):
    return render_to_response('doc/build/html/index.html')
