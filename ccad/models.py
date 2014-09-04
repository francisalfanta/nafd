# -*- coding: utf-8 -*-
import os, sys, uuid  # added for character like Ñ

#import datetime
from django.conf import settings
from django.db import models
from django.forms import ModelForm, forms, ModelChoiceField

from django.utils.translation import ugettext_lazy as _
from django.utils.timezone import *
from django.contrib.auth.models import AbstractUser, Group

from django.db.models import Count, Q, Sum # not in user - just in case to be use
from django.db.models.signals import pre_delete, post_delete, pre_save, post_save

from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.dispatch.dispatcher import receiver

from datetime import timedelta, datetime

#from ccad.models import no_work
# Create your models here.

STATUS_CHOICES  = (
        ('NEW','NEW'),
        ('REN','REN'),
        ('REN/MOD','REN/MOD'),
        ('MOD','MOD'),
        ('STORAGE','STORAGE'),
	    ('DUP','DUPLICATE'),
        ('RECALL', 'RECALL'),
        ('CANCELLED','CANCELLED')
) 
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
        ('REN/MOD', 'REN/MOD'),
        ('RECALL', 'RECALL'),
)
SERVICE_TYPE    = (
        ('MICROWAVE', 'MICROWAVE'),
        ('BWA', 'BWA-WIMAX'),
        ('WDN', 'WIRELESS DATA NETWORK'),
        ('2G', '2G'),
        ('3G', '3G'),
        ('EARTH STATION', 'EARTH STATION'),
)
STATUS_TYPE     = (
        (u'CHECKING REQUIREMENTS', u'CHECKING REQUIREMENTS'),       #1-CR
        (u'ISSUANCE OF SOA', u'ISSUANCE OF SOA'),                   #2-SOA
        (u'PAYMENT', u'PAYMENT'),                                   #3-PAYMENT
        (u'EVALUATION', u'EVALUATION'),                             #4-EVAL
        (u'ENDORSEMENT', u'ENDORSEMENT'),                           #5-FMD
        (u'ENCODING', u'ENCODING'),                                 #6-ENCODE
        (u'REVIEW', u'REVIEW'),                                     #7-REVIEW
        (u'SIGNATURE', u'SIGNATURE'),                               #8-SIGN
        (u'CHIEF SIGNATURE', u'CHIEF SIGNATURE'),                   #9-CHIEF SIGN
        (u'DIRECTOR SIGNATURE', u'DIRECTOR SIGNATURE'),             #10-RB SIGN
        (u'CASHIER STAMP', u'CASHIER STAMP'),                       #11-CASHIER STAMP
        (u'RELEASE TO SECRETARIAT', u'RELEASE TO SECRETARIAT'),     #11-RELEASE
        (u'TASK COMPLETED', u'TASK COMPLETED'),                     #10-COMPLETE
        (u'PENDING', u'PENDING'),
)
ENGR_CHOICES=[('ENDORSEMENT','ENDORSEMENT'),('ENCODING','ENCODE'),('PENDING', 'PEND')]

USAGE_TYPE = (
    ('Main', 'MAIN EQUIPMENT'),
    ('Protection', 'PROTECTION'),
    )
POWER_UNIT = (
    ('dBm', 'dBm'),
    ('kW', 'kW'),
    )
EQUIP_STATUS  = (
        ('NEW','NEW'),
        ('REN','REN'),
        ('REN/MOD','REN/MOD'),
        ('MOD','MOD'),
        ('STORAGE','STORAGE')
    )  
DIRECTORS = (
    ('Ariel Padilla', 'Ariel Padilla'),
    ('Azor Sitchon', 'Azor Sitchon'),
    ('Danilo Cuenca', 'Danilo Cuenca'),
    ('Dante Vengua', 'Dante Vengua'),
    ('Delilah Deles', 'Delilah Deles'),
    ('Edgardo Cabarios', 'Edgardo Cabarios'),
    ('Edgardo Celorico', 'Edgardo Celorico'),
    ('Froilan Jamias', 'Froilan Jamias'),
    ('Jerry Tacay', 'Jerry Tacay'),
    ('Jesus Laureno', 'Jesus Laureno'),
    ('Joselito Leynes', 'Joselito Leynes'),
    ('Josue De Villa Go', 'Josue De Villa Go'),
    ('Nestor Antonio Monroy', 'Nestor Antonio Monroy'),
    ('Onofre Galindo', 'Onofre Galindo'),
    ('Reynaldo Sta. Maria', 'Reynaldo Sta. Maria'),
    ('Romeo Miguel', 'Romeo Miguel'),
    ('Rudy Valdez', 'Rudy Valdez'),
    ('Samuel Young', 'Samual Young'),
    ('Teodoro Buenavista, Jr', 'Teodoro Buenavista, Jr'))
ENCODER = (
    ('DON', 'DON'),
    ('REMY', 'REMY'),
    ('EGG', 'EGG'),
    ('CINDY', 'CINDY'),
    ('ALEX', 'ALEX'),
    ('DONNA', 'DONNA'),
    ('EDMUN', 'EDMUN'))
EVALUATOR = (
    ('ADT', 'ADT'),
    ('ANO', 'ANO'),
    ('EDD', 'EDD'),
    ('FMA', 'FMA'),
    ('VMM', 'VMM'),
    ('SOP', 'SOP'))
##########
# TESTING
'''
class DirectorListManager(models.Manager):
    def get_query_set(self):
        return super(DirectorManager, self).get_query_set().filter(group='Director')
'''
# END TESTING MODULE
###########
class NAFD_User(AbstractUser):
    code_name = models.CharField(max_length=10, blank=True, null=False, unique=True)
    kpi_target= models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    foryear   = models.DecimalField(max_digits=4, decimal_places=0, blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'code_name', 'kpi_target', 'foryear']

    def __unicode__(self):
        return self.code_name

NAFD_User._meta.get_field_by_name('email')[0]._unique=True

class NAFD_USER_GROUPS(models.Model):
    nafd_user = models.ForeignKey(NAFD_User, null=True, on_delete=models.SET_NULL)
    group     = models.ForeignKey(Group, null=True, on_delete=models.SET_NULL)

    objects     = models.Manager()    # default Manager
    #director_objects = DirectorListManager() # Manager to filter for Director Only

    def __unicode__(self):
       return self.nafd_user.code_name

class Province(models.Model):
    province        = models.CharField(max_length=150, blank=True, null=True, verbose_name="Province")

    def __unicode__(self):
        return self.province

    class Meta:
        verbose_name        = "Province"
        verbose_name_plural = "Provinces"
#ok!
class PhilAddress(models.Model):
    id              = models.AutoField(primary_key=True)
    city            = models.CharField(max_length=150, blank=True, null=True, verbose_name="Town/City")
    province        = models.CharField(max_length=150, blank=True, null=True, verbose_name="Province")
    region          = models.CharField(max_length=50, blank=True, null=True, verbose_name="Region")
    regioncode      = models.CharField(max_length=50, blank=True, null=True, verbose_name="Region Code")

    class Meta:
        verbose_name_plural = "Cities / Towns"
        verbose_name        = "Address"
        ordering            = ['city', 'province', 'regioncode']

    def __unicode__(self):
        return u'%s, %s, %s' % (self.city, self.province, self.region)
#ok!
class Classofstation(models.Model):
    id              = models.AutoField(primary_key=True)
    class_name      = models.CharField(max_length=50, blank=True, null=True, verbose_name="Class Name")
    description     = models.CharField(max_length=300, blank=True, null=True, verbose_name="Description") # lic_to_operate

    class Meta:        
        verbose_name_plural = "Class of Stations"
        verbose_name        = "Class of Station"
        ordering            = ['class_name']

    def __unicode__(self):
        return self.class_name
#ok!
class EquipModel(models.Model):
    id              = models.AutoField(primary_key=True)
    make            = models.CharField(max_length=100, blank=True, null=True, verbose_name="Make/Models", default='NO MODEL')    

    class Meta:        
        verbose_name_plural = "Equipment Models"
        verbose_name        = "Equipment Model"
        ordering            = ['make']

    def __unicode__(self):
        return self.make
#ok!
class Antenna(models.Model):
    id              = models.AutoField(primary_key=True)
    antenna_type    = models.CharField(max_length=100, blank=False, null=False, verbose_name="Antenna Type")    
    directivity     = models.CharField(max_length=50, blank=True, null=True, verbose_name="Directivity")    
    height          = models.CharField(max_length=50, blank=True, null=True, verbose_name="Height from Ground")    
    gain            = models.CharField(max_length=100, blank=True, null=True, verbose_name="Gain")    

    def __unicode__(self):
        return self.antenna_type

    class Meta:
        verbose_name        = "Antenna"
#ok!
class LogBook_counter(models.Manager):
    def get_query_set(self):       
        return super(LogBook_counter, self).get_query_set().only('controlNo').latest('id')        
#ok!
class SOA_counter(models.Manager):
    def get_query_set(self):
        present = datetime.now()     
        return super(SOA_counter, self).get_query_set().filter(date_issued__year=present.year, date_issued__month=present.month)
#ok!
class App_type(models.Model):
    id              = models.AutoField(primary_key=True)
    trans_type      = models.CharField(max_length=20, blank=True, null=True, verbose_name='Application Type')

    class Meta:
        verbose_name_plural = 'Applications Types'
        verbose_name        = "Applications Type"

    def __unicode__(self):
        return self.trans_type
## on test #ok!
class FAS_Data(models.Model):
    id              = models.AutoField(primary_key=True)
    ReferenceNumber = models.CharField(max_length=20,blank=True, null=True,verbose_name='Ref No.')
    Licensee        = models.CharField(max_length=30,blank=True, null=True,verbose_name='Licensee')
    Tx              = models.DecimalField(max_digits=10,decimal_places=4,null=True,blank=True, verbose_name='TX (Mhz)')
    Rx              = models.DecimalField(max_digits=10,decimal_places=4,null=True,blank=True, verbose_name='RX (Mhz)')
    CallSign_A      = models.CharField(max_length=30,blank=True, null=True,verbose_name='Call-Sign A')
    CallSign_B      = models.CharField(max_length=30,blank=True, null=True,verbose_name='Call-Sign B')
    Bwe             = models.CharField(max_length=20,blank=True, null=True,verbose_name='BW & Emission')
    Stn_A           = models.CharField(max_length=150,blank=True, null=True,verbose_name='Station A')
    Stn_B           = models.CharField(max_length=150,blank=True, null=True,verbose_name='Station B')
    Remarks_1       = models.TextField(max_length=50,blank=True, null=True,verbose_name='Station A')
    Class           = models.CharField(max_length=20,blank=True, null=True,verbose_name='Class of Station')
    Power_dbm       = models.DecimalField(max_digits=10,decimal_places=4,null=True,blank=True, verbose_name='Power Output (dBm)')
    Power_kW        = models.DecimalField(max_digits=10,decimal_places=4,null=True,blank=True, verbose_name='Power Output (kW)')
    Freq_range      = models.CharField(max_length=20,blank=True, null=True,verbose_name='Frequency Range')
    Make            = models.CharField(max_length=20,blank=True, null=True,verbose_name='Make')
    Model           = models.CharField(max_length=20,blank=True, null=True,verbose_name='Model/Type')
    SN              = models.CharField(max_length=20,blank=True, null=True,verbose_name='Serial Number')
    E_Long_Deg_A    = models.DecimalField(max_digits=10,decimal_places=4,null=True,blank=True, verbose_name='Longitude Degree A')
    E_Long_Min_A    = models.DecimalField(max_digits=10,decimal_places=4,null=True,blank=True, verbose_name='Longitude Minute A')
    E_Long_Sec_A    = models.DecimalField(max_digits=10,decimal_places=4,null=True,blank=True, verbose_name='Longitude Second A')
    # to be continue...
        
    class Meta:
        #db_table    = u'FAS-FAN'
        verbose_name        = u'FAS-FAN'
        verbose_name_plural = u'FAS-FANs'
        ordering    = ['ReferenceNumber']

    def __unicode__(self):
        return self.ReferenceNumber
#ok!
class Carrier(models.Model):
    id              = models.AutoField(primary_key=True)
    companyname     = models.CharField(null=True, max_length=100, blank=True, verbose_name='Company Name')
    street          = models.CharField(null=True, max_length=150, blank=True, verbose_name='Street')
    address         = models.ForeignKey(PhilAddress, null=True, on_delete=models.SET_NULL)# max_digits=10, decimal_places=0, blank=True)
    contactperson   = models.CharField(null=True, max_length=50, blank=True, verbose_name='Contact Person')
    #modifiedby_id   = models.DecimalField(null=True, max_digits=10, decimal_places=0, blank=True)
    #datemodified    = models.DateField(auto_now=True, null=True, blank=True)    
    c_initial       = models.CharField(null=True, max_length=20, blank=True, verbose_name='Company Initial')

    def __unicode__(self):
        return self.companyname

    class Meta:
        verbose_name        = "Public Telecom Entity"
        verbose_name_plural = "Public Telecom Companies"
        ordering            = ['companyname']
    def address_city(self):
        return self.address.city
#ok!
class Sitename(models.Model):   # GPS related
    id              = models.AutoField(primary_key=True)
    site            = models.CharField(max_length=300, blank=True, null=True, verbose_name="Site")
    street          = models.CharField(max_length=150, blank=True, null=True, verbose_name="Street")
    address         = models.ForeignKey(PhilAddress, null=True, on_delete=models.SET_NULL)
    carrier         = models.ForeignKey(Carrier, null=True, on_delete=models.PROTECT)
    deg_long        = models.DecimalField(null=True, max_digits=3, decimal_places=0, blank=True)
    min_long        = models.DecimalField(null=True, max_digits=3, decimal_places=0, blank=True)
    sec_long        = models.DecimalField(null=True, max_digits=5, decimal_places=2, blank=True)
    longitude       = models.CharField(max_length=50, blank=True, null=True, verbose_name="Longitude")
    deg_lat         = models.DecimalField(null=True, max_digits=3, decimal_places=0, blank=True)
    min_lat         = models.DecimalField(null=True, max_digits=3, decimal_places=0, blank=True)
    sec_lat         = models.DecimalField(null=True, max_digits=5, decimal_places=2, blank=True)
    latitude        = models.CharField(max_length=50, blank=True, null=True, verbose_name="Latitude")


    class Meta:        
        verbose_name_plural = "Cell Site names"
        verbose_name        = "Site name"
        permissions=(
             ("engr_oview_sitename", "Engr can only view Sitename"),)

    def __unicode__(self):
        return self.site

    def save(self, *args, **kwargs):               
        self.longitude = str(self.deg_long) + '° - ' + str(self.min_long) + "' - " + str(self.sec_long) +'"'       
        self.latitude = str(self.deg_lat) + '° - ' + str(self.min_lat) + "' - "+ str(self.sec_lat)  +'"'      
        
        super(Sitename, self).save(*args, **kwargs) # Call the "real" save() method.
#ok!
class Official_Receipt(models.Model):
    carrier         = models.ForeignKey(Carrier, null=True, blank= True, on_delete=models.PROTECT)
    or_no           = models.DecimalField(primary_key=True, max_digits=15, verbose_name="Official Receipt", decimal_places=0)
    date_paid       = models.DateField(null=True, verbose_name="Date Paid", blank=True)
    amount          = models.DecimalField(null=True, verbose_name="Amount", max_digits=10, decimal_places=0, blank=True)
    validity_from   = models.DateField(null=False, verbose_name="Valid from", blank=True)
    validity_to     = models.DateField(null=False, verbose_name="Valid until", blank=True)
    remarks         = models.CharField(max_length=2000, blank=True, null=True, verbose_name="Remarks")    
    #dst             = models.CharField(max_length=20, blank=True, null=True, verbose_name="Documentary Stamp") # ???  

    class Meta:
        #db_table            = u'Official_Receipt' #name of table created in oracle sql developer not in django
        verbose_name        = "Official Receipt"
        verbose_name_plural = "Official Receipts"
        ordering            = ["or_no"]
    def __unicode__(self):
        return u'%s' % self.or_no 
