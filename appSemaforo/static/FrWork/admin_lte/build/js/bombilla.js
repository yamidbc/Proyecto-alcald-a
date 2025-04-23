document.addEventListener("DOMContentLoaded", function() {
    // Selecciona todos los elementos con la clase "bombilla"
    var bombillas = document.querySelectorAll(".bombilla");

    // Recorre cada bombilla
    bombillas.forEach(function(bombilla) {
      // Obtiene el color de la bombilla
      var color = bombilla.classList[1]; // verde, amarillo, rojo

      // Agrega la clase de parpadeo según el color
      if (color == "verde") {
        // No parpadea
      } else if (color == "amarillo") {
        bombilla.classList.add("parpadeo-medio");
      } else if (color == "rojo") {
        bombilla.classList.add("parpadeo-rapido");
      }
    });
  });