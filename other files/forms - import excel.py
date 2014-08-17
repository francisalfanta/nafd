# coding:utf-8
from django import forms
from django.forms.util import ErrorList
from django.utils.datastructures import SortedDict
import json
import xlrd

class ImportExcelForm(forms.Form):
    excel_file = forms.FileField(required=False)
    converted_items = forms.CharField(widget=forms.HiddenInput, required=False)
    comment = forms.CharField(widget=forms.TextInput(attrs={'class':'special', 'size': '40', 'style': 'width:240px'}), required=False)
    is_good = forms.BooleanField(widget=forms.HiddenInput(attrs={'class':'special', 'size': '40', 'style': 'text-align:center'}), required=False)
    model_id= forms.IntegerField(widget=forms.HiddenInput, required=False)    # added to get the instance id 
    
    def clean_converted_items(self):
        converted_items = self.cleaned_data['converted_items']
        if not converted_items:
            return None
        try:
            converted_items = json.loads(converted_items)
        except ValueError:
            raise forms.ValidationError(u'Bad converted data')
        return converted_items

    def clean(self):
        cleaned_data = self.cleaned_data
        if not cleaned_data.get('excel_file') and not cleaned_data.get('converted_items'):
            self.errors['excel_file'] = ErrorList([u'Required Field'])
        return cleaned_data

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
        
        return converted_items

    def update_callback(self, request, converted_items):       
        raise NotImplementedError