#ok!
class SOA(models.Model):
    id              = models.AutoField(primary_key=True)
    soa_code        = models.CharField(max_length=20, blank=True, null=True, verbose_name='Statement of Account')
    #date_issued     = models.DateField(auto_now=True, blank=True, null=True)
    official_receipt= models.ForeignKey(Official_Receipt, null=True, blank=True, on_delete=models.SET_NULL)
    date_issued     = models.DateField(blank=True, null=True, default=datetime.now())
    carrier         = models.ForeignKey(Carrier, null=True, verbose_name ='Public Carrier', on_delete=models.PROTECT)
    service_type    = models.CharField(max_length=20, choices=SERVICE_TYPE, default='MICROWAVE', verbose_name='Service')  
    app_type        = models.ManyToManyField(App_type, verbose_name='Application Type')
    issued_by       = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='prepared_by', null=True, blank=True, on_delete=models.SET_NULL)
    approved_by     = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='approved_by', null=True, blank=True, on_delete=models.SET_NULL)
    no_years        = models.DecimalField(null=True, blank=True, decimal_places=0, max_digits=5, default=1, verbose_name='No. of Years')
    validity_from   = models.DateField(default=datetime.now(), null=True, blank=True, verbose_name='Validity from')
    validity_to     = models.DateField(default=lambda:datetime.now()+timedelta(days=365), blank=True, verbose_name='Validity to')    
    suf_fees        = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=15, default=0, verbose_name='SUFs')   
    filing_fee      = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=15, default=0, verbose_name='Filing fee')    
    purchase_fee    = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=15, default=0, verbose_name='Purchase fee')
    possess_fee     = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=15, default=0, verbose_name='Possess fee')
    cprsl_filing_fee= models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=15, default=0, verbose_name='Filing fee for CP/RSL')    
    const_fee       = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=15, default=0, verbose_name='Construction fee')    
    license_fee     = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=15, default=0, verbose_name='License fee')
    inspection_fee  = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=15, default=0, verbose_name='Inspection fee')
    mod_fee         = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=15, default=0, verbose_name='Modification fee')
    mod_filing_fee  = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=15, default=0, verbose_name='Filing fee for Modification')
    storage_fee     = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=15, default=0, verbose_name='Storage fee')
    rsl_dst_fee     = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=15, default=0, verbose_name='DST RSL')
    ppp_dst_fee     = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=15, default=0, verbose_name='DST PPP')
    sto_dst_fee     = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=15, default=0, verbose_name='DST Storage')   
    sur_lic         = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=15, default=0, verbose_name='Surcharge Lic')
    sur_suf         = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=10, default=0, verbose_name='Surcharge SUF')
    duplicate_fee   = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=10, default=0, verbose_name='Duplicate fee')
    channel         = models.DecimalField(null=True, blank=True, decimal_places=0, max_digits=10, default=0, verbose_name='No. of Channel')    
    ppp_units       = models.DecimalField(null=True, blank=True, decimal_places=0, max_digits=10, default=0, verbose_name='No. of PPP Units')
    rsl_units       = models.DecimalField(null=True, blank=True, decimal_places=0, max_digits=10, default=0, verbose_name='No. of RSL Units')
    mod_units       = models.DecimalField(null=True, blank=True, decimal_places=0, max_digits=10, default=0, verbose_name='No. of Mod Units')
    stor_units      = models.DecimalField(null=True, blank=True, decimal_places=0, max_digits=10, default=0, verbose_name='No. of Storage Units')
    demo_fee        = models.DecimalField(null=True, blank=True, decimal_places=0, max_digits=10, default=0, verbose_name='Demo fee')


    objects         = models.Manager() # default manager
    soa_objects     = SOA_counter() # custom manager
    
    class Meta:
        #db_table            = u'ccad_SOA'
        verbose_name_plural = "Statement of Accounts"
        verbose_name        = "Statement of Account"
        ordering            = ['-id']

    def __unicode__(self):
        return u'%s' % self.soa_code

class SOA_App_type(models.Model):
    soa         = models.ForeignKey(SOA, null=True, related_name='soas', on_delete=models.SET_NULL)
    app_type    = models.ForeignKey(App_type, null=True, related_name='apptypes', on_delete=models.SET_NULL)
    

    class Meta:
        db_table = u'soa_app_type'

    #@classmethod
    def _get_work_items(cls, self):        
        if self.app_type.trans_type == 'PPP':
            return self.ppp_units
        elif self.app_type.trans_type == 'CP':
            return self.conts_fee/360
        elif self.app_type.trans_type == 'RSL':
            return self.rsl_units
        elif self.app_type.trans_type == 'MOD':
            return self.mod_units
        elif self.app_type.trans_type == 'STO':
            return self.stor_units
        elif self.app_type.trans_type == 'DEMO':
            return self.ppp_units
        elif self.app_type.trans_type == 'TP':
            return self.rsl_units
        elif self.app_type.trans_type == 'DUP':
            return self.duplicate_fee/120
    wi          = property(_get_work_items)
#ok!
class SOA_detail(models.Model):
    id              = models.AutoField(primary_key=True)
    soa             = models.ForeignKey(SOA, related_name='Statement of Account', verbose_name='Statement of Account')
    site_no         = models.CharField(max_length=20, blank=True, null=True, verbose_name='Site No')                                            ######## added
    sitename        = models.CharField(max_length=100, verbose_name='Site Name')    
    site_addr       = models.CharField(null=True, blank=True, max_length=500, verbose_name='Site Address')
    city            = models.CharField(max_length=50, blank=True, null=True, verbose_name='City')                                               ######## added 
    band            = models.DecimalField(null=True, blank=True, decimal_places=0, max_digits=10, default=0, verbose_name='Band')               ######## added    
    call_sign       = models.CharField(null=True, blank=True, max_length=100, verbose_name='Call-Sign')   
    no_years        = models.DecimalField(null=True, blank=True, decimal_places=0, max_digits=10, default=0, verbose_name='No. of Years')    
    old_chan        = models.DecimalField(null=True, blank=True, decimal_places=0, max_digits=10, default=0, verbose_name='Old No. of Chan')    
    channel         = models.DecimalField(null=True, blank=True, decimal_places=0, max_digits=10, default=0, verbose_name='No. of Channel')    
    ppp_units       = models.DecimalField(null=True, blank=True, decimal_places=0, max_digits=10, default=0, verbose_name='No. of PPP Units')
    rsl_units       = models.DecimalField(null=True, blank=True, decimal_places=0, max_digits=10, default=0, verbose_name='No. of RSL Units')
    freq            = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=15, default=0, verbose_name='Freq')
    bw              = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=15, default=0, verbose_name='Bandwidth')
    suf_rate        = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=5, default=0, verbose_name='SUF rate') 
    suf_fee         = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=15, default=0, verbose_name='SUF')   
    filing_fee      = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=15, default=0, verbose_name='Filing fee')    
    no_ppp_ext      = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=15, default=0, verbose_name='No. of PPP Ext')    
    purchase_fee    = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=15, default=0, verbose_name='Purchase fee')
    possess_fee     = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=15, default=0, verbose_name='Possess fee')
    cprsl_filing_fee= models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=15, default=0, verbose_name='Filing fee for CP/RSL')    
    const_fee       = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=15, default=0, verbose_name='Construction fee')    
    license_fee     = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=15, default=0, verbose_name='License fee')
    inspection_fee  = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=15, default=0, verbose_name='Inspection fee')
    mod_units       = models.DecimalField(null=True, blank=True, decimal_places=0, max_digits=10, default=0, verbose_name='No. of Mod Units')
    mod_fee         = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=15, default=0, verbose_name='Modification fee')
    mod_filing_fee  = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=15, default=0, verbose_name='Filing fee for Modification')
    stor_units      = models.DecimalField(null=True, blank=True, decimal_places=0, max_digits=10, default=0, verbose_name='No. of Storage Units')
    storage_fee     = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=15, default=0, verbose_name='Storage fee')
    rsl_dst_fee     = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=15, default=0, verbose_name='DST RSL')
    ppp_dst_fee     = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=15, default=0, verbose_name='DST PPP')
    sto_dst_fee     = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=15, default=0, verbose_name='DST Storage')   
    sur_lic_percent = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=10, default=0, verbose_name='Surcharge Lic Percent')
    sur_lic         = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=15, default=0, verbose_name='Surcharge Lic')
    sur_suf_percent = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=10, default=0, verbose_name='Surcharge SUF Percent')
    sur_suf         = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=10, default=0, verbose_name='Surcharge SUF')
    duplicate_fee   = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=10, default=0, verbose_name='Duplicate fee')
    demo_fee        = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=10, default=0, verbose_name='Demo fee')

    class Meta:
        verbose_name_plural = "Statement of Account Details"
        verbose_name        = "Statement of Account Detail"

    def __unicode__(self):
        return self.sitename
#ok!
class Pending_desc(models.Model):
    id              = models.AutoField(primary_key=True)
    pend_description= models.CharField(max_length=100, verbose_name='Description', null=False, blank=False, help_text='Option to pend an application')

    class Meta:
        verbose_name_plural = "Pending Options"
        verbose_name        = "Pending Option"
        ordering            = ['pend_description']

    def __unicode__(self):
        return u'%s' % self.pend_description
#ok!
class Letter_LogBook(models.Model):
    id              = models.AutoField(primary_key=True)
    controlNo       = models.CharField(null=True, blank=True, max_length=30,verbose_name = 'Control No')
    dateEntry       = models.DateField(auto_now=True, null=True, verbose_name="Date Entry", blank=True) 
    letter_from     = models.CharField(max_length=150, blank=True, null=True, verbose_name='From', help_text='For non-Carrier Applications')
    letter_to       = models.CharField(max_length=150, blank=True, null=True, verbose_name='To', help_text='For non-Carrier Applications')
    subject         = models.CharField(max_length=250, blank=True, null=True, verbose_name='Subject', help_text='For non-Carrier Applications')
    actiontaken    = models.CharField(max_length=2000, blank=True, null=True, verbose_name='Action taken')

    objects         = models.Manager() # default manager
    logbook_objects = LogBook_counter() # custom manager
    
    class Meta:
        verbose_name_plural = "Logbook for Letters"
        verbose_name        = "Logbook aside from application"

    def __unicode__(self):
        return u'%s' % self.subject     
#ok!
class LogBook_Remarks(models.Model):
    Remarks         = models.CharField(null=True, blank=True, max_length=200,verbose_name = 'Remarks')
    dateEntry       = models.DateField(auto_now=True, null=True, verbose_name="Date Entry", blank=True)
    written_by      = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='writteb_by', null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name_plural = "Logbook Remarks"
        verbose_name        = "Logbook Remark"

    def __unicode__(self):
        return u'%s' % self.subject     
#ok!
class no_work(models.Model):
    NO_WORK_TYPE    = (
        (1, 'WHOLE DAY'),
        (0.5, 'HALF DAY'),
        )
    nowork_day      = models.DateField(verbose_name='Day', unique=True)
    tframe          = models.DecimalField(max_digits=3, decimal_places=1, choices=NO_WORK_TYPE)
    description     = models.CharField(max_length=150, blank=True, null=True)

    class Meta:
         verbose_name        = "Holidays or No work"
#ok!
def validate_theday(value):
    qry = no_work.objects.filter(Q(nowork_day__month=value.month) & Q(nowork_day__day=value.day))
    if qry.exists():
        raise ValidationError(u'The date you specified is a holiday.')
    if value.isoweekday() == 6 or value.isoweekday() == 7:
        raise ValidationError(u'The date you specified is a weekend.')
#ok!
class LogBook(models.Model):
    id              = models.AutoField(primary_key=True)        
    dateEntry       = models.DateField(auto_now=True, verbose_name="Date Entry", null=True, blank=True)
    acceptancedate  = models.DateField(default=datetime.now(), verbose_name="Date of Acceptance", null=True, blank=True, help_text="Date should not fall in holidays or weekend.", validators=[validate_theday])
    controlNo       = models.CharField(null=True, blank=True, max_length=30,verbose_name = 'Control No', help_text="Auto fill-up")
    carrier         = models.ForeignKey(Carrier, null=True, verbose_name ='Public Carrier', on_delete=models.PROTECT)  
    transtype       = models.CharField(max_length=100, default='NEW', verbose_name='Application Type')
    service         = models.CharField(max_length=20, null=True, blank=True, choices=SERVICE_TYPE, verbose_name = 'Service Applied')    
    units           = models.DecimalField(max_digits=10, decimal_places=0, null=True, blank=True, verbose_name='Unit(s)', default=0)
    noofstation     = models.DecimalField(max_digits=10, decimal_places=0, null=True, blank=True, verbose_name='No. of Station(s)', default=0)
    first_stn       = models.CharField(null=True, blank=True, max_length=100,verbose_name = 'First Station')
    last_stn        = models.CharField(null=True, blank=True, max_length=100,verbose_name = 'Last Station')    
    soa             = models.ManyToManyField(SOA, null=True, blank=True, through='Statements')
    current_user    = models.ForeignKey(settings.AUTH_USER_MODEL,  limit_choices_to={'groups__name': "Regulation Branch Personnel"}, null=True, blank=True, related_name='current_user', verbose_name='Assign to', on_delete=models.SET_NULL)
    permitNo        = models.CharField(null=True, blank=True, max_length=30, verbose_name ='Permit No')
    logbook_remarks = models.CharField(null=True, blank=True, max_length=2000, verbose_name ='Remarks')
    #docfile         = models.FileField(upload_to='attachments/%Y/%B', help_text ='max 2.5 megabytes', null=True, blank=True, verbose_name='PPP File')
    status          = models.CharField(max_length=40, choices=STATUS_TYPE, default=u'CHECKING REQUIREMENTS', verbose_name='Status', help_text='Auto fill-up')
    encoder_status  = models.DecimalField(null=True, max_digits=3, default=2, decimal_places=2, blank=True, verbose_name='Encoder Status')
    engr_status     = models.DecimalField(null=True, max_digits=3, default=0.1, decimal_places=2, blank=True, verbose_name='Engr Status')
    chief_status    = models.DecimalField(null=True, max_digits=3, default=2, decimal_places=2, blank=True, verbose_name='Chief Status')
    due_date        = models.DateTimeField(default=lambda:datetime.now()+timedelta(days=3), blank=True)
    ischecked       = models.BooleanField(default=0)    
    fas_data        = models.ForeignKey(FAS_Data, null=True, blank=True, on_delete=models.SET_NULL)     
    engrchoice      = models.CharField(choices=ENGR_CHOICES, max_length=12, null=True, blank=True)    
    pend_at         = models.DecimalField(null=True, blank=True, max_digits=3, decimal_places=0)    
    endorsementfile = models.FileField(upload_to='endorsement/%Y/%B', help_text ='max 2.5 megabytes', null=True, blank=True, verbose_name='Endorsement Letter')    
    pending_desc    = models.ForeignKey(Pending_desc, null=True, blank=True, on_delete=models.SET_NULL)
    stm_count       = models.DecimalField(null=True, blank=True, max_digits=3, decimal_places=0)  

    objects         = models.Manager() # default manager
    logbook_objects = LogBook_counter() # custom manager
    
    class Meta:
        #db_table            = u'Official_Receipt' #name of table created in oracle sql developer not in django
        verbose_name        = "Log Book"
        verbose_name_plural = "Log Entries" 
        ordering            = ["-id"]
        permissions=(
             ("rb_view_logbook", "RB can view Logbook"),
             ("sec_view_logbook", "Secretary can view Logbook"),
             ("encoder_view_logbook", "Encoder can view Logbook"),
             ("engr_view_logbook", "Engr can view Logbook"),
        )

    def __unicode__(self):
        return self.controlNo          
#ok!
class LogBook_audit(models.Model):
    id             = models.AutoField(primary_key=True)
    logbook        = models.ForeignKey(LogBook, verbose_name='Logbook Control No.', null=True)
    username       = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True,  verbose_name='Username', on_delete=models.SET_NULL)
    status         = models.CharField(null=False, blank=False, max_length=40, choices=STATUS_TYPE, default=u'CHECKING REQUIREMENTS', verbose_name='Status')
    log_in         = models.DateTimeField(default=lambda:datetime.now(), verbose_name='Work start')
    log_out        = models.DateTimeField(null=True, blank=True, verbose_name='Work done')
    period_day     = models.DecimalField(null=True, blank=True, max_digits=10, decimal_places=0, verbose_name='Day length')
    period_hour    = models.DecimalField(null=True, blank=True, max_digits=3, decimal_places=0, verbose_name='Hour length')
    period_minute  = models.DecimalField(null=True, blank=True, max_digits=3, decimal_places=0, verbose_name='Minute length')
    is_ontime      = models.NullBooleanField(default=False, null=True, blank=True,)

    class Meta:
        verbose_name        = "Logbook Audit"
        verbose_name_plural = "Logbook Audits"
        ordering            = ["logbook", "id"]

    def __unicode__(self):
        return u'%s-%s' % (self.logbook, self.status)   
#ok!
class PPPfiles(models.Model):
    id              = models.AutoField(primary_key=True)
    logbook         = models.ForeignKey(LogBook, null=True, on_delete=models.SET_NULL)
    user            = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)
    docfile         = models.FileField(upload_to='attachments/%Y/%m/%d', help_text ='max 2.5 megabytes', null=True, blank=True, verbose_name='PPP File') #label='Select a file',        

    class Meta:
        #db_table            = u'Official_Receipt' #name of table created in oracle sql developer not in django
        verbose_name        = "Permit"
        verbose_name_plural = "Permit Files"
        ordering            = ["logbook"]

    def __unicode__(self):
        return u'%s' % (self.logbook)
# New Equip Table to be implemented
def get_sentinel_equipmodel():
    return EquipModel.objects.get(make='NO MODEL')
