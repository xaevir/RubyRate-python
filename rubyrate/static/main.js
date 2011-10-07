/* Put Flash message in Fancy Box on homepage */
/*var paper = Raphael(document.getElementById("arrow"), 120, 60);
var arrow = paper.path('m1,50 h175 v-40 l50,50 l-50 50 v-40 h-175z')
arrow.attr({'fill': 'none', 'stroke':'#F3961C'})
arrow.scale(.5, .5, 0, 0)
*/
/*
if ( $("#wishes").length ) {
  $('#wishes').masonry({
    // options
    itemSelector : '.wish',
    columnWidth : 200,
  });
}
*/
if ( $("#reply-sign").length ) {
var paper = Raphael(document.getElementById("reply-sign"), 24, 22);
var quote = paper.path("M12.981,9.073V6.817l-12.106,6.99l12.106,6.99v-2.422c3.285-0.002,9.052,0.28,9.052,2.269c0,2.78-6.023,4.263-6.023,4.263v2.132c0,0,13.53,0.463,13.53-9.823C29.54,9.134,17.952,8.831,12.981,9.073z")
quote.attr({'fill': '#fff', 'stroke':'#89B4FF'})
quote.scale(.8, .8, 0, 0);
}
/*
//c = quote.clone()
//quote.remove()
//c.scale(1,-1)
/*
var paper = Raphael(document.getElementById("quote3"), 210, 164);
var quote = paper.path("m16,5.333c-7.732,0-14,4.701-14,10.5c0,1.982,0.741,3.833,2.016,5.414L2,25.667l5.613-1.441c2.339,1.317,5.237,2.107,8.387,2.107c7.732,0,14-4.701,14-10.5C30,10.034,23.732,5.333,16,5.333z")
quote.attr({'fill': 'none', 'stroke':'#666'})
quote.scale(7, 5, 0, 0);
c = quote.clone()
quote.remove()
c.scale(1,-1)
*/
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

var product = $('textarea[name="product"]')

product.focus(function() {
    if ($(this).val() == $(this).attr('placeholder')) {
        $(this).val('')
        $(this).removeClass('ui-placeholder')
    };
});
product.blur(function() {
    if ($(this).val() == '') {
        $(this).val($(this).attr('placeholder'))
        $(this).addClass('ui-placeholder')
    };
});

var checkAutofill = function(input) {
	var inputField = $(input);
	var inputLabel = $(input).adjacent('label').first();

	new PeriodicalExecuter(function() {
		if (inputField.value != "") {
			inputLabel.fade({
				duration: p._posterousDefaultAnimationDurationShort,
				to: 0.0
			});
		}
	}, 0.2);
};


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
