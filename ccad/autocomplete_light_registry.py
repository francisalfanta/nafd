from django import http

import autocomplete_light
from ccad.models import *
from django.db.models import Max, Q
#from ccad.admin import DirectorListFilter
from django.core.urlresolvers import reverse
'''
class AutocompleteSitename(autocomplete_light.AutocompleteModelTemplate):
	autocomplete_template = 'template/admin/autocomplete.html'

	def post(self, request, *args, **kwargs):
        choice = LatestRsl.objects.create(site=request.POST['createChoice'])
        return http.HttpResponse(self.choice_html(choice))	

autocomplete_light.register(SOA_detail, AutocompleteSitename)
'''
class CarrierAutocomplete(autocomplete_light.AutocompleteModelBase):	
	model 				= Carrier
  	search_fields		= ['c_initial', 'companyname']
  	choices 			= Carrier.objects.all()  	
	autocomplete_js_attributes	=	{'placeholder': 'name or initial',}
	'''
	attrs = {
		'data-autocomplete-minimum-characters': 0,
		#'placeholder': 'name or initial',
	}
	widget_attrs={
        'data-widget-maximum-values': 4,
        # Enable modern-style widget !
        'class': 'modern-style',
    }
    '''
	#autocomplete_template = 'your_autocomplete_box.html'
	# choices=Person.objects.filter(is_company=False))

	'''def choices_for_request(self):
		choices = super(CarrierAutocomplete, self).choices_for_request()
		if not self.request.user.is_staff:
			choices = choices.filter(private=False)    	
		return choices'''

	def choice_label(self, choice):		
		return u'<a href="%s"?_popup=1" target="_blank" onclick="return showAddAnotherPopup(this);">%s</a>' % (reverse('admin:ccad_carrier_change', args=(choice.id,)), choice,)	
	
class PhilAddressAutocomplete(autocomplete_light.AutocompleteModelBase):
	search_fields 				=	['city']
	autocomplete_js_attributes 	=	{'placeholder': 'Town or City..',}
	#choices 					=	PhilAddress.objects.all()	

	#def choice_label(self, choice):
	#	return u'<a href="%s"?_popup=1" target="_blank" onclick="return showAddAnotherPopup(this);">%s</a>' % (reverse('admin:ccad_philaddress_change', args=(choice.id,)), choice,)

autocomplete_light.register(CarrierAutocomplete)
autocomplete_light.register(PhilAddress, PhilAddressAutocomplete)

class SitenameAutocomplete(autocomplete_light.AutocompleteModelBase):
	search_fields 			    =    ['site', 'street']
	autocomplete_js_attributes 	=	{'placeholder': 'site or street',}

	def choice_label(self, choice):
		return u'<a href="%s"?_popup=1" target="_blank" onclick="return showAddAnotherPopup(this);">%s</a>' % (reverse('admin:ccad_sitename_change', args=(choice.id,)), choice,)

autocomplete_light.register(Sitename, SitenameAutocomplete)

class LogBookAutocomplete(autocomplete_light.AutocompleteModelBase):
	search_fields 				= 	['controlNo']
	autocomplete_js_attributes 	=	{'placeholder': 'control no...',}

	#def choice_label(self, choice):
	#	return u'<a href="%s"?_popup=1" target="_blank" onclick="return showAddAnotherPopup(this);">%s</a>' % (reverse('admin:ccad_logbook_change', args=(choice.id,)), choice,)

autocomplete_light.register(LogBook, LogBookAutocomplete)

class AutocompleteTaggableItems(autocomplete_light.AutocompleteGenericBase):
    choices = (
        Equipment.objects.all(),
        #LatestRsl_v2.objects.all(),        
    )

    search_fields = (
        ('callsign'),
        ('rslno',),       
    )

autocomplete_light.register(AutocompleteTaggableItems)

class EquipmentAutocomplete(autocomplete_light.AutocompleteModelBase):
	search_fields = ['^callsign', '^serialno']
	choices       = (Equipment.objects.all())
	autocomplete_js_attributes = {'placeholder': 'serial or callsign',}
	widget_js_attributes  = {'min_values' : 0,}
	''' version 2
	attrs = {
		'data-autocomplete-minimum-characters': 0,
		'placeholder': 'serial or callsign',
	}
	#widget_attrs = {'data-widget-maximum-values': 3}
	'''
	def choice_label(self, choice):
		return u'<a href="%s"?_popup=1" target="_blank" onclick="return showAddAnotherPopup(this);">%s</a>' % (reverse('admin:ccad_equipment_change', args=(choice.id,)), choice,)

autocomplete_light.register(Equipment, EquipmentAutocomplete)

class EquipModelAutocomplete(autocomplete_light.AutocompleteModelBase):
	search_fields = ['make']
	autocomplete_js_attributes = { 'placeholder': 'Make',}
	widget_js_attributes = { 'min_values': 0,}

	#def choice_label(self, choice):
	#	return u'<a href="%s"?_popup=1" target="_blank" onclick="return showAddAnotherPopup(this);">%s</a>' % (reverse('admin:ccad_equipmodel_change', args=(choice.id,)), choice,)

autocomplete_light.register(EquipModel, EquipModelAutocomplete)

class AntennaAutocomplete(autocomplete_light.AutocompleteModelBase):
	search_fields = ['antenna_type']
	autocomplete_js_attributes = { 'placeholder': 'Antenna type', }
	widget_js_attributes = { 'min_values': 0, }
	'''
	attrs = {
		'data-autocomplete-minimum-characters': 0,
		'placeholder': 'Antenna type',
	}
	'''
	def choice_label(self, choice):
		return u'<a href="%s"?_popup=1" target="_blank" onclick="return showAddAnotherPopup(this);">%s</a>' % (reverse('admin:ccad_antenna_change', args=(choice.id,)), choice,)

