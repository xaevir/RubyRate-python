define([
  'jquery',
  'underscore',
  'backbone',
  'text!templates/nav-item.html',
], function($, _, Backbone, item_tpl){

    var vent = _.extend({}, Backbone.Events);

    var Model = Backbone.Model.extend({
      select: function(){
        this.set({selected: true});
        this.collection.selectAction(this);
      },
      unselect: function(){
        this.set({selected: false});
        this.collection.selectAction(this);
      }

    });

    var Collection = Backbone.Collection.extend({

        url: '/',

        model: Model,

        selectedItem: undefined,
     
    });

    var ItemView = Backbone.View.extend({

        tagName: 'li', 

        events: {
            "click a": "actionSelected"
        },

        initialize: function(){
            this.model.bind("change:selected", this.highlight, this);
            _.bindAll(this, 'render'); 
        },

        highlight: function(model, selected){
            var cssClass = ""
            if (selected){
              cssClass = "highlight"
            }
            $(this.el).attr("class", cssClass);
        },

        unhighlight: function(model, selected){
            if (selected === false) {
                $(this.el).attr("class", cssClass);
            }
        },

        actionSelected: function(e){
            e.preventDefault();
            if (collection.selectedItem == this) return  
            if (collection.selectedItem){ //its already set 
                collection.selectedItem.unselect();
            }
            this.model.select();
        },

        clicked: function(e) {
            e.preventDefault(); 
            var action = this.model.get("action")
              
                
            //if (collection.clicked === this) return
            //set to new value which unsets old value
           /* collection.clicked = this   
            this.label 
            render() the form view
            messages add by label {label: 'wish'} if you pass in an object, 
            then when you need the details you have it
            then an event router that loads the form by   
            */

        },

        template : _.template(item_tpl),


        render: function(){
            var template = this.template(this.model.toJSON());
            $(this.el).html(template);
            return this; 
        },
    });


    var ListView = Backbone.View.extend({

        tagName: 'ul', 
        className: 'unstyled',
        
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


    });

    var collection = new Collection
    collection.reset(json_data);
    var view = new ListView;
    view.render();
    $('.sidenav').html(view.el);

});


