########################################################################
'''
Project Name: Radio Station License Report
Date Done   : January 8, 2013
Purpose     : To create a pdf report like what can be seen in Radio
              Station License Form. This will help view the data more
              easily than in django standard admin form.
              Can also be used to print the report directly to the said
              form.
Author      : Albert James Lopez
Designation : On-Job-Training (November 2012 - March 2013
Email       : ajslopez666@yahoo.com

'''
########################################################################

try:
    from DICSD import settings
except ImportError:
    from nafd_proj import settings
    
from io import BytesIO
from reportlab.pdfgen import canvas
from django.http import HttpResponse

#to be transfer to rsldraft once done!#
try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
from django.utils import encoding, formats
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import inch
from reportlab.lib.utils import ImageReader
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Paragraph, Frame, Table
from reportlab.platypus import BaseDocTemplate, PageTemplate, Paragraph, Frame

#added recently 01/03/2012
from reportlab.platypus import NextPageTemplate, PageBreak
from reportlab.lib.pagesizes import letter

#added 01/06/2013
import re
#added 01/07/2013
import string
import reportlab.rl_config
reportlab.rl_config.warnOnMissingFontGlyphs = 0
pdfmetrics.registerFont(TTFont('arial', 'arial.ttf'))
pdfmetrics.registerFont(TTFont('arialbd', 'arialbd.ttf'))

import reportlab.rl_config
pdfmetrics.registerFont(TTFont('Verdana', 'Verdana.ttf'))
pdfmetrics.registerFont(TTFont('VerdanaB', 'VerdanaB.ttf'))

##added 09/03/2013
from ccad.models import *
from ccad.forms import *
import autocomplete_light
from django.shortcuts import redirect
from django.conf.urls import patterns, include, url
from django.forms.formsets import all_valid
from django.contrib.admin import widgets, helpers
from django.utils.translation import ugettext as _
from django.utils.encoding import force_unicode
from django.contrib.admin.options import csrf_protect_m
from django.db import transaction
import logging
log = logging.getLogger(__name__)

def convert_data_to_string(*obj):
    for i in obj:
        name = re.sub('obj.','',i)
        new_name = encoding.smart_unicode(i, encoding='utf-8', strings_only=False, errors='strict')
        return {name: new_name,}

def convert_data_to_uni(obj):
        new_name = encoding.smart_unicode(obj, encoding='utf-8', strings_only=False, errors='strict')
        return new_name

def export_as_json(modeladmin, request, queryset):
    response = HttpResponse(mimetype="text/javascript")
    serializers.serialize("json", queryset, stream=response)
    return response

def export_selected_objects(modeladmin, request, queryset):
    selected = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
    ct = ContentType.objects.get_for_model(queryset.model)
    return HttpResponseRedirect("/export/?ct=%s&ids=%s" % (ct.pk, ",".join(selected)))

def make_published(modeladmin, request, queryset):
    queryset.update(status='p')
make_published.short_description = "Mark selected stories as published"

