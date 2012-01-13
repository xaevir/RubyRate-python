$.fn.serializeObject = function()
{
    var o = {};
    var a = this.serializeArray();
    $.each(a, function() {
        if (o[this.name] !== undefined) {
            if (!o[this.name].push) {
                o[this.name] = [o[this.name]];
            }
            o[this.name].push(this.value || '');
        } else {
            o[this.name] = this.value || '';
        }
    });
    return o;
};
// how to use
//var params = $('form', this.el).serializeObject();

// Window load event used just in case window height is dependant upon images
$(window).bind("load", function() { 

       var footerHeight = 0,
           footerTop = 0,
           $footer = $("#footer");

       positionFooter();

       function positionFooter() {

                footerHeight = $footer.height();
                footerTop = ($(window).scrollTop()+$(window).height()-footerHeight)+"px";

               if ( ($(document.body).height()+footerHeight) < $(window).height()) {
                   $footer.css({
                        position: "absolute"
                   }).animate({
                        top: footerTop
                   })
               } else {
                   $footer.css({
                        position: "static"
                   })
               }

       }

       $(window)
               .scroll(positionFooter)
               .resize(positionFooter)

});

//move the last list item before the first item. The purpose of this is if the user clicks previous he will be able to see the last item.  
//$('#slide_nav_ul li:first').before($('#slide_nav_ul li:last'));  


var nav_slider = function() {
    slide_items = $('#slide_nav_ul li'); 
    slide_items = $.makeArray(slide_items)
    visible_items = slide_items.slice(0,4)    
    invisible_items_right = slide_items.slice(4)    
    invisible_items_left = Array();    
}



//when user clicks the image for sliding right  
$('#scroll_right').click(function(){  

    
    if (_.isEmpty(invisible_items_right)) return;  
    // To remove and return the first element from an array, use shift() 

    var firstHidden = invisible_items_right.shift()
    visible_items.push(firstHidden)     


    var firstVisible= visible_items.shift();
    invisible_items_left.push(firstVisible)     


    //get the width of the items ( i like making the jquery part dynamic, so if you change the width in the css you won't have o change it here too ) '  

    var item_width = $('#slide_nav_ul li').outerWidth() + 13;  

    //calculate the new left indent of the unordered list  
    var left_indent = parseInt($('#slide_nav_ul').css('left')) - item_width;  

    //make the sliding effect using jquery's anumate function '  
    $('#slide_nav_ul').animate({'left' : left_indent},{queue:false, duration:500},function(){  

        //and get the left indent to the default -210px  
        $('#slide_nav_ul').css({'left' : '-210px'});  
        //dont have to hide bc you cant see due to overflow 

    });  
});  

//when user clicks the image for sliding left  
$('#scroll_left').click(function(){  


    if (_.isEmpty(invisible_items_left)) return;  
    // To remove and return the first element from an array, use shift() 

    var firstVisible= visible_items.pop();
    invisible_items_right.push(firstVisible)   

    var firstHidden = invisible_items_left.shift()
    visible_items.unshift(firstHidden)     




    var item_width = $('#slide_nav_ul li').outerWidth() + 15;  

    /* same as for sliding right except that it's current left indent + the item width (for the sliding right it's - item_width) */  
    var left_indent = parseInt($('#slide_nav_ul').css('left')) + item_width;  

    $('#slide_nav_ul').animate({'left' : left_indent},{queue:false, duration:500},function(){  

    /* when sliding to left we are moving the last item before the first item */  
    //$('#slide_nav_ul li:first').before($('#slide_nav_ul li:last'));  

    /* and again, when we make that change we are setting the left indent of our unordered list to the default -210px */  
    $('#slide_nav_ul').css({'left' : '-210px'});  
    });  

});  


$("#wishes blockquote").hover(
  function () {
    $(this).addClass('reverse-bubble');
    this.path  = $(this).find("svg path")
    this.prev_fill =  this.path.attr('fill')
    this.path.attr('fill', '#fff')
  }, 
  function () {
    $(this).removeClass('reverse-bubble');
    this.path.attr('fill', this.prev_fill)
  }
);

$('#isotope').isotope({
  // options
  itemSelector : '.isotope-item',
  layoutMode : 'masonry'
});


