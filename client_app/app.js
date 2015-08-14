var express = require('express');
var app = express();

app.use(express.static('templates'));

app.get('/', function (req, res) {
  res.redirect('/test.html');
});


var server = app.listen(4000, '127.0.0.1', function () {
  var host = server.address().address;
  var port = server.address().port;
  console.log('Example app listening at http://%s:%s', host, port);
});

module.exports = app;
