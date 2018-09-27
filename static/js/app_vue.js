// Self-Invoking Anonymous Function para encapsulamiento (seguridad)
(function(){
    // TODO: hacer que la dirección venga de la variable de entorno a través del render_template()
    var socket = io.connect("http://" + document.domain + ":" + location.port);

  // Instancia de Vue.js
  var app = new Vue({
    el: "#app",
    delimiters: ['[[', ']]'],
    data: {
      sensores: []
    },
    methods:{
      getSensores: function(){socket.emit("selectAll");}
    },
    created : function() {
      this.getSensores();
    }
  });

  socket.on("respuestaSensores", (resp) => { 
      let sensores = resp.sensores;
      app.sensores = sensores;
  });
  
})();