def print_preview(modeladmin, request, queryset):
    response = HttpResponse(mimetype='application/pdf')
    response['Content-Disposition'] = 'filename = testframe.pdf'

    buffer = StringIO()
    c = canvas.Canvas(buffer)
    doc = BaseDocTemplate(buffer, showBoundary=1, leftMargin= 0.1*inch, rightMargin= 0.1*inch,
                     topMargin= 0.1*inch, bottomMargin= 0.1*inch)   

    story = []
    #Set needed Font Style    
    styles=getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Verdana6', fontName= 'Verdana', fontSize= 6, alignment= 1))
    styles.add(ParagraphStyle(name='Verdana6_left', fontName= 'Verdana', fontSize= 6))
    styles.add(ParagraphStyle(name='Verdana8', fontName= 'Verdana', fontSize= 8, alignment= 1))
    styles.add(ParagraphStyle(name='Verdana8_left', fontName= 'Verdana', fontSize= 8, wordWrap = True))
    styles.add(ParagraphStyle(name='Verdana9', fontName= 'Verdana', fontSize= 9))
    styles.add(ParagraphStyle(name='Verdana9_right', fontName= 'Verdana', fontSize= 9, alignment = 2))
    styles.add(ParagraphStyle(name='Verdana9_center', fontName= 'Verdana', fontSize= 9, alignment = 1))
    styles.add(ParagraphStyle(name='VerdanaB10', fontName= 'VerdanaB', fontSize= 10))

    #coord adjustment
    x = -0.17
    y = 0.61 #0.67
    #Call-Sign Frame
    callsignfr_height = 0
    callsignfr_y = 0
    #Serial Number coordinate adjustment
    set_loc1 = set_loc2 = set_loc3 = set_loc4 = set_loc5 = set_loc6 = 0
    set1_switch = set2_switch = set3_switch = set4_switch = set5_switch = set6_switch = True
    set1_x = 0.4
    set2_x = 1.7
    set3_x = 3
    set35_x = 3.6
    set4_x = 4.3
    set5_x = 5.6
    set6_x = 6.9
    sn1_only = sn2_only = sn3_only = sn4_only = True
    
    for obj in queryset:  
        #Number Conversion
        new_orno = convert_data_to_uni(obj.or_no)
        new_orno2 = convert_data_to_uni(obj.or_no2)
        new_amt = convert_data_to_uni(obj.amount)
        new_amt2 = convert_data_to_uni(obj.amount2)
        
        # updated 03/25/2013
        objtx1 = convert_data_to_uni(obj.tx1)
        objtx2 = convert_data_to_uni(obj.tx2)
        objtx3 = convert_data_to_uni(obj.tx3)
        objtx4 = convert_data_to_uni(obj.tx4)
        objtx5 = convert_data_to_uni(obj.tx5)
        objtx6 = convert_data_to_uni(obj.tx6)
        objtx7 = convert_data_to_uni(obj.tx7)
        objtx8 = convert_data_to_uni(obj.tx8)
        objtx9 = convert_data_to_uni(obj.tx9)
        objtx10 = convert_data_to_uni(obj.tx10)
        objtx11 = convert_data_to_uni(obj.tx11)
        objtx12 = convert_data_to_uni(obj.tx12)
        objrx1 = convert_data_to_uni(obj.rx1)
        objrx2 = convert_data_to_uni(obj.rx2)
        objrx3 = convert_data_to_uni(obj.rx3)
        objrx4 = convert_data_to_uni(obj.rx4)
        objrx5 = convert_data_to_uni(obj.rx5)
        objrx6 = convert_data_to_uni(obj.rx6)
        objrx7 = convert_data_to_uni(obj.rx7)
        objrx8 = convert_data_to_uni(obj.rx8)
        objrx9 = convert_data_to_uni(obj.rx9)
        objrx10 = convert_data_to_uni(obj.rx10)
        objrx11 = convert_data_to_uni(obj.rx11)
        objrx12 = convert_data_to_uni(obj.rx12)
        # end of update
        
        #Date Conversion
        issued_formatted = formats.date_format(obj.issued, 'DATE_FORMAT')
        validityfrom_formatted = formats.date_format(obj.validity_from, 'DATE_FORMAT')
        validityto_formatted = formats.date_format(obj.validity_to, 'DATE_FORMAT')
        
        new_datepd = convert_data_to_uni(obj.date_paid)
        new_datepd2 = convert_data_to_uni(obj.date_paid2)                
        new_issued = convert_data_to_uni(issued_formatted)
        new_validityfrom = convert_data_to_uni(validityfrom_formatted)
        new_validityto = convert_data_to_uni(validityto_formatted)        

        new_tx1min = encoding.smart_unicode(obj.tx1_min, encoding='utf-8', strings_only=False, errors='strict')
        new_tx1max = encoding.smart_unicode(obj.tx1_max, encoding='utf-8', strings_only=False, errors='strict')
        new_tx2min = encoding.smart_unicode(obj.tx2_min, encoding='utf-8', strings_only=False, errors='strict')
        new_tx2max = encoding.smart_unicode(obj.tx2_max, encoding='utf-8', strings_only=False, errors='strict')
        new_tx3min = encoding.smart_unicode(obj.tx3_min, encoding='utf-8', strings_only=False, errors='strict')
        new_tx3max = encoding.smart_unicode(obj.tx3_max, encoding='utf-8', strings_only=False, errors='strict')
        new_tx4min = encoding.smart_unicode(obj.tx4_min, encoding='utf-8', strings_only=False, errors='strict')
        new_tx4max = encoding.smart_unicode(obj.tx4_max, encoding='utf-8', strings_only=False, errors='strict')
        new_tx5min = encoding.smart_unicode(obj.tx5_min, encoding='utf-8', strings_only=False, errors='strict')
        new_tx5max = encoding.smart_unicode(obj.tx5_max, encoding='utf-8', strings_only=False, errors='strict')
        new_tx6min = encoding.smart_unicode(obj.tx6_min, encoding='utf-8', strings_only=False, errors='strict')
        new_tx6max = encoding.smart_unicode(obj.tx6_max, encoding='utf-8', strings_only=False, errors='strict')
        new_tx7min = encoding.smart_unicode(obj.tx7_min, encoding='utf-8', strings_only=False, errors='strict')
        new_tx7max = encoding.smart_unicode(obj.tx7_max, encoding='utf-8', strings_only=False, errors='strict')
        new_tx8min = encoding.smart_unicode(obj.tx8_min, encoding='utf-8', strings_only=False, errors='strict')
        new_tx8max = encoding.smart_unicode(obj.tx8_max, encoding='utf-8', strings_only=False, errors='strict')
        new_tx9min = encoding.smart_unicode(obj.tx9_min, encoding='utf-8', strings_only=False, errors='strict')
        new_tx9max = encoding.smart_unicode(obj.tx9_max, encoding='utf-8', strings_only=False, errors='strict')
        new_tx10min = encoding.smart_unicode(obj.tx10_min, encoding='utf-8', strings_only=False, errors='strict')
        new_tx10max = encoding.smart_unicode(obj.tx10_max, encoding='utf-8', strings_only=False, errors='strict')
        new_tx11min = encoding.smart_unicode(obj.tx11_min, encoding='utf-8', strings_only=False, errors='strict')
        new_tx11max = encoding.smart_unicode(obj.tx11_max, encoding='utf-8', strings_only=False, errors='strict')
        new_tx12min = encoding.smart_unicode(obj.tx12_min, encoding='utf-8', strings_only=False, errors='strict')
        new_tx12max = encoding.smart_unicode(obj.tx12_max, encoding='utf-8', strings_only=False, errors='strict')

        new_rx1min = encoding.smart_unicode(obj.rx1_min, encoding='utf-8', strings_only=False, errors='strict')
        new_rx1max = encoding.smart_unicode(obj.rx1_max, encoding='utf-8', strings_only=False, errors='strict')
        new_rx2min = encoding.smart_unicode(obj.rx2_min, encoding='utf-8', strings_only=False, errors='strict')
        new_rx2max = encoding.smart_unicode(obj.rx2_max, encoding='utf-8', strings_only=False, errors='strict')
        new_rx3min = encoding.smart_unicode(obj.rx3_min, encoding='utf-8', strings_only=False, errors='strict')
        new_rx3max = encoding.smart_unicode(obj.rx3_max, encoding='utf-8', strings_only=False, errors='strict')
        new_rx4min = encoding.smart_unicode(obj.rx4_min, encoding='utf-8', strings_only=False, errors='strict')
        new_rx4max = encoding.smart_unicode(obj.rx4_max, encoding='utf-8', strings_only=False, errors='strict')
        new_rx5min = encoding.smart_unicode(obj.rx5_min, encoding='utf-8', strings_only=False, errors='strict')
        new_rx5max = encoding.smart_unicode(obj.rx5_max, encoding='utf-8', strings_only=False, errors='strict')
        new_rx6min = encoding.smart_unicode(obj.rx6_min, encoding='utf-8', strings_only=False, errors='strict')
        new_rx6max = encoding.smart_unicode(obj.rx6_max, encoding='utf-8', strings_only=False, errors='strict')
        new_rx7min = encoding.smart_unicode(obj.rx7_min, encoding='utf-8', strings_only=False, errors='strict')
        new_rx7max = encoding.smart_unicode(obj.rx7_max, encoding='utf-8', strings_only=False, errors='strict')
        new_rx8min = encoding.smart_unicode(obj.rx8_min, encoding='utf-8', strings_only=False, errors='strict')
        new_rx8max = encoding.smart_unicode(obj.rx8_max, encoding='utf-8', strings_only=False, errors='strict')
        new_rx9min = encoding.smart_unicode(obj.rx9_min, encoding='utf-8', strings_only=False, errors='strict')
        new_rx9max = encoding.smart_unicode(obj.rx9_max, encoding='utf-8', strings_only=False, errors='strict')
        new_rx10min = encoding.smart_unicode(obj.rx10_min, encoding='utf-8', strings_only=False, errors='strict')
        new_rx10max = encoding.smart_unicode(obj.rx10_max, encoding='utf-8', strings_only=False, errors='strict')
        new_rx11min = encoding.smart_unicode(obj.rx11_min, encoding='utf-8', strings_only=False, errors='strict')
        new_rx11max = encoding.smart_unicode(obj.rx11_max, encoding='utf-8', strings_only=False, errors='strict')
        new_rx12min = encoding.smart_unicode(obj.rx12_min, encoding='utf-8', strings_only=False, errors='strict')
        new_rx12max = encoding.smart_unicode(obj.rx12_max, encoding='utf-8', strings_only=False, errors='strict')
        
        #Official Reciept frame
        if bool(new_orno) and bool(new_orno2) \
           and not queryset.filter(id=obj.id).only('or_no2').filter(or_no2__exact=None).count():
            ORfr = Frame((1.2+x)*inch, (9.33+y)*inch, 1.5*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
            doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[ORfr]))
            orno = Paragraph(new_orno+' / '+ new_orno2,styles["Verdana9"])
            story.append(orno)
            ORfr.addFromList(story,c)

            #Amount frame here           
            amtfr = Frame((1.2+x)*inch, (9.16+y)*inch, 1.5*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
            doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[amtfr]))
            amt = Paragraph(new_amt+' / '+ new.amt2,styles["Verdana9"])
            story.append(amt)
            amtfr.addFromList(story,c)

            #Date Paid frame
            datepaidfr = Frame((1.2+x)*inch, (8.99+y)*inch, 2*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
            doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[datepaidfr]))
            datepaid = Paragraph(new_datepd +' / '+ new_datepd2 ,styles["Verdana9"])
            story.append(datepaid)
            datepaidfr.addFromList(story,c)
            
        elif bool(new_orno):
            ORfr = Frame((1.2+x)*inch, (9.33+y)*inch, inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
            doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[ORfr]))
            orno = Paragraph(new_orno,styles["Verdana9"])
            story.append(orno)
            ORfr.addFromList(story,c)

            #Amount frame here           
            amtfr = Frame((1.2+x)*inch, (9.16+y)*inch, inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
            doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[amtfr]))
            amt = Paragraph(new_amt,styles["Verdana9"])
            story.append(amt)
            amtfr.addFromList(story,c)

            #Date Paid frame
            datepaidfr = Frame((1.2+x)*inch, (8.99+y)*inch, inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
            doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[datepaidfr]))
            datepaid = Paragraph(new_datepd,styles["Verdana9"])
            story.append(datepaid)
            datepaidfr.addFromList(story,c)

        #License Number frame
        rslnofr = Frame((6.8+x)*inch, (9.4+y)*inch, 1.5*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
        doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[rslnofr]))
        rsl_no = Paragraph(obj.rslno,styles["Verdana9"])
        story.append(rsl_no)
        rslnofr.addFromList(story,c)

        #Date Issued frame
        date_issuedfr = Frame((6.1+x)*inch, (8.9+y)*inch, 1.4*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
        doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[date_issuedfr]))
        date_issued = Paragraph(new_issued,styles["Verdana9"])
        story.append(date_issued)
        date_issuedfr.addFromList(story,c)

        #Carrier frame
        carrierfr = Frame((3.35+x)*inch,(8.55+y)*inch, 4.5*inch, 0.2*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
        doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[carrierfr]))
        carrier = Paragraph(obj.carrier,styles["VerdanaB10"])
        story.append(carrier)
        carrierfr.addFromList(story,c)

        #Lic to Operate frame
        lic_operatefr = Frame((3.2+x)*inch, (8.3+y)*inch, 2*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
        doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[lic_operatefr]))
        lic_operate = Paragraph(obj.lic_to_operate,styles["Verdana9"])
        story.append(lic_operate)
        lic_operatefr.addFromList(story,c)

        if bool(obj.site) and bool(obj.street):
            #Site-Street frame
            if len(obj.site)+ len(obj.street) < 64:
                sitefr = Frame((2.8+x)*inch, (8.05+y)*inch, 5.2*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
                doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[sitefr]))
                site = Paragraph(obj.site +' - '+ obj.street,styles["Verdana9"])
                story.append(site)
                sitefr.addFromList(story,c)
            else:
                sitefr = Frame((2.8+x)*inch, (8.05+y)*inch, 5.2*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
                doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[sitefr]))
                site = Paragraph(obj.site +' - '+ obj.street,styles["Verdana9"])
                story.append(site)
                sitefr.addFromList(story,c)

            #City frame
            cityfr = Frame((2.8+x)*inch, (7.88+y)*inch, 5.2*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
            doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[cityfr]))
            city = Paragraph(obj.city + ', '+ obj.province + ', ' + obj.region,styles["Verdana9"])
            story.append(city)
            cityfr.addFromList(story,c)

        elif bool(obj.site) and not(obj.street) and bool(obj.city):
            #Site-City frame
            sitefr = Frame((2.8+x)*inch, (8.05+y)*inch, 5.2*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
            doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[sitefr]))
            #add Province name if space available
            if 64 - len(obj.province) <= len(obj.site) + len(obj.city):
                site = Paragraph(obj.site +' - '+ obj.city + ', ' + obj.province +', '+ obj.region,styles["Verdana9"])
            else:
                site = Paragraph(obj.site +' - '+ obj.city, styles["Verdana9"])
            story.append(site)
            sitefr.addFromList(story,c)

        elif bool(obj.site) and not(obj.street) and not bool(obj.city) and bool(obj.province):
            #Site-Province frame
            sitefr = Frame((2.8+x)*inch, (8.05+y)*inch, 5.2*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
            doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[sitefr]))
            #add Province name if space available           
            site = Paragraph(obj.site +' - '+ obj.province +', '+ obj.region,styles["Verdana9"])            
            story.append(site)
            sitefr.addFromList(story,c)
            
        else:
            #Site frame
            sitefr = Frame((2.8+x)*inch, (8.05+y)*inch, 5.2*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
            doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[sitefr]))
            site = Paragraph(obj.site +' - '+ obj.region,styles["Verdana9"])
            story.append(site)
            sitefr.addFromList(story,c)

        #Longitude frame
        longitudefr = Frame((1.05+x)*inch, (7.35+y)*inch, 1.8*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
        doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[longitudefr]))
        longitude = Paragraph(obj.longitude,styles["Verdana9_right"])
        story.append(longitude)
        longitudefr.addFromList(story,c)

        #Latitude frame
        latitudefr = Frame((1.05+x)*inch, (7.1+y)*inch, 1.8*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
        doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[latitudefr]))
        latitude = Paragraph(obj.latitude,styles["Verdana9_right"])
        story.append(latitude)
        latitudefr.addFromList(story,c)

        #Class of Station frame
        class_stationfr = Frame((5.85+x)*inch, (7.55+y)*inch, 1.95*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
        doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[class_stationfr]))
        class_station = Paragraph(obj.class_of_station,styles["Verdana9_center"])
        story.append(class_station)
        class_stationfr.addFromList(story,c)

        
        #Nature of Service frame
        nosfr = Frame((5.85+x)*inch, (7.3+y)*inch, 1.95*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
        doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[nosfr]))
        nature_service = Paragraph(obj.nature_of_service,styles["Verdana9_center"])
        story.append(nature_service)
        nosfr.addFromList(story,c)

        #Call-Sign frame
        if len(obj.callsign) <= 29:
            callsignfr_height = 0.17
            callsignfr_y = 0
        else:
            callsignfr_height = 0.34
            callsignfr_y = -0.17
        callsignfr = Frame((5.4+x)*inch, (callsignfr_y+7.05+y)*inch, 2.3*inch, callsignfr_height*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
        doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[callsignfr]))
        call_sign = Paragraph(obj.callsign,styles["Verdana9_center"])
        story.append(call_sign)
        callsignfr.addFromList(story,c)          
        

        #Hours of Operation frame
        hours_opefr = Frame((5.8+x)*inch, (6.8+y)*inch, 1.9*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
        doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[hours_opefr]))
        hours_ope = Paragraph(' ',styles["Verdana9"])
        story.append(hours_ope)
        hours_opefr.addFromList(story,c)

        #Point of Service frame
        pts_svcfr = Frame((3.65+x)*inch, (6.45+y)*inch, 4.25*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
        doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[pts_svcfr]))
        if bool(obj.ptsvc):
            pts_svc = Paragraph(string.capwords(obj.ptsvc),styles["Verdana9"])
        else:
            pts_svc = Paragraph(string.capwords(obj.ptsvc_callsign),styles["Verdana9"])
        story.append(pts_svc)
        pts_svcfr.addFromList(story,c)

        if bool(obj.tx1):            
            #Tx1 frame
            tx1_fr = Frame((1+x)*inch, (5.58+y)*inch, 0.7*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
            doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[tx1_fr]))
            tx1 = Paragraph(objtx1,styles["Verdana8"])
            story.append(tx1)
            tx1_fr.addFromList(story,c)
            
        elif bool(obj.tx1_min):
            #Tx1 min to max frame
            tx1_min_fr = Frame((1+x)*inch, (5.58+y)*inch, 0.7*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
            doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[tx1_min_fr]))
            tx1_min = Paragraph(new_tx1min +' - '+new_tx1max ,styles["Verdana6"])
            story.append(tx1_min)
            tx1_min_fr.addFromList(story,c)

        if bool(obj.tx2):
            #Tx2 frame
            tx2_fr = Frame((1+x)*inch, (5.41+y)*inch, 0.7*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
            doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[tx2_fr]))
            tx2 = Paragraph(objtx2,styles["Verdana8"])
            story.append(tx2)
            tx2_fr.addFromList(story,c)
            
        elif bool(obj.tx2_min):
            #Tx2 min to max frame
            tx2_min_fr = Frame((1+x)*inch, (5.41+y)*inch, 0.7*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
            doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[tx2_min_fr]))
            tx2_min = Paragraph(new_tx2min +' - '+new_tx2max,styles["Verdana6"])
            story.append(tx2_min)
            tx2_min_fr.addFromList(story,c)

        if bool(obj.tx3):
            #Tx3 frame
            tx3_fr = Frame((1+x)*inch, (5.24+y)*inch, 0.7*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
            doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[tx3_fr]))
            tx3 = Paragraph(objtx3,styles["Verdana8"])
            story.append(tx3)
            tx3_fr.addFromList(story,c)
            
        elif bool(obj.tx3_min):
            #Tx3 min to max frame
            tx3_min_fr = Frame((1+x)*inch, (5.24+y)*inch, 0.7*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
            doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[tx3_min_fr]))
            tx3_min = Paragraph(new_tx3min +' - '+new_tx3max,styles["Verdana6"])
            story.append(tx3_min)
            tx3_min_fr.addFromList(story,c)

        if bool(obj.tx4):
            #Tx4 frame
            tx4_fr = Frame((1+x)*inch, (5.07+y)*inch, 0.7*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
            doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[tx4_fr]))
            tx4 = Paragraph(objtx4,styles["Verdana8"])
            story.append(tx4)
            tx4_fr.addFromList(story,c)
            
        elif bool(obj.tx4_min):           
            #Tx4 min to max frame
            tx4_min_fr = Frame((1+x)*inch, (5.07+y)*inch, 0.7*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
            doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[tx4_min_fr]))
            tx4_min = Paragraph(new_tx4min +' - '+new_tx4max,styles["Verdana6"])
            story.append(tx4_min)
            tx4_min_fr.addFromList(story,c)

        if bool(obj.tx5):    
            #Tx5 frame
            tx5_fr = Frame((1+x)*inch, (4.9+y)*inch, 0.7*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
            doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[tx5_fr]))
            tx5 = Paragraph(objtx5,styles["Verdana8"])
            story.append(tx5)
            tx5_fr.addFromList(story,c)

        elif bool(obj.tx5_min):
            #Tx5 min to max frame
            tx5_min_fr = Frame((1+x)*inch, (4.9+y)*inch, 0.7*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
            doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[tx5_min_fr]))
            tx5_min = Paragraph(new_tx5min +' - '+new_tx5max,styles["Verdana6"])
            story.append(tx5_min)
            tx5_min_fr.addFromList(story,c)

        if bool(obj.tx6):
            #Tx6 frame
            tx6_fr = Frame((1+x)*inch, (4.73+y)*inch, 0.7*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
            doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[tx6_fr]))
            tx6 = Paragraph(objtx6,styles["Verdana8"])
            story.append(tx6)
            tx6_fr.addFromList(story,c)
            
        elif bool(obj.tx6_min):
            #Tx6min to max frame
            tx6_min_fr = Frame((1+x)*inch, (4.73+y)*inch, 0.7*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
            doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[tx6_min_fr]))
            tx6_min = Paragraph(new_tx6min +' - '+new_tx6max,styles["Verdana6"])
            story.append(tx6_min)
            tx6_min_fr.addFromList(story,c)

        if bool(obj.tx7):
            #Tx7 frame
            tx7_fr = Frame((1+x)*inch, (4.56+y)*inch, 0.7*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
            doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[tx7_fr]))
            tx7 = Paragraph(objtx7,styles["Verdana8"])
            story.append(tx7)
            tx7_fr.addFromList(story,c)

        elif bool(obj.tx7_min):
            #Tx7 min to max frame
            tx7_min_fr = Frame((1+x)*inch, (4.56+y)*inch, 0.7*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
            doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[tx7_min_fr]))
            tx7_min = Paragraph(new_tx7min +' - '+new_tx7max,styles["Verdana6"])
            story.append(tx7_min)
            tx7_min_fr.addFromList(story,c)

        if bool(obj.tx8):
            #Tx8 frame
            tx8_fr = Frame((1+x)*inch, (4.39+y)*inch, 0.7*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
            doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[tx8_fr]))
            tx8 = Paragraph(objtx8,styles["Verdana8"])
            story.append(tx8)
            tx8_fr.addFromList(story,c)

        elif bool(obj.tx8_min):
            #Tx8 min to max frame
            tx8_min_fr = Frame((1+x)*inch, (4.39+y)*inch, 0.7*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
            doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[tx8_min_fr]))
            tx8_min = Paragraph(new_tx8min +' - '+new_tx8max,styles["Verdana6"])
            story.append(tx8_min)
            tx8_min_fr.addFromList(story,c)

        if bool(obj.tx9):
            #Tx9 frame
            tx9_fr = Frame((1+x)*inch, (4.22+y)*inch, 0.7*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
            doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[tx9_fr]))
            tx9 = Paragraph(objtx9,styles["Verdana8"])
            story.append(tx9)
            tx9_fr.addFromList(story,c)

        elif bool(obj.tx9_min):
            #Tx9 min to max frame
            tx9_min_fr = Frame((1+x)*inch, (4.22+y)*inch, 0.7*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
            doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[tx9_min_fr]))
            tx9_min = Paragraph(new_tx9min +' - '+new_tx9max,styles["Verdana6"])
            story.append(tx9_min)
            tx9_min_fr.addFromList(story,c)

        if bool(obj.tx10):
            #Tx10 frame
            tx10_fr = Frame((1+x)*inch, (4.05+y)*inch, 0.7*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
            doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[tx10_fr]))
            tx10 = Paragraph(objtx10,styles["Verdana8"])
            story.append(tx10)
            tx10_fr.addFromList(story,c)

        elif bool(obj.tx10_min):
            #Tx10 min to max frame
            tx10_min_fr = Frame((1+x)*inch, (4.05+y)*inch, 0.7*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
            doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[tx10_min_fr]))
            tx10_min = Paragraph(new_tx10min +' - '+new_tx10max,styles["Verdana6"])
            story.append(tx10_min)
            tx10_min_fr.addFromList(story,c)

        if bool(obj.tx11):
            #Tx11 frame
            tx11_fr = Frame((1+x)*inch, (3.88+y)*inch, 0.7*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
            doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[tx11_fr]))
            tx11 = Paragraph(objtx11,styles["Verdana8"])
            story.append(tx11)
            tx11_fr.addFromList(story,c)

        elif bool(obj.tx11_min):
            #Tx11 min to max frame
            tx11_min_fr = Frame((1+x)*inch, (3.88+y)*inch, 0.7*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
            doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[tx11_min_fr]))
            tx11_min = Paragraph(new_tx11min +' - '+new_tx11max,styles["Verdana6"])
            story.append(tx11_min)
            tx11_min_fr.addFromList(story,c)

        if bool(obj.tx12):
            #Tx12 frame
            tx12_fr = Frame((1+x)*inch, (3.71+y)*inch, 0.7*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
            doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[tx12_fr]))
            tx12 = Paragraph(objtx12,styles["Verdana8"])
            story.append(tx12)
            tx12_fr.addFromList(story,c)

        elif bool(obj.tx12_min):
            #Tx12 min to max frame
            tx12_min_fr = Frame((1+x)*inch, (3.71+y)*inch, 0.7*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
            doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[tx12_min_fr]))
            tx12_min = Paragraph(new_tx12min +' - '+new_tx12max,styles["Verdana6"])
            story.append(tx12_min)
            tx12_min_fr.addFromList(story,c)

        if bool(obj.rx1):
            #Rx1 frame
            rx1_fr = Frame((1.75+x)*inch, (5.58+y)*inch, 0.7*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
            doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[rx1_fr]))
            rx1 = Paragraph(objrx1,styles["Verdana8"])
            story.append(rx1)
            rx1_fr.addFromList(story,c)

        elif bool(obj.rx1_min):
            #Rx1 min to max frame
            rx1_min_fr = Frame((1.75+x)*inch, (5.58+y)*inch, 0.7*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
            doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[rx1_min_fr]))
            rx1_min = Paragraph(new_rx1min +' - '+new_rx1max,styles["Verdana6"])
            story.append(rx1_min)
            rx1_min_fr.addFromList(story,c)

        if bool(obj.rx2):
            #Rx2 frame
            rx2_fr = Frame((1.75+x)*inch, (5.41+y)*inch, 0.7*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
            doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[rx2_fr]))
            rx2 = Paragraph(objrx2,styles["Verdana8"])
            story.append(rx2)
            rx2_fr.addFromList(story,c)
    
        elif bool(obj.rx2_min):
            #Rx2 min to max frame
            rx2_min_fr = Frame((1.75+x)*inch, (5.41+y)*inch, 0.7*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
            doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[rx2_min_fr]))
            rx2_min = Paragraph(new_rx2min +' - '+new_rx2max,styles["Verdana6"])
            story.append(rx2_min)
            rx2_min_fr.addFromList(story,c)

        if bool(obj.rx3):
            #Rx3 frame
            rx3_fr = Frame((1.75+x)*inch, (5.24+y)*inch, 0.7*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
            doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[rx3_fr]))
            rx3 = Paragraph(objrx3,styles["Verdana8"])
            story.append(rx3)
            rx3_fr.addFromList(story,c)

        elif bool(obj.rx3_min):
            #Rx3 min to max frame
            rx3_min_fr = Frame((1.75+x)*inch, (5.24+y)*inch, 0.7*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
            doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[rx3_min_fr]))
            rx3_min = Paragraph(new_rx3min +' - '+new_rx3max,styles["Verdana6"])
            story.append(rx3_min)
            rx3_min_fr.addFromList(story,c)

        if bool(obj.rx4):
            #Rx4 frame
            rx4_fr = Frame((1.75+x)*inch, (5.07+y)*inch, 0.7*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
            doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[rx4_fr]))
            rx4 = Paragraph(objrx4,styles["Verdana8"])
            story.append(rx4)
            rx4_fr.addFromList(story,c)

        elif bool(obj.rx4_min):
            #Rx4 min to max frame
            rx4_min_fr = Frame((1.75+x)*inch, (5.07+y)*inch, 0.7*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
            doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[rx4_min_fr]))
            rx4_min = Paragraph(new_rx4min +' - '+new_rx4max,styles["Verdana6"])
            story.append(rx4_min)
            rx4_min_fr.addFromList(story,c)

        if bool(obj.rx5):
            #Rx5 frame
            rx5_fr = Frame((1.75+x)*inch, (4.9+y)*inch, 0.7*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
            doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[rx5_fr]))
            rx5 = Paragraph(objrx5,styles["Verdana8"])
            story.append(rx5)
            rx5_fr.addFromList(story,c)

        elif bool(obj.rx5_min):
            #Rx5 min to max frame
            rx5_min_fr = Frame((1.75+x)*inch, (4.9+y)*inch, 0.7*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
            doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[rx5_min_fr]))
            rx5_min = Paragraph(new_rx5min +' - '+new_rx5max,styles["Verdana6"])
            story.append(rx5_min)
            rx5_min_fr.addFromList(story,c)

        if bool(obj.rx6):
            #Rx6 frame
            rx6_fr = Frame((1.75+x)*inch, (4.73+y)*inch, 0.7*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
            doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[rx6_fr]))
            rx6 = Paragraph(objrx6,styles["Verdana8"])
            story.append(rx6)
            rx6_fr.addFromList(story,c)

        elif bool(obj.rx6_min):
            #Rx6 min to max frame
            rx6_min_fr = Frame((1.75+x)*inch, (4.73+y)*inch, 0.7*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
            doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[rx6_min_fr]))
            rx6_min = Paragraph(new_rx6min +' - '+new_rx6max,styles["Verdana6"])
            story.append(rx6_min)
            rx6_min_fr.addFromList(story,c)

        if bool(obj.rx7):
            #Rx7 frame
            rx7_fr = Frame((1.75+x)*inch, (4.56+y)*inch, 0.7*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
            doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[rx7_fr]))
            rx7 = Paragraph(objrx7,styles["Verdana8"])
            story.append(rx7)
            rx7_fr.addFromList(story,c)

        elif bool(obj.rx7_min):
            #Rx7 min to max frame
            rx7_min_fr = Frame((1.75+x)*inch, (4.56+y)*inch, 0.7*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
            doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[rx7_min_fr]))
            rx7_min = Paragraph(new_rx7min +' - '+new_rx7max,styles["Verdana6"])
            story.append(rx7_min)
            rx7_min_fr.addFromList(story,c)

        if bool(obj.rx8):
            #Rx8 frame
            rx8_fr = Frame((1.75+x)*inch, (4.39+y)*inch, 0.7*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
            doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[rx8_fr]))
            rx8 = Paragraph(objrx8,styles["Verdana8"])
            story.append(rx8)
            rx8_fr.addFromList(story,c)
        
        elif bool(obj.rx8_min):
            #Rx8 min to max frame            
            rx8_min_fr = Frame((1.75+x)*inch, (4.39+y)*inch, 0.7*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
            doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[rx8_min_fr]))
            rx8_min = Paragraph(new_rx8min +' - '+new_rx8max,styles["Verdana6"])
            story.append(rx8_min)
            rx8_min_fr.addFromList(story,c)

        if bool(obj.rx9):
            #Rx9 frame
            rx9_fr = Frame((1.75+x)*inch, (4.22+y)*inch, 0.7*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
            doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[rx9_fr]))
            rx9 = Paragraph(objrx9,styles["Verdana8"])
            story.append(rx9)
            rx9_fr.addFromList(story,c)

        elif bool(obj.rx9_min):
            #Rx9 min to max frame
            rx9_min_fr = Frame((1.75+x)*inch, (4.22+y)*inch, 0.7*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
            doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[rx9_min_fr]))
            rx9_min = Paragraph(new_rx9min +' - '+new_rx9max,styles["Verdana6"])
            story.append(rx9_min)

        if bool(obj.rx10):
            #Rx10 frame
            rx10_fr = Frame((1.75+x)*inch, (4.05+y)*inch, 0.7*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
            doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[rx10_fr]))
            rx10 = Paragraph(objrx10,styles["Verdana8"])
            story.append(rx10)
            rx10_fr.addFromList(story,c)

        elif bool(obj.rx10_min):
            #Rx10 min to max frame
            rx10_min_fr = Frame((1.75+x)*inch, (4.05+y)*inch, 0.7*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
            doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[rx10_min_fr]))
            rx10_min = Paragraph(new_rx10min +' - '+new_rx10max,styles["Verdana6"])
            story.append(rx10_min)
            rx10_min_fr.addFromList(story,c)

        if bool(obj.rx11):
            #Rx11 frame
            rx11_fr = Frame((1.75+x)*inch, (3.88+y)*inch, 0.7*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
            doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[rx11_fr]))
            rx11 = Paragraph(objrx11,styles["Verdana8"])
            story.append(rx11)
            rx11_fr.addFromList(story,c)

        elif bool(obj.rx11_min):
            #Rx11 min to max frame
            rx11_min_fr = Frame((1.75+x)*inch, (3.88+y)*inch, 0.7*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
            doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[rx11_min_fr]))
            rx11_min = Paragraph(new_rx11min +' - '+new_rx11max,styles["Verdana6"])
            story.append(rx11_min)
            rx11_min_fr.addFromList(story,c)

        if bool(obj.rx12):
            #Rx12 frame
            rx12_fr = Frame((1.75+x)*inch, (3.71+y)*inch, 0.7*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
            doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[rx12_fr]))
            rx12 = Paragraph(objrx12,styles["Verdana8"])
            story.append(rx12)
            rx12_fr.addFromList(story,c)

        elif bool(obj.rx12_min):
            #Rx12 min to max frame
            rx12_min_fr = Frame((1.75+x)*inch, (3.71+y)*inch, 0.7*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
            doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[rx12_min_fr]))
            rx12_min = Paragraph(new_rx12min +' - '+new_rx12max,styles["Verdana6"])
            story.append(rx12_min)
            rx12_min_fr.addFromList(story,c)

        #Polarity1 frame
        polar1_fr = Frame((1+x)*inch-(0.5*inch), (5.58+y)*inch, 0.5*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
        doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[polar1_fr]))
        polar1 = Paragraph(obj.polarity1,styles["Verdana8"])
        story.append(polar1)
        polar1_fr.addFromList(story,c)

        #Polarity2 frame
        polar2_fr = Frame((1+x)*inch-(0.5*inch), (5.41+y)*inch, 0.5*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
        doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[polar2_fr]))
        polar2 = Paragraph(obj.polarity2,styles["Verdana8"])
        story.append(polar2)
        polar2_fr.addFromList(story,c)

        #Polarity3 frame
        polar3_fr = Frame((1+x)*inch-(0.5*inch), (5.24+y)*inch, 0.5*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
        doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[polar3_fr]))
        polar3 = Paragraph(obj.polarity3,styles["Verdana8"])
        story.append(polar3)
        polar3_fr.addFromList(story,c)

        #Polarity4 frame
        polar3_fr = Frame((1+x)*inch-(0.5*inch), (5.07+y)*inch, 0.5*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
        doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[polar3_fr]))
        polar3 = Paragraph(obj.polarity3,styles["Verdana8"])
        story.append(polar3)
        polar3_fr.addFromList(story,c)

        #Polarity5 frame
        polar5_fr = Frame((1+x)*inch-(0.5*inch), (4.9+y)*inch, 0.5*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
        doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[polar5_fr]))
        polar5 = Paragraph(obj.polarity5,styles["Verdana8"])
        story.append(polar5)
        polar5_fr.addFromList(story,c)

        #Polarity6 frame
        polar6_fr = Frame((1+x)*inch-(0.5*inch), (4.73+y)*inch, 0.5*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
        doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[polar6_fr]))
        polar6 = Paragraph(obj.polarity6,styles["Verdana8"])
        story.append(polar6)
        polar6_fr.addFromList(story,c)

        #Polarity7 frame
        polar7_fr = Frame((1+x)*inch-(0.5*inch), (4.56+y)*inch, 0.5*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
        doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[polar7_fr]))
        polar7 = Paragraph(obj.polarity7,styles["Verdana8"])
        story.append(polar7)
        polar7_fr.addFromList(story,c)

        #Polarity8 frame
        polar8_fr = Frame((1+x)*inch-(0.5*inch), (4.39+y)*inch, 0.5*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
        doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[polar8_fr]))
        polar8 = Paragraph(obj.polarity8,styles["Verdana8"])
        story.append(polar8)
        polar8_fr.addFromList(story,c)

        #Polarity9 frame
        polar9_fr = Frame((1+x)*inch-(0.5*inch), (4.22+y)*inch, 0.5*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
        doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[polar9_fr]))
        polar9 = Paragraph(obj.polarity9,styles["Verdana8"])
        story.append(polar9)
        polar9_fr.addFromList(story,c)

        #Polarity10 frame
        polar10_fr = Frame((1+x)*inch-(0.5*inch), (4.05+y)*inch, 0.5*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
        doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[polar10_fr]))
        polar10 = Paragraph(obj.polarity10,styles["Verdana8"])
        story.append(polar10)
        polar10_fr.addFromList(story,c)

        #Polarity11 frame
        polar11_fr = Frame((1+x)*inch-(0.5*inch), (3.88+y)*inch, 0.5*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
        doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[polar11_fr]))
        polar11 = Paragraph(obj.polarity11,styles["Verdana8"])
        story.append(polar11)
        polar11_fr.addFromList(story,c)

        #Polarity12 frame
        polar12_fr = Frame((1+x)*inch-(0.5*inch), (3.71+y)*inch, 0.5*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
        doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[polar12_fr]))
        polar12 = Paragraph(obj.polarity12,styles["Verdana8"])
        story.append(polar12)
        polar12_fr.addFromList(story,c)        
        
        #Bandwidth frame
        bw_fr = Frame((2.53+x)*inch, (5.58+y)*inch, inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
        doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[bw_fr]))
        bw = Paragraph(obj.bwe_1,styles["Verdana8"])
        story.append(bw)
        bw_fr.addFromList(story,c)

        #Power frame
        power_fr = Frame((3.53+x)*inch, (5.58+y)*inch, 0.9*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
        doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[power_fr]))
        power = Paragraph(obj.power[0:12],styles["Verdana8_left"])
        story.append(power)
        power_fr.addFromList(story,c)
        
