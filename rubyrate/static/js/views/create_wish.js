define([
  'jquery',
  'underscore',
  'backbone',
  'views/notice',
  'text!/forms/create-wish.html',
  'text!templates/modal.html',
  'libs/bootstrap/bootstrap-modal',
  'libs/jquery-validation/jquery.validate'
], function($, _, Backbone, NoticeView, create_tpl, modal_tpl){


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


    var Model = Backbone.Model.extend({ });

    var Collection = Backbone.Collection.extend({
        url: '/wishes',
        model: Model,
    });

   var CreateView = Backbone.View.extend({
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
            $('.modal-backdrop').remove();
            $('.modal').remove();
            this.success()
        },
        success: function() {
            new NoticeView({'message': 'Wish Created'})            
            //var msg = 'Your message has been sent.'
            //new NoticeView({message: msg})
            //this.$('[name=content]').val('');
        }


 });
    

    return {

        context: '', 

        render: function() {
            if (this.context == 'modal') {
                var collection = new Collection()
                var view = new CreateView({'collection': collection});
                var button = '';
                var bobby = '<form id="bobby"><input class="required" type="text" value="" name="bobby"><input type="submit" value="sumit"></form>'
                var tpl_vars = {
                    heading: 'Make a Wish',
                    body: '', 
                    //body: bobby, 
                    footer: '',
                }
                
                var template  =  _.template(modal_tpl, tpl_vars);
                var el = $(template)  
                $('.modal-body', el).append(view.el)
                $(el).modal({
                    keyboard: true,
                    backdrop: true,
                })
                $(el).modal('show')




            }

        },


    }



});


