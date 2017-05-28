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

io.sockets.on('connection', function(socket) {
    console.log("New connection");

    socket.on('user_data', function (data) {
        console.log(data.user.id,data.user.type);
        console.log("Received: " + data.id);

        if(data.user.type==1){

        }

        else if(data.user.type==2){
            con.query('SELECT * from subscriptions where user_id = ?', [message], function (error, results, fields) {
              if (error) throw error;
              var subscriptions = JSON.stringify(results)
            });
        }



        /*
        con.query('SELECT * from subscriptions where user_id = ?', [message], function (error, results, fields) {
          if (error) throw error;
          var subscriptions = JSON.stringify(results)

        });*/
        socket.send('Text from server');
    });
});
server.listen(3000);