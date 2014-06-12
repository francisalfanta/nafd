var jQuery = django.jQuery;
jQuery(function() {  
  // to unhide checkbox if condition is met
    jQuery('input.engr-choice').click(function(event) {        
      var x = jQuery(this).parent().parent().parent().parent().parent().find('.cb-activity input.checkbox'),
          y = jQuery(this).parent().parent();
      // alert(y.html());
      // endorsement choice
      y.find('.engr-choice-endo').attr('style', 'text-align:center;');    
      // encoder choice
      y.find("input[type=radio]").click(function(){
        y.find('.engr-choice-endo').hide();
        x.attr('checked','checked');
        x.show();
      });
      // pending choice
      y.find("#pending-choice select").click(function(){
        y.find('.engr-choice-endo').hide();
        x.attr('checked','checked');        
        x.show();
      });
            
    }); 
    //endorsement button showing checkbox once click    
    jQuery('#endorse-edit').click(function(){
        var x =jQuery(this).parent().parent().parent().parent();

        x.find('.cb-activity input.checkbox').attr('checked','checked');       
        x.find('.cb-activity input.checkbox').show();
    }); 
});

function hotendorse(id, pk){
  var endorse = '#endorse-'+id,
      jQuerythis   = jQuery(endorse),
      x =     jQuerythis.parent().parent();

    x.parent().parent().parent().find('.cb-activity input.checkbox').prop('checked', true);
    x.find('#endorse-edit').show();   
    x.find('#pending-choice, #encoder-pick, #engr-choice, #edit-soa').hide();
    //clear all content for pending-choice and encoder-pick
    x.find("#encoder-pick input:radio").prop('checked',false);                             
    x.find("#pending-choice select").val('');      
}

function hotencode(id){
  var encode = '#encode-'+id,
      jQuerythis  = jQuery(encode);

  jQuerythis.parent().parent().find('#encoder-pick').show();
  jQuerythis.parent().parent().find('#pending-choice, #endorse-edit, #engr-choice, #edit-soa').hide();
  //clear all content for pending-choice and endorse-edit
  //jQuerythis.parent().parent().find("#endorse-edit a").prop('href','');                             
  jQuerythis.parent().parent().find("#pending-choice select").val('');               
}

function hotpend(id){
  var pend  = '#pend-'+id,
      jQuerythis = jQuery(pend);
          
  jQuerythis.parent().parent().find('#pending-choice, #cancel-action').show();
  jQuerythis.parent().parent().find('#encoder-pick, #endorse-edit, #engr-choice, #edit-soa').hide();                
  //clear all content for encoder-pick and endorse-edit
  //jQuerythis.parent().parent().find("#endorse-edit a").prop('href','');                             
  jQuerythis.parent().parent().find("#encoder-pick input:radio").prop('checked',false);                                      
}

function cancelaction(id){
  var cancelaction = '#cancel-action-'+id,
      jQuerythis        = jQuery(cancelaction),
       x = jQuerythis.parent().parent();
  
  x.parent().parent().find('.cb-activity input.checkbox').prop('checked', false);
  x.find('#engr-choice').show();
  x.find('#encoder-pick, #endorse-edit, #pending-choice, #edit-soa').hide();
  //clear all content for endorse-edit, pending-choice and encoder-pick
  //jQuerythis.parent().parent().find("#endorse-edit a").prop('href','');   
  x.find('.engr-choice-endo').show()                          
  x.find("#encoder-pick input:radio").prop('checked',false);                 
  x.find("#pending-choice select").val('');               
}