###Particulars of Antenna          
        #Directivity frame
        dir_fr = Frame((4.8+x)*inch, (5.45+y)*inch, 0.7*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
        doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[dir_fr]))
        dr = Paragraph(obj.dir,styles["Verdana8_left"])
        story.append(dr)
        dir_fr.addFromList(story,c)

        #Height frame
        ht_fr = Frame((4.8+x)*inch, (5.14+y)*inch, 0.7*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
        doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[ht_fr]))
        ht = Paragraph(obj.h,styles["Verdana8_left"])
        story.append(ht)
        ht_fr.addFromList(story,c)

        #Gain frame
        gn_fr = Frame((4.8+x)*inch, (4.86+y)*inch, 0.7*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
        doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[gn_fr]))
        gn = Paragraph(obj.gn,styles["Verdana8_left"])
        story.append(gn)
        gn_fr.addFromList(story,c)

        #Type of Antenna frame        
        if len(obj.t) <=20:
            toa_fr = Frame((4.8+x)*inch, (4.61+y)*inch, 1.2*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
            doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[toa_fr]))
            toa = Paragraph(obj.t[0:19],styles["Verdana8_left"])
        else:
            toa_fr = Frame((4.8+x)*inch, (4.44+y)*inch, 1.2*inch, 0.34*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
            doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[toa_fr]))
            toa = Paragraph(obj.t,styles["Verdana8_left"])
        story.append(toa)
        toa_fr.addFromList(story,c)
###End of Particulars of Antenna

##Note: Create Error Trap for this frame 01/07/2013
        
        #Remarks1 frame 
        rem1_fr = Frame((6.13+x)*inch, (5.08+y)*inch, 2*inch, 0.67*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
        doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[rem1_fr]))

        ## for verification update
        rem1 = Paragraph(obj.remarks[0:50],styles["Verdana8_left"])
        
        story.append(rem1)
        rem1_fr.addFromList(story,c)

        #Remarks2 frame
        rem2_fr = Frame((6.13+x)*inch, (4.41+y)*inch, 2*inch, 0.67*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
        doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[rem2_fr]))

        ## for verification update
        rem2 = Paragraph(obj.remarks_2[0:50],styles["Verdana8_left"])
        
        story.append(rem2)
        rem2_fr.addFromList(story,c)
    
        #Model frame
        modelfr = Frame((3.6+x)*inch, (3.91+y)*inch, 4*inch, 0.19*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
        doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[modelfr]))
        model = Paragraph(obj.make,styles["VerdanaB10"])
        story.append(model)
        modelfr.addFromList(story,c)

        #Freq Range frame
        freqrangefr = Frame((3.6+x)*inch, (2.86+y)*inch, 4*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
        doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[freqrangefr]))
        freqrange = Paragraph(obj.freqrange,styles["Verdana9"])
        story.append(freqrange)
        freqrangefr.addFromList(story,c)

