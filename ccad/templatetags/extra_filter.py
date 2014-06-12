from django import template
from ccad.views import docname
from ccad.models import *

register = template.Library()

@register.filter
def only_filename(value):
    return docname(value)

@register.filter(name='cei')
def compute_exact_id(value, rb_page_no):    
    new_id = value+(5*(rb_page_no-1))    
    return new_id

@register.filter
def check_pppfiles(value):
	"""Check the entry for any related PPP files
	   return file exist if found """
	pppfiles = PPPfiles.objects.filter(logbook=value)
	if pppfiles.count() > 0:
		return True
	else:
		return False

@register.filter
def pppfile_names(value):
	""" Return a list of file name for the specified logbook """	
	pppfiles = PPPfiles.objects.filter(logbook=value)
	return list(pppfiles)

@register.filter
def orno_list(value):
	""" Return a list of OR No. for the specified logbook """
	statement = Statements.objects.select_related().filter(logbook=value)
	return list(statement)

@register.filter
def check_group(value):
	""" Return Group Name for the given user """
	user = NAFD_User.objects.get(pk=value)
	#print 'user: ', user.username
	group_name_list = list()
	group_list = NAFD_USER_GROUPS.objects.filter(nafd_user=value)	
	for rec in group_list:
		#print 'rec.group: ', rec.group
		group_name_list.append(rec.group.name)
	#print 'group_name_list: ', group_name_list
	return group_name_list