


function series(k){
  var graph_data  = {};
  graph_data[2] = [{'id': 'g', 'valueAxis': ' ', 'lineColor': '#808080', 'bullet': 'round', 'bulletBorderThickness': 1, 'hideBulletsCount': 30, 'title': 'Total', 'valueField': '0', 'fillAlphas': 0}, {'id': 'g1', 'valueAxis': ' ', 'lineColor': '#e6194b', 'bullet': 'round', 'bulletBorderThickness': 1, 'hideBulletsCount': 30, 'title': 'Topic1', 'valueField': '1', 'fillAlphas': 0}, {'id': 'g2', 'valueAxis': ' ', 'lineColor': '#3cb44b', 'bullet': 'round', 'bulletBorderThickness': 1, 'hideBulletsCount': 30, 'title': 'Topic2', 'valueField': '2', 'fillAlphas': 0}];
  graph_data[3] = [{'id': 'g', 'valueAxis': ' ', 'lineColor': '#808080', 'bullet': 'round', 'bulletBorderThickness': 1, 'hideBulletsCount': 30, 'title': 'Total', 'valueField': '0', 'fillAlphas': 0}, {'id': 'g1', 'valueAxis': ' ', 'lineColor': '#e6194b', 'bullet': 'round', 'bulletBorderThickness': 1, 'hideBulletsCount': 30, 'title': 'Topic1', 'valueField': '1', 'fillAlphas': 0}, {'id': 'g2', 'valueAxis': ' ', 'lineColor': '#3cb44b', 'bullet': 'round', 'bulletBorderThickness': 1, 'hideBulletsCount': 30, 'title': 'Topic2', 'valueField': '2', 'fillAlphas': 0}, {'id': 'g3', 'valueAxis': ' ', 'lineColor': '#ffe119', 'bullet': 'round', 'bulletBorderThickness': 1, 'hideBulletsCount': 30, 'title': 'Topic3', 'valueField': '3', 'fillAlphas': 0}];
  graph_data[4] = [{'id': 'g', 'valueAxis': ' ', 'lineColor': '#808080', 'bullet': 'round', 'bulletBorderThickness': 1, 'hideBulletsCount': 30, 'title': 'Total', 'valueField': '0', 'fillAlphas': 0}, {'id': 'g1', 'valueAxis': ' ', 'lineColor': '#e6194b', 'bullet': 'round', 'bulletBorderThickness': 1, 'hideBulletsCount': 30, 'title': 'Topic1', 'valueField': '1', 'fillAlphas': 0}, {'id': 'g2', 'valueAxis': ' ', 'lineColor': '#3cb44b', 'bullet': 'round', 'bulletBorderThickness': 1, 'hideBulletsCount': 30, 'title': 'Topic2', 'valueField': '2', 'fillAlphas': 0}, {'id': 'g3', 'valueAxis': ' ', 'lineColor': '#ffe119', 'bullet': 'round', 'bulletBorderThickness': 1, 'hideBulletsCount': 30, 'title': 'Topic3', 'valueField': '3', 'fillAlphas': 0}, {'id': 'g4', 'valueAxis': ' ', 'lineColor': '#0082c8', 'bullet': 'round', 'bulletBorderThickness': 1, 'hideBulletsCount': 30, 'title': 'Topic4', 'valueField': '4', 'fillAlphas': 0}];
  graph_data[5] = [{'id': 'g', 'valueAxis': ' ', 'lineColor': '#808080', 'bullet': 'round', 'bulletBorderThickness': 1, 'hideBulletsCount': 30, 'title': 'Total', 'valueField': '0', 'fillAlphas': 0}, {'id': 'g1', 'valueAxis': ' ', 'lineColor': '#e6194b', 'bullet': 'round', 'bulletBorderThickness': 1, 'hideBulletsCount': 30, 'title': 'Topic1', 'valueField': '1', 'fillAlphas': 0}, {'id': 'g2', 'valueAxis': ' ', 'lineColor': '#3cb44b', 'bullet': 'round', 'bulletBorderThickness': 1, 'hideBulletsCount': 30, 'title': 'Topic2', 'valueField': '2', 'fillAlphas': 0}, {'id': 'g3', 'valueAxis': ' ', 'lineColor': '#ffe119', 'bullet': 'round', 'bulletBorderThickness': 1, 'hideBulletsCount': 30, 'title': 'Topic3', 'valueField': '3', 'fillAlphas': 0}, {'id': 'g4', 'valueAxis': ' ', 'lineColor': '#0082c8', 'bullet': 'round', 'bulletBorderThickness': 1, 'hideBulletsCount': 30, 'title': 'Topic4', 'valueField': '4', 'fillAlphas': 0}, {'id': 'g5', 'valueAxis': ' ', 'lineColor': '#f58231', 'bullet': 'round', 'bulletBorderThickness': 1, 'hideBulletsCount': 30, 'title': 'Topic5', 'valueField': '5', 'fillAlphas': 0}];
  graph_data[6] = [{'id': 'g', 'valueAxis': ' ', 'lineColor': '#808080', 'bullet': 'round', 'bulletBorderThickness': 1, 'hideBulletsCount': 30, 'title': 'Total', 'valueField': '0', 'fillAlphas': 0}, {'id': 'g1', 'valueAxis': ' ', 'lineColor': '#e6194b', 'bullet': 'round', 'bulletBorderThickness': 1, 'hideBulletsCount': 30, 'title': 'Topic1', 'valueField': '1', 'fillAlphas': 0}, {'id': 'g2', 'valueAxis': ' ', 'lineColor': '#3cb44b', 'bullet': 'round', 'bulletBorderThickness': 1, 'hideBulletsCount': 30, 'title': 'Topic2', 'valueField': '2', 'fillAlphas': 0}, {'id': 'g3', 'valueAxis': ' ', 'lineColor': '#ffe119', 'bullet': 'round', 'bulletBorderThickness': 1, 'hideBulletsCount': 30, 'title': 'Topic3', 'valueField': '3', 'fillAlphas': 0}, {'id': 'g4', 'valueAxis': ' ', 'lineColor': '#0082c8', 'bullet': 'round', 'bulletBorderThickness': 1, 'hideBulletsCount': 30, 'title': 'Topic4', 'valueField': '4', 'fillAlphas': 0}, {'id': 'g5', 'valueAxis': ' ', 'lineColor': '#f58231', 'bullet': 'round', 'bulletBorderThickness': 1, 'hideBulletsCount': 30, 'title': 'Topic5', 'valueField': '5', 'fillAlphas': 0}, {'id': 'g6', 'valueAxis': ' ', 'lineColor': '#911eb4', 'bullet': 'round', 'bulletBorderThickness': 1, 'hideBulletsCount': 30, 'title': 'Topic6', 'valueField': '6', 'fillAlphas': 0}];
  graph_data[7] = [{'id': 'g', 'valueAxis': ' ', 'lineColor': '#808080', 'bullet': 'round', 'bulletBorderThickness': 1, 'hideBulletsCount': 30, 'title': 'Total', 'valueField': '0', 'fillAlphas': 0}, {'id': 'g1', 'valueAxis': ' ', 'lineColor': '#e6194b', 'bullet': 'round', 'bulletBorderThickness': 1, 'hideBulletsCount': 30, 'title': 'Topic1', 'valueField': '1', 'fillAlphas': 0}, {'id': 'g2', 'valueAxis': ' ', 'lineColor': '#3cb44b', 'bullet': 'round', 'bulletBorderThickness': 1, 'hideBulletsCount': 30, 'title': 'Topic2', 'valueField': '2', 'fillAlphas': 0}, {'id': 'g3', 'valueAxis': ' ', 'lineColor': '#ffe119', 'bullet': 'round', 'bulletBorderThickness': 1, 'hideBulletsCount': 30, 'title': 'Topic3', 'valueField': '3', 'fillAlphas': 0}, {'id': 'g4', 'valueAxis': ' ', 'lineColor': '#0082c8', 'bullet': 'round', 'bulletBorderThickness': 1, 'hideBulletsCount': 30, 'title': 'Topic4', 'valueField': '4', 'fillAlphas': 0}, {'id': 'g5', 'valueAxis': ' ', 'lineColor': '#f58231', 'bullet': 'round', 'bulletBorderThickness': 1, 'hideBulletsCount': 30, 'title': 'Topic5', 'valueField': '5', 'fillAlphas': 0}, {'id': 'g6', 'valueAxis': ' ', 'lineColor': '#911eb4', 'bullet': 'round', 'bulletBorderThickness': 1, 'hideBulletsCount': 30, 'title': 'Topic6', 'valueField': '6', 'fillAlphas': 0}, {'id': 'g7', 'valueAxis': ' ', 'lineColor': '#46f0f0', 'bullet': 'round', 'bulletBorderThickness': 1, 'hideBulletsCount': 30, 'title': 'Topic7', 'valueField': '7', 'fillAlphas': 0}];
  graph_data[8] = [{'id': 'g', 'valueAxis': ' ', 'lineColor': '#808080', 'bullet': 'round', 'bulletBorderThickness': 1, 'hideBulletsCount': 30, 'title': 'Total', 'valueField': '0', 'fillAlphas': 0}, {'id': 'g1', 'valueAxis': ' ', 'lineColor': '#e6194b', 'bullet': 'round', 'bulletBorderThickness': 1, 'hideBulletsCount': 30, 'title': 'Topic1', 'valueField': '1', 'fillAlphas': 0}, {'id': 'g2', 'valueAxis': ' ', 'lineColor': '#3cb44b', 'bullet': 'round', 'bulletBorderThickness': 1, 'hideBulletsCount': 30, 'title': 'Topic2', 'valueField': '2', 'fillAlphas': 0}, {'id': 'g3', 'valueAxis': ' ', 'lineColor': '#ffe119', 'bullet': 'round', 'bulletBorderThickness': 1, 'hideBulletsCount': 30, 'title': 'Topic3', 'valueField': '3', 'fillAlphas': 0}, {'id': 'g4', 'valueAxis': ' ', 'lineColor': '#0082c8', 'bullet': 'round', 'bulletBorderThickness': 1, 'hideBulletsCount': 30, 'title': 'Topic4', 'valueField': '4', 'fillAlphas': 0}, {'id': 'g5', 'valueAxis': ' ', 'lineColor': '#f58231', 'bullet': 'round', 'bulletBorderThickness': 1, 'hideBulletsCount': 30, 'title': 'Topic5', 'valueField': '5', 'fillAlphas': 0}, {'id': 'g6', 'valueAxis': ' ', 'lineColor': '#911eb4', 'bullet': 'round', 'bulletBorderThickness': 1, 'hideBulletsCount': 30, 'title': 'Topic6', 'valueField': '6', 'fillAlphas': 0}, {'id': 'g7', 'valueAxis': ' ', 'lineColor': '#46f0f0', 'bullet': 'round', 'bulletBorderThickness': 1, 'hideBulletsCount': 30, 'title': 'Topic7', 'valueField': '7', 'fillAlphas': 0}, {'id': 'g8', 'valueAxis': ' ', 'lineColor': '#f032e6', 'bullet': 'round', 'bulletBorderThickness': 1, 'hideBulletsCount': 30, 'title': 'Topic8', 'valueField': '8', 'fillAlphas': 0}];
  graph_data[9] = [{'id': 'g', 'valueAxis': ' ', 'lineColor': '#808080', 'bullet': 'round', 'bulletBorderThickness': 1, 'hideBulletsCount': 30, 'title': 'Total', 'valueField': '0', 'fillAlphas': 0}, {'id': 'g1', 'valueAxis': ' ', 'lineColor': '#e6194b', 'bullet': 'round', 'bulletBorderThickness': 1, 'hideBulletsCount': 30, 'title': 'Topic1', 'valueField': '1', 'fillAlphas': 0}, {'id': 'g2', 'valueAxis': ' ', 'lineColor': '#3cb44b', 'bullet': 'round', 'bulletBorderThickness': 1, 'hideBulletsCount': 30, 'title': 'Topic2', 'valueField': '2', 'fillAlphas': 0}, {'id': 'g3', 'valueAxis': ' ', 'lineColor': '#ffe119', 'bullet': 'round', 'bulletBorderThickness': 1, 'hideBulletsCount': 30, 'title': 'Topic3', 'valueField': '3', 'fillAlphas': 0}, {'id': 'g4', 'valueAxis': ' ', 'lineColor': '#0082c8', 'bullet': 'round', 'bulletBorderThickness': 1, 'hideBulletsCount': 30, 'title': 'Topic4', 'valueField': '4', 'fillAlphas': 0}, {'id': 'g5', 'valueAxis': ' ', 'lineColor': '#f58231', 'bullet': 'round', 'bulletBorderThickness': 1, 'hideBulletsCount': 30, 'title': 'Topic5', 'valueField': '5', 'fillAlphas': 0}, {'id': 'g6', 'valueAxis': ' ', 'lineColor': '#911eb4', 'bullet': 'round', 'bulletBorderThickness': 1, 'hideBulletsCount': 30, 'title': 'Topic6', 'valueField': '6', 'fillAlphas': 0}, {'id': 'g7', 'valueAxis': ' ', 'lineColor': '#46f0f0', 'bullet': 'round', 'bulletBorderThickness': 1, 'hideBulletsCount': 30, 'title': 'Topic7', 'valueField': '7', 'fillAlphas': 0}, {'id': 'g8', 'valueAxis': ' ', 'lineColor': '#f032e6', 'bullet': 'round', 'bulletBorderThickness': 1, 'hideBulletsCount': 30, 'title': 'Topic8', 'valueField': '8', 'fillAlphas': 0}, {'id': 'g9', 'valueAxis': ' ', 'lineColor': '#d2f53c', 'bullet': 'round', 'bulletBorderThickness': 1, 'hideBulletsCount': 30, 'title': 'Topic9', 'valueField': '9', 'fillAlphas': 0}];
  graph_data[10] = [{'id': 'g', 'valueAxis': ' ', 'lineColor': '#808080', 'bullet': 'round', 'bulletBorderThickness': 1, 'hideBulletsCount': 30, 'title': 'Total', 'valueField': '0', 'fillAlphas': 0}, {'id': 'g1', 'valueAxis': ' ', 'lineColor': '#e6194b', 'bullet': 'round', 'bulletBorderThickness': 1, 'hideBulletsCount': 30, 'title': 'Topic1', 'valueField': '1', 'fillAlphas': 0}, {'id': 'g2', 'valueAxis': ' ', 'lineColor': '#3cb44b', 'bullet': 'round', 'bulletBorderThickness': 1, 'hideBulletsCount': 30, 'title': 'Topic2', 'valueField': '2', 'fillAlphas': 0}, {'id': 'g3', 'valueAxis': ' ', 'lineColor': '#ffe119', 'bullet': 'round', 'bulletBorderThickness': 1, 'hideBulletsCount': 30, 'title': 'Topic3', 'valueField': '3', 'fillAlphas': 0}, {'id': 'g4', 'valueAxis': ' ', 'lineColor': '#0082c8', 'bullet': 'round', 'bulletBorderThickness': 1, 'hideBulletsCount': 30, 'title': 'Topic4', 'valueField': '4', 'fillAlphas': 0}, {'id': 'g5', 'valueAxis': ' ', 'lineColor': '#f58231', 'bullet': 'round', 'bulletBorderThickness': 1, 'hideBulletsCount': 30, 'title': 'Topic5', 'valueField': '5', 'fillAlphas': 0}, {'id': 'g6', 'valueAxis': ' ', 'lineColor': '#911eb4', 'bullet': 'round', 'bulletBorderThickness': 1, 'hideBulletsCount': 30, 'title': 'Topic6', 'valueField': '6', 'fillAlphas': 0}, {'id': 'g7', 'valueAxis': ' ', 'lineColor': '#46f0f0', 'bullet': 'round', 'bulletBorderThickness': 1, 'hideBulletsCount': 30, 'title': 'Topic7', 'valueField': '7', 'fillAlphas': 0}, {'id': 'g8', 'valueAxis': ' ', 'lineColor': '#f032e6', 'bullet': 'round', 'bulletBorderThickness': 1, 'hideBulletsCount': 30, 'title': 'Topic8', 'valueField': '8', 'fillAlphas': 0}, {'id': 'g9', 'valueAxis': ' ', 'lineColor': '#d2f53c', 'bullet': 'round', 'bulletBorderThickness': 1, 'hideBulletsCount': 30, 'title': 'Topic9', 'valueField': '9', 'fillAlphas': 0}, {'id': 'g10', 'valueAxis': ' ', 'lineColor': '#fabebe', 'bullet': 'round', 'bulletBorderThickness': 1, 'hideBulletsCount': 30, 'title': 'Topic10', 'valueField': '10', 'fillAlphas': 0}];




  var s_data = series_data[k];
  var g_data = graph_data[k];


  var chart = AmCharts.makeChart("chartdiv", {
      "hideCredits":true,
      "type": "serial",
      "theme": "light",
      "legend": {
          "position": "right",
          "useGraphSettings": true
      },
      "dataProvider": s_data,
      "synchronizeGrid":true,
      "valueAxes": [{

          "axisColor": "",
          "axisThickness": 2,
          "axisAlpha": 1,
          "position": "left"
      }],
      "graphs": g_data,
      "chartScrollbar": {
        "autoGridCount": true,
        "graph": "g",
        "scrollbarHeight": 40

      },
      "chartCursor": {
          "cursorPosition": "mouse"
      },
      "categoryField": 'date',
      "categoryAxis": {
          "parseDates": true,
          "axisColor": "#DADADA",
          "minorGridEnabled": true
      },
      "export": {
      	"enabled": true,
          "position": "bottom-right"
       }
  });



  chart.addListener("dataUpdated", zoomChart);
  zoomChart();



  function zoomChart(){
      chart.zoomToIndexes(chart.dataProvider.length - 20, chart.dataProvider.length - 1);
  }
}
