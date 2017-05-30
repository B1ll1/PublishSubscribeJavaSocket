var server = require('http').createServer();
var io = require('socket.io')(server);
var mysql = require('mysql');

var con = mysql.createConnection({
  host: "localhost",
  user: "root",
  password: "root",
  database : 'flask'
});

con.connect(function(err) {
  if (err) throw err;
  console.log("Conectado no banco!");
});

function getSubscriptions(data, callback) {
        con.query('SELECT DISTINCT subscriptions.topic from subscriptions', function(err, rows) {
            if (err) {
                callback(err, null);
            } else
                callback(null, rows);
        });
}

io.sockets.on('connection', function(socket) {
    var subscriptions = null;

    socket.on('user_data', function (data) {

        if(data.type==2){
            console.log('Inscrito Conectado');
            getSubscriptions(data, function(err, content, socket) {
                if (err) {
                    console.log(err);
                } else {
                    subscriptions = content;
                }
            });
        }
        else{
             console.log('Analista Conectado');
        }
    });

    socket.on('message', function (data){
        socket.broadcast.emit('publicacoes/'+data.message.topic, { data });
    })
});
server.listen(3000);