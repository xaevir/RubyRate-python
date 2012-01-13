var ChatModule = (function(myApp, $, _, Backbone){
    var api = {}

    var Model = Backbone.Model.extend({
        initialize : function(attributes, options) {
            // this is really just a style thing so no in db
           //     if (_.isEmpty(this.collection.models)) {
            //        this.first_person = this.get('username') || '';  
             //   }                
        },
    });


    var Collection = Backbone.Collection.extend({

        model: Model,

        initialize : function() {

            this.bind('reset', function(){
                myApp.event.trigger('chat:modelsLoaded');
            }, this);

        },
    });


    var Chat = Backbone.Model.extend({
        initialize: function(attributes, options) {
            path = window.location.pathname
            this.url = path + '/chats'

            this.collection = new Collection();
            this.collection.url = path + '/chats/' + this.id + '/messages';

            this.bind("change:id", function() {
                this.collection.url = path + '/chats/' + this.id + '/messages';
            });
        },

    });

    var ItemView = Backbone.View.extend({

        tagName: 'li', 

        template : _.template( $("#chat-item").html()),

        initialize: function() {
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
            //myApp.event.bind("Chat:ScaffoldRendered", this.render, this)
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

    var AddView = Backbone.View.extend({
      
        template : _.template( $("#message-form").html()),

        events: {
          "submit form":  "sendMessage",
        },

        initialize: function() {
            _.bindAll(this, 'render', 'submitHandler', 'sendMessage', 'createChat'); 
            //myApp.event.bind("Chat:ScaffoldRendered", this.render, this)
        },

        render: function() {
            $(this.el).append(this.template({}));
            $('form', this.el).validate({
                rules: {content: 'required'},
                submitHandler: this.submitHandler,
            });
            return this;
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


    myApp.event.bind("bubbleAdded", addBubbleTip, this);

    function addBubbleTip(bubble) {
        var paper = Raphael(bubble.el.firstElementChild.firstElementChild, 22, 22);
        var arc_tip = paper.path('M16.5,0 Q16,10, 8,13Q15,15, 22,11')
        arc_tip.attr({'fill': '#000'  }  )
        arc_tip.scale(-1, 1)
        var svg = paper.canvas 
        $(svg).removeAttr('style')
        $(svg).attr('class', 'svg-speechpointer')
    }

    var chat;
    var collection;

    return {

        tpl: $("#chat-app-tpl").html(),

        setId: function(id) {
            chat = new Chat({ id: id });
            collection = chat.collection;
            chat.fetch();
            collection.fetch();
        },

        render: function() {
            this.el = $(this.tpl);
            var addview = new AddView();
            var listview  = new ListView();
            $("#message-window", this.el).append(listview.render().el);
            $("#message-window ul", this.el).hide();
            $("#add-message", this.el).append(addview.render().el);
        },

        close: function() {
            $(this.el).remove();
            //this.unbind();
        },

        onShow: function() {
            $("#message-window ul", this.el).show('slow');
        }

    }


})(myApp, $, _, Backbone);
