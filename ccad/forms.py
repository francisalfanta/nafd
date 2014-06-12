import autocomplete_light
autocomplete_light.autodiscover()
from autocomplete_light.contrib.generic_m2m import GenericModelForm, \
    GenericModelMultipleChoiceField

from django import forms

from import_excel.forms import ImportExcelForm
from django.db import transaction
from django.contrib.admin import widgets
from django.contrib import messages
from django.forms import ModelForm
from django.forms.widgets import ClearableFileInput
from django.forms.extras.widgets import SelectDateWidget, Select
from django.forms.util import ErrorList

from django.utils.safestring import mark_safe
from django.utils.encoding import force_unicode
from cgi import escape
import xlrd


from ccad.models import *
from ccad.checkbox import *
from django.conf import settings

#class EquipmentForm(forms.ModelForm):   
class EquipmentForm(autocomplete_light.ModelForm):  
    callsign       = forms.CharField(label='Call-Sign', widget=forms.TextInput(attrs={'style':'width:450px; padding:0px;',}))
    #status         = forms.ChoiceField(label='Status', widget=forms.TextInput(attrs={'style':'width:70px; padding:0px; ',}))
    makemodel      = forms.ModelChoiceField(queryset=EquipModel.objects.all(), label="Make / Model", widget=autocomplete_light.ChoiceWidget('EquipModelAutocomplete', attrs={'style':'width:280px;',}))    
    serialno       = forms.CharField(label='Serial No.', widget=forms.TextInput(attrs={'style':'width:280px; padding:0px;',}))
    power          = forms.CharField(label='Power', widget=forms.TextInput(attrs={'style':'width:280px; padding:0px; ',}))
    bwe            = forms.CharField(label='Bandwidth', widget=forms.TextInput(attrs={'style':'width:280px; padding:0px; ',}))
    #usage          = forms.ChoiceField(label='Equipment Usage', widget=forms.TextInput(attrs={'style':'width:70px; padding:0px; ',}))
    freqrange_low  = forms.DecimalField(label='1: Minimum Freq Range', widget=forms.TextInput(attrs={'style':'width:280px; padding:0px; ',}))
    freqrange_low2 = forms.DecimalField(label='2: Minimum Freq Range', widget=forms.TextInput(attrs={'style':'width:280px; padding:0px; ',}), required=False)
    freqrange_high = forms.DecimalField(label='1: Maximum Freq Range', widget=forms.TextInput(attrs={'style':'width:280px; padding:0px; ',}))
    freqrange_high2= forms.DecimalField(label='2: Maximum Freq Range', widget=forms.TextInput(attrs={'style':'width:280px; padding:0px; ',}), required=False)
    tx_min         = forms.DecimalField(label='Tx min', widget=forms.TextInput(attrs={'style':'width:186px; padding:0px; ',}), required=False)
    tx_max         = forms.DecimalField(label='Tx max', widget=forms.TextInput(attrs={'style':'width:186px; padding:0px; ',}), required=False)
    tx             = forms.DecimalField(label='Transmit', widget=forms.TextInput(attrs={'style':'width:186px; padding:0px; ',}), required=False)
    rx             = forms.DecimalField(label='Recieved', widget=forms.TextInput(attrs={'style':'width:186px; padding:0px; ',}), required=False)
    rx_min         = forms.DecimalField(label='Rx min', widget=forms.TextInput(attrs={'style':'width:186px; padding:0px; ',}), required=False)
    rx_max         = forms.DecimalField(label='Rx max', widget=forms.TextInput(attrs={'style':'width:186px; padding:0px; ',}), required=False)
    p_purchase     = forms.CharField(label='Permit to Purchase', widget=forms.TextInput(attrs={'style':'width:280px; padding:0px; ',}))
    p_possess      = forms.CharField(label='Permit to Possess', widget=forms.TextInput(attrs={'style':'width:280px; padding:0px; ',}))
    p_storage      = forms.CharField(label='Permit for Storage', widget=forms.TextInput(attrs={'style':'width:280px; padding:0px; ',}), required=False)

    carrier        = forms.ModelChoiceField(queryset=Carrier.objects.all(), label="Public Telecom Entity", widget=autocomplete_light.ChoiceWidget('CarrierAutocomplete', attrs={'style':'width:520px;',}))        
    antenna        = forms.ModelChoiceField(queryset=Antenna.objects.all(), label="Antenna Details", widget=autocomplete_light.ChoiceWidget('AntennaAutocomplete', attrs={'style':'width:520px;',}))    
   
    class Meta:
        model   = Equipment        
        widgets = autocomplete_light.get_widgets_dict(Equipment)
#ok!
### import excel on SOA detail
class SOA_detail_ppprsl_ImportForm(ImportExcelForm):
    # add fields to original form
    # model_id = forms.CharField(widget=forms.HiddenInput, required=False)     
    def get_converted_items(self, data):
        print 'entered get converted', data['model_id']
        if data['converted_items']:
            return data['converted_items']
        excel_file = data['excel_file']
        book = xlrd.open_workbook(
            file_contents=excel_file.read(), encoding_override='utf-8'
        )
        sheet = book.sheet_by_index(0)
        converted_items = [] 
        ## added        
        r =[]
        lic = 0
        cp  = 0
        pur = 0
        fil = 0
        mod = 0
        sto = 0
        suf_lic = 0
        end_row = 0
        # added 01/12/2014
        # to verify first line                            
        check_cell_id = sheet.cell(9,0)          
        if check_cell_id.value != 'id':                
            raise forms.ValidationError('Hidden row 10 should be SOA field name')             
        ## end error check

        # added 01/08/2014
        # check if site_no, city, and band is present
        is_site = 0
        is_city = 0
        is_band = 0
        for cx in range(sheet.ncols):
            check_cell = sheet.cell(9,cx)
            
            if check_cell.value == 'site_no':
                is_site = 1                
            elif check_cell.value == 'city':
                is_city = 1
            elif check_cell.value =='band':
                is_band = 1
        added_col = +is_site+is_city+is_band
        ## end of checking        

        for rx in range(sheet.nrows):
            row = sheet.row(rx)            
            if not row:                
                continue            
            ## added
            values = []
            from datetime import datetime, timedelta, date
            for cx in range(sheet.ncols): 
                ## look for cell under row number and col number            
                cell = sheet.cell(rx, cx) 
        
                if cell.ctype == xlrd.XL_CELL_DATE:                                                    
                    # Return a tuple
                    dt_tuple = xlrd.xldate_as_tuple(cell.value, book.datemode)                    
                    # Create datetime object from this tuple.                    
                    get_col = date(dt_tuple[0], dt_tuple[1], dt_tuple[2]).isoformat()                  
                elif cell.ctype == xlrd.XL_CELL_NUMBER:
                    get_col = float(cell.value)      
                    ## added 10/21/2013 
                    ## find end row by using total Lic
                    ## add license_fee column
                    if cx == 13+added_col:
                        lic = lic+get_col                                
                    if cx == 17+added_col:
                        cp = cp + get_col                        
                    if cx == 21+added_col:
                        pur = pur + get_col                        
                    if cx == 24+added_col:
                        fil = fil + get_col                        
                    if cx == 26+added_col:
                        mod = mod + get_col                        
                    if cx == 29+added_col:
                        sto = sto + get_col                      
                    if cx == 31+added_col:
                        suf_lic = suf_lic + get_col
                        
                    if lic == sheet.cell(rx,12+added_col).value or cp == sheet.cell(rx,16+added_col).value or pur == sheet.cell(rx,20+added_col).value or fil == sheet.cell(rx,24+added_col).value or mod == sheet.cell(rx,26+added_col).value or sto == sheet.cell(rx,28+added_col).value or suf_lic == sheet.cell(rx,30+added_col).value:
                        end_row = rx
                ## for null value
                 # added 01/12/2014
                # replace space with zero
                elif cell.ctype in (xlrd.XL_CELL_EMPTY, xlrd.XL_CELL_BLANK) or cell.value == ' '  or cell.value == '  ':
                ## end replace       
                    get_col = float(0)
                else:
                    get_col = unicode(sheet.cell(rx, cx).value)

                values.append(get_col)            
            ## original script        
            #values = map(lambda cell: cell.value, row) 
            print 'data model_id: ', data['model_id']           
            values.append(data['model_id'])    ### add the instance id within the row         
            r.append(values)                                  
            ## end added   
            converted_items.append(values)
        #no of stations
        no_of_stations = 0 
        if end_row != 0:
            no_of_stations = end_row-9
            print 'no_of_stations', no_of_stations
            return converted_items[9:end_row]
        else:
            return converted_items[9:]

    @transaction.autocommit
    def update_callback(self, request, converted_items):        
        # get the field name available  
        for field_names in converted_items[:1]:    
            header_name = field_names
        # storage for table fields
        rec_fields = dict()             
   
        for soa_detail in converted_items[1:]:    
            # reset indicators
            indicator = 0                 
            id_indicator = 0
            # assign to dict the values from excel 
            for i in range(len(header_name)):
                
                # take all field names from model               
                for model_field in SOA_detail._meta.fields: 
                                
                    if header_name[i] in ['sitename', 'site_addr', 'call_sign'] and soa_detail[i] == 0:
                        if header_name[i] == 'sitename':
                            indicator = indicator + 1
                        if header_name[i] == 'site_addr':
                            indicator = indicator + 1
                        if header_name[i] == 'call_sign':
                            indicator = indicator + 1
                        ## no action                    
                        soa_detail[i] = ' '
                    
                    # copy only row with id has value
                    if header_name[i] == 'id' and soa_detail[i] != 0:                    
                        id_indicator = 1   

                    # check every header_name if it is in model field name except id
                    # sitename, address, call-sign should not all be empty
                    # do not include id column
                    if header_name[i] == model_field.name and indicator < 3 and header_name[i] != 'id':
                        # update dict if found
                        rec_fields[header_name[i]] = soa_detail[i]
            
            instance        = SOA.objects.get(pk=int(soa_detail[len(header_name)-1]))
            if id_indicator == 1: ## insert only when id value exist     
                SOA_detail.objects.create(soa=instance, **rec_fields)               
