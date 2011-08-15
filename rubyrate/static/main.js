/* Put Flash message in Fancy Box on homepage */
if ( $("#lightbox").length ) {
    var page_home = $("#page-home");
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
