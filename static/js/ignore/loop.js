$(function() {
    //Conecta con el websocket server (en caso de usar namespace, añadirlo a la uri)
    var socket = io.connect("http://" + document.domain + ":" + location.port);
    $("#boton").click(myFunction);
    function myFunction() {
        console.log("GO!");
        var i = 0
        setInterval( () => { 
            i++;
            let mensaje = {"valor": i};
            json = JSON.stringify(mensaje);
            console.log(json);
            socket.emit("updateValue", json);
        }, 1000);
    }

});