#ok~!
class SOA_detail_demodup_ImportForm(ImportExcelForm): 
    def get_converted_items(self, data):
        if data['converted_items']:
            return data['converted_items']
        excel_file = data['excel_file']
        book = xlrd.open_workbook(
            file_contents=excel_file.read(), encoding_override='utf-8'
        )
        sheet = book.sheet_by_index(0)
        converted_items = [] 
        ## added        
        r =[]
        demo = 0        
        pur = 0       
        dup = 0
        fil = 0     
        end_row = 0
        for rx in range(sheet.nrows):
            row = sheet.row(rx)            
            if not row:                
                continue            
            ## added
            values = []
            from datetime import datetime, timedelta, date
            for cx in range(sheet.ncols): 
                ## look for cell under row number and col number            
                cell = sheet.cell(rx, cx)                                           
              
                if cell.ctype == xlrd.XL_CELL_DATE:                                                    
                    # Return a tuple
                    dt_tuple = xlrd.xldate_as_tuple(cell.value, book.datemode)                    
                    # Create datetime object from this tuple.                    
                    get_col = date(dt_tuple[0], dt_tuple[1], dt_tuple[2]).isoformat()                  
                elif cell.ctype == xlrd.XL_CELL_NUMBER:
                    get_col = float(cell.value)                          
                    ## find end row by using total Lic                               
                    if cx == 4:
                        demo = demo + get_col                        
                    if cx == 6:
                        pur = pur + get_col                        
                    if cx == 8:
                        dup = dup + get_col                                            
                    if cx == 10:
                        fil = fil + get_col                                            
                        
                    if demo == sheet.cell(rx,3).value or pur == sheet.cell(rx,5).value or fil == sheet.cell(rx,9).value or dup == sheet.cell(rx,7).value:
                        end_row = rx
                ## for null value
                elif cell.ctype in (xlrd.XL_CELL_EMPTY, xlrd.XL_CELL_BLANK):
                    get_col = 0
                else:
                    get_col = unicode(sheet.cell(rx, cx).value)

                values.append(get_col)            
            ## original script        
            #values = map(lambda cell: cell.value, row)            
            values.append(data['model_id'])    ### add the instance id within the row         
            r.append(values)                                  
            ## end added   
            converted_items.append(values)
       
        if end_row != 0:
            return converted_items[8:end_row]
        else:
            return converted_items[8:]

    @transaction.autocommit
    def update_callback(self, request, converted_items):        
        # get the field name available  
        for field_names in converted_items[:1]:    
            header_name = field_names
        # storage for table fields
        rec_fields = dict()        
   
        for soa_detail in converted_items[1:]:    
            # reset indicators
            indicator = 0                 
            id_indicator = 0
            # assign to dict the values from excel 
            for i in range(len(header_name)):
                
                # take all field names from model
                for model_field in SOA_detail._meta.fields: 
                                   
                    if header_name[i] in ['sitename', 'site_addr', 'call_sign'] and soa_detail[i] == 0:
                        if header_name[i] == 'sitename':
                            indicator = indicator + 1
                        if header_name[i] == 'site_addr':
                            indicator = indicator + 1
                        if header_name[i] == 'call_sign':
                            indicator = indicator + 1
                        ## no action                    
                        soa_detail[i] = ' '
                    
                    # copy only row with id has value
                    if header_name[i] == 'id' and soa_detail[i] != 0:                    
                        id_indicator = 1   

                    # check every header_name if it is in model field name except id
                    # sitename, address, call-sign should not all be empty
                    # do not include id column
                    if header_name[i] == model_field.name and indicator < 3 and header_name[i] != 'id':
                        # update dict if found
                        rec_fields[header_name[i]] = soa_detail[i]
            
            instance        = SOA.objects.get(pk=int(soa_detail[len(header_name)-1]))
            if id_indicator == 1: ## insert only when id value exist     
                SOA_detail.objects.create(soa=instance, **rec_fields)
