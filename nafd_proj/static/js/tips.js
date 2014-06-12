/* tips   
   // header.removeClass('icon-minus').addClass('icon-plus');
   // $("ul.featureList").hide();
  
 ## substr - extracts parts of a string
    syntax - string.substr(start,length)
    eg. - recid = this.id,
          recno = recid.substr(recid.indexOf('-')+1); 
 ## closest() with find()
    pbar = sel.closest('tr#activity-row.target').find('#pbar');
  or
    $(selcb).closest("tr#activity-row").find("#icon").css("visibility","hidden");
 ## find child within parent
    for(var i=0, length = parents.length, found = false; i < length && !found; i++){
      var parent = parents[i];
      if(parent.querySelector('#icon')){
        alert('index is '+i);
        found = true;
      }
    }
 ## remove elements
    eg. <div id="filters">
          <div class="filterData">hello</div>
        </div>
    $("#filters .filterData").remove();
 ## dynamically set color as the value change
    $("#pbar0").bind('progressbarchange', function(event, ui) {
        var selector = "#" + this.id + " > div";
        var value = this.getAttribute( "aria-valuenow" );
        if (value < 10){
            $(selector).css({ 'background': 'Red' });
        } else if (value < 30){
            $(selector).css({ 'background': 'Orange' });
        } else if (value < 50){
            $(selector).css({ 'background': 'Yellow' });
        } else{
            $(selector).css({ 'background': 'LightGreen' });
        }
    });

    ## using css to change color the progress bar##
     .ui-progressbar.ui-widget-content {
     background: url(images/white-40x100.png) #ffffff repeat-x 50% 50%;
     }

    .ui-progressbar.ui-widget-header {
     color: Blue;
     background: url(images/lime-1x100.png) #cccccc repeat-x 50% 50%;
    }

    ## Cancel a default action and prevent it from bubbling up by returning false:
    $("form").bind("submit", function() { return false; })
   

## use jQuery to get a string of text from the onclick attribute and set it as the href attribute.
$('a').attr('href', 
            $('a')[0].getAttribute('onclick')
            .replace("window.open('", '').split(',')[0].replace("'", ''))
      .removeAttr('onclick');  


## Changing class name of tag
jQuery(this).parent().next("i").removeClass('icon-plus').addClass('icon-minus'); 
to

jQuery(this).find('i').toggleClass('icon-plus icon-minus');

 */

/***
/* xample how to hide inline form
        $('.module[id^=module] .row').hide();
        $('.module[id^=module] .row.module').show();
        $('.module[id^=module] .row.module select').each(function(){
            if ($(this).val() != '') 
            {
                var group = $(this).parent().parent().parent().parent();
                var field = $(this).parent().parent().parent();
                var mtype = $(this).val().toLowerCase();
                if (mtype != '') 
                {               
                    $('.row', group).not(field).slideUp('fast');
                    $('.row[class*="'+mtype+'"]', group).slideDown('fast');
                    $('.row[class*="all"]', group).slideDown('fast');
                }
                else
                {
                    $('.row', group).not(field).slideUp('fast');
                }
            }
        });
        $('.module[id^=module] .row.module select').change(function(){
            var group = $(this).parent().parent().parent().parent();
            var field = $(this).parent().parent().parent();
            var mtype = $(this).val().toLowerCase();
            if (mtype != '') 
            {
                $('.row', group).not(field).slideUp('fast');
                $('.row[class*="'+mtype+'"]', group).slideDown('fast');
                $('.row[class*="all"]', group).slideDown('fast');
            }
            else
            {
                $('.row', group).not(field).slideUp('fast');
            }
        }); 
/////////

 /*
    function limit_soadetails(purpose_type):
        var choosen_type = purpose_type;
        // show standard: sitename, site_addr, call_sign, channel
        if (choosen_type == 'ALL'){
            // nothing to hide
        }
        if (choosen_type == 'NEW'){
            //hide mod, filing_mod, mod_units, stor_units,
            //     storage_fee, sto_dst_fee, suf_lic_percent,
            //     sur_lic, sur_suf_percent, sur_suf, duplicate
        }       
        if (choosen_type == 'PPP'){
            // hide const_fee, rsl_units, license_fee, inspection_fee,
            //      mod_units, mod_fee, mod_filing_fee, stor_units,
            //      storage_fee, rsl_dst_fee, sto_dst_fee, suf_fee,
            //      suf_rate, freq, bw, sur_lic_percent, sur_lic,
            //      sur_suf_percent, sur_suf, duplicate_fee
        }
        if (choosen_type == 'REN'){
            // hide ppp_units, filing_fee, purchase_fee, possess_fee,
            //      const_fee, mod_units, mod_fee, mod_filing_fee, stor_units
            //      storage_fee, ppp_dst_fee, sto_dst_fee, duplicate_fee
        }        
        if (choosen_type == 'MOD'){            
            // show mod_units, mod_fee, mod_filing_fee, dst_mod*
        }
        if (choosen_type == 'STO'){
            // show stor_dst_fee, stor_units, storage_fee           
        }
        if (choosen_type == 'DUP'){
            // show duplicate_fee
        }
*/