##SERIAL NUMBER HERE##
        ##Set location of every serial set depending to the number of serial
        ##Serial Number only
        if bool(obj.sn1) and not bool(obj.sn5) and not bool(obj.sn9) and not bool(obj.sn13) and not bool(obj.sn17) and not bool(obj.sn20):
            set1_switch = True
            sn1_only = True            
            set2_switch = set3_switch = set4_switch = set5_switch = set6_switch = False
            set_loc1 = set35_x
        ## Serial Number 1 & 2 only
        elif bool(obj.sn1) and bool(obj.sn2) and not bool(obj.sn5) and not bool(obj.sn9) and not bool(obj.sn13) and not bool(obj.sn17) and not bool(obj.sn20):
            set1_switch = True
            sn1_only = True
            sn2_only = True
            set2_switch = set3_switch = set4_switch = set5_switch = set6_switch = False
            set_loc1 = set35_x
        ## Serial Number 1, 2 & 3 only
        elif bool(obj.sn1) and bool(obj.sn2) and bool(obj.sn3) and not bool(obj.sn5) and not bool(obj.sn9) and not bool(obj.sn13) and not bool(obj.sn17) and not bool(obj.sn20):
            set1_switch = True
            sn1_only = True
            sn2_only = True
            sn3_only = True
            set2_switch = set3_switch = set4_switch = set5_switch = set6_switch = False
            set_loc1 = set35_x
        ## Serial Number 1, 2,3 & 4 only
        elif bool(obj.sn1) and bool(obj.sn2) and bool(obj.sn3) and bool(obj.sn4) and not bool(obj.sn5) and not bool(obj.sn9) and not bool(obj.sn13) and not bool(obj.sn17) and not bool(obj.sn20):
            set1_switch = True
            sn1_only = True
            sn2_only = True
            sn3_only = True
            sn4_only = True
            set2_switch = set3_switch = set4_switch = set5_switch = set6_switch = False
            set_loc1 = set35_x
        elif bool(obj.sn1) and bool(obj.sn5) and not bool(obj.sn9) and not bool(obj.sn13) and not bool(obj.sn17) and not bool(obj.sn20):
            set1_switch = set2_switch = True
            sn1_only = sn2_only = sn3_only = sn4_only = False
            set3_switch = set4_switch = set5_switch = set6_switch = False
            set_loc1 = set3_x
            set_loc2 = set4_x
        elif bool(obj.sn1) and bool(obj.sn5) and bool(obj.sn9) and not bool(obj.sn13) and not bool(obj.sn17) and not bool(obj.sn20):
            set1_switch = set2_switch = set3_switch = True            
            set4_switch = set5_switch = set6_switch = False
            sn1_only = sn2_only = sn3_only = sn4_only = False
            set_loc1 = set3_x
            set_loc2 = set4_x
            set_loc3 = set5_x            
        elif bool(obj.sn1) and bool(obj.sn5) and bool(obj.sn9) and bool(obj.sn13) and not bool(obj.sn17) and not bool(obj.sn20):
            set1_switch = set2_switch = set3_switch = set4_switch = True           
            set5_switch = set6_switch = False
            sn1_only = sn2_only = sn3_only = sn4_only = False
            set_loc1 = set2_x
            set_loc2 = set3_x
            set_loc3 = set4_x
            set_loc4 = set5_x
        elif bool(obj.sn1) and bool(obj.sn5) and bool(obj.sn9) and bool(obj.sn13) and bool(obj.sn17) and not bool(obj.sn20):
            set1_switch = set2_switch = set3_switch = set4_switch = set5_switch = set6_switch = True
            set6_switch = False
            sn1_only = sn2_only = sn3_only = sn4_only = False
            set_loc1 = set2_x
            set_loc2 = set3_x
            set_loc3 = set4_x
            set_loc4 = set5_x
            set_loc5 = set6_x         
        elif bool(obj.sn1) and bool(obj.sn5) and bool(obj.sn9) and bool(obj.sn13) and bool(obj.sn17) and bool(obj.sn20):
            set1_switch = set2_switch = set3_switch = set4_switch = set5_switch = set6_switch = True
            sn1_only = sn2_only = sn3_only = sn4_only = False
            set_loc1 = set1_x
            set_loc2 = set2_x
            set_loc3 = set3_x
            set_loc4 = set4_x
            set_loc5 = set5_x
            set_loc6 = set6_x            
            
        #Serial Number 1 frame
        if set1_switch:
            sn1_fr = Frame((set_loc1+x)*inch, (3.72+y)*inch, 1.2*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
            doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[sn1_fr]))
            if sn1_only == True:
                sn1 = Paragraph(obj.sn1,styles["Verdana8_left"])
            else:
                sn1 = Paragraph(obj.sn1,styles["Verdana8"])
            story.append(sn1)
            sn1_fr.addFromList(story,c)

            #Serial Number 2 frame
            sn2_fr = Frame((set_loc1+x)*inch, (3.55+y)*inch, 1.2*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
            doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[sn2_fr]))
            if sn2_only == True:
                sn2 = Paragraph(obj.sn2,styles["Verdana8_left"])
            else:
                sn2 = Paragraph(obj.sn2,styles["Verdana8"])           
            story.append(sn2)
            sn2_fr.addFromList(story,c)

            #Serial Number 3 frame
            sn3_fr = Frame((set_loc1+x)*inch, (3.38+y)*inch, 1.2*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
            doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[sn3_fr]))
            if sn3_only == True:
                sn3 = Paragraph(obj.sn3,styles["Verdana8_left"])
            else:
                sn3 = Paragraph(obj.sn3,styles["Verdana8"])           
            story.append(sn3)
            sn3_fr.addFromList(story,c)

            #Serial Number 4 frame
            sn4_fr = Frame((set_loc1+x)*inch, (3.21+y)*inch, 1.2*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
            doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[sn4_fr]))
            if sn4_only == True:
                sn4 = Paragraph(obj.sn4,styles["Verdana8_left"])
            else:
                sn4 = Paragraph(obj.sn4,styles["Verdana8"])
            story.append(sn4)
            sn4_fr.addFromList(story,c)

### 2nd Set
        
        if set2_switch:
            #Serial Number 5 frame
            sn5_fr = Frame((set_loc2+x)*inch, (3.72+y)*inch, 1.2*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
            doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[sn5_fr]))
            sn5 = Paragraph(obj.sn5,styles["Verdana8"])
            story.append(sn5)
            sn5_fr.addFromList(story,c)

            #Serial Number 6 frame
            sn6_fr = Frame((set_loc2+x)*inch, (3.55+y)*inch, 1.2*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
            doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[sn6_fr]))
            sn6 = Paragraph(obj.sn6,styles["Verdana8"])
            story.append(sn6)
            sn6_fr.addFromList(story,c)

            #Serial Number 7 frame
            sn7_fr = Frame((set_loc2+x)*inch, (3.38+y)*inch, 1.2*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
            doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[sn7_fr]))
            sn7 = Paragraph(obj.sn7,styles["Verdana8"])
            story.append(sn7)
            sn7_fr.addFromList(story,c)

            #Serial Number 8 frame
            sn8_fr = Frame((set_loc2+x)*inch, (3.21+y)*inch, 1.2*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
            doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[sn8_fr]))
            sn8 = Paragraph(obj.sn8,styles["Verdana8"])
            story.append(sn8)
            sn8_fr.addFromList(story,c)

### 3rd Set
        if set3_switch:
            #Serial Number 9 frame
            sn9_fr = Frame((set_loc3+x)*inch, (3.72+y)*inch, 1.2*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
            doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[sn9_fr]))
            sn9 = Paragraph(obj.sn9,styles["Verdana8"])
            story.append(sn9)
            sn9_fr.addFromList(story,c)

            #Serial Number 10 frame
            sn10_fr = Frame((set_loc3+x)*inch, (3.55+y)*inch, 1.2*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
            doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[sn10_fr]))
            sn10 = Paragraph(obj.sn10,styles["Verdana8"])
            story.append(sn10)
            sn10_fr.addFromList(story,c)

            #Serial Number 11 frame
            sn11_fr = Frame((set_loc3+x)*inch, (3.38+y)*inch, 1.2*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
            doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[sn11_fr]))
            sn11 = Paragraph(obj.sn11,styles["Verdana8"])
            story.append(sn11)
            sn11_fr.addFromList(story,c)

            #Serial Number 12 frame
            sn12_fr = Frame((set_loc3+x)*inch, (3.21+y)*inch, 1.2*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
            doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[sn12_fr]))
            sn12 = Paragraph(obj.sn12,styles["Verdana8"])
            story.append(sn12)
            sn12_fr.addFromList(story,c)

### 4th Set
        if set4_switch:
            #Serial Number 13 frame
            sn13_fr = Frame((set_loc4+x)*inch, (3.72+y)*inch, 1.2*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
            doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[sn13_fr]))
            sn13 = Paragraph(obj.sn13,styles["Verdana8"])
            story.append(sn13)
            sn13_fr.addFromList(story,c)

            #Serial Number 14 frame
            sn14_fr = Frame((set_loc4+x)*inch, (3.55+y)*inch, 1.2*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
            doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[sn14_fr]))
            sn14 = Paragraph(obj.sn14,styles["Verdana8"])
            story.append(sn14)
            sn14_fr.addFromList(story,c)

            #Serial Number 15 frame
            sn15_fr = Frame((set_loc4+x)*inch, (3.38+y)*inch, 1.2*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
            doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[sn15_fr]))
            sn15 = Paragraph(obj.sn15,styles["Verdana8"])
            story.append(sn15)
            sn15_fr.addFromList(story,c)

            #Serial Number 16 frame
            sn16_fr = Frame((set_loc4+x)*inch, (3.21+y)*inch, 1.2*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
            doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[sn16_fr]))
            sn16 = Paragraph(obj.sn16,styles["Verdana8"])
            story.append(sn16)
            sn16_fr.addFromList(story,c)

### 5th Set
        if set5_switch:
            #Serial Number 17 frame
            sn17_fr = Frame((set_loc5+x)*inch, (3.72+y)*inch, 1.2*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
            doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[sn17_fr]))
            sn17 = Paragraph(obj.sn17,styles["Verdana8"])
            story.append(sn17)
            sn17_fr.addFromList(story,c)
    
            #Serial Number 18 frame
            sn18_fr = Frame((set_loc5+x)*inch, (3.55+y)*inch, 1.2*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
            doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[sn18_fr]))
            sn18 = Paragraph(obj.sn18,styles["Verdana8"])
            story.append(sn18)
            sn18_fr.addFromList(story,c)

            #Serial Number 19 frame
            sn19_fr = Frame((set_loc5+x)*inch, (3.38+y)*inch, 1.2*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
            doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[sn19_fr]))
            sn19 = Paragraph(obj.sn19,styles["Verdana8"])
            story.append(sn19)
            sn19_fr.addFromList(story,c)
    
            #Serial Number 20 frame
            sn20_fr = Frame((set_loc5+x)*inch, (3.21+y)*inch, 1.2*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
            doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[sn20_fr]))
            sn20 = Paragraph(obj.sn20,styles["Verdana8"])
            story.append(sn20)
            sn20_fr.addFromList(story,c)

### 6th Set
        if set6_switch:
            #Serial Number 21 frame
            sn21_fr = Frame((set_loc6+x)*inch, (3.72+y)*inch, 1.2*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
            doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[sn21_fr]))
            sn21 = Paragraph(obj.sn21,styles["Verdana8"])
            story.append(sn21)
            sn21_fr.addFromList(story,c)

            #Serial Number 22 frame
            sn22_fr = Frame((set_loc6+x)*inch, (3.55+y)*inch, 1.2*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
            doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[sn22_fr]))
            sn22 = Paragraph(obj.sn22,styles["Verdana8"])
            story.append(sn22)
            sn22_fr.addFromList(story,c)

            #Serial Number 23 frame
            sn23_fr = Frame((set_loc6+x)*inch, (3.38+y)*inch, 1.2*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
            doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[sn23_fr]))
            sn23 = Paragraph(obj.sn23,styles["Verdana8"])
            story.append(sn23)
            sn23_fr.addFromList(story,c)

            #Serial Number 24 frame
            sn24_fr = Frame((set_loc6+x)*inch, (3.21+y)*inch, 1.2*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
            doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[sn24_fr]))
            sn24 = Paragraph(obj.sn24,styles["Verdana8"])
            story.append(sn24)
            sn24_fr.addFromList(story,c)

#### End Serial Number
        
        #Validity from frame
        valid_fromfr = Frame((3.8+x)*inch, (2.52+y)*inch, 2*inch, 0.19*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
        doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[valid_fromfr]))
        valid_from = Paragraph(new_validityfrom,styles["VerdanaB10"])
        story.append(valid_from)
        valid_fromfr.addFromList(story,c)

        #Validity to frame
        valid_tofr = Frame((5.9+x)*inch, (2.52+y)*inch, 2*inch, 0.19*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
        doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[valid_tofr]))
        valid_to = Paragraph(new_validityto,styles["VerdanaB10"])
        story.append(valid_to)
        valid_tofr.addFromList(story,c)
        
        #Signatory frame
        signfr = Frame((5.1+x)*inch, (0.89+y)*inch, 2*inch, 0.19*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
        doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[signfr]))
        signatory = Paragraph(obj.signatory,styles["VerdanaB10"])
        story.append(signatory)
        signfr.addFromList(story,c)

        #Encoder/Evaluator frame
        ee_fr = Frame((1.3+x)*inch, (1+y)*inch-(0.45*inch), 2*inch, 0.19*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
        doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[ee_fr]))
        ee = Paragraph(obj.encoder +'/'+ obj.evaluator,styles["Verdana6_left"])
        story.append(ee)
        ee_fr.addFromList(story,c)               

##Letter Head
        #codes for logo
	logo = "D:\Python27\Django-Projects\ccad\image\logo.jpg" #the directory of the logo
	image = ImageReader(logo)
	c.drawImage(image, 0.7*inch, 10.5*inch, width=1*inch, height=1*inch)

        c.setFont('arial', 10)
        c.drawString(2.2*inch, 11.3*inch, "REPUBLIC OF THE PHILIPPINES")
        c.drawString(2.2*inch, 11.1*inch, "OFFICE OF THE PRESIDENT")
        c.setFont('arialbd', 11)
        c.drawString(2.2*inch, 10.9*inch, "NATIONAL TELECOMMUNICATIONS COMMISSION")
        c.setFont('arial', 10)
        c.drawString(2.2*inch, 10.7*inch, "BIR ROAD, East Triangle, Diliman, Quezon City")
        c.setFont('arialbd', 18)
        c.drawString(2.5*inch, 10.33*inch, "RADIO STATION LICENSE")
        
##Official Receipt Name
        c.setFont('arial', 8)
        c.drawString((0.55+x)*inch, (9.38+y)*inch, "OR NO       :")
        c.drawString((0.55+x)*inch, (9.21+y)*inch, "AMOUNT   :")
        c.drawString((0.55+x)*inch, (9.04+y)*inch, "DATE PAID:")
        c.drawString((0.55+x)*inch, (8.86+y)*inch, "BY: ")
        c.drawString((6.2+x)*inch, (9.45+y)*inch, "LIC. NO:")#added 01/08/13

        c.setFont('VerdanaB', 12)
        c.drawString((6.8+x)*inch, (9.59+y)*inch, obj.status)#added 01/08/13
        
        c.setFont('arial', 10)
        c.drawString((1.55+x)*inch, (8.57+y)*inch, "THIS IS TO CERTIFY")
#change font italicized
        c.drawString((3+x)*inch, (8.59+y)*inch, "that") #insert line, canvas.line(x1,y1,x2,y2)
        c.drawString((7.15+x)*inch, (8.59+y)*inch, "is hereby")
        c.drawString((1+x)*inch, (8.33+y)*inch, "granted this license to operate") #insert line
        c.drawString((1+x)*inch, (8.08+y)*inch, "STATION located at") #insert line
        c.drawString((1+x)*inch, (7.83+y)*inch, "with the following particulars.")
        c.drawString((1.6+x)*inch, (7.6+y)*inch, "Geographical Location:")
        c.drawString((2.9+x)*inch, (7.4+y)*inch, "E. Longitude") #following a line
        c.drawString((2.9+x)*inch, (7.15+y)*inch, "N.Latitude") #following a line
        c.drawString((4.65+x)*inch, (7.6+y)*inch, "Class of Station") #insert line
        c.drawString((4.65+x)*inch, (7.35+y)*inch, "Nature of Service") #insert line
        c.drawString((4.65+x)*inch, (7.1+y)*inch, "CALL SIGN") #insert line
        c.drawString((4.65+x)*inch, (6.85+y)*inch, "Hours of operation") #insert line
        c.drawString((1.05+x)*inch, (6.45+y)*inch, "Points of communication/Service Area") #insert line
