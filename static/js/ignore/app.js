$(function() {
    //Conecta con el websocket server (en caso de usar namespace, añadirlo a la uri)
    var socket = io.connect("http://" + document.domain + ":" + location.port);

    // Consulta todos los sensores de la DB
    $("#select").on("click", () => {
        console.log("Consultada DB");
        socket.emit("selectAll");
    });
    
    let last_record=null;
    // Recibe los sensores que responde el servidor y los muestra en una tabla
    socket.on("respuestaSensores", (resp) => { 
        let sensores = resp.sensores;

        // Si los sensores que recibí no son los mismos que la última vez, actualizo.
        if(sensores != last_record){
            // Vacio la tabla para armarla otra vez.
            $("#tablaSensores").empty();

            $.each(sensores, (i, sensor) => {
                let $tr = $("<tr>").append(
                    $("<td>").text(sensor.id),
                    $("<td>").text(sensor.descripcion),
                    $("<td>").text(sensor.valor)
                ); 
                $("#tablaSensores").append($tr);       
            });
            $("#tablaSensores").show();
            // Guardo los últimos sensores recibidos
            last_record = resp.sensores;
        }
    });    


});