#ok!
class Equipment(models.Model):
    id              = models.AutoField(primary_key=True)  
    #logbook         = models.ForeignKey(LogBook, null=True, blank= True, on_delete=models.SET_NULL)
    logbook         = models.ManyToManyField(LogBook, null=True, blank=True, through='EquipRack')
    carrier         = models.ForeignKey(Carrier, null=True, on_delete=models.PROTECT)
    makemodel       = models.ForeignKey(EquipModel, null=True, blank= True, on_delete=models.SET(get_sentinel_equipmodel))
    antenna         = models.ForeignKey(Antenna, null=True, on_delete=models.SET_NULL)
    sitename        = models.ForeignKey(Sitename, null=True, blank= True, on_delete=models.SET_NULL)
    freqrange_low   = models.DecimalField(max_digits=20,  decimal_places=0, null=True, blank= True)
    freqrange_high  = models.DecimalField(max_digits=20,  decimal_places=0, null=True, blank= True)
    freqrange_low2  = models.DecimalField(max_digits=20,  decimal_places=0, null=True, blank= True)
    freqrange_high2 = models.DecimalField(max_digits=20,  decimal_places=0, null=True, blank= True)
    callsign        = models.CharField(max_length=100, blank=True, null=True, verbose_name="Call-Sign")    
    usages          = models.CharField(max_length=40, choices=USAGE_TYPE, default=u'MAIN', verbose_name='Equipment Usage')    
    serialno        = models.CharField(max_length=100, blank=True, null=True, verbose_name="Serial No")    
    polarity        = models.CharField(max_length=20, blank=True, null=True)    
    tx_min          = models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    tx              = models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)    
    tx_max          = models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx_min          = models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)    
    rx              = models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)    
    rx_max          = models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)    
    bwe             = models.CharField(max_length=50, blank=True, null=True, verbose_name="Bandwidth")
    power           = models.DecimalField(max_digits=10,  decimal_places=0, blank=True, null=True, verbose_name="Power" )
    unit            = models.CharField(max_length=40, choices=POWER_UNIT, default=u'dBm', verbose_name='Unit')   
    p_purchase      = models.CharField(max_length=50, blank=True, null=True, verbose_name='Purchase')
    p_possess       = models.CharField(max_length=50, blank=True, null=True, verbose_name='Possess')
    p_storage       = models.CharField(max_length=50, blank=True, null=True, verbose_name='Storage')    
    status          = models.CharField(max_length=20, choices=EQUIP_STATUS, default='New', verbose_name='Status')

    class Meta:
        #db_table = "Equipment"
        #ordering = ["-date_modified"]
        permissions=(
             ("rb_oview_equipment", "RB can only view Equipment"),
             ("sec_oview_equipment", "Secretary can only view Equipment"),
             ("encoder_oview_equipment", "Encoder can only view Equipment"),
             ("engr_oview_equipment", "Engr can only view Equipment"),
        )

    def __unicode__(self):
        return u'%s-%s' % (self.makemodel.make, self.serialno)

    def equip_freqrange(self):  
        if self.freqrange_low2:      
            return u'%s-%s / %s-%s' % (self.freqrange_low, self.freqrange_high, self.freqrange_low2, self.freqrange_high2)
        else:
            return u'%s-%s' % (self.freqrange_low, self.freqrange_high)
    equip_freqrange.short_description = 'Freq Range'

    def equip_txrx(self):
        if self.tx:
            return u'%s-%s' %(self.tx, self.rx)
        else:
            return u'%s-%s/%s-%s' %(self.tx_min, self.tx_max, self.rx_min, self.rx_max)            
    equip_txrx.short_description = 'Transmit/Received'        

    def equip_powerbwe(self):        
        return u'%s %s / %s' %(self.power, self.unit, self.bwe)            
    equip_powerbwe.short_description = 'Power / BWE'      

    def equip_usagepolarity(self):      
        return u'%s - %s' %(self.usages, self.polarity)
    equip_usagepolarity.short_description = 'Usage/Polarity'



    #def save(self, *args, **kwargs):
    #    print 'sitename: ', self.sitename.id
        #if self.sitename:
        ##    curr_site = Sitename.objects.get(pk=self.sitename.id)
        #   self.sitename = curr_site

class EquipRack(models.Model):
    logbook             = models.ForeignKey(LogBook)#, on_delete=models.SET_NULL)
    equipment           = models.ForeignKey(Equipment)#, on_delete=models.SET_NULL)

    class Meta:        
        verbose_name_plural = "Equipment Racks"
        verbose_name        = "Equipment Rack"

    def equip_makemodel(self):        
        return self.equipment.makemodel
    equip_makemodel.short_description = 'Make/Model'

    def equip_freqrange_low(self):        
        return self.equipment.freqrange_low
    equip_freqrange_low.short_description = 'Freq Range Low'

    def equip_freqrange_high(self):        
        return self.equipment.freqrange_high
    equip_freqrange_high.short_description = 'Freq Range High'

    def equip_power(self):        
        return self.equipment.power
    equip_power.short_description = 'Power'

    def equip_bwe(self):        
        return self.equipment.bwe
    equip_bwe.short_description = 'BWE'

    def equip_sn(self):        
        return self.equipment.serialno
    equip_sn.short_description = 'Serial No'

    def equip_sitename(self):        
        return self.equipment.sitename
    equip_sitename.short_description = 'Sitename'

    def save(self, *args, **kwargs):        
    ## self.units
        equipment  = Equipment.objects.filter(pk=self.equipment.id)      
        logbook    = LogBook.objects.get(pk=self.logbook.id)
        #print 'Enter Save in Equipment Rack'
        for rec in equipment:
            #print 'testing1:', rec.id
            #print 'testing2: %s-%s' % (rec.makemodel_id, rec.serialno)
            logbook.save()                                   
        super(EquipRack, self).save(*args, **kwargs) # Call the "real" save() method.
#ok!
class LatestRsl_v2(models.Model):
    id                  = models.AutoField(primary_key=True)
    logbook             = models.ForeignKey(LogBook, null=True, blank= True, on_delete=models.SET_NULL)
    official_receipt    = models.ManyToManyField(Official_Receipt, through='LatestRsl_v2_Official')  #manytomany
    carrier             = models.ForeignKey(Carrier, null=True, blank= True, verbose_name ='Public Carrier', on_delete=models.PROTECT)        
    sitename            = models.ForeignKey(Sitename,  null=True, blank= True, on_delete=models.SET_NULL)
    equipment           = models.ManyToManyField(Equipment, through='LatestRsl_v2_Equipment')        #manytomany                
    rslno               = models.CharField(max_length=50, blank=True, null=True, verbose_name="License No") ## auto number
    issued              = models.DateField(null=True, verbose_name="Date Issued", blank=True) ## auto date    
    form_serial         = models.DecimalField(null=True, verbose_name="Form Serial#", max_digits=10, decimal_places=0, blank=True)    # auto place   
    status              = models.CharField(max_length=40, choices=SIMPLIFIED_TRANSACTION_TYPE, default=u'NEW', verbose_name='Status')        
    class_of_station    = models.ForeignKey(Classofstation, null=True, blank= True, verbose_name="Class of Station", on_delete=models.SET_NULL)
    nature_of_service   = models.CharField(max_length=20, blank=True, null=True, default=u'CP', verbose_name="Nature of Service")        
    ptsvc               = models.CharField(max_length=300, blank=True, null=True, verbose_name="Point of Service") ## auto place
    remarks             = models.CharField(max_length=2000, blank=True, null=True, verbose_name="Remarks")    
    signatory           = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='rsl_approved_by', null=True, blank= True, verbose_name="Signed by Director", on_delete=models.SET_NULL)    ## auto place    
    evaluator           = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='rsl_evaluated_by', null=True, blank= True, verbose_name="Evaluator" , on_delete=models.SET_NULL)    ## auto place
    encoder             = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='rsl_encoded_by', null=True, blank= True, verbose_name="Encoder", on_delete=models.SET_NULL)    ## auto place
    capacity            = models.CharField(max_length=100, blank=True, null=True, verbose_name="Capacity")
   
    class Meta:
        #db_table            = u'latest_rsl'
        verbose_name_plural = "Latest Radio Station Licenses"
        verbose_name        = "Radio Station License"
        ordering            = ["issued"]
        permissions=(
             ("rb_oview_rsl", "RB can only view RSL"),
             ("sec_oview_rsl", "Secretary can only view RSL"),
             ("encoder_oview_rsl", "Encoder can only view RSL"),
             ("engr_oview_rsl", "Engr can only view RSL"),
        )

    def __unicode__(self):
        return self.rslno
    ''' to display foreign fields'''
    
    def lic_to_operate(self):
        return self.class_of_station.description
    lic_to_operate.short_description = 'License to Operate'
    def sitename_street(self): 
        if self.sitename:       
            if self.sitename.street or self.sitename.street is not None:              
                return self.sitename.street
            else:
                return ' '
    sitename_street.short_description = 'Street'
    def sitename_city(self):
        return self.sitename.address.city
    sitename_city.short_description = 'City'
    def sitename_province(self):
        pass      
        #return self.sitename.address.province 
    sitename_province.short_description = 'Province'
    def sitename_region(self):
        return self.sitename.address.region
    sitename_region.short_description = 'Region'

    def equip_callsign(self):
        if self.equipment:
            if self.equipment.callsign or self.equipment.callsign is not None:
                return self.equipment.callsign
            else:
                return ' '
    equip_callsign.short_description = 'Call-Sign'
    def equip_serialno(self):
        return self.equipment.serialno
    equip_serialno.short_description = 'Serial No'

    def sitename_longitude(self):
        return self.sitename.longitude
    sitename_longitude.short_description = 'Longitude'

    def sitename_latitude(self):
        return self.sitename.latitude
    sitename_latitude.short_description = 'Latitude'

class LatestRsl_v2_Official(models.Model): # Payments
    latestrsl_v2        = models.ForeignKey(LatestRsl_v2, null=True)
    official_receipt    = models.ForeignKey(Official_Receipt, null=True)

    class Meta:
        db_table            = u'ccad_latestrsl_v2_official4594'
        verbose_name_plural = "Related Official Receipts"
        verbose_name        = "Official Receipt for RSL"

class Statements(models.Model):
    logbook             = models.ForeignKey(LogBook, null=True)#, on_delete=models.SET_NULL)
    soa                 = models.ForeignKey(SOA, null=True)#, on_delete=models.SET_NULL)

    class Meta:        
        verbose_name_plural = "Payments"
        verbose_name        = "Payment"

    def save(self, *args, **kwargs): 
        ## self.units 
        logbook = LogBook.objects.get(pk=self.logbook.id)
        soa  = SOA.objects.filter(pk=self.soa.id)              
        print 'Enter Save in Statements'
        for rec in soa:
            #print 'testing1:', rec.id
            #print 'testing2:', rec.rsl_units 
            check_if_mod = SOA_App_type.objects.select_related().filter(soa=rec.id, app_type=5).count()
            #print 'check_if_mod :', check_if_mod
            ## app type RECALL OK!
            if rec.rsl_units == 0 and rec.ppp_units == 0 and rec.stor_units > 0:
                logbook.units = rec.stor_units
                print 'elif RECALL/STORAGE =0=0>0:', logbook.units
            ## no units
            elif rec.rsl_units == 0 and rec.ppp_units == 0 and rec.stor_units == 0 and rec.channel == 0:
                logbook.units = 0
                print 'elif no units =0=0=0=0:', logbook.units 
            ## app type PPP OK!
            elif rec.rsl_units == 0 and rec.ppp_units > 0 and rec.stor_units == 0 and rec.suf_fees == 0:                
                logbook.units = rec.ppp_units
                print 'elif PPP :=0>0=0', logbook.units 
            ## type NEW PPP
            elif rec.channel > 0 and rec.rsl_units == 0 and rec.ppp_units >0:# and rec.ppp_units == 0 and rec.stor_units == 0:
                logbook.units = rec.ppp_units
                print 'rec.channel > 0 and rec.rsl_units == 0 and rec.ppp_units >0=0>0:', rec.ppp_units
            ## app type RSL
            elif rec.rsl_units > 0 and rec.channel == 0:# and rec.ppp_units == 0 and rec.stor_units == 0:
                logbook.units = rec.rsl_units
                print 'rec.rsl_units > 0=0:', rec.rsl_units
            ## ?
            elif rec.channel > 0 and rec.rsl_units == 0:# and rec.ppp_units == 0 and rec.stor_units == 0:
                logbook.units = rec.channel#rec.rsl_units
                print 'rec.channel > 0=0:', rec.channel
            ## either channel or rsl_units is present
            elif rec.channel > 0 and rec.rsl_units > 0:# and rec.ppp_units == 0 and rec.stor_units == 0:
                logbook.units = rec.channel
                print 'either channel or rsl_units is present > 0>0:', rec.channel
                      
            ## app type MOD : combination of RSL, PPP and STORAGE OK!
            elif  check_if_mod > 0:
                logbook.units = rec.stor_units + rec.ppp_units
                print 'elif check_if_mod:', logbook.units                       
            ## self.noofstation
            try:
                station_list = SOA_detail.objects.filter(soa=rec.id)        
                no_stations = station_list.count()
                #print 'station_list.first(sitename) : ',  station_list.first()
                #print 'station_list.last(sitename) : ',  station_list.last()
                stn_first = station_list.first()
                stn_last = station_list.last()
                #print 'stn_first.sitename :', stn_first.sitename[:29]
                logbook.first_stn =  stn_first.sitename[:29]
                logbook.last_stn = stn_last.sitename[:29]
                if no_stations:
                    logbook.noofstation =no_stations
                else:
                    logbook.noofstation = 0
            except:
                # return default value
                logbook.first_stn =  ''
                logbook.last_stn = ''
                logbook.noofstation = 0
            ## self.service        
            logbook.service = rec.service_type
            ## self.transtype
            soa_app_list = SOA_App_type.objects.select_related().filter(soa=rec.id)
            #print 'soa_app_list :', soa_app_list
            app_type_names = ''

            for soap in soa_app_list:
                #print 'inside for loop - soap.app_type.trans_type is :', soap.app_type.trans_type
                #print 'app_type_names.rfind(ALL) :' , app_type_names.rfind('ALL')
                #print 'app_type_names.rfind(PPP) :' , app_type_names.rfind('PPP')
                #print 'app_type_names.rfind(RECALL) :' , app_type_names.rfind('RECALL')
                ## limit app type name 
                if app_type_names:
                    ## if ALL is found
                    if soap.app_type.trans_type == 'ALL':
                        app_type_names = soap.app_type.trans_type
                    ## if no ALL
                    elif soap.app_type.trans_type != 'ALL' and app_type_names.rfind('ALL') == -1:
                        #print 'if mod is found no need to place ppp, sto or recall'
                        
                        if app_type_names.rfind('MOD') >= 0 and (soap.app_type.trans_type == 'STO' \
                            or soap.app_type.trans_type == 'RECALL' or soap.app_type.trans_type == 'PPP'):
                            # Do nothing
                            pass
                            #print 'Not inserting STO, PPP, RECALL once MOD is found'
                        elif soap.app_type.trans_type == 'MOD' and (app_type_names.rfind('PPP') >= 0 or app_type_names.rfind('STO') >= 0 or app_type_names.rfind('RECALL') >= 0):
                            app_type_names = app_type_names.replace('PPP','').replace('STO','').replace('RECALL','') +' / '+ soap.app_type.trans_type                    
                            #print 'app_type_names if mod/ppp: ', app_type_names
                        else:
                            app_type_names = soap.app_type.trans_type+' / '+app_type_names
                            #print 'app_type_names with in else: ', app_type_names
                else:
                    app_type_names = soap.app_type.trans_type
                    #print 'app_type_names outside else: ', app_type_names
            
            #print 'original app type name: ', app_type_names
            clean_app_type_name = app_type_names.replace('/  /','/').replace('//','/')
            if len(clean_app_type_name) >= 17:
                logbook.transtype = 'ALL'
            else:
                logbook.transtype = clean_app_type_name
            ## add app type in control No.
            logbook.controlNo = logbook.controlNo[:13]+logbook.transtype
            
            logbook.save()
        super(Statements, self).save(*args, **kwargs) # Call the "real" save() method.

    def delete(self, *args, **kwargs):
        #print 'return default value'
        self.logbook.units = 0
        self.logbook.service = ''
        self.logbook.transtype = ''
        self.logbook.first_stn =  ''
        self.logbook.last_stn = ''
        self.logbook.noofstation = 0
        self.logbook.controlNo = self.logbook.controlNo[:13]             
        self.logbook.save()
        #print 'Setting to default value'
        super(Statements, self).delete(*args, **kwargs)
#ok!
class LatestRsl_v2_Equipment(models.Model):
    latestrsl_v2 = models.ForeignKey(LatestRsl_v2, null=True)#, on_delete=models.SET_NULL)
    equipment    = models.ForeignKey(Equipment, null=True)#, on_delete=models.SET_NULL)

    def equip_freqrange(self):        
        return u'%s-%s' % (self.equipment.freqrange_low, self.equipment.freqrange_high)
    equip_freqrange.short_description = 'Freq Range'

    def equip_txrx(self):
        if self.tx:
            return u'%s-%s' %(self.equipment.tx, self.equipment.rx)
        else:
            return u'%s-%s/%s-%s' %(self.equipment.tx_min, self.equipment.tx_max, self.equipment.rx_min, self.equipment.rx_max)            
    equip_txrx.short_description = 'Transmit/Received'        

    def equip_powerbwe(self):        
        return u'%s %s / %s' %(self.equipment.power, self.equipment.unit, self.equipment.bwe,)            
    equip_powerbwe.short_description = 'Power / BWE'      

    def equip_purchase(self):        
        return self.equipment.purchase
    equip_purchase.short_description = 'Purchase'  

    def equip_possess(self):        
        return self.equipment.possess
    equip_possess.short_description = 'Possess'  

    def equip_storage(self):        
        return self.equipment.storage
    equip_purchase.short_description = 'Storage'  

    def equip_callsign(self):        
        return self.equipment.callsign
    equip_purchase.short_description = 'Call-Sign'

    def equip_usagepolarity(self):      
        return u'%s - %s' %(self.equipment.usage, self.equipment.polarity)
    equip_usagepolarity.short_description = 'Usage/Polarity'  

    def ant_details(self):
        return u'%s : %s-%s-%s' % (self.equipment.antenna.antenna_type, self.equipment.antenna.directivity, self.equipment.antenna.gain, self.equipment.antenna.height)    

    class Meta: 
        db_table            = u'ccad_latestrsl_v2_equipment'     
        verbose_name_plural = "Related Equipmentsss"
        verbose_name        = "Equipment for RSL"

class KPI(models.Model):
    current_year = models.IntegerField(null=False, blank=False,  default=datetime.now().year, unique=True)
    target       = models.IntegerField(null=False, blank=False)

    class Meta:   
        verbose_name_plural = "Key Performance Indicators"
        verbose_name        = "KPI"

class Suggestion_box(models.Model):
    id             = models.AutoField(primary_key=True)    
    username       = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True,  verbose_name='Username', on_delete=models.SET_NULL)
    title          = models.CharField(max_length=150, blank=True, null=True, verbose_name="Title")    
    remark         = models.CharField(max_length=2000, blank=True, null=True, verbose_name="Remarks")    
    
    class Meta:
        verbose_name        = "Suggestion"
        verbose_name_plural = "Suggestions"
        ordering            = ["id"]

    def __unicode__(self):
        return self.title

