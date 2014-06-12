"""
To group the paragraph with the next flowable such as table

paragraph = Paragraph(header_string, styleH)
paragraph.keepWithNext = True
Story.append(paragraph)
Story.append(table)

"""

# Page Setup
PAGE_WIDTH, PAGE_HEIGHT = landscape(letter)

class MyPdf():
    """
    My PDF
    """
    document            = None

    def __init__(self, file_like_handle=None):
        self.document = BaseDocTemplate(file_like_handle, pagesize=landscape(letter))

        self.build_templates()

    def build_templates(self):

        first_page_frames = []

        #First Page Title Frame
        frame_title = Frame(.25*inch, PAGE_HEIGHT-(1.75*inch), PAGE_WIDTH-(inch*.5), inch*.5, id="frame_title", showBoundary=0)
        first_page_frames.append(frame_title)

        # First Page Body Frames
        frame_body = Frame(.5*inch, PAGE_HEIGHT-(8*inch), PAGE_WIDTH-(inch), inch*6.25, id="frame_body", showBoundary=0)
        first_page_frames.append(frame_body)

        # Second Page Body Frame
        frame_body_full = Frame(.5*inch, PAGE_HEIGHT-(8*inch), PAGE_WIDTH-(inch), inch*7, id="frame_body_full", showBoundary=0)

        templates = []
        templates.append(PageTemplate(frames=first_page_frames, id="first_page", onPage=self.first_page))
        templates.append(PageTemplate(frames=[frame_body_full], id="child_pages", onPage=self.child_pages))
        templates.append(PageTemplate(frames=[frame_body_full], id="child_pages", onPage=self.last_page))
        self.document.addPageTemplates(templates)


    def first_page(self, canvas, doc):
        """
        First page has an image header and footer
        """
        canvas.saveState()
        canvas.drawInlineImage(settings.MEDIA_ROOT + "../static/pdf-header-landscape.png", inch*.25, PAGE_HEIGHT-(1.25 * inch), PAGE_WIDTH-(.5*inch), ((11/8)*inch))
        canvas.drawInlineImage(settings.MEDIA_ROOT + "../static/pdf-footer-landscape.png", inch*.25, inch*.25, PAGE_WIDTH-(.5*inch), (.316*inch))
        canvas.restoreState()


    def child_pages(self, canvas, doc): 
        """
        Second page has a smaller header and the same footer
        """
        canvas.saveState()  
        canvas.setFillColor(HexColor("#f4f3f1"))
        canvas.rect(inch*.25, PAGE_HEIGHT-(.25 * inch), PAGE_WIDTH-(.5*inch), -(.5*inch), fill=1, stroke=0)
        canvas.setFillColor(HexColor("#e5b53b"))
        canvas.setFont('Gotham-Bold', 16)
        canvas.drawString(inch*.5, PAGE_HEIGHT-((.6)*inch), "PAGE")
        canvas.setFillColor(HexColor("#00355f"))
        canvas.drawString(inch*1.75, PAGE_HEIGHT-((.6)*inch), "OVERVIEW")
        canvas.drawInlineImage(settings.MEDIA_ROOT + "../static/pdf-footer-landscape.png", inch*.25, inch*.25, PAGE_WIDTH-(.5*inch), (.316*inch))
        canvas.restoreState()


    def build(self):
        return self.document.build(self.elements)


    def add_first_page(self):

        sample = getSampleStyleSheet()
        style_title = copy.deepcopy(sample['BodyText'])
        style_title.fontSize = 18
        style_title.textColor = HexColor("#00355f")

        style_body  = copy.deepcopy(sample['BodyText'])
        style_body.fontSize = 10
        style_body.alignment = reportlab.lib.enums.TA_LEFT
        style_body.spaceBefore = 25
        style_body.spaceAfter = 15
        style_body.textColor = HexColor("#000000")
        style_body.leading = 14

        self.elements.append(Paragraph("""<font color="#e5b53b">PAGE</font>OVERVIEW""", style_title))
        self.elements.append(FrameBreak())

        self.elements.append(Paragraph("""Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aenean elementum malesuada euismod. Praesent ut ante risus. Aenean eleifend massa elit, non adipiscing ipsum. Integer et arcu tortor, a bibendum metus. Maecenas eget nulla id sem placerat dignissim sit amet et ligula. Donec vitae mi mauris. Praesent lacinia, mauris at malesuada bibendum, metus eros molestie ipsum, sed consequat dolor diam interdum ipsum. Phasellus consectetur auctor laoreet. Suspendisse vel nisl lacus, vitae auctor dui.""", style_body))

        # ADD A CUSTOM REPORTLAB CANVAS OBJECT
        self.elements.append(SomeGraph())

        self.elements.append(Paragraph("""Our strategic allocations for each strategy are determined by our Dynamic Strategic Asset Allocation process - the Science of Dynamic Investing. Our proprietary mathematical model uses updated Price Matters<super>&reg;</super> capital market assumptions (expected return, risk and correlation figures) to determine the optimal allocation to each asset class to achieve the goals of each strategy within the assigned risk tolerance and time horizon. The Art of Dynamic Investing enables us to adapt to changing economic and political realities as we reposition strategies with tactical tilts to the strategic allocations as we see value and momentum of various asset classes being affected during the year. <font color="#e5b53b">The chart below</font> shows the strategic weightings and the tactical allocations to each asset class as of the close of business on the date cited.""", style_body))

        self.elements.append(NextPageTemplate("child_pages"))
        self.elements.append(PageBreak())       

    def add_second_page(self):
        sample = getSampleStyleSheet()
        style_title = copy.deepcopy(sample['BodyText'])
        style_title.fontSize = 18
        style_title.textColor = HexColor("#00355f")

        style_body  = copy.deepcopy(sample['BodyText'])
        style_body.fontSize = 10
        style_body.alignment = reportlab.lib.enums.TA_LEFT
        style_body.spaceBefore = 25
        style_body.spaceAfter = 15
        style_body.textColor = HexColor("#000000")
        style_body.leading = 14

        self.elements.append(Paragraph("""Morbi posuere erat non nunc faucibus rhoncus. Donec at ante at tellus vehicula gravida. Praesent vulputate viverra neque, ut consectetur turpis vestibulum at. Integer interdum diam sed leo vehicula in viverra mauris venenatis. Morbi tristique pretium nunc vel ultrices. Fusce vitae augue lorem, et feugiat lorem. Donec sit amet nulla eget elit feugiat euismod rutrum ut magna. Pellentesque condimentum, tellus at rutrum egestas, dui neque dapibus risus, malesuada mollis risus eros id ligula. Fusce id cursus nulla. Etiam porttitor vulputate tellus eu blandit. Donec elementum erat sed tellus dapibus eleifend. Pellentesque sagittis, libero ac sodales laoreet, erat turpis fringilla est, vel accumsan nunc nisi eget orci. Integer condimentum libero in tellus lacinia ultricies quis ac odio. Vivamus justo urna, faucibus vitae bibendum dapibus, condimentum et ligula. Nullam interdum velit at orci blandit nec suscipit lorem lobortis. Pellentesque purus nunc, pulvinar vitae ullamcorper id, rhoncus sit amet diam.""", style_body))

    def add_disclosures(self):

        sample = getSampleStyleSheet()
        style_d = copy.deepcopy(sample['BodyText'])
        style_d.fontSize        = 8
        style_d.alignment   = reportlab.lib.enums.TA_LEFT
        style_d.textColor   = HexColor("#9D8D85")

        self.elements.append(NextPageTemplate("last_page"))
        self.elements.append(PageBreak())

        self.elements.append(Paragraph("""Important Disclosures""", style_d))

        self.elements.append(Paragraph("""Copyright 2012 Francis Yaconiello All Rights Reserved.""", style_d))