#change font, add lines, lines and lines!
        c.setFont('arialbd', 7)
        c.drawString((4.4+x)*inch,(5.5+y)*inch, "D")#added 01/08/13
        c.drawString((4.4+x)*inch,(5.2+y)*inch, "HAG")#added 01/08/13
        c.drawString((4.4+x)*inch,(4.9+y)*inch, "G")#added 01/08/13
        c.drawString((4.4+x)*inch,(4.65+y)*inch, "T")#added 01/08/13
        c.drawString((1.35+x)*inch, (6.1+y)*inch, "FREQUENCIES")
        c.drawString((1.52+x)*inch, (6.0+y)*inch, "Mhz/Khz")
        c.drawString((0.68+x)*inch, (5.85+y)*inch, "POL               TX                      RX")
        c.drawString((2.65+x)*inch, (6.1+y)*inch, "BANDWIDTH")
        c.drawString((2.6+x)*inch, (6.0+y)*inch, "AND TYPE OF")
        c.drawString((2.70+x)*inch, (5.9+y)*inch, "EMISSION")#to be paragraphed
        c.drawString((3.5+x)*inch, (6.1+y)*inch, "POWER")
        c.drawString((4.55+x)*inch, (6.1+y)*inch, "PARTICULARS OF")
        c.drawString((4.8+x)*inch, (6+y)*inch, "ANTENNA")#to be paragraphed
        c.drawString((6.6+x)*inch, (6.05+y)*inch, "REMARKS")
#change font
        c.setFont('arialbd', 9)
        c.drawString((3.3+x)*inch, (4.2+y)*inch, "PARTICULARS OF EQUIPMENT")
#change font
        c.setFont('arialbd', 10)
        c.drawString((1.8+x)*inch, (3.96+y)*inch, "MAKE/TYPE/MODEL :")
        if set3_switch == False:
            c.drawString((1.8+x)*inch, (3.75+y)*inch, "SERIAL NUMBER :")
        c.drawString((1.8+x)*inch, (2.9+y)*inch, "FREQ. RANGE :")
#change font
        c.setFont('arial', 9)
        c.drawString((1.6+x)*inch, (2.53+y)*inch, "This license is effective from") #insert line
        c.drawString((5.45+x)*inch, (2.53+y)*inch, "to") #insert line
        c.drawString((1.05+x)*inch, (2.38+y)*inch, "unless sooner suspended, cancelled or revoked.")
        c.drawString((1.6+x)*inch, (2.2+y)*inch, "This license is issued subject to the provisions of the Radio Control Law, Act No 3846 as")
        c.drawString((1.05+x)*inch, (2.05+y)*inch, "amended and the regulations promulgated thereunder and the Radio Regulations annexed to the")
        c.drawString((1.05+x)*inch, (1.9+y)*inch, "International Telecommunication Convention in force.") #needs to be paragraphed
#change font
        c.drawString((5.05+x)*inch, (1.4+y)*inch, "By Authority of the Commissioner")
        c.drawString((5.32+x)*inch, (0.84+y)*inch, "Director")
#change font
        c.setFont('arialbd', 8)
        c.drawString((2.15+x)*inch, (0.75+y)*inch, "Note:") #Bold
        c.setFont('arial', 8)
        c.drawString((2.45+x)*inch, (0.75+y)*inch, "This license is valid only when the payment of the required fee is indicated hereon")
#change font
        c.setFont('arialbd', 11)
        c.drawString((1.05+x)*inch, (0.5+y)*inch, "No.") #bold	
	
#LINES
        c.line((3.3+x)*inch, (8.59+y)*inch, (7.05+x)*inch, (8.59+y)*inch) #carrier
        c.line((3.05+x)*inch, (8.31+y)*inch, (7.65+x)*inch, (8.31+y)*inch) #license to operate
        c.line((2.5+x)*inch, (8.08+y)*inch, (7.7+x)*inch, (8.08+y)*inch) #address1
#c.line(2.45*inch, 7.9*inch, 7.7*inch, 7.9*inch) #address2
        c.line((1.05+x)*inch, (7.35+y)*inch, (2.85+x)*inch, (7.35+y)*inch) #longitude
        c.line((1.05+x)*inch, (7.1+y)*inch, (2.85+x)*inch, (7.1+y)*inch) #latitude
        c.line((5.65+x)*inch, (7.55+y)*inch, (7.7+x)*inch, (7.55+y)*inch) #class
        c.line((5.75+x)*inch, (7.3+y)*inch, (7.7+x)*inch, (7.3+y)*inch) #nature
        c.line((5.4+x)*inch, (7.05+y)*inch, (7.7+x)*inch, (7.05+y)*inch) #callsign
        c.line((5.8+x)*inch, (6.8+y)*inch, (7.7+x)*inch, (6.8+y)*inch) #hours
        c.line((3.5+x)*inch, (6.45+y)*inch, (7.7+x)*inch, (6.45+y)*inch)#points of service
        c.line((5.65+x)*inch,(8.92+y)*inch,(7.7+x)*inch,(8.92+y)*inch) #date
        c.line((6.8+x)*inch, (9.4+y)*inch, (8+x)*inch,(9.4+y)*inch)#lic no #added 01/08/12
#table (horizontal lines)
        c.line((1.05+x)*inch,(6.35+y)*inch,(7.7+x)*inch,(6.35+y)*inch)
        c.line((1.05+x)*inch,(6.3+y)*inch,(7.7+x)*inch,(6.3+y)*inch)
        c.line((1.05+x)*inch,(6.25+y)*inch,(7.7+x)*inch,(6.25+y)*inch)
        c.line((1.05+x)*inch,(5.75+y)*inch,(7.7+x)*inch,(5.75+y)*inch)
        c.line((1.05+x)*inch,(4.4+y)*inch,(7.7+x)*inch,(4.4+y)*inch)
        c.line((1.05+x)*inch,(4.35+y)*inch,(7.7+x)*inch,(4.35+y)*inch)
        c.line((1.05+x)*inch,(2.8+y)*inch,(7.7+x)*inch,(2.8+y)*inch)	
        c.line((1.05+x)*inch,(2.75+y)*inch,(7.7+x)*inch,(2.75+y)*inch)
#table (vertical lines)
        c.line((2.5+x)*inch,(6.25+y)*inch,(2.5+x)*inch,(4.4+y)*inch)
        c.line((3.45+x)*inch,(6.25+y)*inch,(3.45+x)*inch,(4.4+y)*inch)
        c.line((3.95+x)*inch,(6.25+y)*inch,(3.95+x)*inch,(4.4+y)*inch)
        c.line((6+x)*inch,(6.25+y)*inch,(6+x)*inch,(4.4+y)*inch)
#date (from-to)
        c.line((3.6+x)*inch,(2.51+y)*inch,(5.35+x)*inch,(2.51+y)*inch) #date from
        c.line((5.65+x)*inch,(2.51+y)*inch,(7.65+x)*inch,(2.51+y)*inch) #date to
        
        c.showPage()
        doc.build(story)        
    
    c.save()
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response
    