autocomplete_light.register(Antenna, AntennaAutocomplete)

class Official_ReceiptAutocomplete(autocomplete_light.AutocompleteModelBase):
	model                      = Official_Receipt
	choices 	  			   = Official_Receipt.objects.all() 
	search_fields  			   = ['or_no']
	autocomplete_js_attributes = { 'placeholder': 'O.R. no', }
	widget_js_attributes = { 'min_values': 0, }
	'''
	attrs = {
		'data-autocomplete-minimum-characters': 0,
		'placeholder': 'O.R. no',
	}
	'''
	def choice_label(self, choice):
		return u'<a href="%s"?_popup=1" target="_blank" onclick="return showAddAnotherPopup(this);">%s</a>' % (reverse('admin:ccad_official_receipt_change', args=(choice.or_no,)), choice,)

autocomplete_light.register(Official_ReceiptAutocomplete)

class StatementsAutocomplete(autocomplete_light.AutocompleteModelBase):
	search_fields = ['soa']
	autocomplete_js_attributes = { 'placeholder': 'Statements of Account', }
	widget_js_attributes = { 'min_values': 0, }
	'''
	attrs = {
		'data-autocomplete-minimum-characters': 0,
		'placeholder': 'Statements of Account',
	}
	'''
	def choice_label(self, choice):
		return u'<a href="%s"?_popup=1" target="_blank" onclick="return showAddAnotherPopup(this);">%s</a>' % (reverse('admin:ccad_soa_change', args=(choice.or_no,)), choice,)

autocomplete_light.register(Statements, StatementsAutocomplete)

class NAFD_User_groups_DirAutocomplete(autocomplete_light.AutocompleteModelBase):
	model = NAFD_USER_GROUPS
	final_list = list()
    	encoder_list = NAFD_USER_GROUPS.objects.select_related().filter(Q(group__name='Director') | Q(group__name='OIC - Director'))
    	for x in encoder_list:
    	    final_list.append(x.nafd_user.id)
	choices = NAFD_User.objects.filter(pk__in=final_list)
	#choices = NAFD_User.objects.all()
	search_fields = ['username', 'first_name', 'last_name', 'email', 'code_name']
	#search_fields = ['code_name']
	autocomplete_js_attributes = { 'placeholder': 'Director',}
	widget_js_attributes = { 'min_values': 0,}


autocomplete_light.register(NAFD_User_groups_DirAutocomplete)

class NAFD_User_groups_EncAutocomplete(autocomplete_light.AutocompleteModelBase):
	model = NAFD_USER_GROUPS
	final_list = list()
    	encoder_list = NAFD_USER_GROUPS.objects.select_related().filter(group__name='Encoder')
    	for x in encoder_list:
    	    final_list.append(x.nafd_user.id)
	choices = NAFD_User.objects.filter(pk__in=final_list)
	search_fields = ['username', 'first_name', 'last_name', 'email', 'code_name']
	#search_fields = ['code_name']
	autocomplete_js_attributes = { 'placeholder': 'Encoder',}
	widget_js_attributes = { 'min_values': 0,}


autocomplete_light.register(NAFD_User_groups_EncAutocomplete)

class NAFD_User_groups_EngrAutocomplete(autocomplete_light.AutocompleteModelBase):
	model = NAFD_USER_GROUPS
	final_list = list()
    	encoder_list = NAFD_USER_GROUPS.objects.select_related().filter(group__name='Engr')
    	for x in encoder_list:
    	    final_list.append(x.nafd_user.id)
	choices = NAFD_User.objects.filter(pk__in=final_list)	
	search_fields = ['username', 'first_name', 'last_name', 'email', 'code_name']
	#search_fields = ['code_name']
	autocomplete_js_attributes = { 'placeholder': 'Engineer',}
	widget_js_attributes = { 'min_values': 0,}

autocomplete_light.register(NAFD_User_groups_EngrAutocomplete)

class NAFD_User_groups_RBListAutocomplete(autocomplete_light.AutocompleteModelBase):
	model = NAFD_USER_GROUPS
	final_list = list()
    	rbuser_list = NAFD_USER_GROUPS.objects.select_related().filter(group__name='Regulation Branch Personnel')
    	for x in rbuser_list:
    	    final_list.append(x.nafd_user.id)
	choices = NAFD_User.objects.filter(pk__in=final_list)	
	search_fields = ['username', 'first_name', 'last_name', 'email', 'code_name']
	#search_fields = ['code_name']
	autocomplete_js_attributes = { 'placeholder': 'RB Personnel',}
	widget_js_attributes = { 'min_values': 0,}

autocomplete_light.register(NAFD_User_groups_RBListAutocomplete)

class SOAAutocomplete(autocomplete_light.AutocompleteModelBase):
	model 						= SOA
	search_fields 				= ['soa_code']
	choices       				= (SOA.objects.all())
	autocomplete_js_attributes 	= {'placeholder': 'Statement of Collection No',}
	widget_js_attributes  		= {'min_values' : 0,}

	def choice_label(self, choice):
		return u'<a href="%s"?_popup=1" target="_blank" onclick="return showAddAnotherPopup(this);">%s</a>' % (reverse('admin:ccad_soa_change', args=(choice.id,)), choice,)

autocomplete_light.register(SOAAutocomplete)
