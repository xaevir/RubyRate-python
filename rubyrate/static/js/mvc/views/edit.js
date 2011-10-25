App.Views.Edit = Backbone.View.extend({
    events: {
        'click .send': 'render',
        "submit form": "save"
    },
    
    initialize: function() {
         _.bindAll(this, 'render');
    },
    
    render: function() {
        e.preventDefault();
        alert('ass')
        var out = '<form>';
        out += "<label for='body'>Body</label>";
        out += "<textarea name='body'></textarea>";

        out += "<button>Send</button>";
        out += "</form>";

        //$(this.el).html(out);
        shit = e.currentTarget
        hello = $(this).parent()
        hello.html(out)
        var no = 'hi'
        $(this.el).parent().append(html(out))
        //$('#app').html(this.el);
        
        //this.$('[name=title]').val(this.model.get('title')); // use val, for security reasons
    }
});


