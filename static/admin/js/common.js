var jQuery = django.jQuery;
jQuery(function() {      
    // mouse hover to every activity    
    jQuery('.activity-row').mouseenter(function(){
        jQuery(this).css('background','#EEEEEE'); 
    }).mouseleave(function(){     
        jQuery(this).css('background','');
    }); 
    // check all
    jQuery('input[name="selector"]').click(function(event) {   
    if(this.checked) {
        jQuery(':checkbox').each(function() {          
            this.checked = true;             
        });
        jQuery('#testcheck').html('Uncheck All');
    } else {
        jQuery(':checkbox').each(function() {
            this.checked = false;                        
        });
        jQuery('#testcheck').html('Check All');
    }
    });
    // removing new icon
    jQuery('tr#activity-row').click(function() {    
       //jQuery(this).find("#icon").css("visibility","hidden");
       jQuery(this).find(".icon").html('');
    });   
     
});

function closeSelf(){
    document.forms['certform'].submit();
    hide(document.getElementById('divform'));
    unHide(document.getElementById('closelink'));

}

function importexcelWindow(id, type){
  var url1          = '/logs/soa_detail/import-ppp-rsl/'+id+'/',  
      url2          = '/logs/soa_detail/import-demo-dup/'+id+'/',
      width         = 1000,
      height        = 800,
      left          = (jQuery(window).width()  - width)  / 2,
      top           = (jQuery(window).height() - height) / 2,             
      opts          = 'status=1' +
                      ',width='  + width  +
                      ',height=' + height +
                      ',top='    + top    +
                      ',left='   + left   +
                      ',resizable=0, scrollbars=1, toolbar=0'; 
      if (type == 1){
        window.open(url1 , "Import Excel" , opts);     
      }
      if (type == 2){
        window.open(url2 , "Import Excel" , opts);     
      }
      //return false;
}

function ImportexcelWindow(id, type){
  var url1          = '/logs/latestrsl/import-from-excel/'+id+'/', 
      url2          = '/logs/ppp/import-from-excel/'+id+'/', 
      width         = 1000,
      height        = 800,
      left          = (jQuery(window).width()  - width)  / 2,
      top           = (jQuery(window).height() - height) / 2,             
      opts          = 'status=1' +
                      ',width='  + width  +
                      ',height=' + height +
                      ',top='    + top    +
                      ',left='   + left   +
                      ',resizable=0, scrollbars=1, toolbar=0';
      if (type == 1){
        window.open(url1 , "Import Excel" , opts);     
      } 
      if (type == 2){
        window.open(url2 , "Import Excel" , opts);     
      }

      
      //return false;
}

function refreshTable(max_record, pbar_kvalue){
  jQuery('#ccad-activity').load("{% url 'logs' url_args|iriencode %}", 
    function(responseTxt, statusTxt, xhr, max_record, pbar_kvalue){
      if (statusTxt == "success") {
        // Assignment || for study
        //jQuery('#content').slideDown('slow').animate({opacity: 10.0}, 5000).slideUp('slow');
        renderProgressbar(max_record, pbar_kvalue);
        jQuery('#pending-choice, #encoder-pick, #endorse-edit, #cancel-action').hide();
      }
    });
  // Temporarily disable during development
  setInterval(refreshTable, 30000);
}
// check if value is a number
function isNumber(n) {
  return !isNaN(parseFloat(n)) && isFinite(n);
}

function createUploader(pk){
  var uploader = new qq.FileUploader({
      element: jQuery('#file-uploader')[0],      
       action: "{% url ajax_upload %}",
        debug: true,
     multiple: false,                    
  onComplete : function(id, fileName, responseJSON) {
                if(responseJSON.success) {
                  alert("success!");
                } else {
                  alert("upload failed!");
                }                    
              },                    
       params: {
               'csrf_token': '{{ csrf_token }}',
               'csrf_name': 'csrfmiddlewaretoken',
               'csrf_xname': 'X-CSRFToken',
               'pk': pk,
              },           
  });
};

function engr_uploadWindow(id, rb_filterby){
  var uploadwindow  = '/logs/engr/upload/'+id+'/',            
      width         = 350,
      height        = 300,
      left          = (jQuery(window).width()  - width)  / 2,
      top           = (jQuery(window).height() - height) / 2,       
      opts          = 'status=1' +
                      ',width='  + width  +
                      ',height=' + height +
                      ',top='    + top    +
                      ',left='   + left   +
                      ',resizable=0, scrollbars=1, toolbar=0', 
  winref = window.open(uploadwindow , "Detail Page" , opts);
  if (winref.closed) {
    
  }
}

function ppp_popupWindow(id, type){  
  var link_to_ppp   = '/logs/detail/ppp/'+id+'/', 
      transtype     = type,
      width         = 1200,
      height        = 800,
      left          = (jQuery(window).width()  - width)  / 2,
      top           = (jQuery(window).height() - height) / 2,       
      opts          = ''; 
  //alert('transtype: '+ transtype.indexOf("RECALL"));
  //alert('transtype: '+ transtype);
  if (transtype.indexOf("NEW")>=0 || transtype.indexOf("PPP")>=0 || transtype.indexOf("TP")>=0 || transtype.indexOf("DEMO")>=0 || transtype.indexOf("STO")>=0){                   

      opts          = 'status=1' +
                      ',width='  + width  +
                      ',height=' + height +
                      ',top='    + top    +
                      ',left='   + left   +
                      ',resizable=0, scrollbars=1, toolbar=0'; 
      window.open(link_to_ppp , "Detail Page" , opts);
  } 
}

function cprsl_popupWindow(id, type){
  var link_to_cprsl = '/logs/detail/cprsl/'+id+'/',
      transtype     = type,
      width         = 1200,
      height        = 800,
      left          = (jQuery(window).width()  - width)  / 2,
      top           = (jQuery(window).height() - height) / 2,       
      opts          = '';      
  //alert('transtype: '+ transtype);
  //alert('transtype.indexOf: '+ transtype.indexOf("RECALL"));
  if (transtype.indexOf("ALL")>=0  || transtype.indexOf("RECALL")>=0 || transtype.indexOf("NEW")>=0 || transtype.indexOf("REN")>=0 || transtype.indexOf("MOD")>=0 || transtype.indexOf("RENMOD")>=0){            

      opts          = 'status=1' +
                      ',width='  + width  +
                      ',height=' + height +
                      ',top='    + top    +
                      ',left='   + left   +
                      ',resizable=0, scrollbars=1, toolbar=0';    
      
      window.open(link_to_cprsl, "Detail Page" , opts);
  }  
}