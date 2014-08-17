"""
A set of request processors that return dictionaries to be merged into a
template context. Each function takes the request object as its only parameter
and returns a dictionary to add to the context.

These are referenced from the setting TEMPLATE_CONTEXT_PROCESSORS and used by
RequestContext.
"""

from ccad.models import *
from datetime import datetime
from decimal import *

def freeze(d):
    if isinstance(d, dict):
        return frozenset((key, freeze(value)) for key, value in d.items())
    elif isinstance(d, list):
        return tuple(freeze(value) for value in d)
    return d

def nafd_staff(request):
    export_data = {}
    export_data['total']=0
    params = {}    
    include_only = ['PPP', 'CP', 'RSL', 'MOD', 'RECALL', 'TP', 'DEMO', 'DUP']
    for i in include_only:
        export_data[i] = 0     	

  	apt      		 = App_type.objects.all()  	
    staff_list 	 = NAFD_User.objects.filter(#Q(groups__name='Encoder')|Q(groups__name='Engr'),
                                            Q(groups__name='NAFD Personnel', is_active=1),
                                            ~Q(groups__name='NAFD Chief'))

    for staff in staff_list:        
        #print 'staff entry: ', staff.id
        apt2 = apt.extra(select={'units':"""SELECT 
                                          SUM( \
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
                                          END) "items" \
                                        FROM ccad_app_type appt, \
                                          ( SELECT DISTINCT sl.controlNo, \
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
                            select_params=(staff.id,))
        # segregate by Application Type
        for rec in apt2:
            if rec.trans_type in include_only:
                if rec.units:
                    export_data[rec.trans_type]=rec.units.normalize()
                    #print 'contain rec.units: ', rec.units
                else:
                    export_data[rec.trans_type]=Decimal(0)
                    #print 'no rec.units: ', rec.units
        # get total
        for i in include_only:
            if export_data[i] ==None:
                export_data[i] = Decimal(0)
                #print 'no rec.units: ', rec.units
            export_data.update(total=export_data['total'] + Decimal(export_data[i]).normalize())
            #print 'export_data[i]: ', export_data[i]

        try:
            user_info = NAFD_User.objects.get(pk=staff.id)
            #print 'staff id: ', user_info.user_id   
            
            if not user_info.kpi_target:
                user_info.kpi_target = 0;
                #print 'user_info.kpi_target: ', user_info.kpi_target

            # verify the set kpi for the current year
            if user_info.foryear == datetime.now().year:
                #print 'if: ', user_info.user_id
                params[staff.id]={
                        staff.username:{
                          'staff_kpi_target':{
                              'target': user_info.kpi_target, 
                              'processed': export_data['total']
                              },
                          staff.username+'_id' :staff.id,               
                                 }
                          }         
            else:
                #print 'else: ', user_info.user_id
                params[staff.id]={
                        staff.username:{
                          'staff_kpi_target':{
                              'target': user_info.kpi_target, 
                              'processed': export_data['total']
                              },
                          staff.username+'_id' :staff.id,               
                                 }
                          }
        except ObjectDoesNotExist:      
            print 'User info  does not exist.'
        #reset values
        export_data['total']=0  
    #print 'params :', params
    return {'params': params}