### end import excel
#ok!
### import excel for PPP
class PPPImportForm(ImportExcelForm):
    @transaction.autocommit
    def update_callback(self, request, converted_items):
        # get the field name available  
        for field_names in converted_items[:1]:    
            header_name = field_names
        # get the model field name
        model_fn = []
        for fn in Equipment._meta.fields:
            model_fn.append(fn.name)
        # storage for table fields
        rec_fields = dict()  
       
        number_fields = ['sitename', 'makemodel', 'carrier', 'antenna', 'tx', 'rx', 'tx_min', 'tx_max', 
                         'rx_min', 'rx_max', 'freqrange_low', 'freqrange_high', 'power', 'freqrange_low2', 'freqrange_high2']

        for ppp_detail in converted_items[1:]:
            # assign to dict the values from excel 

            log_instance        = LogBook.objects.get(pk=int(ppp_detail[len(header_name)-1]))     ### id should be last number
            #print 'log_instance: ', log_instance
            carrier_instance    = Carrier.objects.get(pk=log_instance.carrier.id)   
            #print 'carrier_instance: ', carrier_instance

            for i in range(len(header_name)): 
                # check every header_name if it is in model field name except for number fields
                if header_name[i] in model_fn and not (str(header_name[i])) in number_fields:
                    rec_fields[header_name[i]] = ppp_detail[i]     # working  
                elif header_name[i] == 'makemodel':
                    try:
                        makemodel_instance = EquipModel.objects.get(make=ppp_detail[i])
                        #print 'try makemodel_instance: ', makemodel_instance                        
                    except EquipModel.DoesNotExist:
                        eqmodel = EquipModel.objects.create(make=str(ppp_detail[i]))
                        #print 'eqmodel created'
                        eqmodel.save()
                        #print 'eqmodel.save()'
                        makemodel_instance = EquipModel.objects.get(make=ppp_detail[i])
                        #print 'except makemodel_instance :', makemodel_instance
                    # for double entry
                    except EquipModel.MultipleObjectsReturned:
                        #print 'Double entry'
                        em_list = EquipModel.objects.filter(make=ppp_detail[i])
                        for record in em_list[1:]:
                            # delete double entry
                            print 'Deleting EquipModel id :', record.id
                            record.delete()
                        makemodel_instance = EquipModel.objects.get(make=ppp_detail[i])

                    rec_fields[header_name[i]] = makemodel_instance
                    #print 'rec_fields[header_name[i]] :', makemodel_instance
                   
                elif header_name[i] == 'sitename':                    
                    try:
                        sitename_instance = Sitename.objects.get(site=ppp_detail[i], carrier=carrier_instance)
                        #print 'try sitename_instance: ', sitename_instance
                    except Sitename.DoesNotExist:
                        sitename = Sitename.objects.create(site=str(ppp_detail[i]), carrier=carrier_instance)
                        print 'sitename created'
                        sitename.save()
                        print 'sitename.save()'
                        sitename_instance = Sitename.objects.get(site=ppp_detail[i], carrier=carrier_instance)
                        print 'except sitename_instance: ', sitename_instance
                    # for double entry
                    except Sitename.MultipleObjectsReturned:
                        print 'Double entry'
                        sitename_list = Sitename.objects.filter(site=ppp_detail[i], carrier=carrier_instance)
                        for record in sitename_list[1:]:
                            # delete double entry
                            print 'Deleting Sitename id :', record.id
                            record.delete()
                        sitename_instance = Sitename.objects.get(site=ppp_detail[i], carrier=carrier_instance)

                    rec_fields[header_name[i]] = sitename_instance
                    #print 'rec_fields[header_name[i]]:', sitename_instance
                   
                else:
                    # for null number fields
                    if len(str(ppp_detail[i])) == 0:                         
                        rec_fields[header_name[i]] = 0
                    if 'tx' in str(header_name[i]):
                        rec_fields[header_name[i]] = ppp_detail[i] 
                    elif 'tx_min' in str(header_name[i]):
                        rec_fields[header_name[i]] = ppp_detail[i]      
                    elif 'tx_max' in str(header_name[i]):
                        rec_fields[header_name[i]] = ppp_detail[i]
                    elif 'rx' in str(header_name[i]):
                        rec_fields[header_name[i]] = ppp_detail[i]
                    elif 'rx_min' in str(header_name[i]):
                        rec_fields[header_name[i]] = ppp_detail[i]
                    elif 'rx_max' in str(header_name[i]):
                        rec_fields[header_name[i]] = ppp_detail[i]    
                    elif 'freqrange_low' in str(header_name[i]):
                        rec_fields[header_name[i]] = ppp_detail[i]
                    elif 'freqrange_high' in str(header_name[i]):
                        rec_fields[header_name[i]] = ppp_detail[i]                            
                    elif 'power' in str(header_name[i]):
                        rec_fields[header_name[i]] = ppp_detail[i]              

            rec_fields['unit'] = 'dBm' # default value for field unit 
            #print 'rec_fields: ', rec_fields                  
            ## check for duplicate equipment
            check_dup = Equipment.objects.filter(Q(makemodel=rec_fields['makemodel']), 
                                                 Q(serialno=rec_fields['serialno']),
                                                 Q(p_purchase=rec_fields['p_purchase']),
                                                 Q(p_possess=rec_fields['p_possess']),
                                                 Q(p_storage=rec_fields['p_storage']),)
            if not check_dup:                
                """ Equipment table is ready to accept new record """
                try:
                    new_eq = Equipment.objects.create(carrier=carrier_instance, **rec_fields)                
                    #print 'insert success'
                    # create record in EquipRack
                    EquipRack.objects.create(logbook=log_instance, equipment=new_eq)
                    print 'EquipRack created'
                    messages.success(request, 'Successfully inserted record(s).')
                except:                
                    messages.error(request, 'Fail to insert record.')
                    print 'insert not success'
            else:
                print 'Duplicate Equipment found.'
                messages.error(request, 'Duplicate Record found for Make/Model: %s with serial no: %s' %(rec_fields['makemodel'], rec_fields['serialno']))