class DocFormats(models.Model):
    id              = models.AutoField(primary_key=True)    
    title           = models.CharField(max_length=150, blank=True, null=True, verbose_name="Title")    
    username        = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)
    docfile         = models.FileField(upload_to='formats/%Y/%m/%d', help_text ='max 2.5 megabytes', null=True, blank=True, verbose_name='Format File')

    class Meta:
        #db_table            = u'Official_Receipt' #name of table created in oracle sql developer not in django
        verbose_name        = "Document Format"
        verbose_name_plural = "Document Format"
        ordering            = ["id"]

    def __unicode__(self):
        return self.title
#ok!
class MasterRsl(models.Model):
    id              = models.AutoField(primary_key=True)     
    status          = models.CharField(max_length=20, choices=STATUS_CHOICES, blank=True, null=True, verbose_name="Status")
    rslno           = models.CharField(max_length=50, blank=True, null=True, verbose_name="License No")
    issued          = models.DateField(null=True, verbose_name="Date Issued", blank=True)
    carrier         = models.CharField(max_length=150, blank=True, null=True, verbose_name="Carrier")
    site            = models.CharField(max_length=300, blank=True, null=True, verbose_name="Site")
    street          = models.CharField(max_length=150, blank=True, null=True, verbose_name="Street")
    city            = models.CharField(max_length=150, blank=True, null=True, verbose_name="Town/City")
    province        = models.CharField(max_length=150, blank=True, null=True, verbose_name="Province")
    region          = models.CharField(max_length=50, blank=True, null=True, verbose_name="Region")
    deg_long        = models.DecimalField(null=True, max_digits=10, decimal_places=0, blank=True)
    min_long        = models.DecimalField(null=True, max_digits=10, decimal_places=0, blank=True)
    sec_long        = models.DecimalField(null=True, max_digits=10, decimal_places=0, blank=True)
    longitude       = models.CharField(max_length=50, blank=True, null=True, verbose_name="Longitude")
    deg_lat         = models.DecimalField(null=True, max_digits=10, decimal_places=0, blank=True)
    min_lat         = models.DecimalField(null=True, max_digits=10, decimal_places=0, blank=True)
    sec_lat         = models.DecimalField(null=True, max_digits=10, decimal_places=0, blank=True)
    latitude        = models.CharField(max_length=50, blank=True, null=True, verbose_name="Latitude")
    lic_to_operate  = models.CharField(max_length=50, blank=True, null=True, verbose_name="License to Operate")
    class_of_station = models.CharField(max_length=20, blank=True, null=True, verbose_name="Class of Station")
    nature_of_service = models.CharField(max_length=20, blank=True, null=True, verbose_name="Nature of Service")
    callsign        = models.CharField(max_length=100, blank=True, null=True, verbose_name="Call-Sign")
    ptsvc           = models.CharField(max_length=500, blank=True, null=True, verbose_name="Point of Service")
    ptsvc_callsign  = models.CharField(max_length=150, blank=True, null=True)
    tx1             = models.CharField(max_length=50, blank=True, null=True)
    tx2             = models.CharField(max_length=50, blank=True, null=True)
    tx3             = models.CharField(max_length=50, blank=True, null=True)
    tx4             = models.CharField(max_length=50, blank=True, null=True)
    tx5             = models.CharField(max_length=50, blank=True, null=True)
    tx6             = models.CharField(max_length=50, blank=True, null=True)
    tx7             = models.CharField(max_length=50, blank=True, null=True)
    tx8             = models.CharField(max_length=50, blank=True, null=True)
    tx9             = models.CharField(max_length=50, blank=True, null=True)
    tx10            = models.CharField(max_length=50, blank=True, null=True)
    tx11            = models.CharField(max_length=50, blank=True, null=True)
    tx12            = models.CharField(max_length=50, blank=True, null=True)
    rx1             = models.CharField(max_length=50, blank=True, null=True)
    rx2             = models.CharField(max_length=50, blank=True, null=True)
    rx3             = models.CharField(max_length=50, blank=True, null=True)
    rx4             = models.CharField(max_length=50, blank=True, null=True)
    rx5             = models.CharField(max_length=50, blank=True, null=True)
    rx6             = models.CharField(max_length=50, blank=True, null=True)
    rx7             = models.CharField(max_length=50, blank=True, null=True)
    rx8             = models.CharField(max_length=50, blank=True, null=True)
    rx9             = models.CharField(max_length=50, blank=True, null=True)
    rx10            = models.CharField(max_length=50, blank=True, null=True)
    rx11            = models.CharField(max_length=50, blank=True, null=True)
    rx12            = models.CharField(max_length=50, blank=True, null=True)
    tx1_min             = models.CharField(max_length=50, blank=True, null=True)
    tx2_min             = models.CharField(max_length=50, blank=True, null=True)
    tx3_min             = models.CharField(max_length=50, blank=True, null=True)
    tx4_min             = models.CharField(max_length=50, blank=True, null=True)
    tx5_min             = models.CharField(max_length=50, blank=True, null=True)
    tx6_min             = models.CharField(max_length=50, blank=True, null=True)
    tx7_min             = models.CharField(max_length=50, blank=True, null=True)
    tx8_min             = models.CharField(max_length=50, blank=True, null=True)
    tx9_min             = models.CharField(max_length=50, blank=True, null=True)
    tx10_min            = models.CharField(max_length=50, blank=True, null=True)
    tx11_min            = models.CharField(max_length=50, blank=True, null=True)
    tx12_min            = models.CharField(max_length=50, blank=True, null=True)
    rx1_min             = models.CharField(max_length=50, blank=True, null=True)
    rx2_min             = models.CharField(max_length=50, blank=True, null=True)
    rx3_min             = models.CharField(max_length=50, blank=True, null=True)
    rx4_min             = models.CharField(max_length=50, blank=True, null=True)
    rx5_min             = models.CharField(max_length=50, blank=True, null=True)
    rx6_min             = models.CharField(max_length=50, blank=True, null=True)
    rx7_min             = models.CharField(max_length=50, blank=True, null=True)
    rx8_min             = models.CharField(max_length=50, blank=True, null=True)
    rx9_min             = models.CharField(max_length=50, blank=True, null=True)
    rx10_min            = models.CharField(max_length=50, blank=True, null=True)
    rx11_min            = models.CharField(max_length=50, blank=True, null=True)
    rx12_min            = models.CharField(max_length=50, blank=True, null=True)
    tx1_max             = models.CharField(max_length=50, blank=True, null=True)
    tx2_max             = models.CharField(max_length=50, blank=True, null=True)
    tx3_max             = models.CharField(max_length=50, blank=True, null=True)
    tx4_max             = models.CharField(max_length=50, blank=True, null=True)
    tx5_max             = models.CharField(max_length=50, blank=True, null=True)
    tx6_max             = models.CharField(max_length=50, blank=True, null=True)
    tx7_max             = models.CharField(max_length=50, blank=True, null=True)
    tx8_max             = models.CharField(max_length=50, blank=True, null=True)
    tx9_max             = models.CharField(max_length=50, blank=True, null=True)
    tx10_max            = models.CharField(max_length=50, blank=True, null=True)
    tx11_max            = models.CharField(max_length=50, blank=True, null=True)
    tx12_max            = models.CharField(max_length=50, blank=True, null=True)
    rx1_max             = models.CharField(max_length=50, blank=True, null=True)
    rx2_max             = models.CharField(max_length=50, blank=True, null=True)
    rx3_max             = models.CharField(max_length=50, blank=True, null=True)
    rx4_max             = models.CharField(max_length=50, blank=True, null=True)
    rx5_max             = models.CharField(max_length=50, blank=True, null=True)
    rx6_max             = models.CharField(max_length=50, blank=True, null=True)
    rx7_max             = models.CharField(max_length=50, blank=True, null=True)
    rx8_max             = models.CharField(max_length=50, blank=True, null=True)
    rx9_max             = models.CharField(max_length=50, blank=True, null=True)
    rx10_max            = models.CharField(max_length=50, blank=True, null=True)
    rx11_max            = models.CharField(max_length=50, blank=True, null=True)
    rx12_max            = models.CharField(max_length=50, blank=True, null=True)
    bwe_1           = models.CharField(max_length=50, blank=True, null=True, verbose_name="Bandwidth")
    no              = models.CharField(max_length=50, blank=True, null=True)
    unit            = models.CharField(max_length=10, blank=True, null=True)
    power           = models.CharField(max_length=100, blank=True, null=True, verbose_name="Power")
    a1std           = models.CharField(max_length=10, blank=True, null=True)
    a2ndd           = models.CharField(max_length=10, blank=True, null=True)
    a3rdd           = models.CharField(max_length=10, blank=True, null=True)
    a4th            = models.CharField(max_length=10, blank=True, null=True)
    a5th            = models.CharField(max_length=10, blank=True, null=True)
    a6th            = models.CharField(max_length=10, blank=True, null=True)
    dir             = models.CharField(max_length=50, blank=True, null=True, verbose_name="Directivity")
    a1sth           = models.CharField(max_length=10, blank=True, null=True)
    a2ndh           = models.CharField(max_length=10, blank=True, null=True)
    a3rdh           = models.CharField(max_length=10, blank=True, null=True)
    h               = models.CharField(max_length=50, blank=True, null=True, verbose_name="Height from Ground")
    gain            = models.DecimalField(null=True, max_digits=10, decimal_places=0, blank=True)
    gain2           = models.DecimalField(null=True, max_digits=10, decimal_places=0, blank=True)
    gain3           = models.DecimalField(null=True, max_digits=10, decimal_places=0, blank=True)
    gn              = models.CharField(max_length=100, blank=True, null=True, verbose_name="Gain")
    t               = models.CharField(max_length=100, blank=True, null=True, verbose_name="Antenna Type")
    make            = models.CharField(max_length=150, blank=True, null=True, verbose_name="Make/Model")
    spare_equip_serial  = models.CharField(max_length=150, blank=True, null=True, verbose_name="Spare Equip")
    spare_equip_serial2 = models.CharField(max_length=150, blank=True, null=True, verbose_name="Spare Equip2")
    spare_equip_serial3 = models.CharField(max_length=150, blank=True, null=True, verbose_name="Spare Equip3")
    spare_equip_serial4 = models.CharField(max_length=150, blank=True, null=True, verbose_name="Spare Equip4")
    sn1             = models.CharField(max_length=60, blank=True, null=True, verbose_name="Serial No#1")
    sn2             = models.CharField(max_length=60, blank=True, null=True, verbose_name="Serial No#2")
    sn3             = models.CharField(max_length=60, blank=True, null=True, verbose_name="Serial No#3")
    sn4             = models.CharField(max_length=60, blank=True, null=True, verbose_name="Serial No#4")
    sn5             = models.CharField(max_length=60, blank=True, null=True, verbose_name="Serial No#5")
    sn6             = models.CharField(max_length=60, blank=True, null=True, verbose_name="Serial No#6")
    sn7             = models.CharField(max_length=60, blank=True, null=True, verbose_name="Serial No#7")
    sn8             = models.CharField(max_length=60, blank=True, null=True, verbose_name="Serial No#8")
    sn9             = models.CharField(max_length=60, blank=True, null=True, verbose_name="Serial No#9")
    sn10            = models.CharField(max_length=60, blank=True, null=True, verbose_name="Serial No#10")
    sn11            = models.CharField(max_length=60, blank=True, null=True, verbose_name="Serial No#11")
    sn12            = models.CharField(max_length=60, blank=True, null=True, verbose_name="Serial No#12")
    sn13            = models.CharField(max_length=60, blank=True, null=True, verbose_name="Serial No#13")
    sn14            = models.CharField(max_length=60, blank=True, null=True, verbose_name="Serial No#14")
    sn15            = models.CharField(max_length=60, blank=True, null=True, verbose_name="Serial No#15")
    sn16            = models.CharField(max_length=60, blank=True, null=True, verbose_name="Serial No#16")
    sn17            = models.CharField(max_length=60, blank=True, null=True, verbose_name="Serial No#17")
    sn18            = models.CharField(max_length=60, blank=True, null=True, verbose_name="Serial No#18")
    sn19            = models.CharField(max_length=60, blank=True, null=True, verbose_name="Serial No#19")
    sn20            = models.CharField(max_length=60, blank=True, null=True, verbose_name="Serial No#20")
    sn21            = models.CharField(max_length=60, blank=True, null=True, verbose_name="Serial No#21")
    sn22            = models.CharField(max_length=60, blank=True, null=True, verbose_name="Serial No#22")
    sn23            = models.CharField(max_length=60, blank=True, null=True, verbose_name="Serial No#23")
    sn24            = models.CharField(max_length=60, blank=True, null=True, verbose_name="Serial No#24")
    freqrange       = models.CharField(max_length=100, blank=True, null=True, verbose_name="Freq Range")
    validity_from   = models.DateField(null=True, verbose_name="Valid from", blank=True)
    validity_to     = models.DateField(null=True, verbose_name="Valid until", blank=True)
    extension       = models.DateField(null=True, verbose_name="Extended Until", blank=True)     
    remarks         = models.TextField(max_length=2000, blank=True, null=True, verbose_name="Remarks")
    or_no           = models.DecimalField(null=True, verbose_name="Official Receipt #1", max_digits=10, decimal_places=0, blank=True)
    date_paid       = models.DateField(null=True, verbose_name="Date Paid", blank=True)
    amount          = models.DecimalField(null=True, verbose_name="Amount", max_digits=10, decimal_places=0, blank=True)
    or_no2          = models.DecimalField(null=True, verbose_name="Official Receipt #2", max_digits=10, decimal_places=0, blank=True)
    date_paid2      = models.DateField(null=True, verbose_name="Date Paid", blank=True)
    amount2         = models.DecimalField(null=True, verbose_name="Amount", max_digits=10, decimal_places=0, blank=True)
    encoder         = models.CharField(max_length=50, blank=True, null=True, verbose_name="Encoder")
    evaluator       = models.CharField(max_length=50, blank=True, null=True, verbose_name="Evaluator")
    signatory       = models.CharField(max_length=50, blank=True, null=True, verbose_name="Signed by Director" )
    form_serial     = models.DecimalField(null=True, verbose_name="Form Serial#", max_digits=10, decimal_places=0, blank=True)
    remarks_2       = models.CharField(max_length=300, blank=True, null=True, verbose_name="Other Remarks")
    dst             = models.CharField(max_length=20, blank=True, null=True, default='DST Paid', verbose_name="Documentary Stamp")
    sitename_id     = models.DecimalField(max_digits=10, decimal_places=0)
    cashierstamp_id = models.DecimalField(null=True, max_digits=10, decimal_places=0, blank=True)
    carrier_id      = models.DecimalField(null=True, max_digits=10, decimal_places=0, blank=True)
    makemodel_id    = models.DecimalField(null=True, max_digits=10, decimal_places=0, blank=True)
    freqrange_id    = models.DecimalField(null=True, max_digits=10, decimal_places=0, blank=True)
    equip_used      = models.CharField(max_length=20, blank=True, null=True)
    encoder_id      = models.DecimalField(null=True, max_digits=10, decimal_places=0, blank=True)
    evaluator_id    = models.DecimalField(null=True, max_digits=10, decimal_places=0, blank=True)
    polarity1       = models.CharField(max_length=20, blank=True, null=True)
    polarity2       = models.CharField(max_length=20, blank=True, null=True)
    polarity3       = models.CharField(max_length=20, blank=True, null=True)
    polarity4       = models.CharField(max_length=20, blank=True, null=True)
    polarity5       = models.CharField(max_length=20, blank=True, null=True)
    polarity6       = models.CharField(max_length=20, blank=True, null=True)
    polarity7       = models.CharField(max_length=20, blank=True, null=True)
    polarity8       = models.CharField(max_length=20, blank=True, null=True)
    polarity9       = models.CharField(max_length=20, blank=True, null=True)
    polarity10      = models.CharField(max_length=20, blank=True, null=True)
    polarity11      = models.CharField(max_length=20, blank=True, null=True)
    polarity12      = models.CharField(max_length=20, blank=True, null=True)
    polarity13      = models.CharField(max_length=20, blank=True, null=True)
    polarity14      = models.CharField(max_length=20, blank=True, null=True)    
   
    tx13            =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    tx14            =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    tx15            =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    tx16            =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    tx17            =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    tx18            =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    tx19            =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    tx20            =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    tx21            =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    tx22            =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)    
    rx13            =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx14            =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx15            =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx16            =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx17            =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx18            =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx19            =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx20            =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx21            =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx22            =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)

    tx13_min        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    tx14_min        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    tx15_min        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    tx16_min        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    tx17_min        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    tx18_min        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    tx19_min        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    tx20_min        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    tx21_min        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    tx22_min        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    
    rx13_min        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx14_min        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx15_min        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx16_min        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx17_min        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx18_min        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx19_min        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx20_min        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx21_min        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx22_min        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)

    tx13_max        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    tx14_max        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    tx15_max        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    tx16_max        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    tx17_max        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    tx18_max        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    tx19_max        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    tx20_max        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    tx21_max        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    tx22_max        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    
    rx13_max        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx14_max        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx15_max        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx16_max        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx17_max        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx18_max        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx19_max        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx20_max        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx21_max        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx22_max        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)

    tx23            =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    tx24            =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    tx25            =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    tx26            =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    tx27            =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    tx28            =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    tx29            =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    tx30            =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    tx31            =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    tx32            =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    tx33            =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    tx34            =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    tx35            =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    tx36            =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)

    rx23            =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx24            =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx25            =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx26            =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx27            =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx28            =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx29            =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx30            =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx31            =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx32            =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx33            =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx34            =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx35            =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx36            =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)

    tx23_min        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    tx24_min        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    tx25_min        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    tx26_min        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    tx27_min        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    tx28_min        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    tx29_min        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    tx30_min        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    tx31_min        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    tx32_min        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    tx33_min        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    tx34_min        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    tx35_min        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    tx36_min        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)

    rx23_min        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx24_min        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx25_min        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx26_min        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx27_min        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx28_min        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx29_min        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx30_min        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx31_min        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx32_min        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx33_min        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx34_min        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx35_min        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx36_min        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)

    tx23_max        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    tx24_max        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    tx25_max        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    tx26_max        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    tx27_max        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    tx28_max        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    tx29_max        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    tx30_max        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    tx31_max        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    tx32_max        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    tx33_max        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    tx34_max        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    tx35_max        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    tx36_max        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)

    rx23_max        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx24_max        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx25_max        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx26_max        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx27_max        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx28_max        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx29_max        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx30_max        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx31_max        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx32_max        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx33_max        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx34_max        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx35_max        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx36_max        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    
    callsign1       = models.CharField(max_length=100, blank=True, null=True, verbose_name="Call-Sign1")
    callsign2       = models.CharField(max_length=100, blank=True, null=True, verbose_name="Call-Sign2")
    callsign3       = models.CharField(max_length=100, blank=True, null=True, verbose_name="Call-Sign3")
    callsign4       = models.CharField(max_length=100, blank=True, null=True, verbose_name="Call-Sign4")
    callsign5       = models.CharField(max_length=100, blank=True, null=True, verbose_name="Call-Sign5")
    callsign6       = models.CharField(max_length=100, blank=True, null=True, verbose_name="Call-Sign6")
    callsign7       = models.CharField(max_length=100, blank=True, null=True, verbose_name="Call-Sign7")
    callsign8       = models.CharField(max_length=100, blank=True, null=True, verbose_name="Call-Sign8")
    callsign9       = models.CharField(max_length=100, blank=True, null=True, verbose_name="Call-Sign9")
    callsign10      = models.CharField(max_length=100, blank=True, null=True, verbose_name="Call-Sign10")
    callsign11      = models.CharField(max_length=100, blank=True, null=True, verbose_name="Call-Sign11")
    callsign12      = models.CharField(max_length=100, blank=True, null=True, verbose_name="Call-Sign12")
    callsign13      = models.CharField(max_length=100, blank=True, null=True, verbose_name="Call-Sign13")
    callsign14      = models.CharField(max_length=100, blank=True, null=True, verbose_name="Call-Sign14")
    callsign15      = models.CharField(max_length=100, blank=True, null=True, verbose_name="Call-Sign15")
    callsign16      = models.CharField(max_length=100, blank=True, null=True, verbose_name="Call-Sign16")
    callsign17      = models.CharField(max_length=100, blank=True, null=True, verbose_name="Call-Sign17")
    callsign18      = models.CharField(max_length=100, blank=True, null=True, verbose_name="Call-Sign18")
    callsign19      = models.CharField(max_length=100, blank=True, null=True, verbose_name="Call-Sign19")
    callsign20      = models.CharField(max_length=100, blank=True, null=True, verbose_name="Call-Sign20")
    callsign21      = models.CharField(max_length=100, blank=True, null=True, verbose_name="Call-Sign21")
    callsign22      = models.CharField(max_length=100, blank=True, null=True, verbose_name="Call-Sign22")
    callsign23      = models.CharField(max_length=100, blank=True, null=True, verbose_name="Call-Sign23")
    callsign24      = models.CharField(max_length=100, blank=True, null=True, verbose_name="Call-Sign24")

    old_callsign1       = models.CharField(max_length=100, blank=True, null=True, verbose_name="Old Call-Sign1")
    old_callsign2       = models.CharField(max_length=100, blank=True, null=True, verbose_name="Old Call-Sign2")
    old_callsign3       = models.CharField(max_length=100, blank=True, null=True, verbose_name="Old Call-Sign3")
    old_callsign4       = models.CharField(max_length=100, blank=True, null=True, verbose_name="Old Call-Sign4")
    old_callsign5       = models.CharField(max_length=100, blank=True, null=True, verbose_name="Old Call-Sign5")
    old_callsign6       = models.CharField(max_length=100, blank=True, null=True, verbose_name="Old Call-Sign6")
    old_callsign7       = models.CharField(max_length=100, blank=True, null=True, verbose_name="Old Call-Sign7")
    old_callsign8       = models.CharField(max_length=100, blank=True, null=True, verbose_name="Old Call-Sign8")
    old_callsign9       = models.CharField(max_length=100, blank=True, null=True, verbose_name="Old Call-Sign9")
    old_callsign10      = models.CharField(max_length=100, blank=True, null=True, verbose_name="Old Call-Sign10")
    old_callsign11      = models.CharField(max_length=100, blank=True, null=True, verbose_name="Old Call-Sign11")
    old_callsign12      = models.CharField(max_length=100, blank=True, null=True, verbose_name="Old Call-Sign12")
    old_callsign13      = models.CharField(max_length=100, blank=True, null=True, verbose_name="Old Call-Sign13")
    old_callsign14      = models.CharField(max_length=100, blank=True, null=True, verbose_name="Old Call-Sign14")
    old_callsign15      = models.CharField(max_length=100, blank=True, null=True, verbose_name="Old Call-Sign15")
    old_callsign16      = models.CharField(max_length=100, blank=True, null=True, verbose_name="Old Call-Sign16")
    old_callsign17      = models.CharField(max_length=100, blank=True, null=True, verbose_name="Old Call-Sign17")
    old_callsign18      = models.CharField(max_length=100, blank=True, null=True, verbose_name="Old Call-Sign18")
    old_callsign19      = models.CharField(max_length=100, blank=True, null=True, verbose_name="Old Call-Sign19")
    old_callsign20      = models.CharField(max_length=100, blank=True, null=True, verbose_name="Old Call-Sign20")
    old_callsign21      = models.CharField(max_length=100, blank=True, null=True, verbose_name="Old Call-Sign21")
    old_callsign22      = models.CharField(max_length=100, blank=True, null=True, verbose_name="Old Call-Sign22")
    old_callsign23      = models.CharField(max_length=100, blank=True, null=True, verbose_name="Old Call-Sign23")
    old_callsign24      = models.CharField(max_length=100, blank=True, null=True, verbose_name="Old Call-Sign24")

    purchase_sp1    = models.CharField(max_length=100, blank=True, null=True, verbose_name="Purchase Spare 1")
    purchase_sp2    = models.CharField(max_length=100, blank=True, null=True, verbose_name="Purchase Spare 2")
    purchase_sp3    = models.CharField(max_length=100, blank=True, null=True, verbose_name="Purchase Spare 3")

    possess_sp1    = models.CharField(max_length=100, blank=True, null=True, verbose_name="Possess Share 1")
    possess_sp2    = models.CharField(max_length=100, blank=True, null=True, verbose_name="Possess Share 2")
    possess_sp3    = models.CharField(max_length=100, blank=True, null=True, verbose_name="Possess Share 3")

    storage_sp1    = models.CharField(max_length=100, blank=True, null=True, verbose_name="Storage Share 1")
    storage_sp2    = models.CharField(max_length=100, blank=True, null=True, verbose_name="Storage Share 2")
    storage_sp3    = models.CharField(max_length=100, blank=True, null=True, verbose_name="Storage Share 3")

    purchase1      = models.CharField(max_length=100, blank=True, null=True, verbose_name="Purchase 1")
    purchase2      = models.CharField(max_length=100, blank=True, null=True, verbose_name="Purchase 2")
    purchase3      = models.CharField(max_length=100, blank=True, null=True, verbose_name="Purchase 3")
    purchase4      = models.CharField(max_length=100, blank=True, null=True, verbose_name="Purchase 4")
    purchase5      = models.CharField(max_length=100, blank=True, null=True, verbose_name="Purchase 5")
    purchase6      = models.CharField(max_length=100, blank=True, null=True, verbose_name="Purchase 6")
    purchase7      = models.CharField(max_length=100, blank=True, null=True, verbose_name="Purchase 7")
    purchase8      = models.CharField(max_length=100, blank=True, null=True, verbose_name="Purchase 8")
    purchase9      = models.CharField(max_length=100, blank=True, null=True, verbose_name="Purchase 9")
    purchase10     = models.CharField(max_length=100, blank=True, null=True, verbose_name="Purchase 10")
    purchase11     = models.CharField(max_length=100, blank=True, null=True, verbose_name="Purchase 11")
    purchase12     = models.CharField(max_length=100, blank=True, null=True, verbose_name="Purchase 12")
    purchase13     = models.CharField(max_length=100, blank=True, null=True, verbose_name="Purchase 13")
    purchase14     = models.CharField(max_length=100, blank=True, null=True, verbose_name="Purchase 14")
    purchase15     = models.CharField(max_length=100, blank=True, null=True, verbose_name="Purchase 15")
    purchase16     = models.CharField(max_length=100, blank=True, null=True, verbose_name="Purchase 16")
    purchase17     = models.CharField(max_length=100, blank=True, null=True, verbose_name="Purchase 17")
    purchase18     = models.CharField(max_length=100, blank=True, null=True, verbose_name="Purchase 18")
    purchase19     = models.CharField(max_length=100, blank=True, null=True, verbose_name="Purchase 19")
    purchase20     = models.CharField(max_length=100, blank=True, null=True, verbose_name="Purchase 20")
    purchase21     = models.CharField(max_length=100, blank=True, null=True, verbose_name="Purchase 21")
    purchase22     = models.CharField(max_length=100, blank=True, null=True, verbose_name="Purchase 22")
    purchase23     = models.CharField(max_length=100, blank=True, null=True, verbose_name="Purchase 23")
    purchase24     = models.CharField(max_length=100, blank=True, null=True, verbose_name="Purchase 24")

    possess1      = models.CharField(max_length=100, blank=True, null=True, verbose_name="Possess 1")
    possess2      = models.CharField(max_length=100, blank=True, null=True, verbose_name="Possess 2")
    possess3      = models.CharField(max_length=100, blank=True, null=True, verbose_name="Possess 3")
    possess4      = models.CharField(max_length=100, blank=True, null=True, verbose_name="Possess 4")
    possess5      = models.CharField(max_length=100, blank=True, null=True, verbose_name="Possess 5")
    possess6      = models.CharField(max_length=100, blank=True, null=True, verbose_name="Possess 6")
    possess7      = models.CharField(max_length=100, blank=True, null=True, verbose_name="Possess 7")
    possess8      = models.CharField(max_length=100, blank=True, null=True, verbose_name="Possess 8")
    possess9      = models.CharField(max_length=100, blank=True, null=True, verbose_name="Possess 9")
    possess10     = models.CharField(max_length=100, blank=True, null=True, verbose_name="Possess 10")
    possess11     = models.CharField(max_length=100, blank=True, null=True, verbose_name="Possess 11")
    possess12     = models.CharField(max_length=100, blank=True, null=True, verbose_name="Possess 12")
    possess13     = models.CharField(max_length=100, blank=True, null=True, verbose_name="Possess 13")
    possess14     = models.CharField(max_length=100, blank=True, null=True, verbose_name="Possess 14")
    possess15     = models.CharField(max_length=100, blank=True, null=True, verbose_name="Possess 15")
    possess16     = models.CharField(max_length=100, blank=True, null=True, verbose_name="Possess 16")
    possess17     = models.CharField(max_length=100, blank=True, null=True, verbose_name="Possess 17")
    possess18     = models.CharField(max_length=100, blank=True, null=True, verbose_name="Possess 18")
    possess19     = models.CharField(max_length=100, blank=True, null=True, verbose_name="Possess 19")
    possess20     = models.CharField(max_length=100, blank=True, null=True, verbose_name="Possess 20")
    possess21     = models.CharField(max_length=100, blank=True, null=True, verbose_name="Possess 21")
    possess22     = models.CharField(max_length=100, blank=True, null=True, verbose_name="Possess 22")
    possess23     = models.CharField(max_length=100, blank=True, null=True, verbose_name="Possess 23")
    possess24     = models.CharField(max_length=100, blank=True, null=True, verbose_name="Possess 24")

    old_serial_no_1  =models.CharField(max_length=100, blank=True, null=True, verbose_name="Old Serial No 1")
    old_serial_no_2  =models.CharField(max_length=100, blank=True, null=True, verbose_name="Old Serial No 2")
    old_serial_no_3  =models.CharField(max_length=100, blank=True, null=True, verbose_name="Old Serial No 3")
    old_serial_no_4  =models.CharField(max_length=100, blank=True, null=True, verbose_name="Old Serial No 4")
    old_serial_no_5  =models.CharField(max_length=100, blank=True, null=True, verbose_name="Old Serial No 5")
    old_serial_no_6  =models.CharField(max_length=100, blank=True, null=True, verbose_name="Old Serial No 6")
    old_serial_no_7  =models.CharField(max_length=100, blank=True, null=True, verbose_name="Old Serial No 7")
    old_serial_no_8  =models.CharField(max_length=100, blank=True, null=True, verbose_name="Old Serial No 8")
    old_serial_no_9  =models.CharField(max_length=100, blank=True, null=True, verbose_name="Old Serial No 9")
    old_serial_no_10 =models.CharField(max_length=100, blank=True, null=True, verbose_name="Old Serial No 10")
    old_serial_no_11 =models.CharField(max_length=100, blank=True, null=True, verbose_name="Old Serial No 11")
    old_serial_no_12 =models.CharField(max_length=100, blank=True, null=True, verbose_name="Old Serial No 12")
    old_serial_no_13 =models.CharField(max_length=100, blank=True, null=True, verbose_name="Old Serial No 13")
    old_serial_no_14 =models.CharField(max_length=100, blank=True, null=True, verbose_name="Old Serial No 14")
    old_serial_no_15 =models.CharField(max_length=100, blank=True, null=True, verbose_name="Old Serial No 15")
    old_serial_no_16 =models.CharField(max_length=100, blank=True, null=True, verbose_name="Old Serial No 16")
    old_serial_no_17 =models.CharField(max_length=100, blank=True, null=True, verbose_name="Old Serial No 17")
    old_serial_no_18 =models.CharField(max_length=100, blank=True, null=True, verbose_name="Old Serial No 18")
    old_serial_no_19 =models.CharField(max_length=100, blank=True, null=True, verbose_name="Old Serial No 19")
    old_serial_no_20 =models.CharField(max_length=100, blank=True, null=True, verbose_name="Old Serial No 20")
    old_serial_no_21 =models.CharField(max_length=100, blank=True, null=True, verbose_name="Old Serial No 21")
    old_serial_no_22 =models.CharField(max_length=100, blank=True, null=True, verbose_name="Old Serial No 22")
    old_serial_no_23 =models.CharField(max_length=100, blank=True, null=True, verbose_name="Old Serial No 23")
    old_serial_no_24 =models.CharField(max_length=100, blank=True, null=True, verbose_name="Old Serial No 24")

    storage1      = models.CharField(max_length=100, blank=True, null=True, verbose_name="Storage 1")
    storage2      = models.CharField(max_length=100, blank=True, null=True, verbose_name="Storage 2")
    storage3      = models.CharField(max_length=100, blank=True, null=True, verbose_name="Storage 3")
    storage4      = models.CharField(max_length=100, blank=True, null=True, verbose_name="Storage 4")
    storage5      = models.CharField(max_length=100, blank=True, null=True, verbose_name="Storage 5")
    storage6      = models.CharField(max_length=100, blank=True, null=True, verbose_name="Storage 6")
    storage7      = models.CharField(max_length=100, blank=True, null=True, verbose_name="Storage 7")
    storage8      = models.CharField(max_length=100, blank=True, null=True, verbose_name="Storage 8")
    storage9      = models.CharField(max_length=100, blank=True, null=True, verbose_name="Storage 9")
    storage10     = models.CharField(max_length=100, blank=True, null=True, verbose_name="Storage 10")
    storage11     = models.CharField(max_length=100, blank=True, null=True, verbose_name="Storage 11")
    storage12     = models.CharField(max_length=100, blank=True, null=True, verbose_name="Storage 12")
    storage13     = models.CharField(max_length=100, blank=True, null=True, verbose_name="Storage 13")
    storage14     = models.CharField(max_length=100, blank=True, null=True, verbose_name="Storage 14")
    storage15     = models.CharField(max_length=100, blank=True, null=True, verbose_name="Storage 15")
    storage16     = models.CharField(max_length=100, blank=True, null=True, verbose_name="Storage 16")
    storage17     = models.CharField(max_length=100, blank=True, null=True, verbose_name="Storage 17")
    storage18     = models.CharField(max_length=100, blank=True, null=True, verbose_name="Storage 18")
    storage19     = models.CharField(max_length=100, blank=True, null=True, verbose_name="Storage 19")
    storage20     = models.CharField(max_length=100, blank=True, null=True, verbose_name="Storage 20")
    storage21     = models.CharField(max_length=100, blank=True, null=True, verbose_name="Storage 21")
    storage22     = models.CharField(max_length=100, blank=True, null=True, verbose_name="Storage 22")
    storage23     = models.CharField(max_length=100, blank=True, null=True, verbose_name="Storage 23")
    storage24     = models.CharField(max_length=100, blank=True, null=True, verbose_name="storage 24")

    polarity15    = models.CharField(max_length=20, blank=True, null=True)
    polarity16    = models.CharField(max_length=20, blank=True, null=True)
    polarity17    = models.CharField(max_length=20, blank=True, null=True)
    polarity18    = models.CharField(max_length=20, blank=True, null=True)
    polarity19    = models.CharField(max_length=20, blank=True, null=True)
    polarity20    = models.CharField(max_length=20, blank=True, null=True)
    polarity21    = models.CharField(max_length=20, blank=True, null=True)
    polarity22    = models.CharField(max_length=20, blank=True, null=True)
    polarity23    = models.CharField(max_length=20, blank=True, null=True)
    polarity24    = models.CharField(max_length=20, blank=True, null=True) 

    old_serial_no_sp1 = models.CharField(max_length=100, blank=True, null=True, verbose_name="Old Spare Serial No 1") 
    old_serial_no_sp2 = models.CharField(max_length=100, blank=True, null=True, verbose_name="Old Spare Serial No 2")
    old_serial_no_sp3 = models.CharField(max_length=100, blank=True, null=True, verbose_name="Old Spare Serial No 3") 

    
    old_make_1    = models.CharField(max_length=60, blank=True, null=True, verbose_name="Old Make/Model1")
    old_make_2    = models.CharField(max_length=60, blank=True, null=True, verbose_name="Old Make/Model2")
    old_make_3    = models.CharField(max_length=60, blank=True, null=True, verbose_name="Old Make/Model3")
    old_make_4    = models.CharField(max_length=60, blank=True, null=True, verbose_name="Old Make/Model4")
    old_make_5    = models.CharField(max_length=60, blank=True, null=True, verbose_name="Old Make/Model5")
    old_make_6    = models.CharField(max_length=60, blank=True, null=True, verbose_name="Old Make/Model6")
    old_make_7    = models.CharField(max_length=60, blank=True, null=True, verbose_name="Old Make/Model7")
    old_make_8    = models.CharField(max_length=60, blank=True, null=True, verbose_name="Old Make/Model8")
    old_make_9    = models.CharField(max_length=60, blank=True, null=True, verbose_name="Old Make/Model9")
    old_make_10   = models.CharField(max_length=60, blank=True, null=True, verbose_name="Old Make/Model10")
    old_make_11   = models.CharField(max_length=60, blank=True, null=True, verbose_name="Old Make/Model11")
    old_make_12   = models.CharField(max_length=60, blank=True, null=True, verbose_name="Old Make/Model12")
    old_make_13    = models.CharField(max_length=60, blank=True, null=True, verbose_name="Old Make/Model13")
    old_make_14    = models.CharField(max_length=60, blank=True, null=True, verbose_name="Old Make/Model14")
    old_make_15    = models.CharField(max_length=60, blank=True, null=True, verbose_name="Old Make/Model15")
    old_make_16    = models.CharField(max_length=60, blank=True, null=True, verbose_name="Old Make/Model16")
    old_make_17    = models.CharField(max_length=60, blank=True, null=True, verbose_name="Old Make/Model17")
    old_make_18    = models.CharField(max_length=60, blank=True, null=True, verbose_name="Old Make/Model18")
    old_make_19    = models.CharField(max_length=60, blank=True, null=True, verbose_name="Old Make/Model19")
    old_make_20    = models.CharField(max_length=60, blank=True, null=True, verbose_name="Old Make/Model20")
    old_make_21    = models.CharField(max_length=60, blank=True, null=True, verbose_name="Old Make/Model21")
    old_make_22    = models.CharField(max_length=60, blank=True, null=True, verbose_name="Old Make/Model22")
    old_make_23    = models.CharField(max_length=60, blank=True, null=True, verbose_name="Old Make/Model23")
    old_make_24    = models.CharField(max_length=60, blank=True, null=True, verbose_name="Old Make/Model24")
    old_make_SP1    = models.CharField(max_length=60, blank=True, null=True, verbose_name="Old Make/Modelsp1")
    old_make_SP2    = models.CharField(max_length=60, blank=True, null=True, verbose_name="Old Make/Modelsp2")
    old_make_SP3    = models.CharField(max_length=60, blank=True, null=True, verbose_name="Old Make/Modelsp3")

    capacity      = models.CharField(max_length=100, blank=True, null=True, verbose_name="Capacity")

    tx37            =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    tx38            =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    tx39            =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    tx40            =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    tx41            =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    tx42            =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
  
    rx37            =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx38            =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx39            =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx40            =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx41            =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx42            =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)

    tx37_min        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    tx38_min        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    tx39_min        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    tx40_min        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    tx41_min        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    tx42_min        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    
    rx37_min        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx38_min        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx39_min        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx40_min        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx41_min        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx42_min        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx42_min        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)

    tx37_max        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    tx38_max        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    tx39_max        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    tx40_max        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    tx41_max        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    tx42_max        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    
    rx37_max        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx38_max        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx39_max        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx40_max        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx41_max        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx42_max        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx42_max        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    old_sitename    = models.CharField(max_length=300, blank=True, null=True, verbose_name="Old Site")
    or_no3          = models.DecimalField(null=True, verbose_name="Official Receipt #3", max_digits=10, decimal_places=0, blank=True)
    date_paid3      = models.DateField(null=True, verbose_name="Date Paid", blank=True)
    amount3         = models.DecimalField(null=True, verbose_name="Amount", max_digits=10, decimal_places=0, blank=True)
    logbook_cn      = models.CharField(null=True, blank=True, max_length=30,verbose_name = 'Logbook CN')
    record_cn       = models.CharField(null=True, blank=True, max_length=30,verbose_name = 'Record CN')
    storage_all     = models.CharField(max_length=100, blank=True, null=True, verbose_name="Storage All")
    purchase_all    = models.CharField(max_length=100, blank=True, null=True, verbose_name="Purchase All")
    possess_all     = models.CharField(max_length=100, blank=True, null=True, verbose_name="Possess All")
    old_make_all    = models.CharField(max_length=60, blank=True, null=True, verbose_name="Old Make/Model All")
    
    philaddress   = models.ForeignKey(PhilAddress,  blank=True, null=True, on_delete=models.SET_NULL)
    carrierFK     = models.ForeignKey(Carrier, verbose_name='Carrier',  blank=True, null=True, on_delete=models.SET_NULL) 



    class Meta:
        db_table            = u'master_rsl'
        verbose_name_plural = "Master RSL"
    #    ordering            = ["issued"]
    #def __unicode__(self):
    #    return self.rslno
