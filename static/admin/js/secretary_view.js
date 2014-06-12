var jQuery = django.jQuery;
jQuery(function() {      
   jQuery('input.engr_choices').click(function() {    
      x =     jQuery(this).parent().parent().parent();
      x.find('.cb-activity input.checkbox').prop('checked', true);    
    });   
});

function renderProgressbar(max, dict){
  var myObj = dict;         

  for (var i = 1, c=0; i <= max; i++,c++) { 
    var selicon = '#icon-'+i,
        selcb   = '#id_form-'+c+'-ischecked',
        seltdcb = '#cb-'+i,
        selpbar = '#pbar-'+i,
        selpbarchild = '#pbar-'+i+'>div',
       
        seldetail = 'input#detail-info-'+i,
     
        idlookup = '',
        endpoint = '',
        rec_id   = 0,

        pend_progress_val = 0,
        progress_val = 0,
        
        status = myObj[i].substr(0, myObj[i].indexOf('-')),
        transtype = myObj[i].substr(myObj[i].indexOf('-')+1, myObj[i].indexOf('~')-status.length-1);
        assign_user = myObj[i].substr(myObj[i].indexOf('~')+1, myObj[i].indexOf(':')-transtype.length-status.length-2),       
        current_user = myObj[i].substr(myObj[i].indexOf(':')+1, myObj[i].indexOf('|')-assign_user.length-transtype.length-status.length-3),
        bar_length = myObj[i].indexOf('|'),        
        recent_encoder = myObj[i].substr(bar_length+1,myObj[i].length)
        //alert("|"+status+"|");
        //alert(current_user +'='+ assign_user);
    // check if pending progress bar value
    progress_val = transtype.substr(0,transtype.indexOf('-'));
    //console.log('status: '+status);
    //console.log('transtype: '+transtype);
    //console.log('assign_user: '+assign_user);
    //console.log('current_user: '+current_user);
    //console.log('bar_length: '+bar_length);
    console.log('recent_encoder: '+recent_encoder);

    if (isNumber(Number(progress_val))){
      pend_progress_val = progress_val;
    }    
    // search for record id in onclick function found at element detail-link
    rec_id = jQuery(seldetail).val();    

    if (status =="CHECKING REQUIREMENTS") {  // verified    
      jQuery('#pbar-'+i).progressbar({
        value: 10
      }); 
      jQuery(selpbarchild).css({'background':'orange'}); 
    }
    if (status =="ISSUANCE OF SOA") {  // verified
      jQuery('#pbar-'+i).progressbar({
        value: 20
      }); 
      jQuery(selpbarchild).css({'background':'orange'});                 
    }
    if (status =="PAYMENT") { // verified
      jQuery('#pbar-'+i).progressbar({
        value: 30
      }); 
      jQuery(selpbarchild).css({'background':'lightgreen'}); 
      // need to be change link here
      //jQuery(selaction).prepend('<div><a class="undo-link" href="/ccad/encoderundo/'+rec_id+'">Undo Submit</a></div>');            
      // undo link not needed for secretariat, they have logbook control, edit the logbook
    }
    if (status =="EVALUATION") { // verified
      jQuery('#pbar-'+i).progressbar({
        value: 40
      }); 
      jQuery(selpbarchild).css({'background':'orange'});     
    }
    if (status =="ENDORSEMENT") { // verified
      jQuery('#pbar-'+i).progressbar({
        value: 50
      });       
      jQuery(selpbarchild).css({'background':'lightgreen'});               
    }
    if (status =="ENCODING") {  // verified
      jQuery('#pbar-'+i).progressbar({
        value: 60
      });       
      jQuery(selpbarchild).css({'background':'orange'});           
    }
    if (status =="REVIEW") {  // verified
      jQuery('#pbar-'+i).progressbar({
        value: 70
      }); 
      jQuery(selpbarchild).css({'background':'orange'});  
    }
    if (status =="SIGNATURE") { // verified
      jQuery('#pbar-'+i).progressbar({
        value: 90
      }); 
      jQuery(selpbarchild).css({'background':'orange'});     
    }
    if (status =="CHIEF SIGNATURE") {   // verified
      jQuery('#pbar-'+i).progressbar({
        value: 92
      }); 
      jQuery(selpbarchild).css({'background':'orange'}); 
    }
    if (status =="DIRECTOR SIGNATURE") {  // verified
      jQuery('#pbar-'+i).progressbar({
        value: 94
      }); 
      jQuery(selpbarchild).css({'background':'lightgreen'});  
    }
    if (status =="CASHIER STAMP") {  // verified
      jQuery('#pbar-'+i).progressbar({
        value: 96
      }); 
      jQuery(selpbarchild).css({'background':'lightgreen'});     
    }
    if (status =="RELEASE TO SECRETARIAT") { // verified
      jQuery('#pbar-'+i).progressbar({
        value: 95
      }); 
      jQuery(selpbarchild).css({'background':'lightgreen'});
      // upload button for received from secretariat rec
    }
    if (status =="TASK COMPLETED") { // verified
      jQuery('#pbar-'+i).progressbar({
        value: 100
      }); 
      jQuery(selpbarchild).css({'background':'lightgray'});
    }
    if (status =="PENDING") { // verified
      jQuery('#pbar-'+i).progressbar({
        value: parseInt(pend_progress_val)
      });
      jQuery(selpbarchild).css({'background':'red'});
    } 
  };
}