def preview_data(modeladmin, request, queryset): #added January 16, 2013
    response = HttpResponse(mimetype='application/pdf')
    response['Content-Disposition'] = 'filename = testframe.pdf'

    buffer = StringIO()
    c = canvas.Canvas(buffer)
    doc = BaseDocTemplate(buffer, showBoundary=1, leftMargin= 0.1*inch, rightMargin= 0.1*inch,
                     topMargin= 0.1*inch, bottomMargin= 0.1*inch)   

    story = []
    #Set needed Font Style    
    styles=getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Verdana6', fontName= 'Verdana', fontSize= 6, alignment= 1))
    styles.add(ParagraphStyle(name='Verdana6_left', fontName= 'Verdana', fontSize= 6))
    styles.add(ParagraphStyle(name='Verdana8', fontName= 'Verdana', fontSize= 8, alignment= 1))
    styles.add(ParagraphStyle(name='Verdana8_left', fontName= 'Verdana', fontSize= 8, wordWrap = True))
    styles.add(ParagraphStyle(name='Verdana9', fontName= 'Verdana', fontSize= 9))
    styles.add(ParagraphStyle(name='Verdana9_right', fontName= 'Verdana', fontSize= 9, alignment = 2))
    styles.add(ParagraphStyle(name='Verdana9_center', fontName= 'Verdana', fontSize= 9, alignment = 1))
    styles.add(ParagraphStyle(name='VerdanaB10', fontName= 'VerdanaB', fontSize= 10))

    #coord adjustment
    x = -0.17
    y = 0.61 #0.67
    #Call-Sign Frame
    callsignfr_height = 0
    callsignfr_y = 0
    #Serial Number coordinate adjustment
    set_loc1 = set_loc2 = set_loc3 = set_loc4 = set_loc5 = set_loc6 = 0
    set1_switch = set2_switch = set3_switch = set4_switch = set5_switch = set6_switch = True
    set1_x = 0.4
    set2_x = 1.7
    set3_x = 3
    set35_x = 3.6
    set4_x = 4.3
    set5_x = 5.6
    set6_x = 6.9
    sn1_only = sn2_only = sn3_only = sn4_only = True
    
    for obj in queryset:  
        #Number Conversion
        new_orno = convert_data_to_uni(obj.or_no)
        new_orno2 = convert_data_to_uni(obj.or_no2)
        new_amt = convert_data_to_uni(obj.amount)
        new_amt2 = convert_data_to_uni(obj.amount2)
        
        #Date Conversion
        issued_formatted = formats.date_format(obj.issued, 'DATE_FORMAT')
        validityfrom_formatted = formats.date_format(obj.validity_from, 'DATE_FORMAT')
        validityto_formatted = formats.date_format(obj.validity_to, 'DATE_FORMAT')
        
        new_datepd = convert_data_to_uni(obj.date_paid)
        new_datepd2 = convert_data_to_uni(obj.date_paid2)                
        new_issued = convert_data_to_uni(issued_formatted)
        new_validityfrom = convert_data_to_uni(validityfrom_formatted)
        new_validityto = convert_data_to_uni(validityto_formatted)        

        new_tx1min = encoding.smart_unicode(obj.tx1_min, encoding='utf-8', strings_only=False, errors='strict')
        new_tx1max = encoding.smart_unicode(obj.tx1_max, encoding='utf-8', strings_only=False, errors='strict')
        new_tx2min = encoding.smart_unicode(obj.tx2_min, encoding='utf-8', strings_only=False, errors='strict')
        new_tx2max = encoding.smart_unicode(obj.tx2_max, encoding='utf-8', strings_only=False, errors='strict')
        new_tx3min = encoding.smart_unicode(obj.tx3_min, encoding='utf-8', strings_only=False, errors='strict')
        new_tx3max = encoding.smart_unicode(obj.tx3_max, encoding='utf-8', strings_only=False, errors='strict')
        new_tx4min = encoding.smart_unicode(obj.tx4_min, encoding='utf-8', strings_only=False, errors='strict')
        new_tx4max = encoding.smart_unicode(obj.tx4_max, encoding='utf-8', strings_only=False, errors='strict')
        new_tx5min = encoding.smart_unicode(obj.tx5_min, encoding='utf-8', strings_only=False, errors='strict')
        new_tx5max = encoding.smart_unicode(obj.tx5_max, encoding='utf-8', strings_only=False, errors='strict')
        new_tx6min = encoding.smart_unicode(obj.tx6_min, encoding='utf-8', strings_only=False, errors='strict')
        new_tx6max = encoding.smart_unicode(obj.tx6_max, encoding='utf-8', strings_only=False, errors='strict')
        new_tx7min = encoding.smart_unicode(obj.tx7_min, encoding='utf-8', strings_only=False, errors='strict')
        new_tx7max = encoding.smart_unicode(obj.tx7_max, encoding='utf-8', strings_only=False, errors='strict')
        new_tx8min = encoding.smart_unicode(obj.tx8_min, encoding='utf-8', strings_only=False, errors='strict')
        new_tx8max = encoding.smart_unicode(obj.tx8_max, encoding='utf-8', strings_only=False, errors='strict')
        new_tx9min = encoding.smart_unicode(obj.tx9_min, encoding='utf-8', strings_only=False, errors='strict')
        new_tx9max = encoding.smart_unicode(obj.tx9_max, encoding='utf-8', strings_only=False, errors='strict')
        new_tx10min = encoding.smart_unicode(obj.tx10_min, encoding='utf-8', strings_only=False, errors='strict')
        new_tx10max = encoding.smart_unicode(obj.tx10_max, encoding='utf-8', strings_only=False, errors='strict')
        new_tx11min = encoding.smart_unicode(obj.tx11_min, encoding='utf-8', strings_only=False, errors='strict')
        new_tx11max = encoding.smart_unicode(obj.tx11_max, encoding='utf-8', strings_only=False, errors='strict')
        new_tx12min = encoding.smart_unicode(obj.tx12_min, encoding='utf-8', strings_only=False, errors='strict')
        new_tx12max = encoding.smart_unicode(obj.tx12_max, encoding='utf-8', strings_only=False, errors='strict')

        new_rx1min = encoding.smart_unicode(obj.rx1_min, encoding='utf-8', strings_only=False, errors='strict')
        new_rx1max = encoding.smart_unicode(obj.rx1_max, encoding='utf-8', strings_only=False, errors='strict')
        new_rx2min = encoding.smart_unicode(obj.rx2_min, encoding='utf-8', strings_only=False, errors='strict')
        new_rx2max = encoding.smart_unicode(obj.rx2_max, encoding='utf-8', strings_only=False, errors='strict')
        new_rx3min = encoding.smart_unicode(obj.rx3_min, encoding='utf-8', strings_only=False, errors='strict')
        new_rx3max = encoding.smart_unicode(obj.rx3_max, encoding='utf-8', strings_only=False, errors='strict')
        new_rx4min = encoding.smart_unicode(obj.rx4_min, encoding='utf-8', strings_only=False, errors='strict')
        new_rx4max = encoding.smart_unicode(obj.rx4_max, encoding='utf-8', strings_only=False, errors='strict')
        new_rx5min = encoding.smart_unicode(obj.rx5_min, encoding='utf-8', strings_only=False, errors='strict')
        new_rx5max = encoding.smart_unicode(obj.rx5_max, encoding='utf-8', strings_only=False, errors='strict')
        new_rx6min = encoding.smart_unicode(obj.rx6_min, encoding='utf-8', strings_only=False, errors='strict')
        new_rx6max = encoding.smart_unicode(obj.rx6_max, encoding='utf-8', strings_only=False, errors='strict')
        new_rx7min = encoding.smart_unicode(obj.rx7_min, encoding='utf-8', strings_only=False, errors='strict')
        new_rx7max = encoding.smart_unicode(obj.rx7_max, encoding='utf-8', strings_only=False, errors='strict')
        new_rx8min = encoding.smart_unicode(obj.rx8_min, encoding='utf-8', strings_only=False, errors='strict')
        new_rx8max = encoding.smart_unicode(obj.rx8_max, encoding='utf-8', strings_only=False, errors='strict')
        new_rx9min = encoding.smart_unicode(obj.rx9_min, encoding='utf-8', strings_only=False, errors='strict')
        new_rx9max = encoding.smart_unicode(obj.rx9_max, encoding='utf-8', strings_only=False, errors='strict')
        new_rx10min = encoding.smart_unicode(obj.rx10_min, encoding='utf-8', strings_only=False, errors='strict')
        new_rx10max = encoding.smart_unicode(obj.rx10_max, encoding='utf-8', strings_only=False, errors='strict')
        new_rx11min = encoding.smart_unicode(obj.rx11_min, encoding='utf-8', strings_only=False, errors='strict')
        new_rx11max = encoding.smart_unicode(obj.rx11_max, encoding='utf-8', strings_only=False, errors='strict')
        new_rx12min = encoding.smart_unicode(obj.rx12_min, encoding='utf-8', strings_only=False, errors='strict')
        new_rx12max = encoding.smart_unicode(obj.rx12_max, encoding='utf-8', strings_only=False, errors='strict')
        
        #Official Reciept frame
        if bool(new_orno) and bool(new_orno2) \
           and not queryset.filter(id=obj.id).only('or_no2').filter(or_no2__exact=None).count():
            ORfr = Frame((1.2+x)*inch, (9.33+y)*inch, 1.5*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
            doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[ORfr]))
            orno = Paragraph(new_orno+' / '+ new_orno2,styles["Verdana9"])
            story.append(orno)
            ORfr.addFromList(story,c)

            #Amount frame here           
            amtfr = Frame((1.2+x)*inch, (9.16+y)*inch, 1.5*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
            doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[amtfr]))
            amt = Paragraph(new_amt+' / '+ new.amt2,styles["Verdana9"])
            story.append(amt)
            amtfr.addFromList(story,c)

            #Date Paid frame
            datepaidfr = Frame((1.2+x)*inch, (8.99+y)*inch, 2*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
            doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[datepaidfr]))
            datepaid = Paragraph(new_datepd +' / '+ new_datepd2 ,styles["Verdana9"])
            story.append(datepaid)
            datepaidfr.addFromList(story,c)
            
        elif bool(new_orno):
            ORfr = Frame((1.2+x)*inch, (9.33+y)*inch, inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
            doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[ORfr]))
            orno = Paragraph(new_orno,styles["Verdana9"])
            story.append(orno)
            ORfr.addFromList(story,c)

            #Amount frame here           
            amtfr = Frame((1.2+x)*inch, (9.16+y)*inch, inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
            doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[amtfr]))
            amt = Paragraph(new_amt,styles["Verdana9"])
            story.append(amt)
            amtfr.addFromList(story,c)

            #Date Paid frame
            datepaidfr = Frame((1.2+x)*inch, (8.99+y)*inch, inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
            doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[datepaidfr]))
            datepaid = Paragraph(new_datepd,styles["Verdana9"])
            story.append(datepaid)
            datepaidfr.addFromList(story,c)

        #License Number frame
        rslnofr = Frame((6.8+x)*inch, (9.4+y)*inch, 1.5*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
        doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[rslnofr]))
        rsl_no = Paragraph(obj.rslno,styles["Verdana9"])
        story.append(rsl_no)
        rslnofr.addFromList(story,c)

        #Date Issued frame
        date_issuedfr = Frame((6.1+x)*inch, (8.9+y)*inch, 1.4*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
        doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[date_issuedfr]))
        date_issued = Paragraph(new_issued,styles["Verdana9"])
        story.append(date_issued)
        date_issuedfr.addFromList(story,c)

        #Carrier frame
        carrierfr = Frame((3.35+x)*inch,(8.55+y)*inch, 4.5*inch, 0.2*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
        doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[carrierfr]))
        carrier = Paragraph(obj.carrier,styles["VerdanaB10"])
        story.append(carrier)
        carrierfr.addFromList(story,c)

        #Lic to Operate frame
        lic_operatefr = Frame((3.2+x)*inch, (8.3+y)*inch, 2*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
        doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[lic_operatefr]))
        lic_operate = Paragraph(obj.lic_to_operate,styles["Verdana9"])
        story.append(lic_operate)
        lic_operatefr.addFromList(story,c)

        if bool(obj.site) and bool(obj.street):
            #Site-Street frame
            if len(obj.site)+ len(obj.street) < 64:
                sitefr = Frame((2.8+x)*inch, (8.05+y)*inch, 5.2*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
                doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[sitefr]))
                site = Paragraph(obj.site +' - '+ obj.street,styles["Verdana9"])
                story.append(site)
                sitefr.addFromList(story,c)
            else:
                sitefr = Frame((2.8+x)*inch, (8.05+y)*inch, 5.2*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
                doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[sitefr]))
                site = Paragraph(obj.site +' - '+ obj.street,styles["Verdana9"])
                story.append(site)
                sitefr.addFromList(story,c)

            #City frame
            cityfr = Frame((2.8+x)*inch, (7.88+y)*inch, 5.2*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
            doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[cityfr]))
            city = Paragraph(obj.city + ', '+ obj.province + ', ' + obj.region,styles["Verdana9"])
            story.append(city)
            cityfr.addFromList(story,c)

        elif bool(obj.site) and not(obj.street) and bool(obj.city):
            #Site-City frame
            sitefr = Frame((2.8+x)*inch, (8.05+y)*inch, 5.2*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
            doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[sitefr]))
            #add Province name if space available
            if 64 - len(obj.province) <= len(obj.site) + len(obj.city):
                site = Paragraph(obj.site +' - '+ obj.city + ', ' + obj.province +', '+ obj.region,styles["Verdana9"])
            else:
                site = Paragraph(obj.site +' - '+ obj.city, styles["Verdana9"])
            story.append(site)
            sitefr.addFromList(story,c)

        elif bool(obj.site) and not(obj.street) and not bool(obj.city) and bool(obj.province):
            #Site-Province frame
            sitefr = Frame((2.8+x)*inch, (8.05+y)*inch, 5.2*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
            doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[sitefr]))
            #add Province name if space available           
            site = Paragraph(obj.site +' - '+ obj.province +', '+ obj.region,styles["Verdana9"])            
            story.append(site)
            sitefr.addFromList(story,c)
            
        else:
            #Site frame
            sitefr = Frame((2.8+x)*inch, (8.05+y)*inch, 5.2*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
            doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[sitefr]))
            site = Paragraph(obj.site +' - '+ obj.region,styles["Verdana9"])
            story.append(site)
            sitefr.addFromList(story,c)

        #Longitude frame
        longitudefr = Frame((1.05+x)*inch, (7.35+y)*inch, 1.8*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
        doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[longitudefr]))
        longitude = Paragraph(obj.longitude,styles["Verdana9_right"])
        story.append(longitude)
        longitudefr.addFromList(story,c)

        #Latitude frame
        latitudefr = Frame((1.05+x)*inch, (7.1+y)*inch, 1.8*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
        doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[latitudefr]))
        latitude = Paragraph(obj.latitude,styles["Verdana9_right"])
        story.append(latitude)
        latitudefr.addFromList(story,c)

        #Class of Station frame
        class_stationfr = Frame((5.85+x)*inch, (7.55+y)*inch, 1.95*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
        doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[class_stationfr]))
        class_station = Paragraph(obj.class_of_station,styles["Verdana9_center"])
        story.append(class_station)
        class_stationfr.addFromList(story,c)

        
        #Nature of Service frame
        nosfr = Frame((5.85+x)*inch, (7.3+y)*inch, 1.95*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
        doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[nosfr]))
        nature_service = Paragraph(obj.nature_of_service,styles["Verdana9_center"])
        story.append(nature_service)
        nosfr.addFromList(story,c)

        #Call-Sign frame
        if len(obj.callsign) <= 29:
            callsignfr_height = 0.17
            callsignfr_y = 0
        else:
            callsignfr_height = 0.34
            callsignfr_y = -0.17
        callsignfr = Frame((5.4+x)*inch, (callsignfr_y+7.05+y)*inch, 2.3*inch, callsignfr_height*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
        doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[callsignfr]))
        call_sign = Paragraph(obj.callsign,styles["Verdana9_center"])
        story.append(call_sign)
        callsignfr.addFromList(story,c)          
        

        #Hours of Operation frame
        hours_opefr = Frame((5.8+x)*inch, (6.8+y)*inch, 1.9*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
        doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[hours_opefr]))
        hours_ope = Paragraph(' ',styles["Verdana9"])
        story.append(hours_ope)
        hours_opefr.addFromList(story,c)

        #Point of Service frame
        pts_svcfr = Frame((3.65+x)*inch, (6.45+y)*inch, 4.25*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
        doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[pts_svcfr]))
        if bool(obj.ptsvc):
            pts_svc = Paragraph(string.capwords(obj.ptsvc),styles["Verdana9"])
        else:
            pts_svc = Paragraph(string.capwords(obj.ptsvc_callsign),styles["Verdana9"])
        story.append(pts_svc)
        pts_svcfr.addFromList(story,c)

        if bool(obj.tx1):            
            #Tx1 frame
            tx1_fr = Frame((1+x)*inch, (5.58+y)*inch, 0.7*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
            doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[tx1_fr]))
            tx1 = Paragraph(obj.tx1,styles["Verdana8"])
            story.append(tx1)
            tx1_fr.addFromList(story,c)
            
        elif bool(obj.tx1_min):
            #Tx1 min to max frame
            tx1_min_fr = Frame((1+x)*inch, (5.58+y)*inch, 0.7*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
            doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[tx1_min_fr]))
            tx1_min = Paragraph(new_tx1min +' - '+new_tx1max ,styles["Verdana6"])
            story.append(tx1_min)
            tx1_min_fr.addFromList(story,c)

        if bool(obj.tx2):
            #Tx2 frame
            tx2_fr = Frame((1+x)*inch, (5.41+y)*inch, 0.7*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
            doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[tx2_fr]))
            tx2 = Paragraph(obj.tx2,styles["Verdana8"])
            story.append(tx2)
            tx2_fr.addFromList(story,c)
            
        elif bool(obj.tx2_min):
            #Tx2 min to max frame
            tx2_min_fr = Frame((1+x)*inch, (5.41+y)*inch, 0.7*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
            doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[tx2_min_fr]))
            tx2_min = Paragraph(new_tx2min +' - '+new_tx2max,styles["Verdana6"])
            story.append(tx2_min)
            tx2_min_fr.addFromList(story,c)

        if bool(obj.tx3):
            #Tx3 frame
            tx3_fr = Frame((1+x)*inch, (5.24+y)*inch, 0.7*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
            doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[tx3_fr]))
            tx3 = Paragraph(obj.tx3,styles["Verdana8"])
            story.append(tx3)
            tx3_fr.addFromList(story,c)
            
        elif bool(obj.tx3_min):
            #Tx3 min to max frame
            tx3_min_fr = Frame((1+x)*inch, (5.24+y)*inch, 0.7*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
            doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[tx3_min_fr]))
            tx3_min = Paragraph(new_tx3min +' - '+new_tx3max,styles["Verdana6"])
            story.append(tx3_min)
            tx3_min_fr.addFromList(story,c)

        if bool(obj.tx4):
            #Tx4 frame
            tx4_fr = Frame((1+x)*inch, (5.07+y)*inch, 0.7*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
            doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[tx4_fr]))
            tx4 = Paragraph(obj.tx4,styles["Verdana8"])
            story.append(tx4)
            tx4_fr.addFromList(story,c)
            
        elif bool(obj.tx4_min):           
            #Tx4 min to max frame
            tx4_min_fr = Frame((1+x)*inch, (5.07+y)*inch, 0.7*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
            doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[tx4_min_fr]))
            tx4_min = Paragraph(new_tx4min +' - '+new_tx4max,styles["Verdana6"])
            story.append(tx4_min)
            tx4_min_fr.addFromList(story,c)

        if bool(obj.tx5):    
            #Tx5 frame
            tx5_fr = Frame((1+x)*inch, (4.9+y)*inch, 0.7*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
            doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[tx5_fr]))
            tx5 = Paragraph(obj.tx5,styles["Verdana8"])
            story.append(tx5)
            tx5_fr.addFromList(story,c)

        elif bool(obj.tx5_min):
            #Tx5 min to max frame
            tx5_min_fr = Frame((1+x)*inch, (4.9+y)*inch, 0.7*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
            doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[tx5_min_fr]))
            tx5_min = Paragraph(new_tx5min +' - '+new_tx5max,styles["Verdana6"])
            story.append(tx5_min)
            tx5_min_fr.addFromList(story,c)

        if bool(obj.tx6):
            #Tx6 frame
            tx6_fr = Frame((1+x)*inch, (4.73+y)*inch, 0.7*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
            doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[tx6_fr]))
            tx6 = Paragraph(obj.tx6,styles["Verdana8"])
            story.append(tx6)
            tx6_fr.addFromList(story,c)
            
        elif bool(obj.tx6_min):
            #Tx6min to max frame
            tx6_min_fr = Frame((1+x)*inch, (4.73+y)*inch, 0.7*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
            doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[tx6_min_fr]))
            tx6_min = Paragraph(new_tx6min +' - '+new_tx6max,styles["Verdana6"])
            story.append(tx6_min)
            tx6_min_fr.addFromList(story,c)

        if bool(obj.tx7):
            #Tx7 frame
            tx7_fr = Frame((1+x)*inch, (4.56+y)*inch, 0.7*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
            doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[tx7_fr]))
            tx7 = Paragraph(obj.tx7,styles["Verdana8"])
            story.append(tx7)
            tx7_fr.addFromList(story,c)

        elif bool(obj.tx7_min):
            #Tx7 min to max frame
            tx7_min_fr = Frame((1+x)*inch, (4.56+y)*inch, 0.7*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
            doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[tx7_min_fr]))
            tx7_min = Paragraph(new_tx7min +' - '+new_tx7max,styles["Verdana6"])
            story.append(tx7_min)
            tx7_min_fr.addFromList(story,c)

        if bool(obj.tx8):
            #Tx8 frame
            tx8_fr = Frame((1+x)*inch, (4.39+y)*inch, 0.7*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
            doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[tx8_fr]))
            tx8 = Paragraph(obj.tx8,styles["Verdana8"])
            story.append(tx8)
            tx8_fr.addFromList(story,c)

        elif bool(obj.tx8_min):
            #Tx8 min to max frame
            tx8_min_fr = Frame((1+x)*inch, (4.39+y)*inch, 0.7*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
            doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[tx8_min_fr]))
            tx8_min = Paragraph(new_tx8min +' - '+new_tx8max,styles["Verdana6"])
            story.append(tx8_min)
            tx8_min_fr.addFromList(story,c)

        if bool(obj.tx9):
            #Tx9 frame
            tx9_fr = Frame((1+x)*inch, (4.22+y)*inch, 0.7*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
            doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[tx9_fr]))
            tx9 = Paragraph(obj.tx9,styles["Verdana8"])
            story.append(tx9)
            tx9_fr.addFromList(story,c)

        elif bool(obj.tx9_min):
            #Tx9 min to max frame
            tx9_min_fr = Frame((1+x)*inch, (4.22+y)*inch, 0.7*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
            doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[tx9_min_fr]))
            tx9_min = Paragraph(new_tx9min +' - '+new_tx9max,styles["Verdana6"])
            story.append(tx9_min)
            tx9_min_fr.addFromList(story,c)

        if bool(obj.tx10):
            #Tx10 frame
            tx10_fr = Frame((1+x)*inch, (4.05+y)*inch, 0.7*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
            doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[tx10_fr]))
            tx10 = Paragraph(obj.tx10,styles["Verdana8"])
            story.append(tx10)
            tx10_fr.addFromList(story,c)

        elif bool(obj.tx10_min):
            #Tx10 min to max frame
            tx10_min_fr = Frame((1+x)*inch, (4.05+y)*inch, 0.7*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
            doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[tx10_min_fr]))
            tx10_min = Paragraph(new_tx10min +' - '+new_tx10max,styles["Verdana6"])
            story.append(tx10_min)
            tx10_min_fr.addFromList(story,c)

        if bool(obj.tx11):
            #Tx11 frame
            tx11_fr = Frame((1+x)*inch, (3.88+y)*inch, 0.7*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
            doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[tx11_fr]))
            tx11 = Paragraph(obj.tx11,styles["Verdana8"])
            story.append(tx11)
            tx11_fr.addFromList(story,c)

        elif bool(obj.tx11_min):
            #Tx11 min to max frame
            tx11_min_fr = Frame((1+x)*inch, (3.88+y)*inch, 0.7*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
            doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[tx11_min_fr]))
            tx11_min = Paragraph(new_tx10min +' - '+new_tx10max,styles["Verdana6"])
            story.append(tx11_min)
            tx11_min_fr.addFromList(story,c)

        if bool(obj.tx12):
            #Tx12 frame
            tx12_fr = Frame((1+x)*inch, (3.71+y)*inch, 0.7*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
            doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[tx12_fr]))
            tx12 = Paragraph(obj.tx11,styles["Verdana8"])
            story.append(tx12)
            tx12_fr.addFromList(story,c)

        elif bool(obj.tx12_min):
            #Tx12 min to max frame
            tx12_min_fr = Frame((1+x)*inch, (3.71+y)*inch, 0.7*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
            doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[tx12_min_fr]))
            tx12_min = Paragraph(new_tx10min +' - '+new_tx10max,styles["Verdana6"])
            story.append(tx12_min)
            tx12_min_fr.addFromList(story,c)

        if bool(obj.rx1):
            #Rx1 frame
            rx1_fr = Frame((1.75+x)*inch, (5.58+y)*inch, 0.7*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
            doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[rx1_fr]))
            rx1 = Paragraph(obj.rx1,styles["Verdana8"])
            story.append(rx1)
            rx1_fr.addFromList(story,c)

        elif bool(obj.rx1_min):
            #Rx1 min to max frame
            rx1_min_fr = Frame((1.75+x)*inch, (5.58+y)*inch, 0.7*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
            doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[rx1_min_fr]))
            rx1_min = Paragraph(new_rx1min +' - '+new_rx1max,styles["Verdana6"])
            story.append(rx1_min)
            rx1_min_fr.addFromList(story,c)

        if bool(obj.rx2):
            #Rx2 frame
            rx2_fr = Frame((1.75+x)*inch, (5.41+y)*inch, 0.7*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
            doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[rx2_fr]))
            rx2 = Paragraph(obj.rx2,styles["Verdana8"])
            story.append(rx2)
            rx2_fr.addFromList(story,c)
    
        elif bool(obj.rx2_min):
            #Rx2 min to max frame
            rx2_min_fr = Frame((1.75+x)*inch, (5.41+y)*inch, 0.7*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
            doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[rx2_min_fr]))
            rx2_min = Paragraph(new_rx2min +' - '+new_rx2max,styles["Verdana6"])
            story.append(rx2_min)
            rx2_min_fr.addFromList(story,c)

        if bool(obj.rx3):
            #Rx3 frame
            rx3_fr = Frame((1.75+x)*inch, (5.24+y)*inch, 0.7*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
            doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[rx3_fr]))
            rx3 = Paragraph(obj.rx3,styles["Verdana8"])
            story.append(rx3)
            rx3_fr.addFromList(story,c)

        elif bool(obj.rx3_min):
            #Rx3 min to max frame
            rx3_min_fr = Frame((1.75+x)*inch, (5.24+y)*inch, 0.7*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
            doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[rx3_min_fr]))
            rx3_min = Paragraph(new_rx3min +' - '+new_rx3max,styles["Verdana6"])
            story.append(rx3_min)
            rx3_min_fr.addFromList(story,c)

        if bool(obj.rx4):
            #Rx4 frame
            rx4_fr = Frame((1.75+x)*inch, (5.07+y)*inch, 0.7*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
            doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[rx4_fr]))
            rx4 = Paragraph(obj.rx4,styles["Verdana8"])
            story.append(rx4)
            rx4_fr.addFromList(story,c)

        elif bool(obj.rx4_min):
            #Rx4 min to max frame
            rx4_min_fr = Frame((1.75+x)*inch, (5.07+y)*inch, 0.7*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
            doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[rx4_min_fr]))
            rx4_min = Paragraph(new_rx4min +' - '+new_rx4max,styles["Verdana6"])
            story.append(rx4_min)
            rx4_min_fr.addFromList(story,c)

        if bool(obj.rx5):
            #Rx5 frame
            rx5_fr = Frame((1.75+x)*inch, (4.9+y)*inch, 0.7*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
            doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[rx5_fr]))
            rx5 = Paragraph(obj.rx5,styles["Verdana8"])
            story.append(rx5)
            rx5_fr.addFromList(story,c)

        elif bool(obj.rx5_min):
            #Rx5 min to max frame
            rx5_min_fr = Frame((1.75+x)*inch, (4.9+y)*inch, 0.7*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
            doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[rx5_min_fr]))
            rx5_min = Paragraph(new_rx5min +' - '+new_rx5max,styles["Verdana6"])
            story.append(rx5_min)
            rx5_min_fr.addFromList(story,c)

        if bool(obj.rx6):
            #Rx6 frame
            rx6_fr = Frame((1.75+x)*inch, (4.73+y)*inch, 0.7*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
            doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[rx6_fr]))
            rx6 = Paragraph(obj.rx6,styles["Verdana8"])
            story.append(rx6)
            rx6_fr.addFromList(story,c)

        elif bool(obj.rx6_min):
            #Rx6 min to max frame
            rx6_min_fr = Frame((1.75+x)*inch, (4.73+y)*inch, 0.7*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
            doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[rx6_min_fr]))
            rx6_min = Paragraph(new_rx6min +' - '+new_rx6max,styles["Verdana6"])
            story.append(rx6_min)
            rx6_min_fr.addFromList(story,c)

        if bool(obj.rx7):
            #Rx7 frame
            rx7_fr = Frame((1.75+x)*inch, (4.56+y)*inch, 0.7*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
            doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[rx7_fr]))
            rx7 = Paragraph(obj.rx7,styles["Verdana8"])
            story.append(rx7)
            rx7_fr.addFromList(story,c)

        elif bool(obj.rx7_min):
            #Rx7 min to max frame
            rx7_min_fr = Frame((1.75+x)*inch, (4.56+y)*inch, 0.7*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
            doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[rx7_min_fr]))
            rx7_min = Paragraph(new_rx7min +' - '+new_rx7max,styles["Verdana6"])
            story.append(rx7_min)
            rx7_min_fr.addFromList(story,c)

        if bool(obj.rx8):
            #Rx8 frame
            rx8_fr = Frame((1.75+x)*inch, (4.39+y)*inch, 0.7*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
            doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[rx8_fr]))
            rx8 = Paragraph(obj.rx8,styles["Verdana8"])
            story.append(rx8)
            rx8_fr.addFromList(story,c)
        
        elif bool(obj.rx8_min):
            #Rx8 min to max frame            
            rx8_min_fr = Frame((1.75+x)*inch, (4.39+y)*inch, 0.7*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
            doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[rx8_min_fr]))
            rx8_min = Paragraph(new_rx8min +' - '+new_rx8max,styles["Verdana6"])
            story.append(rx8_min)
            rx8_min_fr.addFromList(story,c)

        if bool(obj.rx9):
            #Rx9 frame
            rx9_fr = Frame((1.75+x)*inch, (4.22+y)*inch, 0.7*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
            doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[rx9_fr]))
            rx9 = Paragraph(obj.rx9,styles["Verdana8"])
            story.append(rx9)
            rx9_fr.addFromList(story,c)

        elif bool(obj.rx9_min):
            #Rx9 min to max frame
            rx9_min_fr = Frame((1.75+x)*inch, (4.22+y)*inch, 0.7*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
            doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[rx9_min_fr]))
            rx9_min = Paragraph(new_rx9min +' - '+new_rx9max,styles["Verdana6"])
            story.append(rx9_min)

        if bool(obj.rx10):
            #Rx10 frame
            rx10_fr = Frame((1.75+x)*inch, (4.05+y)*inch, 0.7*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
            doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[rx10_fr]))
            rx10 = Paragraph(obj.rx10,styles["Verdana8"])
            story.append(rx10)
            rx10_fr.addFromList(story,c)

        elif bool(obj.rx10_min):
            #Rx10 min to max frame
            rx10_min_fr = Frame((1.75+x)*inch, (4.05+y)*inch, 0.7*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
            doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[rx10_min_fr]))
            rx10_min = Paragraph(new_rx10min +' - '+new_rx10max,styles["Verdana6"])
            story.append(rx10_min)
            rx10_min_fr.addFromList(story,c)

        if bool(obj.rx11):
            #Rx11 frame
            rx11_fr = Frame((1.75+x)*inch, (3.88+y)*inch, 0.7*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
            doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[rx11_fr]))
            rx11 = Paragraph(obj.rx11,styles["Verdana8"])
            story.append(rx11)
            rx11_fr.addFromList(story,c)

        elif bool(obj.rx11_min):
            #Rx11 min to max frame
            rx11_min_fr = Frame((1.75+x)*inch, (3.88+y)*inch, 0.7*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
            doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[rx11_min_fr]))
            rx11_min = Paragraph(new_rx11min +' - '+new_rx11max,styles["Verdana6"])
            story.append(rx11_min)
            rx11_min_fr.addFromList(story,c)

        if bool(obj.rx12):
            #Rx12 frame
            rx12_fr = Frame((1.75+x)*inch, (3.71+y)*inch, 0.7*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
            doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[rx12_fr]))
            rx12 = Paragraph(obj.rx12,styles["Verdana8"])
            story.append(rx12)
            rx12_fr.addFromList(story,c)

        elif bool(obj.rx12_min):
            #Rx12 min to max frame
            rx12_min_fr = Frame((1.75+x)*inch, (3.71+y)*inch, 0.7*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
            doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[rx12_min_fr]))
            rx12_min = Paragraph(new_rx12min +' - '+new_rx12max,styles["Verdana6"])
            story.append(rx12_min)
            rx12_min_fr.addFromList(story,c)

        #Polarity1 frame
        polar1_fr = Frame((1+x)*inch-(0.5*inch), (5.58+y)*inch, 0.5*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
        doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[polar1_fr]))
        polar1 = Paragraph(obj.polarity1,styles["Verdana8"])
        story.append(polar1)
        polar1_fr.addFromList(story,c)

        #Polarity2 frame
        polar2_fr = Frame((1+x)*inch-(0.5*inch), (5.41+y)*inch, 0.5*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
        doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[polar2_fr]))
        polar2 = Paragraph(obj.polarity2,styles["Verdana8"])
        story.append(polar2)
        polar2_fr.addFromList(story,c)

        #Polarity3 frame
        polar3_fr = Frame((1+x)*inch-(0.5*inch), (5.24+y)*inch, 0.5*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
        doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[polar3_fr]))
        polar3 = Paragraph(obj.polarity3,styles["Verdana8"])
        story.append(polar3)
        polar3_fr.addFromList(story,c)

        #Polarity4 frame
        polar3_fr = Frame((1+x)*inch-(0.5*inch), (5.07+y)*inch, 0.5*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
        doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[polar3_fr]))
        polar3 = Paragraph(obj.polarity3,styles["Verdana8"])
        story.append(polar3)
        polar3_fr.addFromList(story,c)

        #Polarity5 frame
        polar5_fr = Frame((1+x)*inch-(0.5*inch), (4.9+y)*inch, 0.5*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
        doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[polar5_fr]))
        polar5 = Paragraph(obj.polarity5,styles["Verdana8"])
        story.append(polar5)
        polar5_fr.addFromList(story,c)

        #Polarity6 frame
        polar6_fr = Frame((1+x)*inch-(0.5*inch), (4.73+y)*inch, 0.5*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
        doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[polar6_fr]))
        polar6 = Paragraph(obj.polarity6,styles["Verdana8"])
        story.append(polar6)
        polar6_fr.addFromList(story,c)

        #Polarity7 frame
        polar7_fr = Frame((1+x)*inch-(0.5*inch), (4.56+y)*inch, 0.5*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
        doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[polar7_fr]))
        polar7 = Paragraph(obj.polarity7,styles["Verdana8"])
        story.append(polar7)
        polar7_fr.addFromList(story,c)

        #Polarity8 frame
        polar8_fr = Frame((1+x)*inch-(0.5*inch), (4.39+y)*inch, 0.5*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
        doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[polar8_fr]))
        polar8 = Paragraph(obj.polarity8,styles["Verdana8"])
        story.append(polar8)
        polar8_fr.addFromList(story,c)

        #Polarity9 frame
        polar9_fr = Frame((1+x)*inch-(0.5*inch), (4.22+y)*inch, 0.5*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
        doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[polar9_fr]))
        polar9 = Paragraph(obj.polarity9,styles["Verdana8"])
        story.append(polar9)
        polar9_fr.addFromList(story,c)

        #Polarity10 frame
        polar10_fr = Frame((1+x)*inch-(0.5*inch), (4.05+y)*inch, 0.5*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
        doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[polar10_fr]))
        polar10 = Paragraph(obj.polarity10,styles["Verdana8"])
        story.append(polar10)
        polar10_fr.addFromList(story,c)

        #Polarity11 frame
        polar11_fr = Frame((1+x)*inch-(0.5*inch), (3.88+y)*inch, 0.5*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
        doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[polar11_fr]))
        polar11 = Paragraph(obj.polarity11,styles["Verdana8"])
        story.append(polar11)
        polar11_fr.addFromList(story,c)

        #Polarity12 frame
        polar12_fr = Frame((1+x)*inch-(0.5*inch), (3.71+y)*inch, 0.5*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
        doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[polar12_fr]))
        polar12 = Paragraph(obj.polarity12,styles["Verdana8"])
        story.append(polar12)
        polar12_fr.addFromList(story,c)        
        
        #Bandwidth frame
        bw_fr = Frame((2.53+x)*inch, (5.58+y)*inch, inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
        doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[bw_fr]))
        bw = Paragraph(obj.bwe_1,styles["Verdana8"])
        story.append(bw)
        bw_fr.addFromList(story,c)

        #Power frame
        power_fr = Frame((3.53+x)*inch, (5.58+y)*inch, 0.9*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
        doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[power_fr]))
        power = Paragraph(obj.power[0:12],styles["Verdana8_left"])
        story.append(power)
        power_fr.addFromList(story,c)
        