#ok!
class LatestRsl(models.Model):
    id              = models.AutoField(primary_key=True)  #id              = models.DecimalField(primary_key=True, decimal_places=0, max_digits=10)
    
    logbook         = models.ForeignKey(LogBook, null=True, blank= True)
    status          = models.CharField(max_length=20, blank=True, null=True, verbose_name="Status")
    rslno           = models.CharField(max_length=50, blank=True, null=True, verbose_name="License No")
    issued          = models.DateField(null=True, verbose_name="Date Issued", blank=True)
    carrier         = models.CharField(max_length=150, blank=True, null=True, verbose_name="Carrier")
    site            = models.CharField(max_length=300, blank=True, null=True, verbose_name="Site")
    street          = models.CharField(max_length=150, blank=True, null=True, verbose_name="Street")
    city            = models.CharField(max_length=150, blank=True, null=True, verbose_name="Town/City")
    province        = models.CharField(max_length=150, blank=True, null=True, verbose_name="Province")
    region          = models.CharField(max_length=50, blank=True, null=True, verbose_name="Region")
    deg_long        = models.DecimalField(null=True, max_digits=10, decimal_places=0, blank=True)
    min_long        = models.DecimalField(null=True, max_digits=10, decimal_places=0, blank=True)
    sec_long        = models.DecimalField(null=True, max_digits=10, decimal_places=0, blank=True)
    longitude       = models.CharField(max_length=50, blank=True, null=True, verbose_name="Longitude")
    deg_lat         = models.DecimalField(null=True, max_digits=10, decimal_places=0, blank=True)
    min_lat         = models.DecimalField(null=True, max_digits=10, decimal_places=0, blank=True)
    sec_lat         = models.DecimalField(null=True, max_digits=10, decimal_places=0, blank=True)
    latitude        = models.CharField(max_length=50, blank=True, null=True, verbose_name="Latitude")
    lic_to_operate  = models.CharField(max_length=50, blank=True, null=True, verbose_name="License to Operate")
    class_of_station = models.CharField(max_length=20, blank=True, null=True, verbose_name="Class of Station")
    nature_of_service = models.CharField(max_length=20, blank=True, null=True, verbose_name="Nature of Service", default='CP')
    callsign        = models.CharField(max_length=100, blank=True, null=True, verbose_name="Call-Sign")
    ptsvc           = models.CharField(max_length=500, blank=True, null=True, verbose_name="Point of Service")
    ptsvc_callsign  = models.CharField(max_length=150, blank=True, null=True)
    tx1             =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    tx2             =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    tx3             =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    tx4             =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    tx5             =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    tx6             =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    tx7             =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    tx8             =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    tx9             =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    tx10            =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    tx11            =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    tx12            =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx1             =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx2             =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx3             =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx4             =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx5             =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx6             =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx7             =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx8             =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx9             =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx10            =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx11            =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx12            =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    tx1_min         =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    tx2_min         =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    tx3_min         =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    tx4_min         =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    tx5_min         =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    tx6_min         =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    tx7_min         =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    tx8_min         =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    tx9_min         =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    tx10_min        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    tx11_min        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    tx12_min        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx1_min         =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx2_min         =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx3_min         =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx4_min         =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx5_min         =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx6_min         =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx7_min         =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx8_min         =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx9_min         =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx10_min        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx11_min        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx12_min        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    tx1_max         =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    tx2_max         =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    tx3_max         =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    tx4_max         =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    tx5_max         =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    tx6_max         =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    tx7_max         =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    tx8_max         =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    tx9_max         =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    tx10_max        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    tx11_max        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    tx12_max        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx1_max         =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx2_max         =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx3_max         =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx4_max         =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx5_max         =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx6_max         =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx7_max         =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx8_max         =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx9_max         =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx10_max        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx11_max        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx12_max        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)

    bwe_1           = models.CharField(max_length=50, blank=True, null=True, verbose_name="Bandwidth")
    no              = models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    unit            = models.CharField(max_length=10, blank=True, null=True)
    power           = models.CharField(max_length=100, blank=True, null=True, verbose_name="Power")
    a1std           = models.CharField(max_length=10, blank=True, null=True)
    a2ndd           = models.CharField(max_length=10, blank=True, null=True)
    a3rdd           = models.CharField(max_length=10, blank=True, null=True)
    a4th            = models.CharField(max_length=10, blank=True, null=True)
    a5th            = models.CharField(max_length=10, blank=True, null=True)
    a6th            = models.CharField(max_length=10, blank=True, null=True)
    dir             = models.CharField(max_length=50, blank=True, null=True, verbose_name="Directivity")
    a1sth           = models.CharField(max_length=10, blank=True, null=True)
    a2ndh           = models.CharField(max_length=10, blank=True, null=True)
    a3rdh           = models.CharField(max_length=10, blank=True, null=True)
    h               = models.CharField(max_length=50, blank=True, null=True, verbose_name="Height from Ground")
    gain            = models.DecimalField(null=True, max_digits=10, decimal_places=0, blank=True)
    gain2           = models.DecimalField(null=True, max_digits=10, decimal_places=0, blank=True)
    gain3           = models.DecimalField(null=True, max_digits=10, decimal_places=0, blank=True)
    gn              = models.CharField(max_length=100, blank=True, null=True, verbose_name="Gain")
    t               = models.CharField(max_length=100, blank=True, null=True, verbose_name="Antenna Type")
    make            = models.CharField(max_length=150, blank=True, null=True, verbose_name="Make/Model")
    spare_equip_serial = models.CharField(max_length=150, blank=True, null=True, verbose_name="Spare Equip")
    spare_equip_serial2 = models.CharField(max_length=150, blank=True, null=True, verbose_name="Spare Equip2")
    spare_equip_serial3 = models.CharField(max_length=150, blank=True, null=True, verbose_name="Spare Equip3")
    spare_equip_serial4 = models.CharField(max_length=150, blank=True, null=True, verbose_name="Spare Equip4")
    sn1             = models.CharField(max_length=60, blank=True, null=True, verbose_name="Serial No#1")
    sn2             = models.CharField(max_length=60, blank=True, null=True, verbose_name="Serial No#2")
    sn3             = models.CharField(max_length=60, blank=True, null=True, verbose_name="Serial No#3")
    sn4             = models.CharField(max_length=60, blank=True, null=True, verbose_name="Serial No#4")
    sn5             = models.CharField(max_length=60, blank=True, null=True, verbose_name="Serial No#5")
    sn6             = models.CharField(max_length=60, blank=True, null=True, verbose_name="Serial No#6")
    sn7             = models.CharField(max_length=60, blank=True, null=True, verbose_name="Serial No#7")
    sn8             = models.CharField(max_length=60, blank=True, null=True, verbose_name="Serial No#8")
    sn9             = models.CharField(max_length=60, blank=True, null=True, verbose_name="Serial No#9")
    sn10            = models.CharField(max_length=60, blank=True, null=True, verbose_name="Serial No#10")
    sn11            = models.CharField(max_length=60, blank=True, null=True, verbose_name="Serial No#11")
    sn12            = models.CharField(max_length=60, blank=True, null=True, verbose_name="Serial No#12")
    sn13            = models.CharField(max_length=60, blank=True, null=True, verbose_name="Serial No#13")
    sn14            = models.CharField(max_length=60, blank=True, null=True, verbose_name="Serial No#14")
    sn15            = models.CharField(max_length=60, blank=True, null=True, verbose_name="Serial No#15")
    sn16            = models.CharField(max_length=60, blank=True, null=True, verbose_name="Serial No#16")
    sn17            = models.CharField(max_length=60, blank=True, null=True, verbose_name="Serial No#17")
    sn18            = models.CharField(max_length=60, blank=True, null=True, verbose_name="Serial No#18")
    sn19            = models.CharField(max_length=60, blank=True, null=True, verbose_name="Serial No#19")
    sn20            = models.CharField(max_length=60, blank=True, null=True, verbose_name="Serial No#20")
    sn21            = models.CharField(max_length=60, blank=True, null=True, verbose_name="Serial No#21")
    sn22            = models.CharField(max_length=60, blank=True, null=True, verbose_name="Serial No#22")
    sn23            = models.CharField(max_length=60, blank=True, null=True, verbose_name="Serial No#23")
    sn24            = models.CharField(max_length=60, blank=True, null=True, verbose_name="Serial No#24")
    freqrange       = models.CharField(max_length=100, blank=True, null=True, verbose_name="Freq Range")
    validity_from   = models.DateField(null=True, verbose_name="Valid from", blank=True)
    validity_to     = models.DateField(null=True, verbose_name="Valid until", blank=True)
    extension       = models.DateField(null=True, verbose_name="Extended Until", blank=True)
    remarks         = models.CharField(max_length=2000, blank=True, null=True, verbose_name="Remarks")
    
    or_no           = models.DecimalField(null=True, verbose_name="Official Receipt #1", max_digits=10, decimal_places=0, blank=True)
    date_paid       = models.DateField(null=True, verbose_name="Date Paid", blank=True)
    amount          = models.DecimalField(null=True, verbose_name="Amount", max_digits=10, decimal_places=0, blank=True)
    or_no2          = models.DecimalField(null=True, verbose_name="Official Receipt #2", max_digits=10, decimal_places=0, blank=True)
    date_paid2      = models.DateField(null=True, verbose_name="Date Paid", blank=True)
    amount2         = models.DecimalField(null=True, verbose_name="Amount", max_digits=10, decimal_places=0, blank=True)
   
    or_no3          = models.DecimalField(null=True, verbose_name="Official Receipt #3", max_digits=10, decimal_places=0, blank=True)
    date_paid3      = models.DateField(null=True, verbose_name="Date Paid", blank=True)
    amount3         = models.DecimalField(null=True, verbose_name="Amount", max_digits=10, decimal_places=0, blank=True)
    updater         = models.CharField(max_length=50, blank=True, null=True, verbose_name="Updated by")
    encoder         = models.CharField(max_length=50, blank=True, null=True, verbose_name="Encoder", choices=ENCODER)
    evaluator       = models.CharField(max_length=50, blank=True, null=True, verbose_name="Evaluator", choices=EVALUATOR)
    signatory       = models.CharField(max_length=50, blank=True, null=True, verbose_name="Signed by Director", choices=DIRECTORS)
    form_serial     = models.DecimalField(null=True, verbose_name="Form Serial#", max_digits=10, decimal_places=0, blank=True)
    remarks_2       = models.CharField(max_length=300, blank=True, null=True, verbose_name="Other Remarks")
    dst             = models.CharField(max_length=20, blank=True, null=True, verbose_name="Documentary Stamp")
    sitename_id     = models.DecimalField(max_digits=10, decimal_places=0)
    cashierstamp_id = models.DecimalField(null=True, max_digits=10, decimal_places=0, blank=True)
    carrier_id      = models.DecimalField(null=True, max_digits=10, decimal_places=0, blank=True)
    makemodel_id    = models.DecimalField(null=True, max_digits=10, decimal_places=0, blank=True)
    freqrange_id    = models.DecimalField(null=True, max_digits=10, decimal_places=0, blank=True)
    equip_used      = models.CharField(max_length=20, blank=True, null=True)
    encoder_id      = models.DecimalField(null=True, max_digits=10, decimal_places=0, blank=True)
    evaluator_id    = models.DecimalField(null=True, max_digits=10, decimal_places=0, blank=True)
    polarity1       = models.CharField(max_length=20, blank=True, null=True)
    polarity2       = models.CharField(max_length=20, blank=True, null=True)
    polarity3       = models.CharField(max_length=20, blank=True, null=True)
    polarity4       = models.CharField(max_length=20, blank=True, null=True)
    polarity5       = models.CharField(max_length=20, blank=True, null=True)
    polarity6       = models.CharField(max_length=20, blank=True, null=True)
    polarity7       = models.CharField(max_length=20, blank=True, null=True)
    polarity8       = models.CharField(max_length=20, blank=True, null=True)
    polarity9       = models.CharField(max_length=20, blank=True, null=True)
    polarity10      = models.CharField(max_length=20, blank=True, null=True)
    polarity11      = models.CharField(max_length=20, blank=True, null=True)
    polarity12      = models.CharField(max_length=20, blank=True, null=True)
    polarity13      = models.CharField(max_length=20, blank=True, null=True)
    polarity14      = models.CharField(max_length=20, blank=True, null=True)    
   
    tx13            =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    tx14            =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    tx15            =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    tx16            =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    tx17            =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    tx18            =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    tx19            =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    tx20            =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    tx21            =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    tx22            =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)    
    rx13            =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx14            =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx15            =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx16            =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx17            =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx18            =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx19            =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx20            =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx21            =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx22            =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)

    tx13_min        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    tx14_min        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    tx15_min        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    tx16_min        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    tx17_min        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    tx18_min        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    tx19_min        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    tx20_min        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    tx21_min        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    tx22_min        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    
    rx13_min        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx14_min        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx15_min        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx16_min        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx17_min        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx18_min        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx19_min        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx20_min        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx21_min        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx22_min        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)

    tx13_max        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    tx14_max        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    tx15_max        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    tx16_max        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    tx17_max        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    tx18_max        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    tx19_max        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    tx20_max        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    tx21_max        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    tx22_max        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    
    rx13_max        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx14_max        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx15_max        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx16_max        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx17_max        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx18_max        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx19_max        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx20_max        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx21_max        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx22_max        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)

    tx23            =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    tx24            =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    tx25            =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    tx26            =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    tx27            =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    tx28            =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    tx29            =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    tx30            =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    tx31            =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    tx32            =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    tx33            =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    tx34            =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    tx35            =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    tx36            =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)

    rx23            =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx24            =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx25            =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx26            =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx27            =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx28            =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx29            =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx30            =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx31            =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx32            =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx33            =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx34            =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx35            =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx36            =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)

    tx23_min        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    tx24_min        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    tx25_min        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    tx26_min        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    tx27_min        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    tx28_min        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    tx29_min        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    tx30_min        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    tx31_min        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    tx32_min        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    tx33_min        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    tx34_min        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    tx35_min        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    tx36_min        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)

    rx23_min        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx24_min        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx25_min        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx26_min        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx27_min        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx28_min        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx29_min        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx30_min        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx31_min        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx32_min        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx33_min        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx34_min        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx35_min        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx36_min        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)

    tx23_max        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    tx24_max        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    tx25_max        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    tx26_max        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    tx27_max        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    tx28_max        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    tx29_max        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    tx30_max        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    tx31_max        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    tx32_max        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    tx33_max        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    tx34_max        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    tx35_max        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    tx36_max        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)

    rx23_max        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx24_max        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx25_max        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx26_max        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx27_max        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx28_max        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx29_max        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx30_max        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx31_max        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx32_max        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx33_max        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx34_max        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx35_max        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx36_max        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    
    callsign1       = models.CharField(max_length=100, blank=True, null=True, verbose_name="Call-Sign1")
    callsign2       = models.CharField(max_length=100, blank=True, null=True, verbose_name="Call-Sign2")
    callsign3       = models.CharField(max_length=100, blank=True, null=True, verbose_name="Call-Sign3")
    callsign4       = models.CharField(max_length=100, blank=True, null=True, verbose_name="Call-Sign4")
    callsign5       = models.CharField(max_length=100, blank=True, null=True, verbose_name="Call-Sign5")
    callsign6       = models.CharField(max_length=100, blank=True, null=True, verbose_name="Call-Sign6")
    callsign7       = models.CharField(max_length=100, blank=True, null=True, verbose_name="Call-Sign7")
    callsign8       = models.CharField(max_length=100, blank=True, null=True, verbose_name="Call-Sign8")
    callsign9       = models.CharField(max_length=100, blank=True, null=True, verbose_name="Call-Sign9")
    callsign10      = models.CharField(max_length=100, blank=True, null=True, verbose_name="Call-Sign10")
    callsign11      = models.CharField(max_length=100, blank=True, null=True, verbose_name="Call-Sign11")
    callsign12      = models.CharField(max_length=100, blank=True, null=True, verbose_name="Call-Sign12")
    callsign13      = models.CharField(max_length=100, blank=True, null=True, verbose_name="Call-Sign13")
    callsign14      = models.CharField(max_length=100, blank=True, null=True, verbose_name="Call-Sign14")
    callsign15      = models.CharField(max_length=100, blank=True, null=True, verbose_name="Call-Sign15")
    callsign16      = models.CharField(max_length=100, blank=True, null=True, verbose_name="Call-Sign16")
    callsign17      = models.CharField(max_length=100, blank=True, null=True, verbose_name="Call-Sign17")
    callsign18      = models.CharField(max_length=100, blank=True, null=True, verbose_name="Call-Sign18")
    callsign19      = models.CharField(max_length=100, blank=True, null=True, verbose_name="Call-Sign19")
    callsign20      = models.CharField(max_length=100, blank=True, null=True, verbose_name="Call-Sign20")
    callsign21      = models.CharField(max_length=100, blank=True, null=True, verbose_name="Call-Sign21")
    callsign22      = models.CharField(max_length=100, blank=True, null=True, verbose_name="Call-Sign22")
    callsign23      = models.CharField(max_length=100, blank=True, null=True, verbose_name="Call-Sign23")
    callsign24      = models.CharField(max_length=100, blank=True, null=True, verbose_name="Call-Sign24")

    old_callsign1       = models.CharField(max_length=100, blank=True, null=True, verbose_name="Old Call-Sign1")
    old_callsign2       = models.CharField(max_length=100, blank=True, null=True, verbose_name="Old Call-Sign2")
    old_callsign3       = models.CharField(max_length=100, blank=True, null=True, verbose_name="Old Call-Sign3")
    old_callsign4       = models.CharField(max_length=100, blank=True, null=True, verbose_name="Old Call-Sign4")
    old_callsign5       = models.CharField(max_length=100, blank=True, null=True, verbose_name="Old Call-Sign5")
    old_callsign6       = models.CharField(max_length=100, blank=True, null=True, verbose_name="Old Call-Sign6")
    old_callsign7       = models.CharField(max_length=100, blank=True, null=True, verbose_name="Old Call-Sign7")
    old_callsign8       = models.CharField(max_length=100, blank=True, null=True, verbose_name="Old Call-Sign8")
    old_callsign9       = models.CharField(max_length=100, blank=True, null=True, verbose_name="Old Call-Sign9")
    old_callsign10      = models.CharField(max_length=100, blank=True, null=True, verbose_name="Old Call-Sign10")
    old_callsign11      = models.CharField(max_length=100, blank=True, null=True, verbose_name="Old Call-Sign11")
    old_callsign12      = models.CharField(max_length=100, blank=True, null=True, verbose_name="Old Call-Sign12")
    old_callsign13      = models.CharField(max_length=100, blank=True, null=True, verbose_name="Old Call-Sign13")
    old_callsign14      = models.CharField(max_length=100, blank=True, null=True, verbose_name="Old Call-Sign14")
    old_callsign15      = models.CharField(max_length=100, blank=True, null=True, verbose_name="Old Call-Sign15")
    old_callsign16      = models.CharField(max_length=100, blank=True, null=True, verbose_name="Old Call-Sign16")
    old_callsign17      = models.CharField(max_length=100, blank=True, null=True, verbose_name="Old Call-Sign17")
    old_callsign18      = models.CharField(max_length=100, blank=True, null=True, verbose_name="Old Call-Sign18")
    old_callsign19      = models.CharField(max_length=100, blank=True, null=True, verbose_name="Old Call-Sign19")
    old_callsign20      = models.CharField(max_length=100, blank=True, null=True, verbose_name="Old Call-Sign20")
    old_callsign21      = models.CharField(max_length=100, blank=True, null=True, verbose_name="Old Call-Sign21")
    old_callsign22      = models.CharField(max_length=100, blank=True, null=True, verbose_name="Old Call-Sign22")
    old_callsign23      = models.CharField(max_length=100, blank=True, null=True, verbose_name="Old Call-Sign23")
    old_callsign24      = models.CharField(max_length=100, blank=True, null=True, verbose_name="Old Call-Sign24")

    purchase_sp1    = models.CharField(max_length=100, blank=True, null=True, verbose_name="Purchase Spare 1")
    purchase_sp2    = models.CharField(max_length=100, blank=True, null=True, verbose_name="Purchase Spare 2")
    purchase_sp3    = models.CharField(max_length=100, blank=True, null=True, verbose_name="Purchase Spare 3")

    possess_sp1    = models.CharField(max_length=100, blank=True, null=True, verbose_name="Possess Share 1")
    possess_sp2    = models.CharField(max_length=100, blank=True, null=True, verbose_name="Possess Share 2")
    possess_sp3    = models.CharField(max_length=100, blank=True, null=True, verbose_name="Possess Share 3")

    storage_sp1    = models.CharField(max_length=100, blank=True, null=True, verbose_name="Storage Share 1")
    storage_sp2    = models.CharField(max_length=100, blank=True, null=True, verbose_name="Storage Share 2")
    storage_sp3    = models.CharField(max_length=100, blank=True, null=True, verbose_name="Storage Share 3")
    
    purchase1      = models.CharField(max_length=100, blank=True, null=True, verbose_name="Purchase 1")
    purchase2      = models.CharField(max_length=100, blank=True, null=True, verbose_name="Purchase 2")
    purchase3      = models.CharField(max_length=100, blank=True, null=True, verbose_name="Purchase 3")
    purchase4      = models.CharField(max_length=100, blank=True, null=True, verbose_name="Purchase 4")
    purchase5      = models.CharField(max_length=100, blank=True, null=True, verbose_name="Purchase 5")
    purchase6      = models.CharField(max_length=100, blank=True, null=True, verbose_name="Purchase 6")
    purchase7      = models.CharField(max_length=100, blank=True, null=True, verbose_name="Purchase 7")
    purchase8      = models.CharField(max_length=100, blank=True, null=True, verbose_name="Purchase 8")
    purchase9      = models.CharField(max_length=100, blank=True, null=True, verbose_name="Purchase 9")
    purchase10     = models.CharField(max_length=100, blank=True, null=True, verbose_name="Purchase 10")
    purchase11     = models.CharField(max_length=100, blank=True, null=True, verbose_name="Purchase 11")
    purchase12     = models.CharField(max_length=100, blank=True, null=True, verbose_name="Purchase 12")
    purchase13     = models.CharField(max_length=100, blank=True, null=True, verbose_name="Purchase 13")
    purchase14     = models.CharField(max_length=100, blank=True, null=True, verbose_name="Purchase 14")
    purchase15     = models.CharField(max_length=100, blank=True, null=True, verbose_name="Purchase 15")
    purchase16     = models.CharField(max_length=100, blank=True, null=True, verbose_name="Purchase 16")
    purchase17     = models.CharField(max_length=100, blank=True, null=True, verbose_name="Purchase 17")
    purchase18     = models.CharField(max_length=100, blank=True, null=True, verbose_name="Purchase 18")
    purchase19     = models.CharField(max_length=100, blank=True, null=True, verbose_name="Purchase 19")
    purchase20     = models.CharField(max_length=100, blank=True, null=True, verbose_name="Purchase 20")
    purchase21     = models.CharField(max_length=100, blank=True, null=True, verbose_name="Purchase 21")
    purchase22     = models.CharField(max_length=100, blank=True, null=True, verbose_name="Purchase 22")
    purchase23     = models.CharField(max_length=100, blank=True, null=True, verbose_name="Purchase 23")
    purchase24     = models.CharField(max_length=100, blank=True, null=True, verbose_name="Purchase 24")

    possess1      = models.CharField(max_length=100, blank=True, null=True, verbose_name="Possess 1")
    possess2      = models.CharField(max_length=100, blank=True, null=True, verbose_name="Possess 2")
    possess3      = models.CharField(max_length=100, blank=True, null=True, verbose_name="Possess 3")
    possess4      = models.CharField(max_length=100, blank=True, null=True, verbose_name="Possess 4")
    possess5      = models.CharField(max_length=100, blank=True, null=True, verbose_name="Possess 5")
    possess6      = models.CharField(max_length=100, blank=True, null=True, verbose_name="Possess 6")
    possess7      = models.CharField(max_length=100, blank=True, null=True, verbose_name="Possess 7")
    possess8      = models.CharField(max_length=100, blank=True, null=True, verbose_name="Possess 8")
    possess9      = models.CharField(max_length=100, blank=True, null=True, verbose_name="Possess 9")
    possess10     = models.CharField(max_length=100, blank=True, null=True, verbose_name="Possess 10")
    possess11     = models.CharField(max_length=100, blank=True, null=True, verbose_name="Possess 11")
    possess12     = models.CharField(max_length=100, blank=True, null=True, verbose_name="Possess 12")
    possess13     = models.CharField(max_length=100, blank=True, null=True, verbose_name="Possess 13")
    possess14     = models.CharField(max_length=100, blank=True, null=True, verbose_name="Possess 14")
    possess15     = models.CharField(max_length=100, blank=True, null=True, verbose_name="Possess 15")
    possess16     = models.CharField(max_length=100, blank=True, null=True, verbose_name="Possess 16")
    possess17     = models.CharField(max_length=100, blank=True, null=True, verbose_name="Possess 17")
    possess18     = models.CharField(max_length=100, blank=True, null=True, verbose_name="Possess 18")
    possess19     = models.CharField(max_length=100, blank=True, null=True, verbose_name="Possess 19")
    possess20     = models.CharField(max_length=100, blank=True, null=True, verbose_name="Possess 20")
    possess21     = models.CharField(max_length=100, blank=True, null=True, verbose_name="Possess 21")
    possess22     = models.CharField(max_length=100, blank=True, null=True, verbose_name="Possess 22")
    possess23     = models.CharField(max_length=100, blank=True, null=True, verbose_name="Possess 23")
    possess24     = models.CharField(max_length=100, blank=True, null=True, verbose_name="Possess 24")

    old_serial_no_1  =models.CharField(max_length=100, blank=True, null=True, verbose_name="Old Serial No 1")
    old_serial_no_2  =models.CharField(max_length=100, blank=True, null=True, verbose_name="Old Serial No 2")
    old_serial_no_3  =models.CharField(max_length=100, blank=True, null=True, verbose_name="Old Serial No 3")
    old_serial_no_4  =models.CharField(max_length=100, blank=True, null=True, verbose_name="Old Serial No 4")
    old_serial_no_5  =models.CharField(max_length=100, blank=True, null=True, verbose_name="Old Serial No 5")
    old_serial_no_6  =models.CharField(max_length=100, blank=True, null=True, verbose_name="Old Serial No 6")
    old_serial_no_7  =models.CharField(max_length=100, blank=True, null=True, verbose_name="Old Serial No 7")
    old_serial_no_8  =models.CharField(max_length=100, blank=True, null=True, verbose_name="Old Serial No 8")
    old_serial_no_9  =models.CharField(max_length=100, blank=True, null=True, verbose_name="Old Serial No 9")
    old_serial_no_10 =models.CharField(max_length=100, blank=True, null=True, verbose_name="Old Serial No 10")
    old_serial_no_11 =models.CharField(max_length=100, blank=True, null=True, verbose_name="Old Serial No 11")
    old_serial_no_12 =models.CharField(max_length=100, blank=True, null=True, verbose_name="Old Serial No 12")
    old_serial_no_13 =models.CharField(max_length=100, blank=True, null=True, verbose_name="Old Serial No 13")
    old_serial_no_14 =models.CharField(max_length=100, blank=True, null=True, verbose_name="Old Serial No 14")
    old_serial_no_15 =models.CharField(max_length=100, blank=True, null=True, verbose_name="Old Serial No 15")
    old_serial_no_16 =models.CharField(max_length=100, blank=True, null=True, verbose_name="Old Serial No 16")
    old_serial_no_17 =models.CharField(max_length=100, blank=True, null=True, verbose_name="Old Serial No 17")
    old_serial_no_18 =models.CharField(max_length=100, blank=True, null=True, verbose_name="Old Serial No 18")
    old_serial_no_19 =models.CharField(max_length=100, blank=True, null=True, verbose_name="Old Serial No 19")
    old_serial_no_20 =models.CharField(max_length=100, blank=True, null=True, verbose_name="Old Serial No 20")
    old_serial_no_21 =models.CharField(max_length=100, blank=True, null=True, verbose_name="Old Serial No 21")
    old_serial_no_22 =models.CharField(max_length=100, blank=True, null=True, verbose_name="Old Serial No 22")
    old_serial_no_23 =models.CharField(max_length=100, blank=True, null=True, verbose_name="Old Serial No 23")
    old_serial_no_24 =models.CharField(max_length=100, blank=True, null=True, verbose_name="Old Serial No 24")

    storage1      = models.CharField(max_length=100, blank=True, null=True, verbose_name="Storage 1")
    storage2      = models.CharField(max_length=100, blank=True, null=True, verbose_name="Storage 2")
    storage3      = models.CharField(max_length=100, blank=True, null=True, verbose_name="Storage 3")
    storage4      = models.CharField(max_length=100, blank=True, null=True, verbose_name="Storage 4")
    storage5      = models.CharField(max_length=100, blank=True, null=True, verbose_name="Storage 5")
    storage6      = models.CharField(max_length=100, blank=True, null=True, verbose_name="Storage 6")
    storage7      = models.CharField(max_length=100, blank=True, null=True, verbose_name="Storage 7")
    storage8      = models.CharField(max_length=100, blank=True, null=True, verbose_name="Storage 8")
    storage9      = models.CharField(max_length=100, blank=True, null=True, verbose_name="Storage 9")
    storage10     = models.CharField(max_length=100, blank=True, null=True, verbose_name="Storage 10")
    storage11     = models.CharField(max_length=100, blank=True, null=True, verbose_name="Storage 11")
    storage12     = models.CharField(max_length=100, blank=True, null=True, verbose_name="Storage 12")
    storage13     = models.CharField(max_length=100, blank=True, null=True, verbose_name="Storage 13")
    storage14     = models.CharField(max_length=100, blank=True, null=True, verbose_name="Storage 14")
    storage15     = models.CharField(max_length=100, blank=True, null=True, verbose_name="Storage 15")
    storage16     = models.CharField(max_length=100, blank=True, null=True, verbose_name="Storage 16")
    storage17     = models.CharField(max_length=100, blank=True, null=True, verbose_name="Storage 17")
    storage18     = models.CharField(max_length=100, blank=True, null=True, verbose_name="Storage 18")
    storage19     = models.CharField(max_length=100, blank=True, null=True, verbose_name="Storage 19")
    storage20     = models.CharField(max_length=100, blank=True, null=True, verbose_name="Storage 20")
    storage21     = models.CharField(max_length=100, blank=True, null=True, verbose_name="Storage 21")
    storage22     = models.CharField(max_length=100, blank=True, null=True, verbose_name="Storage 22")
    storage23     = models.CharField(max_length=100, blank=True, null=True, verbose_name="Storage 23")
    storage24     = models.CharField(max_length=100, blank=True, null=True, verbose_name="storage 24")

    polarity15    = models.CharField(max_length=20, blank=True, null=True)
    polarity16    = models.CharField(max_length=20, blank=True, null=True)
    polarity17    = models.CharField(max_length=20, blank=True, null=True)
    polarity18    = models.CharField(max_length=20, blank=True, null=True)
    polarity19    = models.CharField(max_length=20, blank=True, null=True)
    polarity20    = models.CharField(max_length=20, blank=True, null=True)
    polarity21    = models.CharField(max_length=20, blank=True, null=True)
    polarity22    = models.CharField(max_length=20, blank=True, null=True)
    polarity23    = models.CharField(max_length=20, blank=True, null=True)
    polarity24    = models.CharField(max_length=20, blank=True, null=True) 

    old_serial_no_sp1 = models.CharField(max_length=100, blank=True, null=True, verbose_name="Old Spare Serial No 1") 
    old_serial_no_sp2 = models.CharField(max_length=100, blank=True, null=True, verbose_name="Old Spare Serial No 2")
    old_serial_no_sp3 = models.CharField(max_length=100, blank=True, null=True, verbose_name="Old Spare Serial No 3")

    tx37            =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    tx38            =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    tx39            =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    tx40            =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    tx41            =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    tx42            =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
  
    rx37            =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx38            =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx39            =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx40            =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx41            =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx42            =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)

    tx37_min        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    tx38_min        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    tx39_min        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    tx40_min        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    tx41_min        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    tx42_min        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    
    rx37_min        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx38_min        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx39_min        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx40_min        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx41_min        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx42_min        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx42_min        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)

    tx37_max        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    tx38_max        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    tx39_max        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    tx40_max        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    tx41_max        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    tx42_max        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    
    rx37_max        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx38_max        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx39_max        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx40_max        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx41_max        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx42_max        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    rx42_max        =models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True) 
    
    capacity      = models.CharField(max_length=100, blank=True, null=True, verbose_name="Capacity")

    old_make_1    = models.CharField(max_length=60, blank=True, null=True, verbose_name="Old Make/Model1")
    old_make_2    = models.CharField(max_length=60, blank=True, null=True, verbose_name="Old Make/Model2")
    old_make_3    = models.CharField(max_length=60, blank=True, null=True, verbose_name="Old Make/Model3")
    old_make_4    = models.CharField(max_length=60, blank=True, null=True, verbose_name="Old Make/Model4")
    old_make_5    = models.CharField(max_length=60, blank=True, null=True, verbose_name="Old Make/Model5")
    old_make_6    = models.CharField(max_length=60, blank=True, null=True, verbose_name="Old Make/Model6")
    old_make_7    = models.CharField(max_length=60, blank=True, null=True, verbose_name="Old Make/Model7")
    old_make_8    = models.CharField(max_length=60, blank=True, null=True, verbose_name="Old Make/Model8")
    old_make_9    = models.CharField(max_length=60, blank=True, null=True, verbose_name="Old Make/Model9")
    old_make_10   = models.CharField(max_length=60, blank=True, null=True, verbose_name="Old Make/Model10")
    old_make_11   = models.CharField(max_length=60, blank=True, null=True, verbose_name="Old Make/Model11")
    old_make_12   = models.CharField(max_length=60, blank=True, null=True, verbose_name="Old Make/Model12")
    old_make_13    = models.CharField(max_length=60, blank=True, null=True, verbose_name="Old Make/Model13")
    old_make_14    = models.CharField(max_length=60, blank=True, null=True, verbose_name="Old Make/Model14")
    old_make_15    = models.CharField(max_length=60, blank=True, null=True, verbose_name="Old Make/Model15")
    old_make_16    = models.CharField(max_length=60, blank=True, null=True, verbose_name="Old Make/Model16")
    old_make_17    = models.CharField(max_length=60, blank=True, null=True, verbose_name="Old Make/Model17")
    old_make_18    = models.CharField(max_length=60, blank=True, null=True, verbose_name="Old Make/Model18")
    old_make_19    = models.CharField(max_length=60, blank=True, null=True, verbose_name="Old Make/Model19")
    old_make_20    = models.CharField(max_length=60, blank=True, null=True, verbose_name="Old Make/Model20")
    old_make_21    = models.CharField(max_length=60, blank=True, null=True, verbose_name="Old Make/Model21")
    old_make_22    = models.CharField(max_length=60, blank=True, null=True, verbose_name="Old Make/Model22")
    old_make_23    = models.CharField(max_length=60, blank=True, null=True, verbose_name="Old Make/Model23")
    old_make_24    = models.CharField(max_length=60, blank=True, null=True, verbose_name="Old Make/Model24")
    old_make_SP1    = models.CharField(max_length=60, blank=True, null=True, verbose_name="Old Make/Modelsp1")
    old_make_SP2    = models.CharField(max_length=60, blank=True, null=True, verbose_name="Old Make/Modelsp2")
    old_make_SP3    = models.CharField(max_length=60, blank=True, null=True, verbose_name="Old Make/Modelsp3")
    old_sitename    = models.CharField(max_length=300, blank=True, null=True, verbose_name="Old Site")
   
    philaddress     = models.ForeignKey(PhilAddress,  blank=True, null=True, on_delete=models.SET_NULL)
    carrierFK       = models.ForeignKey(Carrier, verbose_name='Carrier',  blank=True, null=True, on_delete=models.SET_NULL) 
    logbook_cn      = models.CharField(null=True, blank=True, max_length=30,verbose_name = 'Logbook CN')
    record_cn       = models.CharField(null=True, blank=True, max_length=30,verbose_name = 'Record CN') 
    storage_all     = models.CharField(max_length=100, blank=True, null=True, verbose_name="Storage All")
    purchase_all    = models.CharField(max_length=100, blank=True, null=True, verbose_name="Purchase All")
    possess_all     = models.CharField(max_length=100, blank=True, null=True, verbose_name="Possess All")
    old_make_all    = models.CharField(max_length=150, blank=True, null=True, verbose_name="Old Make/Model All")

    class Meta:
        db_table            = u'latest_rsl'
        verbose_name_plural = "Latest RSLs"
        verbose_name        = "Latest RSL"
        ordering            = ["issued"]
    def __unicode__(self):
        return self.rslno
