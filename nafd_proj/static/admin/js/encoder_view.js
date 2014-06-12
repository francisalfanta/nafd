var jQuery = django.jQuery
function renderProgressbar(max, dict){
  var myObj = dict;         

  for (var i = 1, c=0; i <= max; i++,c++) { 
    var selpbar = '#pbar-'+i,
        selpbarchild = '#pbar-'+i+'>div',
        selaction = '#action-'+i, 
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
        //alert(current_user +'='+ assign_user);
    // check if pending progress bar value
    progress_val = transtype.substr(0,transtype.indexOf('-'));
    //console.log('status: '+status);
    console.log('transtype: '+transtype);
    //console.log('assign_user: '+assign_user);
    //console.log('current_user: '+current_user);
    //console.log('bar_length: '+bar_length);
    //console.log('recent_encoder: '+recent_encoder);
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
    if (status =="ISSUANCE OF SOA") { // verified
      jQuery('#pbar-'+i).progressbar({
        value: 20
      }); 
      jQuery(selpbarchild).css({'background':'orange'});             
    }
    if (status =="PAYMENT") { // verified
      jQuery('#pbar-'+i).progressbar({
        value: 30
      }); 
      jQuery(selpbarchild).css({'background':'orange'});       
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
      jQuery(selpbarchild).css({'background':'orange'});      
    }
    if (status =="ENCODING") { // verified
      jQuery('#pbar-'+i).progressbar({
          value: 60
      });          
      if (current_user.localeCompare(assign_user) == 0) {          
        jQuery(selpbarchild).css({'background':'lightgreen'}); 
      } else { 
        jQuery(selpbarchild).css({'background':'lightgray'}); 
      }
    }
    if (status =="REVIEW") { // verified
      jQuery('#pbar-'+i).progressbar({
        value: 70
      }); 
      jQuery(selpbarchild).css({'background':'orange'});                
      if (current_user.localeCompare(recent_encoder) == 0) {    // comparing previous encoder with current user
        jQuery(selaction).prepend('<div><a class="undo-link" href="/logs/encoder/undo/'+rec_id+'" style="font-size:14; font-weight:bold">Undo Submit</a></div>');        
      }
    }
    if (status =="SIGNATURE") { //verified
      jQuery('#pbar-'+i).progressbar({
        value: 90
      }); 
      jQuery(selpbarchild).css({'background':'lightgray'});      
    }
    // signature by chief division
    if (status =="CHIEF SIGNATURE") {   //verified
      jQuery('#pbar-'+i).progressbar({
        value: 92
      }); 
      jQuery(selpbarchild).css({'background':'lightgray'});                          
    }
    // signature by director
    if (status =="DIRECTOR SIGNATURE") {  //verified
      jQuery('#pbar-'+i).progressbar({
        value: 94
      }); 
      jQuery(selpbarchild).css({'background':'lightgray'});                          
    }
    // cashier stamp
    if (status =="CASHIER STAMP") {   //verified
      jQuery('#pbar-'+i).progressbar({
        value: 96
      }); 
      jQuery(selpbarchild).css({'background':'lightgray'});                          
    }
    if (status =="RELEASE TO SECRETARIAT") { //verified
      jQuery('#pbar-'+i).progressbar({
        value: 98
      }); 
      jQuery(selpbarchild).css({'background':'lightgray'});              
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
