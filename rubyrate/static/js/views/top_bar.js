define([
  'jquery',
  'underscore',
  'backbone',
  'views/create_wish',
], function($, _, Backbone, CreateWishView){

   var TopBarController = Backbone.View.extend({
    
        
        initialize: function() {
            _.bindAll(this, 'render', 'createWish' ); 
        },

        events: {
            "click .action-create-wish" : "createWish",
        },

        createWish: function(e) {
            e.preventDefault();
            CreateWishView.context = 'modal';        
            CreateWishView.render();
        },
    });

    return TopBarController
});