#############
# Receive the pre_delete signal and delete the file associated with the model instance.
#ok!
def cfile_counter(c):
    if c < 10:
        c = '000'+str(c)
    elif c < 100:
        c = '00'+str(c)
    elif c < 1000:
        c = '0'+str(c)
    else:
        c = str(c)
    return c
#ok!
def cmonth_counter():
    now = make_aware(datetime.now(),get_default_timezone())
  
    m = now.month
    if m < 10:
        m = '0'+str(m)
    else:
        m = str(m)
    return m
#ok!
def check_controlNo(queryset):
    first_4 = queryset.controlNo[0:4]
    next_3  = queryset.controlNo[5:7]

    if first_4.isdigit():
        qry_year = int(first_4)
        #print 'qry_year is true: ', qry_year
    else:
        qry_year = datetime.now().year    
        #print 'qry_year is false: ', qry_year

    if next_3.isdigit():
        qry_month = int(next_3)
        #print 'qry_month is true: ', qry_month
    else:
        qry_month = datetime.now().month
        #print 'qry_month is false: ', qry_month
    #print 'year: ', qry_year
    #print 'month', qry_month
    now = make_aware(datetime.now(),get_default_timezone())
    #print 'now.year: ', now.year
    #print 'now.month: ', now.month   
    if now.year == qry_year and now.month == qry_month:   # check if its a new month
        next_counter = int(queryset.controlNo[8:12]) +1
    else:
        next_counter = 0
    #print 'next_counter', next_counter
    return next_counter
