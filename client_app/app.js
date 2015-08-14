var express = require('express');
var config = require('./config.js');

if (process.argv[2] != 'production') {
  var host = config.development.CLIENT_HOST;
  var port = config.development.CLIENT_PORT;
}

var app = express();


app.use(express.static('client_app/templates'));

app.get('/', function (req, res) {
  console.log('Home Page Ping');
  res.redirect('/test.html');
});


var server = app.listen(port, host, function () {
  var host = server.address().address;
  var port = server.address().port;
  console.log('Listening on http://%s:%s', host, port);
});

module.exports = app;
