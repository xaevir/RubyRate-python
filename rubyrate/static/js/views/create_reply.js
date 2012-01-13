define([
  'jquery',
  'underscore',
  'backbone',
  'views/notice',
  'text!/forms/create-reply.html',
  'libs/jquery-validation/jquery.validate'
], function($, _, Backbone, NoticeView, create_tpl){


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




   var CreateView = Backbone.View.extend({
        className: 'clearfx',
        template : _.template(create_tpl),

        initialize: function() {
            _.bindAll(this, 'render', 'submitHandler' ); 
            //myApp.event.bind("Chat:ScaffoldRendered", this.render, this)
            this.render();
        },

        render: function(){
            var template = this.template({});
            $(this.el).html(template);
            var form = $('form', this.el); 
            $(form).validate({
                submitHandler: this.submitHandler, 
            });

            return this; 
        },        

        events: {
          //"submit form":  "submitHandler",
        },

        submitHandler: function(form) {
            var params = $('form', this.el).serializeObject();
            this.collection.create(params, {error:
                function(model, resp){
                    $('html').html(resp.responseText)    
                }}
            );
            this.success()
        },
        success: function() {
            new NoticeView({'message': 'Reply Sent'})            
            //var msg = 'Your message has been sent.'
            //new NoticeView({message: msg})
            //this.$('[name=content]').val('');
        }


 });
    
    return CreateView 
    
});


