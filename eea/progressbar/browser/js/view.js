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

/** Metadata Progress (document completion) viewlet
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
    console.log("ProgressMetadata Not implemented yet");
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
  var progressbars = jQuery('.eea-progressbar');
  if(progressbars.length){
    progressbars.EEAProgressBar();
  }

  var progresstrails = jQuery('.eea-progresstrail');
  if(progresstrails.length){
    progresstrails.EEAProgressTrail();
  }
});
