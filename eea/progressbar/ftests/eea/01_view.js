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

casper.test.begin('Progressbar test 2', function(test) {
   casper.start("http://" + url + "/");
   casper.waitForSelector(x("//a[normalize-space(text())='View your Plone site']"),
       function success() {
           test.assertExists(x("//a[normalize-space(text())='View your Plone site']"));
           this.click(x("//a[normalize-space(text())='View your Plone site']"));
       },
       function fail() {
           test.assertExists(x("//a[normalize-space(text())='View your Plone site']"));
   });
   casper.waitForSelector("#parent-fieldname-title",
       function success() {
           test.assertExists("#parent-fieldname-title");
           this.click("#parent-fieldname-title");
       },
       function fail() {
           test.assertExists("#parent-fieldname-title");
   });
   casper.waitForSelector("#parent-fieldname-title",
       function success() {
           test.assertExists("#parent-fieldname-title");
           this.click("#parent-fieldname-title");
       },
       function fail() {
           test.assertExists("#parent-fieldname-title");
   });
   casper.waitForSelector(x("//*[contains(text(), \'Welcome to Plone\')]"),
       function success() {
           test.assertExists(x("//*[contains(text(), \'Welcome to Plone\')]"));
         },
       function fail() {
           test.assertExists(x("//*[contains(text(), \'Welcome to Plone\')]"));
   });
    
   casper.wait(1000);
   casper.then(function() {
          this.captureSelector("screenshot_eea.png", "html");
   });

   casper.run(function() {test.done();});
});
   
}
else {
    this.echo('Error: No URL given', 'ERROR');
}