### end import excel for PPP
#ok!
### import excel for rsl
class RSLImportForm(ImportExcelForm):
    ## added 01/13/2014    
    def get_converted_items(self, data):
        print 'entered get converted', data['model_id']
        if data['converted_items']:
            return data['converted_items']
        excel_file = data['excel_file']
        book = xlrd.open_workbook(
            file_contents=excel_file.read(), encoding_override='utf-8'
        )
        sheet = book.sheet_by_index(0)
        converted_items = [] 
        ## added        
        r =[]     
        ## added 01/13/2014   
        char_fields = []
        num_fields  = []
        date_fields = []
        header_location = {}        
       
        for model_field in LatestRsl._meta.fields:
          if isinstance(model_field, models.CharField):
              char_fields.append(model_field.name)
          elif isinstance(model_field, models.IntegerField):
              num_fields.append(model_field.name)
          elif isinstance(model_field, models.DateTimeField):
              date_fields.append(model_field.name)
       
        # to verify first line and indicate location
        for cx in range(sheet.ncols):                           
            header_name = sheet.cell(0,cx)
            #print 'header_name: ', header_name.value.lower()
            if type(header_name.value) == int:
                header_location[cx]= header_name.value
            else:
                header_location[cx]= header_name.value.lower()
        ## end 01/13/2014

        for rx in range(sheet.nrows):
            row = sheet.row(rx)            
            if not row:                
                continue            
            ## added
            if sheet.cell(rx,0).value:
                print 'Row contain data'

                values = []
                from datetime import datetime, timedelta, date
                for cx in range(sheet.ncols): 
                    ## look for cell under row number and col number                              
                    cell = sheet.cell(rx, cx)                                          
                    if cell.ctype == xlrd.XL_CELL_DATE or header_location[cx] in date_fields: 
                        #print 'Date: %s and location : %s' %(cell.ctype, header_location[cx])
                        # check for null value
                        if cell.value in (xlrd.XL_CELL_EMPTY, xlrd.XL_CELL_BLANK, ' '):
                            get_col = None#"1900-01-01"
                        # Return a tuple                    
                        dt_tuple = xlrd.xldate_as_tuple(cell.value, book.datemode)                    
                        # Create datetime object from this tuple.                    
                        get_col = date(dt_tuple[0], dt_tuple[1], dt_tuple[2]).isoformat()
                        #print 'get_col: ', get_col

                    elif cell.ctype == xlrd.XL_CELL_NUMBER or header_location[cx] in num_fields:
                        #print 'Number: %s and location : %s' %(cell.ctype, header_location[cx])
                        # check for null value
                        if cell.value in (xlrd.XL_CELL_EMPTY, xlrd.XL_CELL_BLANK, ' '):
                            get_col = None#float(0)
                        get_col = float(cell.value)      
                        #print 'get_col: ', get_col                
                    else:
                        #print 'Unknown: %s and location : %s' %(cell.ctype, header_location[cx])
                        if cell.value in (xlrd.XL_CELL_EMPTY, xlrd.XL_CELL_BLANK, ' '):
                            get_col = null
                        else:
                            get_col = unicode(sheet.cell(rx, cx).value)
                        #print 'get_col: ', get_col
                    #print 'header_name: %s - value: %s' % (header_location[cx], get_col)
                    values.append(get_col)            
                ## original script        
                #values = map(lambda cell: cell.value, row)            
                values.append(data['model_id'])    ### add the instance id within the row         
                
            else:
                print 'Empty data'
            
            r.append(values)                                  
            ## end added 

            converted_items.append(values)
        
        return converted_items
    ## end
    ## working def
    @transaction.autocommit
    def update_callback(self, request, converted_items):      
        rec_fields = dict()
        ## added 01/13/2014   
        char_fields = []
        num_fields  = []
        date_fields = []
        header_location = {}
        pur_counter = 0
        pos_counter = 0
        sto_counter = 0
        old_make_counter = 0
        old_serial_counter = 0
        sn_counter = 0
        spare_sn_counter = 0
        notable_fields = ['purchase', 'possess', 'storage']        
       
        for model_field in LatestRsl._meta.fields:
          if isinstance(model_field, models.CharField):            
              char_fields.append(model_field.name)
              # check number of field according to field name stated
              if model_field.name.find('purchase') >= 0 and model_field.name.find('_sp') == -1:
                  pur_counter = pur_counter + 1  
                  #print 'purchase found: ', model_field.name 
              if model_field.name.find('possess') >= 0 and model_field.name.find('_sp') == -1:
                  pos_counter = pos_counter + 1  
                  #print 'possess found: ', model_field.name
              if model_field.name.find('storage') >= 0 and model_field.name.find('_sp') == -1:
                  sto_counter = pos_counter + 1  
                  #print 'storage found: ', model_field.name
              if model_field.name.find('old_make') >= 0 and model_field.name.find('_SP') == -1:
                  old_make_counter = old_make_counter + 1  
                  #print 'old make found: ', model_field.name
              if model_field.name.find('old_serial') >= 0 and model_field.name.find('_sp') == -1:
                  old_serial_counter = old_serial_counter + 1  
                  #print 'old serial found: ', model_field.name
              if model_field.name.find('sn') >= 0 and model_field.name.find('_sp') == -1:
                  sn_counter = sn_counter + 1  
                  #print 'serial no found: ', model_field.name
              if model_field.name.find('spare_equip_serial') >= 0 and model_field.name.find('_sp') == -1:
                  spare_sn_counter = spare_sn_counter + 1  
                  #print 'spare sn found: ', model_field.name

          elif isinstance(model_field, models.DecimalField):
              num_fields.append(model_field.name)
          elif isinstance(model_field, models.DateField):
              date_fields.append(model_field.name)
        #print 'char_fields: ', char_fields
        #print 'num_fields: ', num_fields
        #print 'date_fields: ', date_fields
        #print 'total purchase fields :', pur_counter
        #print 'total possess fields :', pos_counter
        #print 'total storage fields :', sto_counter
        #print 'total old_make fields :', old_make_counter
        #print 'total old_serial fields :', old_serial_counter
        #print 'serial no fields :', sn_counter
        #print 'spare sn fields :', spare_sn_counter

        for first_line in converted_items[:1]:
            # to verify first line and indicate location
            for i in range(len(first_line)): 
                if type(first_line[i]) == int:
                    header_location[i]= first_line[i]
                else:
                    header_location[i]= first_line[i].lower()
                #print 'header_location[%s]: %s' %(i, header_location[i])
        
        for rsl_detail in converted_items[1:]:            
            # assign to dict the values from excel 
            for i in range(len(header_location)-1):   # range of columns found in header_name                               
                if header_location[i] in num_fields:                    
                    if rsl_detail[i] != '':
                    #    rec_fields[header_location[i]] = None
                    #else:
                        rec_fields[header_location[i]] = float(rsl_detail[i])                    
                    #print 'num_fields: %s-%s' % (header_location[i], rsl_detail[i])                    
                elif header_location[i] in date_fields:                 
                    if rsl_detail[i] != '':
                    #    rec_fields[header_location[i]] = None
                    #else:
                        rec_fields[header_location[i]] = rsl_detail[i]  
                    #print 'date_fields: ', header_location[i] 
                else:
                    if header_location[i] not in notable_fields:
                        #print 'rsl_detail[%s]: %s' %(i, rsl_detail[i])
                        rec_fields[header_location[i]] = rsl_detail[i]
            #print '%s form_serial : %s' % (rec_fields['rslno'], rec_fields['form_serial'])
            for i in range(len(header_location)-1):   # range of columns found in header_name     
                # add permit to purchase, permit to possess, and permit to possess (storage)
                # to all equivalent purchase1, purchase2, purchase3
                for no_fields in range(len(notable_fields)):
                    if header_location[i] == notable_fields[no_fields] and rsl_detail[i]:
                        #print 'notable_fields: ', notable_fields[no_fields] 
                        ##check serial content
                        for x in range(1, sn_counter+1):
                            sn = 'sn'+ str(x)
                            #print 'sn: ', sn
                            check_field = notable_fields[no_fields]+ str(x)
                            if sn in rec_fields and rec_fields[sn]:                            
                                #print '%s: %s' % (notable_fields[no_fields], x)
                                if check_field in rec_fields and not rec_fields[check_field]:
                                    rec_fields[check_field] = rsl_detail[i]
                                    #print 'rec_fields[%s]: %s' %(check_field, rsl_detail[i])
                                #print 'if sn1 and %s exist follow value in rec_fields[%s]: %s' %(check_field, check_field, rec_fields[check_field])
                        for y in range(1, spare_sn_counter+1):
                            if y == 1:
                                spare_sn = 'spare_equip_serial'                            
                            else:
                                spare_sn = 'spare_equip_serial'+str(y)
                            check_field_sp = notable_fields[no_fields]+'_sp'+str(y)
                            #print 'spare_sn: ', spare_sn
                            #print '%s_sp: %s = %s' % (notable_fields[no_fields], check_field_sp, rec_fields[check_field_sp])
                            #if 'spare_equip_serial' in rec_fields and rec_fields['spare_equip_serial']:
                            if spare_sn in rec_fields and rec_fields[spare_sn]:
                                #print 'field %s in %s ' %(notable_fields[no_fields], rec_fields[spare_sn])
                                #if not rec_fields[check_fields_sp]:
                                if check_field_sp in rec_fields and not rec_fields[check_field_sp]:                                   
                                    rec_fields[check_field_sp] = rsl_detail[i]   
                                    #print 'if spare sn and %s exist follow value in %s: %s' %(check_field_sp, check_field_sp, rsl_detail[i])
                        if notable_fields[no_fields] == 'storage':
                            #print 'rsl_detail[%s]: %s' %(i, rsl_detail[i])   
                            #print 'notable_fields: ', notable_fields[no_fields]                   
                            ##check old serial number content                      
                            for old_sn in range(1, old_serial_counter+1):
                                sn = 'old_serial_no_'+ str(old_sn)
                                #print 'old_serial_no: ', sn
                                check_field = notable_fields[no_fields]+ str(old_sn)
                                if sn in rec_fields and rec_fields[sn]:                            
                                    #print '%s: %s' % (notable_fields[no_fields], old_sn)
                                    if check_field in rec_fields and not rec_fields[check_field]:
                                        rec_fields[check_field] = rsl_detail[i]
                                        #print 'rec_fields[%s]: %s' %(check_field, rsl_detail[i])
                                    #print 'if old serial and %s exist follow value in rec_fields[%s]: %s' %(check_field, check_field, rec_fields[check_field])
            
            #print '%s form_serial : %s' % (rec_fields['rslno'], rec_fields['form_serial'])
           
            log_instance        = LogBook.objects.get(pk=int(rsl_detail[len(header_location)-1]))     ### id should be last number            
            #print 'logbook', log_instance
            #sitename_instance   = Sitename.objects.get(pk=int(obj_detail[141]))   ### sitename table
            #cashier_instance    = Official_Receipt.objects.get(pk=int(obj_detail[141]))    ### cashier table
            #carrier_instance    = Carrier.objects.get(pk=int(obj_detail[141]))    ### carrier table
            #make_instance       = EquipModel.objects.get(pk=int(obj_detail[141])) ### EquipModel table
            #freqrange_instance  = Equipment.objects.get(pk=int(obj_detail[141]))  ### freqrange table            
            #encoder_instance    = User.objects.get(pk=int(obj_detail[141]))       ### User table
            #evaluator_instance  = User.objects.get(pk=int(obj_detail[141]))       ### User table
            #print 'check logbook id: ', int(rsl_detail[len(header_location)-1])
            #print 'final output: ', rec_fields
            try:
                LatestRsl.objects.create(logbook=log_instance, **rec_fields)
                # empty dict
                rec_fields.clear()
                #print 'insert success'
                messages.success(request, 'Successfully inserted record(s).')
            except:                
                messages.error(request, 'Fail to insert record.')
                #print 'insert not success'
        ## end 01/13/2014
