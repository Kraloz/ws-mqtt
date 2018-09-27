(function(){
    var socket = io.connect("http://" + document.domain + ":" + location.port);
    var sensores;
    var last_sensores=null;

    $(function() {
        //Conecta con el websocket server (en caso de usar namespace, añadirlo a la uri)
        getSensores();
        $("select.id").change(updateTabla);
        //$("select.id").trigger("change");
    });
// Funcion para TRAER los valores nuevos
    function getSensores(){
        socket.emit("selectAll");
    }

    function updateTabla(){
        getSensores();
        
        var select_id = $("select.id").val();
        var indice;
        $.each(sensores, (i, sensor) => {
            if(select_id==sensor.id){
                indice = i;
            }
        });
        $("td.descripcion").text(sensores[indice].descripcion);
        $("input.valor").val(sensores[indice].valor);
        // $("input.valor").text(sensores[indice].valor);
    }


    socket.on("respuestaSensores", (resp) => {
        // obj con valores
        sensores = resp.sensores;

        // Voy a rearmar los valores
        if(sensores != last_sensores){
            var last_value = $("select.id").val();
            $("select.id").empty();
            last_sensores = sensores;  
            $.each(sensores, (i, sensor) => {
                // Attacheo los brand new values
                $("select.id").append(new Option(sensor.id.toString(), sensor.id.toString()));
            });
            
            try {
                $("select.id").off(change);
                $("select.id").text(last_value);
                $("select.id").change(updateTabla);
            }
            catch(err) {
                // Estoy recibiendo una excepción que TIENE sentido
                // $("select.id").off(change); está mal
                // change debería ser una cadena
                // pero siendo cadena, el select NO anda
                // idk why pasa pero voy a dejarlo así hasta consultar con pablo
                // estre try-catch es para que no aparezca el error feo en consola
            }
        }
    });

})();