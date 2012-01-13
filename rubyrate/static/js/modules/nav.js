var NavModule = (function(myApp, $, _, Backbone){
    var nav = {}
    var ItemModel = Backbone.Model.extend({
        select: function(){
            this.set({selected: true});
            myApp.event.trigger("region:loadChat", this);
        }
    });

    var ItemCollection = Backbone.Collection.extend({
        initialize : function(attributes, options) {
            path = window.location.pathname
            this.url = path + '/chats/nav'
        },
        model: ItemModel,

    });

    var ItemView = Backbone.View.extend({

        tagName: 'li', 

        events: {
            "click a": "chatSelected"
        },

        template : _.template( $("#chat-nav-item").html()),

        initialize: function() {
            _.bindAll(this, 'render'); 
            this.model.bind("change:selected", this.highlight, this);
        },

        chatSelected: function(e){
            e.preventDefault();
            this.model.select();
        },

        highlight: function(model, selected){
            var cssClass = ""
            if (selected){
                cssClass = "highlight"
            }
            $(this.el).attr("class", cssClass);
        },

        render: function(){
            var template = this.template(this.model.toJSON())
            $(this.el).html(template);
        },

        loadChat: function(e) {
            var wish_id = this.model.get("wish_id");
            var chat = new Chat({ id: wish_id });
            chat.fetch();
            chat.messages.fetch();
            new App.Views.Chat({'model': chat} )
        },


    });

    var ListView = Backbone.View.extend({

        el: $('#chat-nav'), 

        events: { },

        initialize: function() {
            this.collection.bind('add', this.addOne, this);
            this.collection.bind('reset', this.addAll, this);
            this.collection.fetch();        

        },

        addOne: function(chat){
            var itemView = new ItemView({ model: chat });
            itemView.render();
            $(this.el).append(itemView.el);
        },

        addAll: function() {
            this.collection.each(this.addOne, this);
        },


    });

    var collection = new ItemCollection();
    var view = new ListView({'collection': collection})


})(myApp, $, _, Backbone);
