define([
  'underscore', 
  'backbone',    
  'models/message'
], function(_, Backbone, Model){

    var Messages = Backbone.Collection.extend({
        url: '/wishes',
        model: Model,
    });



  var message = Backbone.Model.extend({

  });

  return message;

});


var projectModel = Backbone.Model.extend({
    defaults: {
      name: "Harry Potter"
    }
  });
  // You usually don't return a model instantiated
  return projectModel;
