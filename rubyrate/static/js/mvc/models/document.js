var Document = Backbone.Model.extend({
    url : function() {
      var base = 'messages';
      if (this.isNew()) return base;
      return base + (base.charAt(base.length - 1) == '/' ? '' : '/') + this.id;
    }
});


