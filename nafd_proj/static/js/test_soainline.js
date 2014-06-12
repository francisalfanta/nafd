(function($) {
    function calc_lic(){
        var mother  = $(".grp-td.rsl_units").parent(),
            sel     = $(".grp-td.rsl_units").find('input'),
            lic     = mother.children('div.grp-td.license_fee').children('input'),
            insp_fee= mother.children('div.grp-td.inspection_fee').children('input'),
            constr  = mother.children('div.grp-td.const_fee').children('input'),
            file    = mother.children('div.grp-td.filing_fee').children('input'),
            lic_dst = mother.children('div.grp-td.rsl_dst_fee').children('input'),

            lic_rate= 480,
            if_rate = 480,
            constr_rate = 360,
            filing_rate = 180,
            dst         = 15;
            //alert(sel.val());
            // Set value
            lic.val(parseInt(sel.val(),10)*lic_rate);
            insp_fee.val(parseInt(sel.val(),10)*if_rate);
            constr.val(parseInt(sel.val(),10)*constr_rate);
            file.val(parseInt(sel.val(),10)*filing_rate);
            lic_dst.val(dst);

        // SUF value
        var suf    = mother.children('div.grp-td.suf_fee').children('input'),                               
            bw     = mother.children('div.grp-td.bw').children('input'),
            unit   = mother.children('div.grp-td.rsl_units').children('input'),
            rate   = mother.children('div.grp-td.suf_rate').children('input');                

            if ($.isNumeric(bw.val()) && $.isNumeric(unit.val()) && unit.val()>0) {
                suf.val(parseInt(rate.val(),10)*1000*parseInt(bw.val(),10)*parseInt(unit.val(),10));                
            }else if ($.isNumeric(bw.val())){                
                //alert('no unit');
                suf.val(parseInt($(this).val(),10)*1000*parseInt(bw.val(),10));                            
            } 
    }

    function calc_renlic(){
        var mother  = $(".grp-td.rsl_units").parent(),
            sel     = $(".grp-td.rsl_units").find('input'),
            lic     = mother.children('div.grp-td.license_fee').children('input'),
            insp_fee= mother.children('div.grp-td.inspection_fee').children('input'),
            lic_dst = mother.children('div.grp-td.rsl_dst_fee').children('input'),

            lic_rate= 480,
            if_rate = 480,
            dst         = 15;
            //alert(sel.val());
            // Set value
            lic.val(parseInt(sel.val(),10)*lic_rate);
            insp_fee.val(parseInt(sel.val(),10)*if_rate);
            lic_dst.val(dst);

        // SUF value
        var suf    = mother.children('div.grp-td.suf_fee').children('input'),                               
            bw     = mother.children('div.grp-td.bw').children('input'),
            unit   = mother.children('div.grp-td.rsl_units').children('input'),
            rate   = mother.children('div.grp-td.suf_rate').children('input');                

            if ($.isNumeric(bw.val()) && $.isNumeric(unit.val()) && unit.val()>0) {
                suf.val(parseInt(rate.val(),10)*1000*parseInt(bw.val(),10)*parseInt(unit.val(),10));                
            }else if ($.isNumeric(bw.val())){                
                //alert('no unit');
                suf.val(parseInt($(this).val(),10)*1000*parseInt(bw.val(),10));                            
            } 
    }

    $(document).ready(function(){ 
        $(".grp-td").css({ 'padding': '5px 5px 5px 5px' });             
        $(".grp-th").css({ 'padding': '1px 5px 1px 5px' });
        $(".grp-th").css({ 'font-weight': 'bold' });
        // background color per group
        $(".grp-td.ppp_units").css({ 'background-color': 'yellow' });   
        $(".grp-td.purchase_fee").css({ 'background-color': 'yellow' });   
        $(".grp-td.possess_fee").css({ 'background-color': 'yellow' });   
        $(".grp-td.ppp_dst_fee").css({ 'background-color': 'yellow' });   

        $(".grp-td.rsl_units").css({ 'background-color': 'yellowgreen' });
        $(".grp-td.license_fee").css({ 'background-color': 'yellowgreen' });
        $(".grp-td.inspection_fee").css({ 'background-color': 'yellowgreen' });
        $(".grp-td.rsl_dst_fee").css({ 'background-color': 'yellowgreen' });

        $(".grp-td.mod_filing_fee").css({ 'background-color': 'orange' });
        $(".grp-td.mod_units").css({ 'background-color': 'orange' });
        $(".grp-td.mod_fee").css({ 'background-color': 'orange' });

        $(".grp-td.stor_units").css({ 'background-color': 'red' });
        $(".grp-td.storage_fee").css({ 'background-color': 'red' });
        $(".grp-td.sto_dst_fee").css({ 'background-color': 'red' });

        $(".grp-td.suf_fee").css({ 'background-color': 'blue' });
        $(".grp-td.suf_rate").css({ 'background-color': 'blue' });
        $(".grp-td.freq").css({ 'background-color': 'blue' });
        $(".grp-td.bw").css({ 'background-color': 'blue' });
        
        // SUF Rate value        
        $(".grp-td.suf_rate input").change(function() {
            var mother = $(this).parent().parent(),
                suf    = mother.children('div.grp-td.suf_fee').children('input'),                               
                bw     = mother.children('div.grp-td.bw').children('input'),
                unit   = mother.children('div.grp-td.rsl_units').children('input');                 
            
            if ($.isNumeric(bw.val()) && $.isNumeric(unit.val()) && unit.val()>0) {
                suf.val(parseInt($(this).val(),10)*1000*parseInt(bw.val(),10)*parseInt(unit.val(),10));                
            }else if ($.isNumeric(bw.val())){                                
                suf.val(parseInt($(this).val(),10)*1000*parseInt(bw.val(),10));                            
            }            
        });
        // BW - assigning rate
        $(".grp-td.bw input").change(function() {
            var mother = $(this).parent().parent(),
                suf    = mother.children('div.grp-td.suf_fee').children('input'),                
                rate   = mother.children('div.grp-td.suf_rate').children('input'),
                unit   = mother.children('div.grp-td.rsl_units').children('input');  
     
            if ($.isNumeric(rate.val()) && $.isNumeric(unit.val()) && unit.val()>0){     
                suf.val(parseInt($(this).val(),10)*1000*parseInt(rate.val(),10)*parseInt(unit.val(),10));                
            }else if ($.isNumeric(rate.val())){                                
                suf.val(parseInt($(this).val(),10)*1000*parseInt(rate.val(),10));                            
            }
        });
        // Frequency - assigning rate
        $(".grp-td.freq input").change(function() {
            var sel  = $(this),
                rate = sel.parent().parent().children('div.grp-td.suf_rate').children('input');     
                        
            if (sel.val()>0 && sel.val()<=10){
                //alert('high rate');
                rate.val(2);                
            }else if (sel.val()>10 && sel.val()<=20){           
                //alert('mid rate');
                rate.val(1.5);                
            }else if (sel.val()>20){           
                //alert('mid rate');
                rate.val(1.25);                
            }
        });
        // PPP rate
        $(".grp-td.ppp_units").change(function() {
            var mother  = $(this).parent(),
                sel     = $(this).find('input'),
                pur     = mother.children('div.grp-td.purchase_fee').children('input'),
                poss    = mother.children('div.grp-td.possess_fee').children('input'),
                ppp_dst = mother.children('div.grp-td.ppp_dst_fee').children('input'),

                pur_rate  = 96,
                poss_rate = 60,
                dst   = 15;            
            //alert(mother.children('div.grp-td.purchase_fee').children('input').html());    
            //alert($(this).find('input').val());            
            // Set value
            pur.val(parseInt(sel.val(),10)*pur_rate);
            poss.val(parseInt(sel.val(),10)*poss_rate);
            ppp_dst.val(dst);
        });
        // MOD Rate
        $(".grp-td.mod_units").change(function() {
            var mother  = $(this).parent(),
                sel     = $(this).find('input'),
                mod     = mother.children('div.grp-td.mod_fee').children('input'),
                file    = mother.children('div.grp-td.mod_filing_fee').children('input'),
                mod_dst = mother.children('div.grp-td.rsl_dst_fee').children('input'),

                mod_rate= 180,
                mod_file= 180,
                dst     = 15;
                //alert(sel.val());
                // Sel value
                mod.val(parseInt(sel.val(),10)*mod_rate);
                file.val(mod_file);
                mod_dst.val(dst);
        });
        // RECALL Rate
        $(".grp-td.stor_units").change(function() {
            var mother  = $(this).parent(),
                sel     = $(this).find('input'),
                storage = mother.children('div.grp-td.storage_fee').children('input'),
                stor_dst= mother.children('div.grp-td.sto_dst_fee').children('input'),

                stor_rate = 60,
                dst  = 15;
                //alert(sel.val());
                // Set value
                storage.val(parseInt(sel.val(),10)*stor_rate);
                stor_dst.val(dst);
        });
        // NEW and REN Rate
        $(".grp-td.rsl_units").on('change', function(){
            if ($('input#id_app_type_3').is(':checked')){                
                calc_lic();    
            }
            if ($('input#id_app_type_5').is(':checked')){                
                calc_renlic();        
            }
        });
        // Channel value
        $(".grp-td.channel").change(function() {
            var mother  = $(this).parent(),
                sel     = $(this).find('input'),                             
                unit    = mother.children('div.grp-td.rsl_units').children('input');  
                        
            if (unit.val()==0) {               
                // Set value to RSL unit
                unit.val(parseInt(sel.val(),10));
            }                          
            calc_lic();            
        });
    });
})(django.jQuery);