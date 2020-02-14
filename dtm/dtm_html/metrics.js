function metrics(){
  var data = [{name: "CaoJuan2009", data: avgcossim_data, showInLegend: true,},
              {name: "Deveaud2014", data: avgjs_data, showInLegend: true,}]

  Highcharts.chart('metrics', {
    credits: {
       enabled: false
   },

    title: {
      text: "Metrics vs number of topics"
    },

    subtitle: {
      text: ' '
    },

    yAxis: {
      title: {
        text: ''
      }
    },
    xAxis: {
      tickInterval: 1,
      title: {
        text: 'Number of topics'
      }

    },
    legend: {
      layout: 'vertical',
      align: 'right',
      verticalAlign: 'middle',
      display: false,
    },

    plotOptions: {
      series: {
        label: {
          connectorAllowed: false
        },
        pointStart: 2
      }
    },

    series: data,

    responsive: {
      rules: [{
        condition: {
          maxWidth: 500
        },
        chartOptions: {
          legend: {
            layout: 'horizontal',
            align: 'center',
            verticalAlign: 'bottom'
          }
        }
      }]
    }

  })

}
metrics()