function addBubbleTip(el) {
    $('.tip-left').each(function(index) {
        var paper = Raphael(this, 22, 22);
        var arc_tip = paper.path('M16.5,0 Q16,10, 8,13Q15,15, 22,11')
        arc_tip.attr({'stroke': '#C4E9FF', 'fill': '#E5F5FF'})
        
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
}


if ($('.bubble').length){
    addBubbleTip()
}

if ( $(".btn-reply").length ) {
    createReplyArrow()
}   

var Notice = Backbone.View.extend({
    className: "success",
    displayLength: 5000,
    defaultMessage: '',
    
    initialize: function() {
        _.bindAll(this, 'render');
        this.message = this.options.message || this.defaultMessage;
        this.render();
    },
    
    render: function() {
        var view = this;
        
        $(this.el).html(this.message);
        $(this.el).hide();
        $('#flash').html(this.el);
        $(this.el).slideDown();
        $.doTimeout(this.displayLength, function() {
            $(view.el).slideUp();
            $.doTimeout(2000, function() {
                view.remove();
            });
        });
        return this;
    }
});


if ( $("#flash .success").length ) {
    var msg = $("#flash .success").html()
    new Notice({message: msg})
}

var ErrorView = NoticeView.extend({
    className: "error",
    defaultMessage: 'Uh oh! Something went wrong. Please try again.'
});


var Message = Backbone.Model.extend({
    initialize : function(attributes, options) {
        // this is really just a style thing so no in db
            if (_.isEmpty(this.collection.models)) {
                this.first_person = this.get('username') || '';  
            }                
    },
});


var Messages = Backbone.Collection.extend({
    model: Message,
});


var NavItem = Backbone.Model.extend({
});

NavItems = Backbone.Collection.extend({
    initialize : function(attributes, options) {
        path = window.location.pathname
        this.url = path + '/chats/nav'
    },
    model: NavItem,

});

var Chat = Backbone.Model.extend({
    initialize: function(attributes, options) {
        path = window.location.pathname
        this.url = path + '/chats'

        this.messages = new Messages();
        this.messages.url = path + '/chats/' + this.id + '/messages';

        this.bind("change:id", function() {
            this.messages.url = path + '/chats/' + this.id + '/messages';
        });

    },

});

var App = {
    Views: {},
    Views.Notice: Notice,
    Routers: {},
    Collections: {},
    init: function() {
        var docs = new NavItems();
        docs.fetch();        
        new App.Views.Nav({'collection': docs})
    }
};

App.Views.Message = Backbone.View.extend({

    tagName: 'li', 

    template : _.template( $("#chat-item").html()),

    initialize: function() {
        _.bindAll(this, 'render'); 
    },

    render: function(){
        //var data = this.model.toJSON();
        $(this.el).html();
        return this; 
    },
    
});


App.Views.Chat = Backbone.View.extend({

    el: $('#main-chat'), 

    template1 : _.template( $("#message-form").html()),

    template : _.template( $("#chat-item").html()),

    events: {
      "submit form":  "sendMessage",
    },

    initialize: function() {
        this.model.messages.bind('add', this.addOne, this);
        this.model.messages.bind('reset', this.addAll, this);
        _.bindAll(this, 'render', 'submitHandler', 'sendMessage', 'createChat', 'addOne'); 
        //this.render();
        $('form', this.el).validate({
            rules: {content: 'required'},
            submitHandler: this.submitHandler,
        })
    },

    render: function() {
        $(this.el).append(this.template1({}));
    },

    addOne: function(message){
        var data = message.toJSON();
        //data['username'] = this.model.get('username') 
        data['first_person'] = message.first_person 

        $('ul', this.el).append(this.template(data));
        addBubbleTip()
    },

    addAll: function() {
        this.model.messages.each(this.addOne);
    },
    
    submitHandler: function(form) {
        if (this.model.isNew()) {
            this.createChat()
        } else {
            this.sendMessage()
        }
    },

    createChat: function(){
        var data =  this.model.toJSON()
        var content = this.$('[name=content]').val();
        data['content'] = content
        $.ajax({
            type: 'POST',
            url: this.model.url,
            dataType: 'json',
            data: JSON.stringify(data),
            context: this,
            success: function(data) {
                this.model.set({id: data['id']});              
                var message = new Message({'content': data['content']})
                this.model.messages.add(message)
                this.success()  
            },
            error: function(data) {
                $('html').html(data.responseText)
            }
        });
    },

    sendMessage: function() {
        var content = this.$('[name=content]').val();
        this.model.messages.create({'content': content},{error:
            function(model, resp){
                $('html').html(resp.responseText)    
            }}
        );
        this.success()
    },
    success: function() {
        var msg = 'Your message has been sent. We will email you when their is a reply'
        new NoticeView({message: msg})
        this.$('[name=content]').val('');
    }

});



App.Views.NavSingle = Backbone.View.extend({

    tagName: 'li', 

    events: {
      "click a":  "loadChat",
    },

    template : _.template( $("#chat-nav").html()),

    initialize: function() {
        _.bindAll(this, 'render'); 
    },

    render: function(){
        var template = this.template(this.model.toJSON())
        $(this.el).html(template);
        return this; 
    },

    loadChat: function(e) {
        var wish_id = this.model.get("wish_id");
        var chat = new Chat({ id: wish_id });
        chat.fetch();
        chat.messages.fetch();
        new App.Views.Chat({'model': chat} )
    },


});


App.Views.Nav = Backbone.View.extend({

    el: $('#slide_nav_ul'), 


    initialize: function() {
        _.bindAll(this, 'addOne'); 
        this.collection.bind('add', this.addOne, this);
        this.collection.bind('reset', this.addAll, this);
    },



    addOne: function(chat){
        var view = new App.Views.NavSingle({ model: chat });
        var h = view.render().el;
        $( this.el).append(h);
    },

    addAll: function() {
        this.collection.each(this.addOne);
        nav_slider();
    },


});



if ( $("#app").length ) {
    App.init();
}





/*
  var ListView = Backbone.View.extend({
    el: $('convo-messages'), // el attaches to existing element
    events: {
      'click button#.create-message': 'addItem'
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
*/
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