###Particulars of Antenna          
        #Directivity frame
        dir_fr = Frame((4.8+x)*inch, (5.45+y)*inch, 0.7*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
        doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[dir_fr]))
        dr = Paragraph(obj.dir,styles["Verdana8_left"])
        story.append(dr)
        dir_fr.addFromList(story,c)

        #Height frame
        ht_fr = Frame((4.8+x)*inch, (5.14+y)*inch, 0.7*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
        doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[ht_fr]))
        ht = Paragraph(obj.h,styles["Verdana8_left"])
        story.append(ht)
        ht_fr.addFromList(story,c)

        #Gain frame
        gn_fr = Frame((4.8+x)*inch, (4.86+y)*inch, 0.7*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
        doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[gn_fr]))
        gn = Paragraph(obj.gn,styles["Verdana8_left"])
        story.append(gn)
        gn_fr.addFromList(story,c)

        #Type of Antenna frame        
        if len(obj.t) <=20:
            toa_fr = Frame((4.8+x)*inch, (4.61+y)*inch, 1.2*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
            doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[toa_fr]))
            toa = Paragraph(obj.t[0:19],styles["Verdana8_left"])
        else:
            toa_fr = Frame((4.8+x)*inch, (4.44+y)*inch, 1.2*inch, 0.34*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
            doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[toa_fr]))
            toa = Paragraph(obj.t,styles["Verdana8_left"])
        story.append(toa)
        toa_fr.addFromList(story,c)
