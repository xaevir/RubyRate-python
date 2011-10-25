/*
if ($('#wish').length){
   $LAB
   .script("/static/js/mvc/application.js").wait()
   .script("/static/js/mvc/models/document.js").wait()
   .script("/static/js/mvc/routers/documents.js").wait()
   .script("/static/js/mvc/views/edit.js").wait()
   .script("/static/js/mvc/views/index.js")
   .script("/static/js/mvc/views/notice.js")
   .wait(function(){
      App.init();
   });
}
*/


(function($){
  var ListView = Backbone.View.extend({
    el: $('body'), // el attaches to existing element
    // `events`: Where DOM events are bound to View methods. Backbone doesn't have a separate controller to handle such bindings; it all happens in a View.
    events: {
      'click a.create-message': 'addItem'
    },
    initialize: function(){
      _.bindAll(this, 'render', 'addItem'); // every function that uses 'this' as the current object should be in here
      
      this.counter = 0; // total number of items added thus far
      this.render();
    },
    // `render()` now introduces a button to add a new list item.
    render: function(){
      $(this.el).append("<button id='add'>Add list item</button>");
      $('#add').after("<ul></ul>");
    },
    // `addItem()`: Custom function called via `click` event above.
    addItem: function(e){
      e.preventDefault()
        var out = '<form>';
        out += "<label for='body'>Body</label>";
        out += "<textarea name='body'></textarea>";
        
        
        out += "<button>send</button>";
        out += "</form>";

      $(e.currentTarget).parent().append(out);
      this.counter++;
    }
  });

  var listView = new ListView();      
})(jQuery);/***
    Draw the speech bubble tips
****/
if ($('.bubble').length){
    arc_tip_div = $('<div id="arc-tip" style="display: none"></div>')
    $('body').before(arc_tip_div)

    // Create regular tip
    var paper = Raphael(document.getElementById('arc-tip'), 81, 40);
    var  arc_tip = paper.path('M35,0Q30,35,10,35Q60,30,65,0')

    arc_tip.attr({'fill': 'none', 'stroke':'#ccc' , 
            'stroke-linejoin': 'round', 'stroke-linecap':'butt', 
            })


    $('.tip-left').each(function(index) {
        var paper = Raphael(this, 81, 36);
        var arc_tip = paper.path('M35,0Q30,35,10,35Q60,30,65,0')
        arc_tip.scale(.5, .5, 0,0)
        var svg = $(this).find('svg')
        svg.removeAttr('style')
        svg.attr('class', 'tip-container')
        var arc_top = paper.path('M35,0 H65')
        var line = $(this).find('path:last-child')
        $(line).attr({'class':'svg-top'})
    });

    $('.tip-right').each(function(index) {
        var paper = Raphael(this, 81, 36);
        var arc_tip = paper.path('M35,0Q30,35,10,35Q60,30,65,0')
        arc_tip.scale(-1, 1, 0, 0)
        arc_tip.scale(.5, .5, 0, 0)
        var svg = $(this).find('svg')
        svg.removeAttr('style')
        svg.attr('class', 'tip-container')
        var arc_top = paper.path('M35,0 H65')
        var line = $(this).find('path:last-child')
        $(line).attr({'class':'svg-top'})
    });
}

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