/* Hide all Fields
 // Select all fields
        $("input#id_app_type_0").on("click", function(e){      
            if($(this).is(':checked')){              
                $('div.grp-group.grp-tabular').hide();
                $('div#soa_detail_set-group').show();                               
            }else{
                $('div#soa_detail_set-group').hide();
            }
        });
        // Only PPP
        $("input#id_app_type_1").on("click", function(e){      
            if($(this).is(':checked')){     
              if($("input#id_app_type_2").is(':checked')){ 
                $('div#soa_detail_set-7-group').hide();        
              }else{
                $('div.grp-group.grp-tabular').hide();
                $('div#soa_detail_set-7-group').show();   
              }
            }else {
                $('div#soa_detail_set-7-group').hide();
            }
        }); 
        // Only New
        $("input#id_app_type_2").on("click", function(e){      
            if($(this).is(':checked')){              
                $('div.grp-group.grp-tabular').hide();
                $('div#soa_detail_set-6-group').show();                                
            }else {
                $('div#soa_detail_set-6-group').hide();
            }
        });
        // Only Mod
        $("input#id_app_type_3").on("click", function(e){      
            if($(this).is(':checked')){              
                $('div.grp-group.grp-tabular').hide();
                $('div#soa_detail_set-4-group').show();                           
            }else {
                $('div#soa_detail_set-4-group').hide();
            }
        });
        // Only Ren
        $("input#id_app_type_4").on("click", function(e){      
            if($(this).is(':checked')){ 
              if($("input#id_app_type_2").is(':checked')){            
                $('div#soa_detail_set-5-group').hide(); 
              }else{
                $('div.grp-group.grp-tabular').hide();
                $('div#soa_detail_set-5-group').show();                            
              }
            }else {
                $('div#soa_detail_set-5-group').hide();
            }
        });
        // Only Recall with Standard Fields
        $("input#id_app_type_5").on("click", function(e){      
            if($(this).is(':checked')){  
              if($("input#id_app_type_2").is(':checked')){             
                $('div.grp-group.grp-tabular').hide();
                $('div#soa_detail_set-9-group').show(); 
              }else{
                $('div.grp-group.grp-tabular').hide();
                $('div#soa_detail_set-3-group').show();
              }
            }else {
              if($("input#id_app_type_2").is(':checked')){             
                $('div.grp-group.grp-tabular').hide();
                $('div#soa_detail_set-6-group').show(); 
              }
                $('div#soa_detail_set-3-group').hide();
            }
        });
        // Only Duplicate
        $("input#id_app_type_6").on("click", function(e){      
            if($(this).is(':checked')){              
                $('div.grp-group.grp-tabular').hide();
                $('div#soa_detail_set-2-group').show();                        
            }else {
                $('div#soa_detail_set-2-group').hide();
            }
        });  
        // Only Demo
        $("input#id_app_type_7").on("click", function(e){      
            if($(this).is(':checked')){              
                $('div.grp-group.grp-tabular').hide();
                $('div#soa_detail_set-8-group').show();                        
            }else {
                $('div#soa_detail_set-8-group').hide();
            }
        });  
        // $('div#soa_detail_set-9-group').show();       
        /*
        $("#id_app_type").on("click", function(e){
            if($(this).value == 'PPP'){
                alert($(this).value);
                $('div.grp-group.grp-tabular').hide();
                $('div#soa_detail_set-7-group').show();   
            }
        })
/**
 * Find the next element matching a certain selector. Differs from next() in
 *  that it searches outside the current element's parent.
 *  
 * @param selector The selector to search for
 * @param steps (optional) The number of steps to search, the default is 1
 * @param scope (optional) The scope to search in, the default is document wide 
 */
$.fn.findNext = function(selector, steps, scope)
{
    // Steps given? Then parse to int 
    if (steps)
    {
        steps = Math.floor(steps);
    }
    else if (steps === 0)
    {
        // Stupid case :)
        return this;
    }
    else
    {
        // Else, try the easy way
        var next = this.next(selector);
        if (next.length)
            return next;
        // Easy way failed, try the hard way :)
        steps = 1;
    }

    // Set scope to document or user-defined
    scope = (scope) ? $(scope) : $(document);

    // Find kids that match selector: used as exclusion filter
    var kids = this.find(selector);

    // Find in parent(s)
    hay = $(this);
    while(hay[0] != scope[0])
    {
        // Move up one level
        hay = hay.parent();     
        // Select all kids of parent
        //  - excluding kids of current element (next != inside),
        //  - add current element (will be added in document order)
        var rs = hay.find(selector).not(kids).add($(this));
        // Move the desired number of steps
        var id = rs.index(this) + steps;
        // Result found? then return
        if (id > -1 && id < rs.length)
            return $(rs[id]);
    }
    // Return empty result
    return $([]);
};
    
$.fn.findPrev = function(selector, steps, scope)
{
    // Steps given? Then parse to int 
    if (steps)
    {
        steps = Math.floor(steps);
    }
    else if (steps === 0)
    {
        // Stupid case :)
        return this;
    }
    else
    {
        // Else, try the easy way
        var prev = this.prev(selector);
        if (prev.length)
            return prev;
        // Easy way failed, try the hard way :)
        steps = 1;
    }

    // Set scope to document or user-defined
    scope = (scope) ? $(scope) : $(document);

    // Find kids that match selector: used as exclusion filter
    var kids = this.find(selector);

    // Find in parent(s)
    hay = $(this);
    while(hay[0] != scope[0])
    {
        // Move up one level
        hay = hay.parent();     
        // Select all kids of parent
        //  - excluding kids of current element (next != inside),
        //  - add current element (will be added in document order)
        var rs = hay.find(selector).not(kids).add($(this));
        // Move the desired number of steps
        var id = rs.index(this) + steps;
        // Result found? then return
        if (id > -1 && id < rs.length)
            return $(rs[id]);
    }
    // Return empty result
    return $([]);
};
});
*/

//for (var  key in jsonData){
  //  if (jsonData.hasOwnProperty(key)) {
  //    alert(key + " -> " + jsonData[key]);
  //     console.log(value);
  //  }    
  //} 
  //Object.keys(jsonData).forEach(function(value) {
  //      console.log(value);
  //  });
  