### end import excel for rsl
#ok!
#class Official_ReceiptForm(forms.ModelForm):
class Official_ReceiptForm(autocomplete_light.ModelForm):
    carrier     = forms.ModelChoiceField(queryset=Carrier.objects.all(), label="Public Telecom Entity", widget=autocomplete_light.ChoiceWidget('CarrierAutocomplete', attrs={'style':'width:520px;',}))        
    remarks     = forms.CharField(label="Remarks", widget=forms.Textarea(), required=False)
    class Meta:
        model = Official_Receipt
        widgets = autocomplete_light.get_widgets_dict(Official_Receipt)
    
    #def __init__(self, *args, **kwargs):
    #    super(Official_ReceiptForm, self).__init__(*args, **kwargs)
    #    self.fields['validity_from'].widget = widgets.AdminDateWidget()
    #    self.fields['validity_to'].widget = widgets.AdminDateWidget()
        #self.fields['mytime'].widget = widgets.AdminTimeWidget()
        #self.fields['mydatetime'].widget = widgets.AdminSplitDateTime()
#ok!
#class SoaForm(forms.ModelForm): 
class SoaForm(autocomplete_light.ModelForm): 
    soa_code        = forms.CharField(label='Statement of Collection', required=False, help_text="Auto fill-up", widget=forms.TextInput(attrs={'style': 'width:120px; padding:0px; ',}))
    carrier         = forms.ModelChoiceField(queryset=Carrier.objects.all(), label="Public Telecom Entity", widget=autocomplete_light.ChoiceWidget('CarrierAutocomplete', attrs={'style':'width:520px;',}))               
    app_type        = forms.ModelMultipleChoiceField(widget=ColumnCheckboxSelectMultiple(columns=1, ), 
                                              queryset=App_type.objects.all(), label='Application Type')
    no_years        = forms.CharField(label='No. of Years', initial=1, widget=forms.TextInput(attrs={'style': 'width:120px; padding:0px; ',}))
    official_receipt= forms.ModelChoiceField(queryset=Official_Receipt.objects.all(), required=False, label="Official Receipt", widget=autocomplete_light.ChoiceWidget('Official_ReceiptAutocomplete', attrs={'style':'width:520px;',}))           
    #def __init__(self, *args, **kwargs):
    #    super(SoaForm, self).__init__(*args, **kwargs)
        #self.fields['app_type'].widget = forms.CheckboxSelectMultiple(choices=self.fields['app_type'].choices)        

    class Meta:
        model = SOA
        widgets = autocomplete_light.get_widgets_dict(SOA)
#ok!
class ShortNameClarableFileInput(ClearableFileInput):
    def render(self, name, value, attrs=None):
        substitutions = {
            'initial_text': self.initial_text,
            'input_text': self.input_text,
            'clear_template': '',
            'clear_checkbox_label': self.clear_checkbox_label,
        }
        template = u'%(input)s'
        substitutions['input'] = super(ClearableFileInput, self).render(name, value, attrs)

        if value and hasattr(value, "url"):
            template = self.template_with_initial
            substitutions['initial'] = (u'<a href="%s">%s</a>'
                                        % (escape(value.url),
                                           escape(force_unicode(os.path.basename(value.url))))) # I just changed this line
            if not self.is_required:
                checkbox_name = self.clear_checkbox_name(name)
                checkbox_id = self.clear_checkbox_id(checkbox_name)
                substitutions['clear_checkbox_name'] = conditional_escape(checkbox_name)
                substitutions['clear_checkbox_id'] = conditional_escape(checkbox_id)
                substitutions['clear'] = CheckboxInput().render(checkbox_name, False, attrs={'id': checkbox_id})
                substitutions['clear_template'] = self.template_with_clear % substitutions

        return mark_safe(template % substitutions)
