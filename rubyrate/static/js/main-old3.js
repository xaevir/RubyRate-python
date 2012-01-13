var appEl = document.getElementById("app")
if (appEl != null) {
   $LAB
   .script("/static/js/libs/jquery/jquery.js")
   .script("/static/js/libs/underscore/underscore.js").wait()
   .script("/static/js/libs/backbone/backbone.js")
   .script("/static/js/libs/jquery-validation/jquery.validate.js")
   .script("/static/js/libs/raphael-min.js").wait()
   .script("/static/js/app.js").wait()
   .script("/static/js/modules/nav.js")
   .script("/static/js/modules/chat.js").wait()
   .script("/static/js/events.js")
   .wait(function(){

    var nav = NavModule.load()

   });
}






