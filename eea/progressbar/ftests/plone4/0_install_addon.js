/*==============================================================================*/
/* Casper generated Tue Oct 24 2017 10:53:20 GMT+0300 (GTB Daylight Time) */
/*==============================================================================*/

var x = require('casper').selectXPath;
casper.options.viewportSize = {width: 1920, height: 974};
casper.options.pageSettings = {
    userName: 'admin',
    password: 'admin'
};
casper.on('page.error', function(msg, trace) {
   this.echo('Error: ' + msg, 'ERROR');
   for(var i=0; i<trace.length; i++) {
       var step = trace[i];
       this.echo('   ' + step.file + ' (line ' + step.line + ')', 'ERROR');
   }
});


var url ;

if (casper.cli.has("url")) {
url = casper.cli.get("url");
    
casper.echo("Url is " + url);

casper.test.begin('Progressbar test', function(test) {
   casper.start("http://" + url + "/");
   casper.waitForSelector("form#add-plone-site input[type=submit][value='Create a new Plone site']",
       function success() {
           test.assertExists("form#add-plone-site input[type=submit][value='Create a new Plone site']", "create new plone site");
           this.click("form#add-plone-site input[type=submit][value='Create a new Plone site']");
       },
       function fail() {
           test.assertExists("form#add-plone-site input[type=submit][value='Create a new Plone site']", "create new plone site");
   });
   /* submit form */
   casper.waitForSelector("form input[value='eea.progressbar:default']",
       function success() {
           test.assertExists("form input[value='eea.progressbar:default']", "eea.progressbar check box is present");
           this.click("form input[value='eea.progressbar:default']");
       },
       function fail() {
           test.assertExists("form input[value='eea.progressbar:default']", "eea.progressbar check box is present");
   });
   casper.waitForSelector("form input[type=submit][value='Create Plone Site']",
       function success() {
           test.assertExists("form input[type=submit][value='Create Plone Site']", "create the plone site");
           this.click("form input[type=submit][value='Create Plone Site']");
       },
       function fail() {
           test.assertExists("form input[type=submit][value='Create Plone Site']", "create the plone site");
   });

   casper.wait(1000);   
   casper.then(function() {
          this.captureSelector("screenshot1.png", "html");
   });

   casper.waitForSelector(".progressbar-viewlet.percentage",
          function success() {
              test.assertExists(".progressbar-viewlet.percentage", "Percentage progressbar exists on home page");
          },
          function fail() {
              test.assertExists(".progressbar-viewlet.percentage", "Percentage progressbar exists on home page");
   });
   casper.waitForSelector(".progressbar-viewlet.trail",
             function success() {
                 test.assertExists(".progressbar-viewlet.trail", "Trail progressbar exists on home page");
             },
             function fail() {
                 test.assertExists(".progressbar-viewlet.trail", "Trail progressbar exists on home page");
    });   

   casper.run(function() {test.done();});
});
    
}
else {
    this.echo('Error: No URL given', 'ERROR');
}