#ok!
#class SoadetailForm(forms.ModelForm):
class SoadetailForm(autocomplete_light.ModelForm):
    sitename        = forms.CharField(required=False, label='Sitename', widget=forms.TextInput(attrs={'style':'width:200px; padding:0px;', 'autocomplete':'on',}))
    site_no         = forms.CharField(required=False, label='Site No', widget=forms.TextInput(attrs={'style':'width:70px; padding:0px;', 'autocomplete':'on',}))
    city            = forms.CharField(required=False, label='City', widget=forms.TextInput(attrs={'style':'width:100px; padding:0px;', 'autocomplete':'on',}))
    site_addr       = forms.CharField(required=True, label='Address', widget=forms.TextInput(attrs={'style':'width:200px; padding:0px;', 'autocomplete':'on',}))
    band            = forms.CharField(required=False, label='Band', widget=forms.TextInput(attrs={'style':'width:46px; padding:0px;', 'autocomplete':'on',}))  
    call_sign       = forms.CharField(required=False, label='Call-Sign', widget=forms.TextInput(attrs={'style':'width:70px; padding:0px; text-align:right;',}))
    no_years        = forms.DecimalField(label='No.Yrs', widget=forms.TextInput(attrs={'style':'width:46px; padding:0px; text-align:center;',}))
    ppp_units       = forms.DecimalField(label='No.PPP', widget=forms.TextInput(attrs={'style':'width:46px; padding:0px; text-align:center;',}))
    old_chan        = forms.DecimalField(label='Old.Ch', widget=forms.TextInput(attrs={'style':'width:42px; padding:0px; text-align:center;',}))
    channel         = forms.DecimalField(label='No.Ch', widget=forms.TextInput(attrs={'style':'width:42px; padding:0px; text-align:center;',}))
    filing_fee      = forms.DecimalField(label='File Fee', widget=forms.TextInput(attrs={'style':'width:52px; padding:0px; text-align:right;',}))
    no_ppp_ext      = forms.DecimalField(label='No.PPP Ext', widget=forms.TextInput(attrs={'style':'width:100%; padding:0px; text-align:right;',}))    
    purchase_fee    = forms.DecimalField(label='Pur Fee', widget=forms.TextInput(attrs={'style':'width:52px; padding:0px; text-align:right;',}))
    possess_fee     = forms.DecimalField(label='Poss Fee', widget=forms.TextInput(attrs={'style':'width:60px; padding:0px; text-align:right;',}))
    cprsl_filing_fee= forms.DecimalField(label='FF for CP', widget=forms.TextInput(attrs={'style':'width:62px; padding:0px; text-align:right;',}))
    const_fee       = forms.DecimalField(label='Const Fee', widget=forms.TextInput(attrs={'style':'width:66px; padding:0px; text-align:right;',}))
    rsl_units       = forms.DecimalField(label='No.Lic', widget=forms.TextInput(attrs={'style':'width:42px; padding:0px; text-align:center;',}))
    license_fee     = forms.DecimalField(label='Lic', widget=forms.TextInput(attrs={'style':'width:52px; padding:0px; text-align:right;',}))
    inspection_fee  = forms.DecimalField(label='IF', widget=forms.TextInput(attrs={'style':'width:52px; padding:0px; text-align:right;',}))
    mod_units       = forms.DecimalField(label='No.Mod', widget=forms.TextInput(attrs={'style':'width:52px; padding:0px; text-align:center;',}))
    mod_fee         = forms.DecimalField(label='Mod', widget=forms.TextInput(attrs={'style':'width:52px; padding:0px; text-align:right;',}))
    mod_filing_fee  = forms.DecimalField(label='Mod File', widget=forms.TextInput(attrs={'style':'width:55px; padding:0px; text-align:right;',}))
    stor_units      = forms.DecimalField(label='No.Stor', widget=forms.TextInput(attrs={'style':'width:52px; padding:0px; text-align:center;',}))
    storage_fee     = forms.DecimalField(label='Stor Fee', widget=forms.TextInput(attrs={'style':'width:55px; padding:0px; text-align:right;',}))
    rsl_dst_fee     = forms.DecimalField(label='Lic DST', widget=forms.TextInput(attrs={'style':'width:52px; padding:0px; text-align:right;',}))
    ppp_dst_fee     = forms.DecimalField(label='PPP DST', widget=forms.TextInput(attrs={'style':'width:54px; padding:0px; text-align:right;',}))
    sto_dst_fee     = forms.DecimalField(label='Stor DST', widget=forms.TextInput(attrs={'style':'width:57px; padding:0px; text-align:right;',}))
    suf_fee         = forms.DecimalField(label='SUF', widget=forms.TextInput(attrs={'style':'width:62px; padding:0px; text-align:right;',}))
    suf_rate        = forms.DecimalField(label='SUF rate', widget=forms.TextInput(attrs={'style':'width:56px; padding:0px; text-align:right;',}))
    freq            = forms.DecimalField(label='Freq', widget=forms.TextInput(attrs={'style':'width:42px; padding:0px; text-align:right;',}))
    bw              = forms.DecimalField(label='BW', widget=forms.TextInput(attrs={'style':'width:42px; padding:0px; text-align:center;',}))
    sur_lic_percent = forms.DecimalField(label='Sur Lic %', widget=forms.TextInput(attrs={'style':'width:62px; padding:0px; text-align:right;',}))
    sur_lic         = forms.DecimalField(label='Sur Lic', widget=forms.TextInput(attrs={'style':'width:52px; padding:0px; text-align:right;',}))
    sur_suf_percent = forms.DecimalField(label='Sur SUF %', widget=forms.TextInput(attrs={'style':'width:64px; padding:0px; text-align:right;',}))
    sur_suf         = forms.DecimalField(label='SUR SUF', widget=forms.TextInput(attrs={'style':'width:62px; padding:0px; text-align:right;',}))
    duplicate_fee   = forms.DecimalField(label='Dup Fee', widget=forms.TextInput(attrs={'style':'width:42px; padding:0px; text-align:right;',}))

    #def __init__(self, *args, **kwargs):
    #    super(SoadetailForm, self).__init__(*args, **kwargs)
        #self.fields['ppp_units'].widget = forms.TextInput(attrs={'size':10,})
    
    class Meta:
        model = SOA_detail
#OK!
#class LogBookForm(ModelForm):
class LogBookForm(autocomplete_light.ModelForm):
    ENGR_CHOICES=[('ENDORSEMENT','ENDORSEMENT'),('ENCODING','ENCODE'),('PENDING', 'PEND')]
    logbook_remarks = forms.CharField(widget=forms.Textarea(), label="Place your remark", required=False)
    docfile         = forms.FileField(label = '',help_text ='max 2.5 megabytes', widget=ShortNameClarableFileInput(), required=False) 
    # need to be added to work in modelformset_factory   
    engrchoice      = forms.ChoiceField(widget=forms.RadioSelect, choices=ENGR_CHOICES, required=False)
    #pending_desc    = forms.ModelChoiceField()
    endorsementfile = forms.FileField(widget=ShortNameClarableFileInput(), required=False)
    units           = forms.DecimalField(label="Unit(s)", widget=forms.TextInput(attrs={'style':'width:200px;', }), required=False)
    noofstation     = forms.DecimalField(label="No. of Station", widget=forms.TextInput(attrs={'style':'width:200px;', }), required=False)
    permitNo        = forms.CharField(label="Permit No.", widget=forms.TextInput(attrs={'style':'width:610px;', }), required=False)
    carrier         = forms.ModelChoiceField(Carrier.objects.all(), label="Public Telecom Entity", widget=autocomplete_light.ChoiceWidget('CarrierAutocomplete', attrs={'style':'width:520px;',}))
    current_user    = forms.ModelChoiceField(queryset=NAFD_User.objects.all(), label="Assign to", widget=autocomplete_light.ChoiceWidget('NAFD_User_groups_RBListAutocomplete', attrs={'style':'width:140px;',}))
    
    class Meta:        
        model = LogBook
        #fields = ('docfile', 'engrchoice', 'endorsementfile')
        #widgets = {
        #    'docfile': ShortNameClarableFileInput,
        #    'endorsementfile': ShortNameClarableFileInput,
            #'engrchoice':forms.RadioSelect(choices=ENGR_CHOICES),
        #}
        #widgets = autocomplete_light.get_widgets_dict(LogBook)

class LatestRslForm(ModelForm):
    class Meta:
        model = LatestRsl
#OK !
class PPPfilesForm(forms.Form):
    docfile = forms.FileField(label = 'Select a file',help_text ='max. 42 megabyts')

    class Meta:
        model = PPPfiles
#ok!
#class PPPInlineForm(ModelForm):
class PPPInlineForm(autocomplete_light.ModelForm):
    makemodel      = forms.ModelChoiceField(queryset=EquipModel.objects.all(), label='Make/Model', widget=autocomplete_light.ChoiceWidget('EquipModelAutocomplete',attrs={'style':'width:230px; padding:0px; background: rgb(238, 238, 238); border-color: rgb(238, 238, 238);', }))
    freqrange_low  = forms.CharField(required=False, label='Freq Range Low', widget=forms.TextInput(attrs={'style':'width:120px; padding:0px; background: rgb(238, 238, 238); border-color: rgb(238, 238, 238);', 'autocomplete':'on',}))
    freqrange_high = forms.CharField(required=False, label='Freq Range High', widget=forms.TextInput(attrs={'style':'width:120px; padding:0px; background: rgb(238, 238, 238); border-color: rgb(238, 238, 238);', 'autocomplete':'on',}))
    power          = forms.CharField(required=False, label='Power', widget=forms.TextInput(attrs={'style':'width:70px; padding:0px; background: rgb(238, 238, 238); border-color: rgb(238, 238, 238);', 'autocomplete':'on',}))
    bwe            = forms.CharField(required=False, label='BWE', widget=forms.TextInput(attrs={'style':'width:70px; padding:0px; background: rgb(238, 238, 238); border-color: rgb(238, 238, 238);', 'autocomplete':'on',}))
    serialno       = forms.CharField(required=False, label='SerialNo', widget=forms.TextInput(attrs={'style':'width:150px; padding:0px; background: rgb(238, 238, 238); border-color: rgb(238, 238, 238);', 'autocomplete':'on',}))
    sitename       = forms.ModelChoiceField(queryset=Sitename.objects.all(), label='Sitename', widget=autocomplete_light.ChoiceWidget('SitenameAutocomplete', attrs={'style':'width:190px; padding:0px; background: rgb(238, 238, 238); border-color: rgb(238, 238, 238);',}))
    
    class Meta:
        model = Equipment
        #widgets = autocomplete_light.get_widgets_dict(Equipment)       
