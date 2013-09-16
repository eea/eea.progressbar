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

jQuery(document).ready(function($){
  var progressbars = jQuery('.eea-progressbar');
  if(progressbars.length){
    return progressbars.EEAProgressBar();
  }
});
