define([
  'jquery',
  'underscore',
  'backbone',
  'router', // Request router.js
], function($, _, Backbone, Router){
  var initialize = function(){
    // Pass in our Router module and call it's initialize function
    Router.initialize();
    // load modules
    if (window.load_module) {
        switch(load_module) { 
            case 'wishes':
                require(['views/wishes/list'], function(wishesListView) {
                    wishesListView.render();
                });
                break;
            default:{}
        }
    }        
  }

  return {
    initialize: initialize
  };
});