#ok!
#class RslInlineForm(ModelForm):
class RslInlineForm(autocomplete_light.ModelForm):
    id                  = forms.DecimalField(label='ID', widget=forms.TextInput(attrs={'style':'width:30px; padding:0px;', 'autocomplete':'on',}))
    rslno               = forms.CharField(label='License No', widget=forms.TextInput(attrs={'style':'width:150px; padding:0px;', 'autocomplete':'on',}))
    sitename            = forms.ModelChoiceField(queryset=Sitename.objects.all(), label='Sitename', widget=autocomplete_light.ChoiceWidget('SitenameAutocomplete', attrs={'style':'width:150px; ',}), required=False) 
    ptsvc               = forms.CharField(label='Point of Service/Call-Sign', widget=forms.TextInput(attrs={'style':'width:250px; padding:0px;', 'autocomplete':'on',}), required=False)    
    
    class Meta:
        model = LatestRsl_v2
        #widgets = autocomplete_light.get_widgets_dict(Equipment)   

SIMPLIFIED_TRANSACTION_TYPE= (
        ('ALL', 'ALL'),
        ('TP', 'TP'),
        ('DEMO', 'DEMO'),
        ('PPP', 'PPP'),
        ('NEW', 'NEW'),
        ('REN', 'REN'),    
        ('MOD', 'MOD'),
        ('STO', 'STORAGE'),
        ('DUP', 'DUPLICATE'),
        ('RENMOD', 'REN/MOD'),
        ('RECALL', 'RECALL'))
#OK!
#class LatestRsl_v2Form(GenericModelForm):
class LatestRsl_v2Form(autocomplete_light.ModelForm): 
    #equipment           = forms.ModelMultipleChoiceField(Equipment.objects.select_related().all(),
    #    widget=autocomplete_light.MultipleChoiceWidget('EquipmentAutocomplete'), required=True)
    #official_receipt    = forms.ModelMultipleChoiceField(Official_Receipt.objects.select_related().all(),
    #    widget=autocomplete_light.MultipleChoiceWidget('Official_ReceiptAutocomplete'), required=True)
    #status              = forms.ChoiceField(label='Status', widget=forms.Select(attrs={'style':'width:139px;'}, choices=SIMPLIFIED_TRANSACTION_TYPE))    
    logbook             = forms.ModelChoiceField(LogBook.objects.all(), label="Logbook", widget=autocomplete_light.ChoiceWidget('LogBookAutocomplete', attrs={'style':'width:520px;',}))
    carrier             = forms.ModelChoiceField(Carrier.objects.all(), label="Public Telecom Entity", widget=autocomplete_light.ChoiceWidget('CarrierAutocomplete', attrs={'style':'width:520px;',}))    
    sitename            = forms.ModelChoiceField(Sitename.objects.all(), label="Sitename", widget=autocomplete_light.ChoiceWidget('SitenameAutocomplete', attrs={'style':'width:520px;',}))
    rslno               = forms.CharField(label='License No', widget=forms.TextInput(attrs={'style':'width:139px; padding:0px;', 'autocomplete':'on',}))
    lic_to_operate      = forms.CharField(label='License to Operate', widget=forms.TextInput(attrs={'style':'width:220px; padding:0px; background: rgb(238, 238, 238); border-color: rgb(238, 238, 238);', 'autocomplete':'on',}))
    capacity            = forms.CharField(label='Capacity', widget=forms.TextInput(attrs={'style':'width:50px; padding:0px;', 'autocomplete':'on',}))
    nature_of_service   = forms.CharField(label='Nature of Service', widget=forms.TextInput(attrs={'style':'width:50px; padding:0px;', 'autocomplete':'on',}), initial='CP')
    ptsvc               = forms.CharField(required=False, label='Point of Service', widget=forms.TextInput(attrs={'style':'width:812px; padding:0px;', 'autocomplete':'on',}))
    sitename_street     = forms.CharField(required=False, label='Street', widget=forms.TextInput(attrs={'style':'width:760px; padding:0px; background: rgb(238, 238, 238); border-color: rgb(238, 238, 238);', 'autocomplete':'on', }))
    sitename_city       = forms.CharField(required=False, label='City', widget=forms.TextInput(attrs={'style':'width:200px; padding:0px; background: rgb(238, 238, 238); border-color: rgb(238, 238, 238);', 'autocomplete':'on',}))
    sitename_province   = forms.CharField(required=False, label='Province', widget=forms.TextInput(attrs={'style':'width:200px; padding:0px; background: rgb(238, 238, 238); border-color: rgb(238, 238, 238);', 'autocomplete':'on',}))
    sitename_region     = forms.CharField(required=False, label='Region', widget=forms.TextInput(attrs={'style':'width:200px; padding:0px; background: rgb(238, 238, 238); border-color: rgb(238, 238, 238);', 'autocomplete':'on',}))
    sitename_longitude  = forms.CharField(required=False, label='Longitude', widget=forms.TextInput(attrs={'style':'width:200px; padding:0px; background: rgb(238, 238, 238); border-color: rgb(238, 238, 238);', 'autocomplete':'on',}))
    sitename_latitude   = forms.CharField(required=False, label='Latitude', widget=forms.TextInput(attrs={'style':'width:200px; padding:0px; background: rgb(238, 238, 238); border-color: rgb(238, 238, 238);', 'autocomplete':'on',}))
    equip_callsign      = forms.CharField(required=False, label='Call-Sign', widget=forms.TextInput(attrs={'style':'width:80px; padding:0px;', 'autocomplete':'on',}))
    remarks             = forms.CharField(label="Remarks", widget=forms.Textarea(), required=False)
    capacity            = forms.CharField(required=False, label='Capacity', widget=forms.TextInput(attrs={'style':'width:80px; padding:0px;', 'autocomplete':'on',})) 

    signatory           = forms.ModelChoiceField(queryset=NAFD_User.objects.all(), label="Signatory", widget=autocomplete_light.ChoiceWidget('NAFD_User_groups_DirAutocomplete', attrs={'style':'width:140px;',}))
    evaluator           = forms.ModelChoiceField(queryset=NAFD_User.objects.all(), label="Evaluator", widget=autocomplete_light.ChoiceWidget('NAFD_User_groups_EngrAutocomplete', attrs={'style':'width:140px;',}))
    encoder             = forms.ModelChoiceField(queryset=NAFD_User.objects.all(), label="Encoder", widget=autocomplete_light.ChoiceWidget('NAFD_User_groups_EncAutocomplete', attrs={'style':'width:140px;',}))
    class Meta:
        model = LatestRsl_v2
        #widgets = autocomplete_light.get_widgets_dict(LatestRsl_v2)
        #read_only = ['sitename_longitude',]
