define([
  'jquery',
  'underscore',
  'backbone',
  'views/top_bar',
], function($, _, Backbone, TopBarController, noticeView){

    var App = {
        initialize: function() {
            new TopBarController({el: '.topbar'})
        },


        RegionManager: function () {
            var currentView;
            var el = "#mainregion";
            var region = {};

            var closeView = function (view) {
                if (view && view.close) {
                    view.close();
                }
            };

            var openView = function (view) {
                view.render();
                $(el).html(view.el);
                if (view.onShow) {
                    view.onShow();
                }
            };

            region.show = function (view) {
                closeView(currentView);
                currentView = view;
                openView(currentView);
            };

            return region;
        },
    }
    App.initialize()    
});
