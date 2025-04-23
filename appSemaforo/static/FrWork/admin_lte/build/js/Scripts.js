
// Importa la biblioteca de gráficos Chart.js
const Chart = require('chart.js');

// Crea un gráfico de torta
const torta = document.getElementById('grafico-torta').getContext('2d');
const chartTorta = new Chart(torta, {
  type: 'pie',
  data: {
    labels: ['Etiqueta 1', 'Etiqueta 2', 'Etiqueta 3'],
    datasets: [{
      label: 'Dataset 1',
      data: [10, 20, 30],
      backgroundColor: [
        'rgba(255, 99, 132, 0.2)',
        'rgba(54, 162, 235, 0.2)',
        'rgba(255, 206, 86, 0.2)'
      ],
      borderColor: [
        'rgba(255, 99, 132, 1)',
        'rgba(54, 162, 235, 1)',
        'rgba(255, 206, 86, 1)'
      ],
      borderWidth: 1
    }]
  },
  options: {
    title: {
      display: true,
      text: 'Gráfico de Torta'
    }
  }
});

// Crea un gráfico de línea
const linea = document.getElementById('grafico-linea').getContext('2d');
const chartLinea = new Chart(linea, {
  type: 'line',
  data: {
    labels: ['Etiqueta 1', 'Etiqueta 2', 'Etiqueta 3'],
    datasets: [{
      label: 'Dataset 1',
      data: [10, 20, 30],
      backgroundColor: 'rgba(255, 99, 132, 0.2)',
      borderColor: 'rgba(255, 99, 132, 1)',
      borderWidth: 1
    }]
  },
  options: {
    title: {
      display: true,
      text: 'Gráfico de Línea'
    }
  }
});
