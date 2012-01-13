// Filename: router.js
define([
  'jquery',
  'underscore',
  'backbone',
  //'views/users/list'
], function($, _, Backbone, wishesListView, userListView ){
  var AppRouter = Backbone.Router.extend({
    routes: {
      // Define some URL routes
      'wishes': 'showWishes',
      'users': 'showUsers',

      // Default
      '*actions': 'defaultAction'
    },
    showWishes: function(){
      // Call render on the module we loaded in via the dependency array
      // 'views/projects/list'
      wishesListView.render();
    },
      // As above, call render on our loaded module
      // 'views/users/list'
    showUsers: function(){
      userListView.render();
    },
    defaultAction: function(actions){
      // We have no matching route, lets display the home page
      //mainHomeView.render();
    }
  });

  var initialize = function(){
    var app_router = new AppRouter;
    Backbone.history.start();
  };
  return {
    initialize: initialize
  };
});


