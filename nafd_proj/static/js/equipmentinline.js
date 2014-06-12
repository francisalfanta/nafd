(function($) {
    $(document).ready(function(){ 
        $(".grp-module.grp-table").css({ 'padding': '0px 0px 0px 0px' });  
        $(".grp-module.grp-thread").css({ 'padding': '0px 0px 0px 0px' });   
        $(".grp-tr").css({ 'padding': '0px 0px 0px 0px' });          
        $(".grp-th").css({ 'padding': '0px 0px 0px 0px' });    
        $(".grp-td").css({ 'padding': '0px 0px 0px 0px' });    

         $(".grp-module.grp-tbody").css({ 'padding': '0px 0px 0px 0px' }); 
        //$(".grp-th").css({ 'font-weight': 'bold' });
        // background color per group
        //$(".grp-td.ppp_units").css({ 'background-color': 'yellow' });   
        $(".grp-td.ppp_units").css({ 'border-top-color': 'yellow' });   
        $(".grp-td.ppp_units").css({ 'border-right-color': 'yellow' });   
        $(".grp-td.ppp_units").css({ 'border-bottom-color': 'yellow' });   
        $(".grp-td.ppp_units").css({ 'border-left-color': 'yellow' });         
    });
})(django.jQuery);