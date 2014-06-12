(function($) {
    function toggle_suf(status){
      if (status == 0){
        // hide SUF
        $('input#id_app_type_0').removeAttr('checked');
        //$('.grp-th.suf-rate, .grp-th.freq, .grp-th.bw, .grp-th.suf').hide();
        //$('.grp-td.suf_rate, .grp-td.freq, .grp-td.bw, .grp-td.suf_fee').hide();
        //$('.grp-td.suf_rate input, .grp-td.freq input, .grp-td.bw input, .grp-td.suf_fee input').val(0);
      }else if (status == 1){
        // show SUF
        $('input#id_app_type_0').prop('checked', true);
        //$('.grp-th.suf-rate, .grp-th.freq, .grp-th.bw, .grp-th.suf').show();
        //$('.grp-td.suf_rate, .grp-td.freq, .grp-td.bw, .grp-td.suf_fee').show();
      }
    }

    function toggle_ppp(status){
      if (status == 1){
        // show PPP         
        $("input#id_app_type_2").prop('checked', true);        
        //$('.grp-th.no-ppp, .grp-th.pur-fee, .grp-th.poss-fee, .grp-th.ppp-dst').show();
        //$('.grp-td.ppp_units, .grp-td.purchase_fee, .grp-td.possess_fee, .grp-td.ppp_dst_fee').show();        
      }else if (status == 0){
        // hide PPP
        $("input#id_app_type_2").removeAttr('checked');
        //$('.grp-th.no-ppp, .grp-th.pur-fee, .grp-th.poss-fee, .grp-th.ppp-dst').hide();
        //$('.grp-td.ppp_units, .grp-td.purchase_fee, .grp-td.possess_fee, .grp-td.ppp_dst_fee').hide();
        //$('.grp-td.ppp_units input, .grp-td.purchase_fee input, .grp-td.possess_fee input, .grp-td.ppp_dst_fee input').val(0);
      }
    }

    function toggle_demo(status){
      if (status == 1){
        // show Demo
        $("input#id_app_type_8").prop('checked', true);        
        //$('.grp-th.no-lic, .grp-th.file-fee, .grp-th.lic-dst').show();
        //$('.grp-td.rsl_units, .grp-td.filing_fee, .grp-td.rsl_dst_fee').show();
      }else if (status == 0){
        // hide Demo
        $("input#id_app_type_8").removeAttr('checked');        
        //$('.grp-th.no-lic, .grp-th.file-fee, .grp-th.lic-dst').hide();
        //$('.grp-td.rsl_units, .grp-td.filing_fee, .grp-td.rsl_dst_fee').hide();
        //$('.grp-td.rsl_units input, .grp-td.filing_fee input, .grp-td.rsl_dst_fee input').val(0);
      }
    }

    function toggle_dup(status){
      if (status == 1){
        // show Duplicate
        $("input#id_app_type_7").prop('checked', true);        
        //$('.grp-th.dup-fee').show();
        //$('.grp-td.duplicate_fee').show();
      }else if (status == 0){
        // hide Duplicate
        $("input#id_app_type_7").removeAttr('checked');
        //$('.grp-th.dup-fee').hide();
        //$('.grp-td.duplicate_fee').hide();
        //$('.grp-td.duplicate_fee input').val(0);
      }
    }

    function toggle_mod(status){
      if (status == 1) {
        // show MOD
        $("input#id_app_type_4").prop('checked', true);        
        //$('.grp-th.no-mod, .grp-th.mod, .grp-th.mod-file, .grp-th.lic-dst').show();
        //$('.grp-td.mod_units, .grp-td.mod_fee, .grp-td.mod_filing_fee, .grp-td.rsl_dst_fee').show();
      }else if (status == 0){
        // hide MOD
        $("input#id_app_type_4").removeAttr('checked');
        //$('.grp-th.no-mod, .grp-th.mod, .grp-th.mod-file, .grp-th.lic-dst').hide();
        //$('.grp-td.mod_units, .grp-td.mod_fee, .grp-td.mod_filing_fee, .grp-td.rsl_dst_fee').hide();
        //$('.grp-td.mod_units input, .grp-td.mod_fee input, .grp-td.mod_filing_fee input, .grp-td.rsl_dst_fee input').val(0);
      }
    }

    function toggle_recall(status){
      if (status == 1){
        // show RECALL
        $("input#id_app_type_6").prop('checked', true);
        //$('.grp-th.no-stor, .grp-th.stor-fee, .grp-th.stor-dst').show();
        //$('.grp-td.stor_units, .grp-td.storage_fee, .grp-td.sto_dst_fee').show();
      }else if (status == 0){
        // hide RECALL
        $("input#id_app_type_6").removeAttr('checked');
        //$('.grp-th.no-stor, .grp-th.stor-fee, .grp-th.stor-dst').hide();
        //$('.grp-td.stor_units, .grp-td.storage_fee, .grp-td.sto_dst_fee').hide();
        //$('.grp-td.stor_units input, .grp-td.storage_fee input, .grp-td.sto_dst_fee input').val(0);
      }
    }

    function toggle_newlic(status){
      if (status == 1) {
        // show License
        $('input#id_app_type_3').prop('checked', true);
        //$('.grp-th.no-chan, .grp-th.file-fee, .grp-th.const-fee, .grp-th.no-lic, .grp-th.lic, .grp-th.if, .grp-th.lic-dst').show();
        //$('.grp-td.channel, .grp-td.filing_fee, .grp-td.const_fee, .grp-td.rsl_units, .grp-td.license_fee, .grp-td.inspection_fee, .grp-td.rsl_dst_fee').show();                    
      }else if (status ==0) {
        // hide License
        $('input#id_app_type_3').removeAttr('checked');
        //$('.grp-th.no-chan, .grp-th.file-fee, .grp-th.const-fee, .grp-th.no-lic, .grp-th.lic, .grp-th.if, .grp-th.lic-dst').hide();
        //$('.grp-td.channel, .grp-td.filing_fee, .grp-td.const_fee, .grp-td.rsl_units, .grp-td.license_fee, .grp-td.inspection_fee, .grp-td.rsl_dst_fee').hide();
        //$('.grp-td.channel input, .grp-td.filing_fee input, .grp-td.const_fee input, .grp-td.rsl_units input, .grp-td.license_fee input , .grp-td.inspection_fee input, .grp-td.rsl_dst_fee input').val(0);
      }
    }

    function toggle_renewlic(status){
      if (status == 1) {
        // show License
        $('input#id_app_type_5').prop('checked', true);
        //$('.grp-th.no-chan, .grp-th.no-lic, .grp-th.lic, .grp-th.if, .grp-th.lic-dst').show();
        //$('.grp-td.channel, .grp-td.rsl_units, .grp-td.license_fee, .grp-td.inspection_fee, .grp-td.rsl_dst_fee').show();                    
      }else if (status ==0) {
        // hide License
        $('input#id_app_type_5').removeAttr('checked');
        //$('.grp-th.no-chan, .grp-th.no-lic, .grp-th.lic, .grp-th.if, .grp-th.lic-dst').hide();
        //$('.grp-td.channel, .grp-td.rsl_units, .grp-td.license_fee, .grp-td.inspection_fee, .grp-td.rsl_dst_fee').hide();
        //$('.grp-td.channel input, .grp-td.rsl_units input, .grp-td.license_fee input, .grp-td.inspection_fee input, .grp-td.rsl_dst_fee input').val(0);
      }
    }
    
    function toggle_sur(status){
      if (status == 1){
        // show Surcharge
        //$('.grp-th.sur-lic, .grp-th.sur-suf').show();
        //$('.grp-td.sur_lic_percent, .grp-td.sur_lic, .grp-td.sur_suf_percent, .grp-td.sur_suf').show();
      }else if(status == 0){
        // hide Surcharge
        //$('.grp-th.sur-lic, .grp-th.sur-suf').hide();
        //$('.grp-td.sur_lic_percent, .grp-td.sur_lic, .grp-td.sur_suf_percent, .grp-td.sur_suf').hide();
        //$('.grp-td.sur_lic_percent input, .grp-td.sur_lic input, .grp-td.sur_suf_percent input, .grp-td.sur_suf input').val(0);
      }     
    }
        
    $(document).ready(function(){     
        // Initialize inline table                        
        //$('div#soa_detail_set-group').show();
        //$('.grp-th.suf-rate, .grp-th.freq, .grp-th.bw, .grp-th.suf').hide();
        //$('.grp-td.suf_rate, .grp-td.freq, .grp-td.bw, .grp-td.suf_fee').hide();
        //$('.grp-th.no-ppp, .grp-th.pur-fee, .grp-th.poss-fee, .grp-th.ppp-dst').hide();
        //$('.grp-td.ppp_units, .grp-td.purchase_fee, .grp-td.possess_fee, .grp-td.ppp_dst_fee').hide();
        //$('.grp-th.no-lic, .grp-th.file-fee, .grp-th.lic-dst').hide();
        //$('.grp-td.rsl_units, .grp-td.filing_fee, .grp-td.rsl_dst_fee').hide();
        //$('.grp-th.dup-fee').hide();
        //$('.grp-td.duplicate_fee').hide();
        //$('.grp-th.no-mod, .grp-th.mod, .grp-th.mod-file, .grp-th.lic-dst').hide();
        //$('.grp-td.mod_units, .grp-td.mod_fee, .grp-td.mod_filing_fee, .grp-td.rsl_dst_fee').hide();        
        //$('.grp-th.no-stor, .grp-th.stor-fee, .grp-th.stor-dst').hide();
        //$('.grp-td.stor_units, .grp-td.storage_fee, .grp-td.sto_dst_fee').hide();        
        //$('.grp-th.no-chan, .grp-th.file-fee, .grp-th.const-fee, .grp-th.no-lic, .grp-th.lic, .grp-th.if, .grp-th.lic-dst').hide();
        //$('.grp-td.channel, .grp-td.filing_fee, .grp-td.const_fee, .grp-td.rsl_units, .grp-td.license_fee, .grp-td.inspection_fee, .grp-td.rsl_dst_fee').hide();        
        //$('.grp-th.no-chan, .grp-th.no-lic, .grp-th.lic, .grp-th.if, .grp-th.lic-dst').hide();
        //$('.grp-td.channel, .grp-td.rsl_units, .grp-td.license_fee, .grp-td.inspection_fee, .grp-td.rsl_dst_fee').hide();        
        //toggle_sur(0); 
        
        //var no_checked = 0;
        /*
        $('input:checkbox:checked').each(function(){
            no_checked = no_checked+1;
            var v_id  = $(this).attr('id');
            //alert(v_id);
            if (v_id == 'id_app_type_0'){
              toggle_suf(1);
            }
            if (v_id == 'id_app_type_1'){
              toggle_suf(1);
              toggle_ppp(1);                     
              toggle_mod(1);
              toggle_recall(1);
              toggle_newlic(1);   
              toggle_sur(1); 
            }
            if (v_id == 'id_app_type_2'){
              toggle_ppp(1);             
            }
            if (v_id == 'id_app_type_3'){
              toggle_newlic(1);
            }
            if (v_id == 'id_app_type_4'){
              toggle_mod(1);
            }
            if (v_id == 'id_app_type_5'){
              toggle_renewlic(1);
            }
            if (v_id == 'id_app_type_6'){
              toggle_recall(1);
            }
            if (v_id == 'id_app_type_7'){
              toggle_dup(1);
            }
            if (v_id == 'id_app_type_8'){
              toggle_demo(1);
            }
        });
        /*alert(no_checked);
        if (no_checked == 0) {            
            toggle_suf(0);
            toggle_ppp(0);
            toggle_dup(0);
            toggle_demo(0);
            toggle_mod(0);
            toggle_recall(0);
            toggle_newlic(0);   
            toggle_sur(0);       
        }        
       
        $('#id_service_type').change(function(){            
            if($(this).val() === '2G' || $(this).val() === '3G'){              
              toggle_suf(0);
            }else{              
              toggle_suf(1);
            }
        });
        /* Only SUF
        $("input#id_app_type_0").on("click", function(e){
          if($(this).is(':checked')){
            // show SUF
            toggle_suf(1);
          }else {
            // hide SUF
            toggle_suf(0);
          }
        });     
        /* Select all fields
        $("input#id_app_type_1").on("click", function(e){
          toggle_dup(0); // hide Duplicate          

          if($(this).is(':checked')){
            $('input#id_app_type_1').prop('checked', true);           
            toggle_ppp(1); // show PPP            
            toggle_suf(1); // show SUF
            toggle_newlic(1); // show License            
            toggle_mod(1); // show MOD
            toggle_recall(1); // show Storage            
            toggle_sur(1); // show Surcharge            
            toggle_renewlic(1); //show REN
          }else {
            $('input#id_app_type_1').removeAttr('checked');            
            toggle_ppp(0); // hide PPP
            toggle_suf(0); // hide SUF            
            toggle_newlic(0); // hide License            
            toggle_mod(0); // hide MOD
            toggle_recall(0); // hide Storage
            toggle_sur(0); // hide Surcharge 
            toggle_renewlic(0); // hide REN           
          }
        });
        // Only PPP
        $("input#id_app_type_2").on("click", function(e){
          if($(this).is(':checked')){               
            toggle_ppp(1); *//*show PPP   
          }else {            
            toggle_ppp(0); // hide PPP
          }
        });
        */// Only New
        $("input#id_app_type_3").on("click", function(e){   
          //toggle_demo(0); // hide Demo          
          //toggle_dup(0); // hide Duplicate          
          //toggle_recall(0); // hide Storage          
          //toggle_mod(0); // hide MOD
          //toggle_sur(0); // hide Surcharge
          
          if($(this).is(':checked')){
            $("input#id_app_type_2").prop('checked', true);
            $("input#id_app_type_9").prop('checked', true);
            $("input#id_app_type_10").prop('checked', true);
            //toggle_ppp(1); // show PPP         
            //toggle_suf(1); // show SUF
            //toggle_newlic(1); // show License            
          }else{
            $("input#id_app_type_2").prop('checked', false);
            $("input#id_app_type_9").prop('checked', false);
            $("input#id_app_type_10").prop('checked', false);
            //toggle_ppp(0); // hide PPP
            //toggle_suf(0); // hide SUF
            //toggle_newlic(0); // hide License            
          }
        });
        // Only Mod
        $("input#id_app_type_4").on("click", function(e){  
          if($(this).is(':checked')){
            $("input#id_app_type_2").prop('checked', true);
            $("input#id_app_type_6").prop('checked', true);
            $("input#id_app_type_9").prop('checked', true);
            $("input#id_app_type_10").prop('checked', true);
            //toggle_mod(1); // show MOD
          }else{
            $("input#id_app_type_2").prop('checked', false);
            $("input#id_app_type_2").prop('checked', false);
            $("input#id_app_type_9").prop('checked', false);
            $("input#id_app_type_10").prop('checked', false);
            //toggle_mod(0); // hide MOD
          }
        });
        /* Only Ren
        $("input#id_app_type_5").on("click", function(e){ 
          if($(this).is(':checked')){
            $("input#id_app_type_10").prop('checked', true);
            //toggle_suf(1); // show SUF
            //toggle_renewlic(1); // show License            
            //toggle_sur(1); // show Surcharge
          }else{
            $("input#id_app_type_10").prop('checked', false);
            //toggle_suf(0); // hide SUF
            //toggle_renewlic(0); // hide License            
            //toggle_sur(0); // hide Surcharge            
          }
        });
        /* Only Recall with Standard Fields
        $("input#id_app_type_6").on("click", function(e){
          if($(this).is(':checked')){
            toggle_recall(1); // show Storage            
          }else{
            toggle_recall(0); // hide Storage
          }
        });
        // Only Duplicate
        $("input#id_app_type_7").on("click", function(e){ 
          if($(this).is(':checked')){
            toggle_dup(1); // show Duplicate            
          }else{
            toggle_dup(0); // hide Duplicate            
          }
        });
        // Only Demo
        $("input#id_app_type_8").on("click", function(e){      
          if($(this).is(':checked')){
            toggle_demo(1); // show Demo
          }else{
            toggle_demo(0); // hide Demo
          }
        });*/
    });   
})(django.jQuery);