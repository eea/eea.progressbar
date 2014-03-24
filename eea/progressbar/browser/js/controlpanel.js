if(!window.EEA){
  var EEA = {
    who: 'eea.progressbar',
    version: '3.0'
  };
}

EEA.ProgressTool = function(context, options){
  var self = this;
  self.context = context;
  self.settings = {

  };

  if(options){
    jQuery.extend(self.settings, options);
  }

  self.initialize();
};

EEA.ProgressTool.prototype = {
  initialize: function(){
    var self = this;
    self.width = self.context.width();
    self.reload();
  },

  reload: function(){
    var self = this;
    self.widgets =  self.context.find('.eea-progressbar-widget');
    self.widgets.each(function(){
      var context = jQuery(this);
      var adapter = new EEA.ProgressToolWidget(context, {parent: self.context});
      context.data('EEAProgressToolWidget', adapter);
    });

    self.context.masonry({
      itemSelector: '.eea-progressbar-widget',
      gutter: 5,
      isFitWidth: true
    });
  }
};

EEA.ProgressToolWidget = function(context, options){
  var self = this;
  self.context = context;
  self.parent = options.parent;
  self.settings = {};

  if(options){
    jQuery.extend(self.settings, options);
  }

  self.initialize();
};

EEA.ProgressToolWidget.prototype = {
  initialize: function(){
    var self = this;
    self.width = 320;
    self.form = self.context.find('form').hide();
    self.button = self.context.find('.buttons a');

    self.context.width(self.width);

    // Events
    self.button.click(function(evt){
      evt.preventDefault();
      if(self.context.css('z-index') == '9999'){
        self.context.css('z-index', 'auto');
      }else{
        self.context.css('z-index', '9999');
      }
      self.form.slideToggle('fast', function(){
        self.parent.masonry('layout');
      });
    });

    self.context.find('a').click(function(evt){
      evt.preventDefault();
      return;
    });
  }
};

jQuery.fn.EEAProgressTool = function(options){
  return this.each(function(){
    var context = jQuery(this);
    var adapter = new EEA.ProgressTool(context, options);
    context.data('EEAProgressTool', adapter);
  });
};

jQuery(document).ready(function(){
  var items = jQuery('#eea-progressbar-cpanel');
  if(!items.length){
    return;
  }

  var settings = {};
  items.EEAProgressTool(settings);
});
