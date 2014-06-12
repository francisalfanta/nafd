#from models import SOA, SOA_detail, Sitename

from django.http import HttpResponse
from django.utils import encoding, formats

import re
import string

import reportlab.rl_config

from reportlab.pdfgen import canvas

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from reportlab.lib.units import inch
from reportlab.lib.utils import ImageReader
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

from reportlab.platypus import Paragraph, Frame, Table
from reportlab.platypus import BaseDocTemplate, PageTemplate, Paragraph, Frame
from reportlab.platypus import NextPageTemplate, PageBreak

from reportlab.lib.pagesizes import landscape

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

"""Setting Custom Page Size """
PAGE_WIDTH, PAGE_HEIGHT = (13*inch, 8.5*inch)
custom_page = (PAGE_WIDTH, PAGE_HEIGHT)

class SOA_pdf():
    """
    Notes to ponder
    write a class to create and encapsulate your PDF document object
        The first PDF doc I wrote kept growing in scope - having all of the logic in the view became too much to manage
        Your class should have a function to build out each of your page templates
        If your page templates use callbacks onPage= each of those callbacks should also be defined separately in your class
        Each unique section of data should have its own function (in my case: page 1, page 2, 
        and disclosures each got a function because they were logically different chunks of data)
    """    
    buffer = StringIO()
    c = canvas.Canvas(buffer, pagesize=landscape(custom_page))
    # Used the file contain in the buffer,
    # set by custom_page and don't allow splitting across frames
    def __init__(self, file_handle=None):
        self.document = BaseDocTemplate(file_handle, showBoundary=1, leftMargin= 0.1*inch, rightMargin= 0.1*inch,
                                        topMargin= 0.1*inch, bottomMargin= 0.1*inch, pageSize=landscape(custom_page), allowSplitting=0, 
                                        title="Statement of Collection Report", author="Francis T.M. Alfanta")
        self.build_templates()

    def build_templates(self):
        soa_page_frames = []

        #header
        frame_header = Frame(0.25*inch, PAGE_HEIGHT-inch,PAGE_WIDTH-0.25*inch,PAGE_HEIGHT-0.75*inch,
                             id="frame_header", showBoundary=1)

        templates = []
        templates.append(PageTemplate(frames=frame_header, id="first_page", onPage=self.soa_header))
        self.document.addPageTemplates(templates)

    def soa_header(self, canvas, doc):        
        # header
        canvas.saveState()
        canvas.setFillColor(HexColor("#f4f3f1"))
        canvas.rect(inch*.25, PAGE_HEIGHT-(.25 * inch), PAGE_WIDTH-(.5*inch), -(.5*inch), fill=1, stroke=0)
        canvas.setFillColor(HexColor("#e5b53b"))
        canvas.setFont('Gotham-Bold', 16)
        canvas.drawString(inch*.5, PAGE_HEIGHT-((.6)*inch), "PAGE")
        canvas.setFillColor(HexColor("#00355f"))
        canvas.drawString(inch*1.75, PAGE_HEIGHT-((.6)*inch), "OVERVIEW")
        #canvas.drawInlineImage(settings.MEDIA_ROOT + "../static/pdf-footer-landscape.png", inch*.25, inch*.25, PAGE_WIDTH-(.5*inch), (.316*inch))
        canvas.restoreState()

    def build(self):
        return self.document.build(self)



    