#ok!
@receiver (pre_save, sender=Letter_LogBook)
def Letter_controlNo(sender, instance, **kwargs):   
    try:
        qry = LogBook.logbook_objects.all()
        #print 'qry :', qry
        qry2 = Letter_LogBook.logbook_objects.all()    
        #print 'qry2 :', qry2
        logbook_cn = check_controlNo(qry)
        #print 'logbook_cn: ', logbook_cn
        letter_cn = check_controlNo(qry2)
        #print 'letter_cn: ', logbook_cn
    except ObjectDoesNotExist:
        #print "Either LogBook or Letter doesn't exist."
        #qry = LogBook.logbook_objects.none()        
        logbook_cn = 0
        letter_cn = 0

    if logbook_cn > letter_cn:                # choose what control no is the latest
        next_counter = logbook_cn             # between logbook and letter    
        #print 'logbook_cn > letter_cn'
    elif logbook_cn < letter_cn:              # choose what control no is the latest
        next_counter = letter_cn
        #print 'logbook_cn < letter_cn'
    elif logbook_cn == letter_cn and logbook_cn > 0:              # choose what control no is the latest
        next_counter = letter_cn+1
        #print 'logbook_cn == letter_cn and logbook_cn > 0'
    else:
        next_counter = 0
        #print 'next_counter = 0'
    #print 'next_counter: ', next_counter
    if not instance.pk:       
        c = cfile_counter(next_counter)       # format the counter
        # return a formated Control No
        instance.controlNo = str(datetime.now().year)+'-'+cmonth_counter()+'-'+c
