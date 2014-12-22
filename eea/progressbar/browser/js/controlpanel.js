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

EEA.ProgressTool.Events = {
  reloadWidget: 'eea-progressbar-reloadWidget'
};

EEA.ProgressTool.prototype = {
  initialize: function(){
    var self = this;
    self.width = self.context.width();
    self.action = self.context.data('url');

    // Events
    jQuery(EEA.ProgressTool.Events).bind(EEA.ProgressTool.Events.reloadWidget, function(evt, data){
      self.reloadWidget(data.widget, data.newWidget);
      self.context.masonry('reloadItems');
      self.context.masonry('layout');
    });

    jQuery('#add-new-widget').click(function(evt){
      evt.preventDefault();
      var dialog = jQuery('#add-new-widget-dialog').dialog({
        modal: true,
        title: 'Add new widget',
        buttons: {
          Add: function() {
            self.addWidget();
            dialog.dialog( 'close' );
          },
          Cancel: function() {
            dialog.dialog( 'close' );
          }
        },
        close: function() {
          jQuery('#add-new-widget-dialog form')[ 0 ].reset();
          jQuery('#new-widget-name').removeClass( 'ui-state-error' );
        }
      });

    form = dialog.find( 'form' ).on( 'submit', function( event ) {
      event.preventDefault();
      self.addWidget();
      dialog.dialog( 'close' );
    });
    return;
    });

    self.reload();
  },

  addWidget: function() {
    var self = this;
    var new_name = jQuery('#new-widget-name').val();
    var url = jQuery('#add-new-widget').attr('href');

    if(new_name && url) {
      $.ajax({
        type: 'POST',
        url: url,
        data: { name: new_name },
        success: function(data) {
          var widget = jQuery(data);
          self.context.prepend(self.reloadWidget(widget));
          self.context.masonry('reloadItems');
          self.context.masonry('layout');
        }
      });
    }
  },

  reload: function(){
    var self = this;
    self.widgets =  self.context.find('.eea-progressbar-widget');
    self.widgets.each(function(){
      var widget = jQuery(this);
      return self.reloadWidget(widget);
    });

    self.context.masonry({
      itemSelector: '.masonry-widget',
      gutter: 5,
      isResizable: true,
      isFitWidth: true
    });

    self.context.sortable({
      items: '.eea-progressbar-widget',
//      placeholder: 'ui-state-highlight',
      forcePlaceholderSize: true,
      opacity: 0.7,
      delay: 300,
      cursor: 'crosshair',
      tolerance: 'pointer',
      start: function(event, ui){
        ui.item.removeClass('masonry-widget');
        self.context.masonry('reloadItems');
        self.context.masonry('layout');
      },
      change: function(event, ui){
        self.context.masonry('reloadItems');
        self.context.masonry('layout');
      },
      stop: function(event, ui){
        ui.item.addClass('masonry-widget');
        self.context.masonry('reloadItems');
        self.context.masonry('layout');
      },
      update: function(event, ui){
        self.reorder(self.context.sortable('toArray'));
      }
    });
  },

  reloadWidget: function(widget, newWidget){
    var self = this;
    if(newWidget){
      widget.replaceWith(newWidget);
      widget = newWidget;
    }
    var adapter = new EEA.ProgressTool.Widget(widget, {parent: self.context});
    widget.data('EEAProgressToolWidget', adapter);
    return widget;
  },

  reorder: function(order){
    var self = this;

    order = jQuery.map(order, function(item, idx){
      return item.replace('progress-schema-', '');
    });

    var query = {'order': order, 'ajax': true};
    jQuery.ajax({
      traditional: true,
      type: 'post',
      url: self.action + '.reorder',
      data: query,
      success: function(data){
        console.log(data);
      }
    });
  }
};

EEA.ProgressTool.Widget = function(context, options){
  var self = this;
  self.context = context;
  self.parent = options.parent;
  self.settings = {};

  if(options){
    jQuery.extend(self.settings, options);
  }

  self.initialize();
};

EEA.ProgressTool.Widget.prototype = {
  initialize: function(){
    var self = this;
    self.width = 320;
    self.context.addClass('masonry-widget');
    self.form = self.context.find('form').hide();
    self.button = self.context.find('.buttons a');
    self.field = self.context.data('field');

    self.context.width(self.width);
    self.context.find('textarea').attr('rows', 3);

    // Events
    jQuery(':input', self.form).change(function(){
      self.context.addClass('changed');
    });

    self.context.find('a').click(function(evt){
      evt.preventDefault();
      return;
    });

    self.form.submit(function(evt){
      evt.preventDefault();
      return false;
    });

    if(!self.context.hasClass('custom')){
      self.form.find('input[type="submit"][name$="actions.reset"]').remove();
    }

    if(self.context.hasClass('extrafield')){
      self.context.find('.widget-close').click(function(evt){
        evt.preventDefault();
        var name = self.context.attr('data-field');
        var url = $(this).attr('href');
        $.ajax({
          type: 'POST',
          url: url,
          data: { name: name },
          success: function(data) {
            if (data === 'True') {
              self.context.remove();
            }
          }
        });
        return false;
      });
    }

    self.form.find('input[type="submit"]').click(function(evt){
      evt.preventDefault();
      return self.submit(jQuery(this));
    });

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
  },

  submit: function(button){
    var self = this;
    var action = self.form.attr('action');
    var name = button.attr('name');
    var query = name + '=ajax&';
    query += self.form.serialize();

    jQuery.ajax({
      traditional: true,
      type: 'post',
      url: action,
      data: query,
      success: function(data){
        self.reload(data);
      }
    });
  },

  reload: function(msg){
    var self = this;
    var action = self.form.attr('action');
    action = action.split('.schema')[0] + 'view.metadata';
    var query = {field: self.field};
    jQuery.get(action, query, function(data){
      jQuery(EEA.ProgressTool.Events).trigger(
        EEA.ProgressTool.Events.reloadWidget, {
          widget: self.context,
          newWidget: $(data)
        });
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
