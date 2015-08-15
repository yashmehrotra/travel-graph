var express = require('express');
var config = require('./config.js');
var path = require('path');
if (process.argv[2] != 'production') {
  var host = config.development.CLIENT_HOST;
  var port = config.development.CLIENT_PORT;
}

var app = express();


app.use(express.static('client_app/templates'));

app.get('/*', function (req, res) {
  res.sendFile(path.join(__dirname+'/public/index.html'));
});


var server = app.listen(port, host, function () {
  var host = server.address().address;
  var port = server.address().port;
  console.log('Listening on http://%s:%s', host, port);
});

module.exports = app;
