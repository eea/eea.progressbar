if(window.EEA === undefined){
  var EEA = {
    who: 'eea.progressbar',
    version: '1.3'
  };
}

EEA.ProgressBar = function(context, options){
  var self = this;
  self.context = context;

  self.settings = {
    baseurl: ""
  };

  if(options){
    jQuery.extend(self.settings, options);
  }

  self.initialize();
};

EEA.ProgressBar.prototype = {
  initialize: function(){
    var self = this;

    if(!self.settings.baseurl){
      var baseurl = self.context.data('baseurl');
      if(baseurl){
        self.settings.baseurl = baseurl + '/';
      }
    }

    // Handle eea.workflow async workflow change
    if(window.AsyncWorkflow){
      jQuery(AsyncWorkflow.Events).bind(AsyncWorkflow.Events.WORKFLOW_MENU_REFRESHED, function(evt, data){
        self.reload();
      });
    }
  },

  reload: function(){
    var self = this;
    jQuery.get(self.settings.baseurl + '@@progress.bar', {}, function(data){
      var html = jQuery(data).html();
      self.context.html(html);
    });
  }
};

jQuery.fn.EEAProgressBar = function(options){
  return this.each(function(){
    var context = jQuery(this);
    var adapter = new EEA.ProgressBar(context, options);
    context.data('EEAProgressBar', adapter);
  });
};

EEA.ProgressTrail = function(context, options){
  var self = this;
  self.context = context;
  self.settings = {
    baseurl: ""
  };

  if(options){
    jQuery.extend(self.settings, options);
  }

  self.initialize();
};

EEA.ProgressTrail.prototype = {
  initialize: function(){
    var self = this;

    if(!self.settings.baseurl){
      var baseurl = self.context.data('baseurl');
      if(baseurl){
        self.settings.baseurl = baseurl + '/';
      }
    }

    // Handle eea.workflow async workflow change
    if(window.AsyncWorkflow){
      jQuery(AsyncWorkflow.Events).bind(AsyncWorkflow.Events.WORKFLOW_MENU_REFRESHED, function(evt, data){
        self.reload();
      });
    }
  },

  reload: function(){
    var self = this;
    jQuery.get(self.settings.baseurl + '@@progress.trail', {}, function(data){
      var html = jQuery(data).html();
      self.context.html(html);
    });
  }
};

jQuery.fn.EEAProgressTrail = function(options){
  return this.each(function(){
    var context = jQuery(this);
    var adapter = new EEA.ProgressTrail(context, options);
    context.data('EEAProgressTrail', adapter);
  });
};

/** Editing Progress (document completion) viewlet
 *
 * @param context
 * @param options
 * @constructor
 */
EEA.ProgressMetadata = function(context, options){
  var self = this;
  self.context = context;
  self.settings = {

  };

  if(options){
    jQuery.extend(self.settings, options);
  }

  self.initialize();
};

EEA.ProgressMetadata.prototype = {
  initialize: function(){
    var self = this;
    self.fields = self.context.find('.progress-field');
    self.prevButton = self.context.find('.progress-nav span.prev');
    self.nextButton = self.context.find('.progress-nav span.next');
    self.first = self.context.find('.progress-field:first-child');
    self.last = self.context.find('.progress-field:last-child');
    self.width = 0;

    self.windowWidth = jQuery(window).width();

    // Handle events
    jQuery(window).resize(function(){
      var windowWidth = jQuery(window).width();
      if(windowWidth != self.windowWidth){
        self.windowWidth = windowWidth;
        self.reload();
      }
    });

    self.nextButton.click(function(){
      setTimeout(function(){
        self.next();
        self.prev();
      }, 510);
    });

    self.prevButton.click(function(){
      setTimeout(function(){
        self.prev();
        self.next();
      }, 510);
    });

    self.prev();
    self.reload();
  },

  reload: function(){
    var self = this;
    self.width = self.context.find('.progress-metadata').width();
    self.context.find('.metadata-bar').width(self.width - 50);

    var divide = 1;
    if(self.width >= 400){
      divide = 2;
    }
    if(self.width >= 700){
      divide = 3;
    }
    if(self.width >= 1000){
      divide = 4;
    }
    if(self.width >= 1300){
      divide = 5;
    }

    if(self.fields.length < divide){
      self.context.find('.progress-nav').remove();
      return;
    }

    self.context.find('.progress-field').width(self.width / divide);
    self.context.unbind('.serialScroll');
    self.context.serialScroll({
      target: '.progress-metadata',
      items: '.progress-field',
      prev: '.progress-nav span.prev',
      next: '.progress-nav span.next',
      step: divide,
      duration: 500,
      cycle: false
    });
  },

  next: function(){
    var self = this;
    if(!self.last.length){
      return;
    }
    var left = self.last.position().left;
    if(left < self.width - 10){
      self.nextButton.addClass('end');
    }else{
      self.nextButton.removeClass('end');
    }
  },

  prev: function(){
    var self = this;
    if(!self.first.length){
      return;
    }
    var left = self.first.position().left;
    if(left > -10){
      self.prevButton.addClass('end');
    }else{
      self.prevButton.removeClass('end');
    }
  }
};

jQuery.fn.EEAProgressMetadata = function(options){
  return this.each(function(){
    var context = jQuery(this);
    var adapter = new EEA.ProgressMetadata(context, options);
    context.data('EEAProgressMetadata', adapter);
  });
};

jQuery(document).ready(function($){
  /* Progress bar */
  var progressbars = jQuery('.eea-progressbar');
  if(progressbars.length){
    progressbars.EEAProgressBar();
  }

  /* Progress trail */
  var progresstrails = jQuery('.eea-progresstrail');
  if(progresstrails.length){
    progresstrails.EEAProgressTrail();
  }

  /* Progress metadata */
  var progressmeta = jQuery('.eea-progress-metadata');
  if(progressmeta.length){
    progressmeta.EEAProgressMetadata();
  }
});
