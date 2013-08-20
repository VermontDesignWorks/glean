var page = require('webpage').create();
page.open('http://localhost:8000', function(){
	page.render('frontpage.png');
	phantom.exit();
});

