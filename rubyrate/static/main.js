/* Put Flash message in Fancy Box on homepage */
if ( $("#lightbox").length ) {
    var page_home = $("#home");
    page_home.append('<a id="hidden_link" href="#lightbox"></a>');
    // for some reason even tho I am loading the js at the end of the page,
    // I need this doc ready function or else the element doesnt exist.  
    $(document).ready(function() {
        if ( $("#lightbox") ) {
        $("#hidden_link").fancybox({
            'hideOnContentClick': true,
            'padding'           : 50
        });
        $("#hidden_link").trigger('click');
        }
    });
}


 //show notification, default type is 'message'  

/* emulate placeholder */
//var inputs = $('#product_needed_form [type=text]')

// resetting browser with some values the user already filled in causes both 
// the user values and the label to appear on top of one another 
/*inputs.each(function(index) {
    if ($(this).val() != ''){
        $(this).prev().css('display', 'none')
    }
})
*/
/*
inputs.focus(function() {
    if ($(this).val() == '') {
        $(this).prev().css({'position':'static', 'color': '#666'})
    };
});
inputs.blur(function() {
    if ($(this).val() == '') {
        $(this).prev().css('display', 'block')
    };
});
*/
