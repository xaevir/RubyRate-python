define([
  'order!libs/jquery/jquery-min',
  'order!libs/underscore/underscore-min',
  'order!libs/backbone/backbone-min'  
  'text!templates/wish/wishTpl.html'
], function(wishTpl){

    var vent = _.extend({}, Backbone.Events);

    var Model = Backbone.Model.extend({});

    var Collection = Backbone.Collection.extend({

        url = '/wishes',

        model: Model,

        initialize : function() {
            this.bind('reset', function(){
                myApp.event.trigger('chat:modelsLoaded');
            }, this);
        }
    });


    var ItemView = Backbone.View.extend({

        tagName: 'li', 

        template : _.template(wishTpl),

        initialize: function() {var listview  = 
            _.bindAll(this, 'render'); 
        },

        render: function(){
            var template = this.template(this.model.toJSON())
            $(this.el).html(template);
            myApp.event.trigger('bubbleAdded', this);
            return this; 
        },
        
    });


    var ListView = Backbone.View.extend({

        tagName: 'ul', 

        initialize: function() {
            _.bindAll(this, 'render'); 
            render();
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


    });

    var model;
    var collection;
    new ListView();


  // Our module now returns an instantiated view
  // Sometimes you might return an un-instantiated view e.g. return projectListView
  return new projectListView;
});