function renderProgressbar(max, dict){
  var myObj = dict;         

  for (var i = 1, c=0; i <= max; i++,c++) { 
    var selicon = '#icon-'+i,                 //check
        selcb   = '#id_form-'+c+'-ischecked', //check
        seltdcb = '#cb-'+i,                   //check
        selpbar = '#pbar-'+i,                 //check
        selpbarchild = '#pbar-'+i+'>div',     //check
        selaction = '#action-'+i,             //check

        selengraction = '#engr-action-'+i,    //check
        selengr_action_here = '#engr-'
        seleditsoa = '#edit-soa-'+i,          //check

        seldetail = 'input#detail-info-'+i,   //check
        seluploadbtn = 'span#upload-btn-'+i,  //check
        undolink  = 'ccad/encoderundo/'+i,
        seleditrsl = 'a#edit-rsl-'+i,
        idlookup = '',
        endpoint = '',
        rec_id   = 0,
        eval_action = '#eval-action-'+i,
        engr_action = '#engr_action-here-'+i,
        selendorsementfile = '#endorsement-file-'+i,
        selppp = '#ppp-file-name-'+i,
        selfas = '#fas-file-name-'+i,

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
    //idlookup = jQuery(seldetail)[0].getAttribute('onclick');    
    //endpoint = idlookup.indexOf(',',12);      
    //rec_id   = idlookup.substr(12,endpoint-12); 
    rec_id = jQuery(seldetail).val();

    if (status =="CHECKING REQUIREMENTS") {  // verified
      jQuery('#pbar-'+i).progressbar({
        value: 10
      }); 
      jQuery(selpbarchild).css({'background':'lightgreen'});     
    }
    if (status =="ISSUANCE OF SOA") {  // verified
      jQuery('#pbar-'+i).progressbar({
        value: 20
      }); 
      if (current_user.localeCompare(assign_user) == 0) { 
        jQuery(selpbarchild).css({'background':'lightgreen'});                        
      } else {
        jQuery(selpbarchild).css({'background':'orange'});  
      }  
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
      var cbinput = jQuery(seltdcb).find('.checkbox');
      cbinput.attr('style','display:none;');
  
      if (current_user.localeCompare(assign_user) == 0) { 
        jQuery(selpbarchild).css({'background':'lightgreen'});              
        cbinput.attr('style','display:block;'); 
      } else {        
        jQuery(selpbarchild).css({'background':'orange'});                                    
      }     
    }
    if (status =="ENDORSEMENT") { // verified
      jQuery('#pbar-'+i).progressbar({
        value: 50
      }); 
      jQuery(selpbarchild).css({'background':'orange'});                                    
      if (current_user.localeCompare(assign_user) == 0) {                
        jQuery(selengraction).html('');      
      }   
    }
    if (status =="ENCODING") {  // verified
      jQuery('#pbar-'+i).progressbar({
        value: 60
      });    
      jQuery(selpbarchild).css({'background':'orange'});      
    }
    if (status =="REVIEW") { // verified
      jQuery('#pbar-'+i).progressbar({
        value: 70
      }); 
      if (current_user.localeCompare(assign_user) == 0) { 
        jQuery(selpbarchild).css({'background':'lightgreen'});                    
      } else {
        jQuery(selpbarchild).css({'background':'orange'});  // verified  
      }
    }
    // signature by verify
    if (status =="SIGNATURE") { // verified
      jQuery('#pbar-'+i).progressbar({
        value: 90
      }); 
      if (current_user.localeCompare(assign_user) == 0) { 
        jQuery(selpbarchild).css({'background':'lightgreen'});             
      } else {
        jQuery(selpbarchild).css({'background':'orange'});    
      }
    }
    // signature by chief division
    if (status =="CHIEF SIGNATURE") {   // verified
      jQuery('#pbar-'+i).progressbar({
        value: 92
      }); 
      jQuery(selpbarchild).css({'background':'lightgray'}); 
    }
    // signature by director
    if (status =="DIRECTOR SIGNATURE") {  // verified
      jQuery('#pbar-'+i).progressbar({
        value: 94
      }); 
      jQuery(selpbarchild).css({'background':'lightgray'});
    }
    // cashier stamp
    if (status =="CASHIER STAMP") {  // verified
      jQuery('#pbar-'+i).progressbar({
        value: 96
      }); 
      jQuery(selpbarchild).css({'background':'lightgray'});
    }
    if (status =="RELEASE TO SECRETARIAT") {  // verified
      jQuery('#pbar-'+i).progressbar({
        value: 98
      }); 
      jQuery(selpbarchild).css({'background':'lightgray'});
    }
    if (status =="TASK COMPLETED") {  // verified
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
