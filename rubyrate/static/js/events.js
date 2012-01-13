var EventsRouter = (function(myApp, Backbone, $){
   
    myApp.event.bind("region:loadChat", loadChat);


    function loadChat(model){
        var id = model.get("wish_id");
        ChatModule.setId(id); 
        myApp.event.bind("chat:modelsLoaded", function(){
            myApp.RegionManager.show(ChatModule);
        });
    }



})(myApp, ChatModule, Backbone, $);