#ok!
@receiver (pre_save, sender=LogBook)
def LogBook_controlNo(sender, instance, **kwargs):   
    now = make_aware(datetime.now(),get_default_timezone())    
    try:
        qry = LogBook.logbook_objects.all()
        qry2 = Letter_LogBook.logbook_objects.all()    
        logbook_cn = check_controlNo(qry)
        letter_cn = check_controlNo(qry2)
    except ObjectDoesNotExist:
        print "Either LogBook or Letter doesn't exist."
        qry = LogBook.objects.none()        
        logbook_cn = 0
        letter_cn = 0
    
    if logbook_cn > letter_cn:                # choose what control no is the latest
        next_counter = logbook_cn             # between logbook and letter
    elif logbook_cn < letter_cn:              # choose what control no is the latest
        next_counter = letter_cn
    elif logbook_cn == letter_cn and logbook_cn > 0:              # choose what control no is the latest
        next_counter = letter_cn+1
    else:
        next_counter = 0   
    #print 'next_counter', next_counter
    apptype = instance.transtype.replace('NEW','').replace('//','/')
    #print 'apptype: ', apptype
    if not instance.pk: 
        c = cfile_counter(next_counter)       # format the counter
        # return a formated Control No
        instance.controlNo = str(now.year)+'-'+cmonth_counter()+'-'+c+'-'+apptype    
    else:       # during update
        instance.stm_count = Statements.objects.filter(logbook=instance.pk).count()
        # added 07-23-2014      
        if instance.status  == 'CHECKING REQUIREMENTS':
            instance.encoder_status = 2;
            instance.engr_status  = 0.1;
            instance.chief_status = 2;        
        elif instance.status == 'ISSUANCE OF SOA':
            instance.encoder_status = 2;
            instance.engr_status  = 0.2;
            instance.chief_status = 2;        
        elif instance.status == 'PAYMENT':
            instance.encoder_status = 2;
            instance.engr_status  = 1.5;
            instance.chief_status = 0.1;          
        elif instance.status == 'EVALUATION':
            instance.encoder_status = 2;
            instance.engr_status  = 0.4;
            instance.chief_status = 2;
        elif instance.status == 'ENDORSEMENT': 
            instance.encoder_status = 2;
            instance.engr_status  = 0.5;
            instance.chief_status = 0.2;          
        elif instance.status == 'ENCODING':
            instance.encoder_status = 1;
            instance.engr_status  = 2;
            instance.chief_status = 2;          
        elif instance.status == 'REVIEW':
            instance.encoder_status = 1.5;
            instance.engr_status = 0.7;
            instance.chief_status = 2;              
        elif instance.status == 'SIGNATURE':
            instance.encoder_status = 3;
            instance.engr_status  = 0.8;
            instance.chief_status = 0.3;
        elif instance.status == 'CHIEF SIGNATURE':
            instance.encoder_status = 3;
            instance.engr_status  = 2.5;
            instance.chief_status = 0.4;
        elif instance.status == 'DIRECTOR SIGNATURE':          
            instance.encoder_status = 3;
            instance.engr_status  = 2.7;
            instance.chief_status = 0.5;
        elif instance.status == 'CASHIER STAMP':
            instance.encoder_status = 3;
            instance.engr_status  = 2.9;
            instance.chief_status = 0.6;
        elif instance.status == 'RELEASE TO SECRETARIAT':      
            instance.encoder_status = 3;
            instance.engr_status  = 0.9;
            instance.chief_status = 0.7;          
        elif instance.status == 'TASK COMPLETED':            
            instance.encoder_status = 4;
            instance.engr_status  = 4;
            instance.chief_status = 4;
        # end added 07-23-2014        
#ok!
# temporary disable while uploading previous SOA
@receiver(pre_save, sender=SOA)
def SOA_controlNo(sender, instance, **kwargs):    
    d = instance.no_years * 365
    instance.validity_to = instance.validity_from+timedelta(days=int(d))

    c = SOA.soa_objects.count()
    if not instance.pk:    
        c = cfile_counter(c)
        if not instance.soa_code:
            # return a formated Control No
            instance.soa_code = str(datetime.now().year)+'-'+cmonth_counter()+'-'+c

@receiver(post_save, sender=SOA_detail)
def compute_suf(sender, instance, **kwargs):
    #print 'instance.soa :', instance.soa.id
    #print 'instance.suf_fee :', instance.suf_fee
    try:
        soa_instance = SOA.objects.get(pk=instance.soa.id)
        #print 'SOA object found with suf_fees :', soa_instance.suf_fees        
    except:
        print 'compute_suf: No SOA found'
        soa_instance = SOA.objects.none()

    detail_suf_sum = SOA_detail.objects.filter(soa=instance.soa.id).aggregate(Sum('suf_fee'))
    #if soa_instance.suf_fees != detail_suf_sum['suf_fee__sum']:
    soa_instance.suf_fees = detail_suf_sum['suf_fee__sum']
    #print 'Assigning new suf_fees :', soa_instance.suf_fees
    soa_instance.save()
    #print 'Saving new suf_fees'

@receiver (post_save, sender=KPI)
def staff_KPI(sender, instance, **kwargs):     
    staff_count = 0
    staff_target= 0
    staff_list   = NAFD_User.objects.filter(groups__name='NAFD Personnel').filter(Q(groups__name='Encoder')|Q(groups__name='Engr')) 
    staff_count  = staff_list.count()
    #print 'Staff count: ', staff_count
    ## find current kpi target
    try: 
        nafd_kpitarget = KPI.objects.get(current_year=datetime.now().year)
        staff_target   = nafd_kpitarget.target
        #print 'NAFD KPI target', nafd_kpitarget.target
    except ObjectDoesNotExist:
        staff_target = 0
        #print 'Object Does not Exist: staff target = 0'
    
    for staff in staff_list:
        staff_rec = NAFD_User.objects.get(pk=staff.id)
        #print 'staff_rec id: ', staff_rec.kpi_target
        staff_rec.kpi_target = staff_target/staff_count
        #print 'staff kpi_target: ', staff_rec.kpi_target
        staff_rec.save()

''' depreciated in Django 1.5
class UserProfile(models.Model):
    # Required field
    user = models.OneToOneField(User)
    # Other Fields
    code_name = models.CharField(max_length=10, blank=True, null=True)
    kpi_target= models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    foryear   = models.DecimalField(max_digits=4, decimal_places=0, blank=True, null=True)

    def __unicode__(self):
        return self.code_name
'''
#ok!
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        NAFD_User.objects.create(pk=instance)

post_save.connect(create_user_profile, sender=settings.AUTH_USER_MODEL)

@receiver (pre_save, sender=LatestRsl_v2)
def LRsl_controlNo(sender, instance, **kwargs):
    if instance.sitename.address:
        print 'province: ', instance.sitename.address.province     
        sitename_province =instance.sitename.address.province  

@receiver (post_save, sender=LogBook_audit)
def LogBook_audit_duedate(sender, instance, **kwargs): 
    # update is_ontime column  
    # if task completed status <= to due date
    # it's ontime else otherwise
    print 'instance.status :', instance.status    
    if instance.status == 'TASK COMPLETED':
        # find due date    
        logbook = LogBook.objects.get(pk=instance.logbook_id)
        print 'logbook.due_date: ', logbook.due_date
        if instance.log_in <= logbook.due_date:
            print 'The task completed on time'
            instance.is_ontime = True
        else:
            print 'The task completed NOT on time'
            instance.is_ontime = False
    

