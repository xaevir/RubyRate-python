define([
  'jquery',
  'underscore',
  'backbone',
  'libs/doTimeout'            
], function($, _, Backbone){


    var Notice = Backbone.View.extend({
        className: "alert-message success",
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
            $('.topbar').after(this.el);
            $(this.el).hide();
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
    return Notice
});
