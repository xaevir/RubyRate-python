require.config({
    paths: {
        jquery: 'libs/jquery/jquery-min',
        underscore: 'libs/underscore/underscore-min',
        backbone: 'libs/backbone/backbone-optamd3-min',
        text: 'libs/require/text',
        domReady: 'libs/require/domReady',
        //templates: '../templates',
    },
    baseUrl: "/static/js",
});



require(['app'], function(App){

    App.initialize();

});
