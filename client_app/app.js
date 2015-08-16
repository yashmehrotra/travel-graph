var express = require('express');
var config = require('./config.js');
var path = require('path');
if (process.argv[2] != 'production') {
  var host = config.development.CLIENT_HOST;
  var port = config.development.CLIENT_PORT;
} else {
  var host = config.production.CLIENT_HOST;
  var port = config.production.CLIENT_PORT;
}

var app = express();


app.use('/public', express.static(__dirname + '/public'));
app.use('/dist', express.static(__dirname + '/dist'));

app.get('/*', function (req, res) {
  res.sendFile(path.join(__dirname+'/public/index.html'));
});


var server = app.listen(port, host, function () {
  var host = server.address().address;
  var port = server.address().port;
  console.log('Listening on http://%s:%s', host, port);
});

module.exports = app;
