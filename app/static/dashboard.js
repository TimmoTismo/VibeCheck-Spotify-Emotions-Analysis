/* globals Chart:false, feather:false */

(function () {
  'use strict'

  feather.replace()
  var num = Array.from(Array(50).keys());

  // Graphs
  var ch_valence = document.getElementById('valenceChart')
  var ch_energy = document.getElementById('energyChart')

  // eslint-disable-next-line no-unused-vars
  var valenceChart = new Chart(ch_valence, {
    type: 'line',
    data: {
      labels: num,
      // labels: "{{user_data['played_at'].tolist()}}",
      datasets: [{
        data: val,
        label: 'Valence',
        lineTension: 0,
        backgroundColor: 'transparent',
        borderColor: '#007bff',
        borderWidth: 4,
        pointBackgroundColor: '#007bff'
      }]
    },
    options: {
      scales: {
        yAxes: [{
          ticks: {
            beginAtZero: false
          }
        }]
      },
      legend: {
        display: true
      }
    }
  })

  var energyChart = new Chart(ch_energy, {
    type: 'line',
    data: {
      labels: num,
      // labels: "{{user_data['played_at'].tolist()}}",
      datasets: [{
        data: energy,
        label: 'Energy',
        lineTension: 0,
        backgroundColor: 'transparent',
        borderColor: '#1DB954',
        borderWidth: 4,
        pointBackgroundColor: '#1DB954'
      }]
    },
    options: {
      scales: {
        yAxes: [{
          ticks: {
            beginAtZero: false
          }
        }]
      },
      legend: {
        display: true
      }
    }
  })
  
})()