#OK!
#class LatestRsl_v2_EquipmentForm(GenericModelForm):
class LatestRsl_v2_EquipmentForm(autocomplete_light.ModelForm):
    equipment           = forms.ModelChoiceField(Equipment.objects.all(), label="Equipment", widget=autocomplete_light.ChoiceWidget('EquipmentAutocomplete', attrs={'style':'width:420px;',}))    
    equip_freqrange     = forms.CharField(required=False, label="Freq Range", widget=forms.TextInput(attrs={'style':'background: rgb(238, 238, 238); border-color: rgb(238, 238, 238);', 'autocomplete':'on',}))       
    equip_callsign      = forms.CharField(required=False, label="Call-Sign", widget=forms.TextInput(attrs={'style':'background: rgb(238, 238, 238); border-color: rgb(238, 238, 238);', 'autocomplete':'on',}))        
    equip_usagepolarity = forms.CharField(required=False, label="Usage/Polarity", widget=forms.TextInput(attrs={'style':'background: rgb(238, 238, 238); border-color: rgb(238, 238, 238);', 'autocomplete':'on',}))                
    equip_txrx          = forms.CharField(required=False, label="Transmit/Recieved", widget=forms.TextInput(attrs={'style':'background: rgb(238, 238, 238); border-color: rgb(238, 238, 238);', 'autocomplete':'on',}))                    
    equip_powerbwe      = forms.CharField(required=False, label="Power/BWE", widget=forms.TextInput(attrs={'style':'background: rgb(238, 238, 238); border-color: rgb(238, 238, 238);', 'autocomplete':'on',}))        
    equip_purchase      = forms.CharField(required=False, label="Purchase", widget=forms.TextInput(attrs={'style':'background: rgb(238, 238, 238); border-color: rgb(238, 238, 238);', 'autocomplete':'on',}))    
    equip_possess       = forms.CharField(required=False, label="Possess", widget=forms.TextInput(attrs={'style':'background: rgb(238, 238, 238); border-color: rgb(238, 238, 238);', 'autocomplete':'on',}))    
    equip_storage       = forms.CharField(required=False, label="Storage", widget=forms.TextInput(attrs={'style':'background: rgb(238, 238, 238); border-color: rgb(238, 238, 238);', 'autocomplete':'on',}))            
    ant_details         = forms.CharField(required=False, label="Antenna Details", widget=forms.Textarea(attrs={'style':'background: rgb(238, 238, 238); border-color: rgb(238, 238, 238);', 'autocomplete':'on',}))     

    class Meta:
        model = LatestRsl_v2_Equipment
        #widgets = autocomplete_light.get_widgets_dict(LatestRsl_v2_Equipment)      

class PhilAddressForm(ModelForm):    
    def __init__(self, *args, **kwargs): 
        super(PhilAddressForm, self).__init__(*args, **kwargs)              
        self.fields['province'].queryset = Province.objects.all()

    province = forms.ModelChoiceField(queryset=None, empty_label=None)   

    class META:
        #CHOICES = Province.objects.all()
        model   = PhilAddress
        #widget  = {
        #    'province': Select(choices=((x.province, x.province) for x in CHOICES ),)
        #}

#from models import NUser #you can use get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.admin import UserAdmin

class MyUserChangeForm(UserChangeForm):
    code_name   = forms.CharField(required=False, label='Alias', widget=forms.TextInput(attrs={'style':'width:118px; padding:0px;', 'autocomplete':'on',}))
    kpi_target  = forms.DecimalField(required=False, label='KPI Target', widget=forms.TextInput(attrs={'style':'width:118px; padding:0px;', 'autocomplete':'on',}))
    foryear     = forms.DecimalField(required=False, label='For year', widget=forms.TextInput(attrs={'style':'width:118px; padding:0px;', 'autocomplete':'on',}))
    
    class Meta(UserChangeForm.Meta):
        model = NAFD_User

class MyUserCreationForm(UserCreationForm): 
    def clean_username(self):
        # Since User.username is unique, this check is redundant,
        # but it sets a nicer error message than the ORM. See #13147.
        username = self.cleaned_data["username"]
        try:
            NAFD_User._default_manager.get(username=username)
        except NAFD_User.DoesNotExist:
            return username
        raise forms.ValidationError(self.error_messages['duplicate_username'])

    class Meta(UserCreationForm.Meta):
        model = NAFD_User

#class CarrierForm(ModelForm):autocomplete_light.ModelForm
class CarrierForm(autocomplete_light.ModelForm):
    address = forms.ModelChoiceField(queryset=PhilAddress.objects.all(), label="City/Province", widget=autocomplete_light.ChoiceWidget('PhilAddressAutocomplete', attrs={'style':'width:220px;',}))

    class Meta:
        model   = Carrier
        #widgets = autocomplete_light.get_widgets_dict(Carrier)

class SitenameForm(autocomplete_light.ModelForm):
    deg_long    = forms.CharField(label='Deg long.', widget=forms.TextInput(attrs={'style':'width:50px; padding:0px;',}))
    min_long    = forms.CharField(label='Min long.', widget=forms.TextInput(attrs={'style':'width:50px; padding:0px;',}))
    sec_long    = forms.CharField(label='Sec long.', widget=forms.TextInput(attrs={'style':'width:50px; padding:0px;',}))
    deg_lat     = forms.CharField(label='Deg lat.', widget=forms.TextInput(attrs={'style':'width:50px; padding:0px;',}))
    min_lat     = forms.CharField(label='Min long.', widget=forms.TextInput(attrs={'style':'width:50px; padding:0px;',}))
    sec_lat     = forms.CharField(label='Sec long.', widget=forms.TextInput(attrs={'style':'width:50px; padding:0px;',}))
    address     = forms.ModelChoiceField(queryset=PhilAddress.objects.all(), label="Address", widget=autocomplete_light.ChoiceWidget('PhilAddressAutocomplete', attrs={'style':'width:520px;',}))        
    carrier     = forms.ModelChoiceField(queryset=Carrier.objects.all(), label="Public Telecom Entity", widget=autocomplete_light.ChoiceWidget('CarrierAutocomplete', attrs={'style':'width:520px;',}))        

    class Meta:
        model   = Sitename
        widgets = autocomplete_light.get_widgets_dict(Sitename)

class StatementForm(autocomplete_light.ModelForm):
    soa     = forms.ModelChoiceField(queryset=SOA.objects.all(), label="SOA", widget=autocomplete_light.ChoiceWidget('SOAAutocomplete', attrs={'style':'width:180px;',}))        

class RSL_ORForm(autocomplete_light.ModelForm):
    official_receipt     = forms.ModelChoiceField(queryset=Official_Receipt.objects.all(), label="Official Receipt", widget=autocomplete_light.ChoiceWidget('Official_ReceiptAutocomplete', attrs={'style':'width:180px;',}))        

## for testing
class EquipRackForm(autocomplete_light.ModelForm):
    equipment           = forms.ModelChoiceField(queryset=Equipment.objects.all(), label="Equipment", widget=autocomplete_light.ChoiceWidget('EquipmentAutocomplete', attrs={'style':'width:180px;',}))        
    equip_makemodel     = forms.CharField(required=False, label="Make/Model", widget=forms.TextInput(attrs={'style':'width:230px; background: rgb(238, 238, 238); border-color: rgb(238, 238, 238);', 'autocomplete':'on',}))       
    equip_freqrange_low = forms.CharField(required=False, label="Freq Range Low", widget=forms.TextInput(attrs={'style':'width:120px; background: rgb(238, 238, 238); border-color: rgb(238, 238, 238);', 'autocomplete':'on',}))       
    equip_freqrange_high= forms.CharField(required=False, label="Freq Range High", widget=forms.TextInput(attrs={'style':'width:120px; background: rgb(238, 238, 238); border-color: rgb(238, 238, 238);', 'autocomplete':'on',}))       
    equip_power         = forms.CharField(required=False, label="Power", widget=forms.TextInput(attrs={'style':'width:70px; background: rgb(238, 238, 238); border-color: rgb(238, 238, 238);', 'autocomplete':'on',}))       
    equip_bwe           = forms.CharField(required=False, label="BWE", widget=forms.TextInput(attrs={'style':'width:70px; background: rgb(238, 238, 238); border-color: rgb(238, 238, 238);', 'autocomplete':'on',}))       
    equip_sn            = forms.CharField(required=False, label="Serial No", widget=forms.TextInput(attrs={'style':'width:150px; background: rgb(238, 238, 238); border-color: rgb(238, 238, 238);', 'autocomplete':'on',}))       
    equip_sitename      = forms.CharField(required=False, label="Sitename", widget=forms.TextInput(attrs={'style':'width:190px; background: rgb(238, 238, 238); border-color: rgb(238, 238, 238);', 'autocomplete':'on',}))       
## end     

