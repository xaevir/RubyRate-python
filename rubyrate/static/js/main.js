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

$('#isotope').isotope({
  // options
  itemSelector : '.isotope-item',
  layoutMode : 'masonry'
});

function createPerson() {
    $('.zip-code').each(function(index) {
        var paper = Raphael(this, 22, 29);
        var person = paper.path("M21.021,16.349c-0.611-1.104-1.359-1.998-2.109-2.623c-0.875,0.641-1.941,1.031-3.103,1.031c-1.164,0-2.231-0.391-3.105-1.031c-0.75,0.625-1.498,1.519-2.111,2.623c-1.422,2.563-1.578,5.192-0.35,5.874c0.55,0.307,1.127,0.078,1.723-0.496c-0.105,0.582-0.166,1.213-0.166,1.873c0,2.932,1.139,5.307,2.543,5.307c0.846,0,1.265-0.865,1.466-2.189c0.201,1.324,0.62,2.189,1.463,2.189c1.406,0,2.545-2.375,2.545-5.307c0-0.66-0.061-1.291-0.168-1.873c0.598,0.574,1.174,0.803,1.725,0.496C22.602,21.541,22.443,18.912,21.021,16.349zM15.808,13.757c2.362,0,4.278-1.916,4.278-4.279s-1.916-4.279-4.278-4.279c-2.363,0-4.28,1.916-4.28,4.279S13.445,13.757,15.808,13.757z")
        person.attr({'fill': '#666', 'stroke':'none'})
        var svg = paper.canvas 
        $(svg).removeAttr('style')
        $(svg).attr('class', 'svg-person')
    });
}

function addBubbleTip() {
    $('.tip-left').each(function(index) {
        var paper = Raphael(this, 22, 22);
        var arc_tip = paper.path('M16.5,0 Q16,10, 8,13Q15,15, 22,11')
        var svg = paper.canvas 
        $(svg).removeAttr('style')
        $(svg).attr('class', 'svg-speechpointer')
        //var arc_top = paper.path('M35,0 H65')
        //var line = $(this).find('path:last-child')
        //$(line).attr({'class':'svg-top'})
    });

    $('.tip-right').each(function(index) {
        var paper = Raphael(this, 22, 22);
        var arc_tip = paper.path('M16.5,0 Q16,10, 8,13Q15,15, 22,11')
        arc_tip.attr({'fill': '#000'  }  )
        arc_tip.scale(-1, 1)
        var svg = paper.canvas 
        $(svg).removeAttr('style')
        $(svg).attr('class', 'svg-speechpointer')
    });
}

function createReplyArrow() {
    $('.btn-reply-small').each(function(index) {
        var paper = Raphael(this, 18, 17);
        var reply_arrow = paper.path("M12.981,9.073V6.817l-12.106,6.99l12.106,6.99v-2.422c3.285-0.002,9.052,0.28,9.052,2.269c0,2.78-6.023,4.263-6.023,4.263v2.132c0,0,13.53,0.463,13.53-9.823C29.54,9.134,17.952,8.831,12.981,9.073z")
        reply_arrow.attr({'fill': '#006EB7', 'stroke':'none'})
        reply_arrow.scale(.6, .6, 0, 0)
    });
    $('.btn-reply-large').each(function(index) {
        var paper = Raphael(this, 24, 22);
        var reply_arrow = paper.path("M12.981,9.073V6.817l-12.106,6.99l12.106,6.99v-2.422c3.285-0.002,9.052,0.28,9.052,2.269c0,2.78-6.023,4.263-6.023,4.263v2.132c0,0,13.53,0.463,13.53-9.823C29.54,9.134,17.952,8.831,12.981,9.073z")
        reply_arrow.attr({'fill': '#006EB7', 'stroke':'none'})
        reply_arrow.scale(.8, .8, 0, 0)
    });

/*
    $('#messages .tip-left .btn-reply').each(function(index) {
        var paper = Raphael(this, 24, 22);
        var reply_arrow = paper.path("M12.981,9.073V6.817l-12.106,6.99l12.106,6.99v-2.422c3.285-0.002,9.052,0.28,9.052,2.269c0,2.78-6.023,4.263-6.023,4.263v2.132c0,0,13.53,0.463,13.53-9.823C29.54,9.134,17.952,8.831,12.981,9.073z")
        reply_arrow.attr({'fill': '#006EB7', 'stroke':'none'})
        reply_arrow.scale(.8, .8, 0, 0)
    });
*/
}


if ($('.bubble').length){
    addBubbleTip()
}

if ( $(".btn-reply").length ) {
    createReplyArrow()
}   

// load template library
var app = {
        template : Array()
    };

$.get('/static/js/mvc/templates.html',function(result){
    $('.template', $(result)).each(function(){
        app.template[this.id] = _.template( $(this).html() );
    });
});


  var ListView = Backbone.View.extend({
    el: $('convo-messages'), // el attaches to existing element
    events: {
      'click button#create-messagesubmit': 'addItem'
    },
    initialize: function(){
      _.bindAll(this, 'render', 'addItem'); // every function that uses 'this' as the current object should be in here
      
      this.counter = 0; // total number of items added thus far
      this.render();
    },
    // `render()` now introduces a button to add a new list item.
    render: function(){
    },
    // `addItem()`: Custom function called via `click` event above.
    addItem: function(e){
        e.preventDefault()
        var blockq = $(e.currentTarget).parent()
        blockq.wrap('<div class="convo"></div>')

        $(e.currentTarget).parent().after(app.template.create_message());
        this.counter++;
    }
  });

  var listView = new ListView();      

/***
    Draw the speech bubble tips
****/



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
/*
if ( $("#lightbox").length ) {
    var body = $("body");
    body.append('<a id="hidden_link" href="#lightbox"></a>');
    // for some reason even tho I am loading the js at the end of the page,
    // I need this doc ready function or else the element doesnt exist.  
    $(document).ready(function() {
        $("#hidden_link").fancybox({
            //'hideOnContentClick': true,
            'padding'           : 50,
            'width'             : 560,
        });
        $("#hidden_link").trigger('click');
    });
}
*/
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
