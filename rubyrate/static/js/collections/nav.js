define([
  'Underscore',
  'Backbone',
  // Pull in the Model module from above
  'models/nav'
], function(_, Backbone, navModel){
  var navCollection = Backbone.Collection.extend({
    model: navModel,
    initialize : function(attributes, options) {
        path = window.location.pathname
        this.url = path + '/chats/nav'
    },    
  });
  // You don't usually return a collection instantiated
  return new navCollection;
});