###End of Particulars of Antenna

##Note: Create Error Trap for this frame 01/07/2013
        
        #Remarks1 frame 
        rem1_fr = Frame((6.13+x)*inch, (5.08+y)*inch, 2*inch, 0.67*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
        doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[rem1_fr]))                           
        rem1 = Paragraph(obj.remarks,styles["Verdana8_left"])
        story.append(rem1)
        rem1_fr.addFromList(story,c)

        #Remarks2 frame
        rem2_fr = Frame((6.13+x)*inch, (4.41+y)*inch, 2*inch, 0.67*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
        doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[rem2_fr]))          
        rem2 = Paragraph(obj.remarks_2,styles["Verdana8_left"])
        story.append(rem2)
        rem2_fr.addFromList(story,c)
    
        #Model frame
        modelfr = Frame((3.6+x)*inch, (3.91+y)*inch, 4*inch, 0.19*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
        doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[modelfr]))
        model = Paragraph(obj.make,styles["VerdanaB10"])
        story.append(model)
        modelfr.addFromList(story,c)

        #Freq Range frame
        freqrangefr = Frame((3.6+x)*inch, (2.86+y)*inch, 4*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
        doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[freqrangefr]))
        freqrange = Paragraph(obj.freqrange,styles["Verdana9"])
        story.append(freqrange)
        freqrangefr.addFromList(story,c)

##SERIAL NUMBER HERE##
        ##Set location of every serial set depending to the number of serial
        ##Serial Number only
        if bool(obj.sn1) and not bool(obj.sn5) and not bool(obj.sn9) and not bool(obj.sn13) and not bool(obj.sn17) and not bool(obj.sn20):
            set1_switch = True
            sn1_only = True            
            set2_switch = set3_switch = set4_switch = set5_switch = set6_switch = False
            set_loc1 = set35_x
        ## Serial Number 1 & 2 only
        elif bool(obj.sn1) and bool(obj.sn2) and not bool(obj.sn5) and not bool(obj.sn9) and not bool(obj.sn13) and not bool(obj.sn17) and not bool(obj.sn20):
            set1_switch = True
            sn1_only = True
            sn2_only = True
            set2_switch = set3_switch = set4_switch = set5_switch = set6_switch = False
            set_loc1 = set35_x
        ## Serial Number 1, 2 & 3 only
        elif bool(obj.sn1) and bool(obj.sn2) and bool(obj.sn3) and not bool(obj.sn5) and not bool(obj.sn9) and not bool(obj.sn13) and not bool(obj.sn17) and not bool(obj.sn20):
            set1_switch = True
            sn1_only = True
            sn2_only = True
            sn3_only = True
            set2_switch = set3_switch = set4_switch = set5_switch = set6_switch = False
            set_loc1 = set35_x
        ## Serial Number 1, 2,3 & 4 only
        elif bool(obj.sn1) and bool(obj.sn2) and bool(obj.sn3) and bool(obj.sn4) and not bool(obj.sn5) and not bool(obj.sn9) and not bool(obj.sn13) and not bool(obj.sn17) and not bool(obj.sn20):
            set1_switch = True
            sn1_only = True
            sn2_only = True
            sn3_only = True
            sn4_only = True
            set2_switch = set3_switch = set4_switch = set5_switch = set6_switch = False
            set_loc1 = set35_x
        elif bool(obj.sn1) and bool(obj.sn5) and not bool(obj.sn9) and not bool(obj.sn13) and not bool(obj.sn17) and not bool(obj.sn20):
            set1_switch = set2_switch = True
            sn1_only = sn2_only = sn3_only = sn4_only = False
            set3_switch = set4_switch = set5_switch = set6_switch = False
            set_loc1 = set3_x
            set_loc2 = set4_x
        elif bool(obj.sn1) and bool(obj.sn5) and bool(obj.sn9) and not bool(obj.sn13) and not bool(obj.sn17) and not bool(obj.sn20):
            set1_switch = set2_switch = set3_switch = True            
            set4_switch = set5_switch = set6_switch = False
            sn1_only = sn2_only = sn3_only = sn4_only = False
            set_loc1 = set3_x
            set_loc2 = set4_x
            set_loc3 = set5_x            
        elif bool(obj.sn1) and bool(obj.sn5) and bool(obj.sn9) and bool(obj.sn13) and not bool(obj.sn17) and not bool(obj.sn20):
            set1_switch = set2_switch = set3_switch = set4_switch = True           
            set5_switch = set6_switch = False
            sn1_only = sn2_only = sn3_only = sn4_only = False
            set_loc1 = set2_x
            set_loc2 = set3_x
            set_loc3 = set4_x
            set_loc4 = set5_x
        elif bool(obj.sn1) and bool(obj.sn5) and bool(obj.sn9) and bool(obj.sn13) and bool(obj.sn17) and not bool(obj.sn20):
            set1_switch = set2_switch = set3_switch = set4_switch = set5_switch = set6_switch = True
            set6_switch = False
            sn1_only = sn2_only = sn3_only = sn4_only = False
            set_loc1 = set2_x
            set_loc2 = set3_x
            set_loc3 = set4_x
            set_loc4 = set5_x
            set_loc5 = set6_x         
        elif bool(obj.sn1) and bool(obj.sn5) and bool(obj.sn9) and bool(obj.sn13) and bool(obj.sn17) and bool(obj.sn20):
            set1_switch = set2_switch = set3_switch = set4_switch = set5_switch = set6_switch = True
            sn1_only = sn2_only = sn3_only = sn4_only = False
            set_loc1 = set1_x
            set_loc2 = set2_x
            set_loc3 = set3_x
            set_loc4 = set4_x
            set_loc5 = set5_x
            set_loc6 = set6_x            
            
        #Serial Number 1 frame
        if set1_switch:
            sn1_fr = Frame((set_loc1+x)*inch, (3.72+y)*inch, 1.2*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
            doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[sn1_fr]))
            if sn1_only == True:
                sn1 = Paragraph(obj.sn1,styles["Verdana8_left"])
            else:
                sn1 = Paragraph(obj.sn1,styles["Verdana8"])
            story.append(sn1)
            sn1_fr.addFromList(story,c)

            #Serial Number 2 frame
            sn2_fr = Frame((set_loc1+x)*inch, (3.55+y)*inch, 1.2*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
            doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[sn2_fr]))
            if sn2_only == True:
                sn2 = Paragraph(obj.sn2,styles["Verdana8_left"])
            else:
                sn2 = Paragraph(obj.sn2,styles["Verdana8"])           
            story.append(sn2)
            sn2_fr.addFromList(story,c)

            #Serial Number 3 frame
            sn3_fr = Frame((set_loc1+x)*inch, (3.38+y)*inch, 1.2*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
            doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[sn3_fr]))
            if sn3_only == True:
                sn3 = Paragraph(obj.sn3,styles["Verdana8_left"])
            else:
                sn3 = Paragraph(obj.sn3,styles["Verdana8"])           
            story.append(sn3)
            sn3_fr.addFromList(story,c)

            #Serial Number 4 frame
            sn4_fr = Frame((set_loc1+x)*inch, (3.21+y)*inch, 1.2*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
            doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[sn4_fr]))
            if sn4_only == True:
                sn4 = Paragraph(obj.sn4,styles["Verdana8_left"])
            else:
                sn4 = Paragraph(obj.sn4,styles["Verdana8"])
            story.append(sn4)
            sn4_fr.addFromList(story,c)

### 2nd Set
        
        if set2_switch:
            #Serial Number 5 frame
            sn5_fr = Frame((set_loc2+x)*inch, (3.72+y)*inch, 1.2*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
            doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[sn5_fr]))
            sn5 = Paragraph(obj.sn5,styles["Verdana8"])
            story.append(sn5)
            sn5_fr.addFromList(story,c)

            #Serial Number 6 frame
            sn6_fr = Frame((set_loc2+x)*inch, (3.55+y)*inch, 1.2*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
            doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[sn6_fr]))
            sn6 = Paragraph(obj.sn6,styles["Verdana8"])
            story.append(sn6)
            sn6_fr.addFromList(story,c)

            #Serial Number 7 frame
            sn7_fr = Frame((set_loc2+x)*inch, (3.38+y)*inch, 1.2*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
            doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[sn7_fr]))
            sn7 = Paragraph(obj.sn7,styles["Verdana8"])
            story.append(sn7)
            sn7_fr.addFromList(story,c)

            #Serial Number 8 frame
            sn8_fr = Frame((set_loc2+x)*inch, (3.21+y)*inch, 1.2*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
            doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[sn8_fr]))
            sn8 = Paragraph(obj.sn8,styles["Verdana8"])
            story.append(sn8)
            sn8_fr.addFromList(story,c)

### 3rd Set
        if set3_switch:
            #Serial Number 9 frame
            sn9_fr = Frame((set_loc3+x)*inch, (3.72+y)*inch, 1.2*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
            doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[sn9_fr]))
            sn9 = Paragraph(obj.sn9,styles["Verdana8"])
            story.append(sn9)
            sn9_fr.addFromList(story,c)

            #Serial Number 10 frame
            sn10_fr = Frame((set_loc3+x)*inch, (3.55+y)*inch, 1.2*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
            doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[sn10_fr]))
            sn10 = Paragraph(obj.sn10,styles["Verdana8"])
            story.append(sn10)
            sn10_fr.addFromList(story,c)

            #Serial Number 11 frame
            sn11_fr = Frame((set_loc3+x)*inch, (3.38+y)*inch, 1.2*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
            doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[sn11_fr]))
            sn11 = Paragraph(obj.sn11,styles["Verdana8"])
            story.append(sn11)
            sn11_fr.addFromList(story,c)

            #Serial Number 12 frame
            sn12_fr = Frame((set_loc3+x)*inch, (3.21+y)*inch, 1.2*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
            doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[sn12_fr]))
            sn12 = Paragraph(obj.sn12,styles["Verdana8"])
            story.append(sn12)
            sn12_fr.addFromList(story,c)

### 4th Set
        if set4_switch:
            #Serial Number 13 frame
            sn13_fr = Frame((set_loc4+x)*inch, (3.72+y)*inch, 1.2*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
            doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[sn13_fr]))
            sn13 = Paragraph(obj.sn13,styles["Verdana8"])
            story.append(sn13)
            sn13_fr.addFromList(story,c)

            #Serial Number 14 frame
            sn14_fr = Frame((set_loc4+x)*inch, (3.55+y)*inch, 1.2*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
            doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[sn14_fr]))
            sn14 = Paragraph(obj.sn14,styles["Verdana8"])
            story.append(sn14)
            sn14_fr.addFromList(story,c)

            #Serial Number 15 frame
            sn15_fr = Frame((set_loc4+x)*inch, (3.38+y)*inch, 1.2*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
            doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[sn15_fr]))
            sn15 = Paragraph(obj.sn15,styles["Verdana8"])
            story.append(sn15)
            sn15_fr.addFromList(story,c)

            #Serial Number 16 frame
            sn16_fr = Frame((set_loc4+x)*inch, (3.21+y)*inch, 1.2*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
            doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[sn16_fr]))
            sn16 = Paragraph(obj.sn16,styles["Verdana8"])
            story.append(sn16)
            sn16_fr.addFromList(story,c)

### 5th Set
        if set5_switch:
            #Serial Number 17 frame
            sn17_fr = Frame((set_loc5+x)*inch, (3.72+y)*inch, 1.2*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
            doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[sn17_fr]))
            sn17 = Paragraph(obj.sn17,styles["Verdana8"])
            story.append(sn17)
            sn17_fr.addFromList(story,c)
    
            #Serial Number 18 frame
            sn18_fr = Frame((set_loc5+x)*inch, (3.55+y)*inch, 1.2*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
            doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[sn18_fr]))
            sn18 = Paragraph(obj.sn18,styles["Verdana8"])
            story.append(sn18)
            sn18_fr.addFromList(story,c)

            #Serial Number 19 frame
            sn19_fr = Frame((set_loc5+x)*inch, (3.38+y)*inch, 1.2*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
            doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[sn19_fr]))
            sn19 = Paragraph(obj.sn19,styles["Verdana8"])
            story.append(sn19)
            sn19_fr.addFromList(story,c)
    
            #Serial Number 20 frame
            sn20_fr = Frame((set_loc5+x)*inch, (3.21+y)*inch, 1.2*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
            doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[sn20_fr]))
            sn20 = Paragraph(obj.sn20,styles["Verdana8"])
            story.append(sn20)
            sn20_fr.addFromList(story,c)

### 6th Set
        if set6_switch:
            #Serial Number 21 frame
            sn21_fr = Frame((set_loc6+x)*inch, (3.72+y)*inch, 1.2*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
            doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[sn21_fr]))
            sn21 = Paragraph(obj.sn21,styles["Verdana8"])
            story.append(sn21)
            sn21_fr.addFromList(story,c)

            #Serial Number 22 frame
            sn22_fr = Frame((set_loc6+x)*inch, (3.55+y)*inch, 1.2*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
            doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[sn22_fr]))
            sn22 = Paragraph(obj.sn22,styles["Verdana8"])
            story.append(sn22)
            sn22_fr.addFromList(story,c)

            #Serial Number 23 frame
            sn23_fr = Frame((set_loc6+x)*inch, (3.38+y)*inch, 1.2*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
            doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[sn23_fr]))
            sn23 = Paragraph(obj.sn23,styles["Verdana8"])
            story.append(sn23)
            sn23_fr.addFromList(story,c)

            #Serial Number 24 frame
            sn24_fr = Frame((set_loc6+x)*inch, (3.21+y)*inch, 1.2*inch, 0.17*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
            doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[sn24_fr]))
            sn24 = Paragraph(obj.sn24,styles["Verdana8"])
            story.append(sn24)
            sn24_fr.addFromList(story,c)

#### End Serial Number
        
        #Validity from frame
        valid_fromfr = Frame((3.8+x)*inch, (2.52+y)*inch, 2*inch, 0.19*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
        doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[valid_fromfr]))
        valid_from = Paragraph(new_validityfrom,styles["VerdanaB10"])
        story.append(valid_from)
        valid_fromfr.addFromList(story,c)

        #Validity to frame
        valid_tofr = Frame((5.9+x)*inch, (2.52+y)*inch, 2*inch, 0.19*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
        doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[valid_tofr]))
        valid_to = Paragraph(new_validityto,styles["VerdanaB10"])
        story.append(valid_to)
        valid_tofr.addFromList(story,c)
        
        #Signatory frame
        signfr = Frame((5.1+x)*inch, (0.89+y)*inch, 2*inch, 0.19*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
        doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[signfr]))
        signatory = Paragraph(obj.signatory,styles["VerdanaB10"])
        story.append(signatory)
        signfr.addFromList(story,c)

        #Encoder/Evaluator frame
        ee_fr = Frame((1.3+x)*inch, (1+y)*inch-(0.45*inch), 2*inch, 0.19*inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
        doc.addPageTemplates(PageTemplate(id= 'rsl_frame', frames=[ee_fr]))
        ee = Paragraph(obj.encoder +'/'+ obj.evaluator,styles["Verdana6_left"])
        story.append(ee)
        ee_fr.addFromList(story,c)
        
        doc.build(story)
        c.showPage()
    
    c.save()
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response     