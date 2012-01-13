define([
  'jquery',
  'underscore',
  'backbone',
  'libs/isotope.min',
  'libs/raphael-min',
  'text!templates/wish-item.html',
  'views/create_reply',
  'domReady!',
], function($, _, Backbone, I, R, wishTemplate, CreateReplyView){


    var ItemView = Backbone.View.extend({

        tagName: 'li', 
        className: 'wish',

        template : _.template(wishTemplate),

        initialize: function() { 
            _.bindAll(this, 'render', 'reply'); 
        },

        events: {
            'click .action-reply': 'reply',
          //"submit form":  "submitHandler",
        },

        reply: function(){
            if (this.model.has('selected')) return; 
            this.model.set({selected: true})

            var width = $('blockquote', this.el).outerWidth()
            var replyView = new CreateReplyView({collection: collection})                          
            replyView.render()
            $(replyView.el).css('width', width);
            var height = $(replyView.el).outerHeight()
            replyView.height = $(replyView.el).outerHeight();

            var emptyDiv = $('<div class="emptyDiv"></div>');
            emptyDiv.css('height', replyView.height);

            $(this.el).append(emptyDiv)
            $(this.el).addClass('altered')

            $('.action-reply', this.el).fadeOut();
            $('blockquote', this.el).css('box-shadow', ' 1px 1px 2px #ddd');
            $('#wishes').isotope('reLayout')
            
            $(replyView.el).hide();
            $(this.el).append(replyView.el);
            $(replyView.el).slideDown()
            
        },

        render: function(){
            var data = this.model.toJSON();
            data['context'] = 'sender';
            data['reply'] = true;
            var template = this.template(data);
            $(this.el).html(template);
            //this.addBubbleTip(this)
            vent.trigger('bubbleAdded', this);
            return this; 
        },
       
        addBubbleTip: function(model) {
            var paper = Raphael(model.el.firstElementChild, 22, 22);
            var arc_tip = paper.path('M16.5,0 Q16,10, 8,13Q15,15, 22,11')
            arc_tip.attr({'stroke': '#70CAFF', 'fill': '#E5F5FF'})
            var svg = paper.canvas 
            $(svg).removeAttr('style')
            $(svg).attr('class', 'tip')
        }

    });

    return new (Backbone.View.extend({

        tagName: 'ul', 
        id: 'wishes',
        className: 'unstyled clearfx',

        initialize: function() {
            _.bindAll(this, 'render'); 
        },
        
        render: function() {
            collection.each(this.addOne, this);
            return this;
        },

        addOne: function(model){
            var view = new ItemView({model: model});
            view.render();
            $(this.el).append(view.el);
        },

    }))()

    });

    var collection = new Collection
    collection.reset(window.json_data);
    var view = new ListView;
    view.render();
    $('.app').html(view.el);
    $('#wishes').isotope({
      itemSelector : '.wish',
      layoutMode : 'masonry'
    });

});


