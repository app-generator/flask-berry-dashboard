'use strict';

document.addEventListener('DOMContentLoaded', function () {
  setTimeout(function () {
    floatchart();
  }, 500);
});

// var testVar = document.getElementById("fcast_sales").innerHTML; /* get testVar for chart from html */
// refactor below to lookup number of coststreams forecasted
let fcast_vals_raw_1 = document.getElementById("fcast_vals_raw_1").innerHTML; /* get coststream1 forecast values for chart from index.html */
let fcast_vals_raw_2 = document.getElementById("fcast_vals_raw_2").innerHTML; /* get coststream2 forecast values for chart from index.html */
let fcast_vals_raw_3 = document.getElementById("fcast_vals_raw_3").innerHTML; /* get coststream1 forecast values for chart from index.html */
let fcast_vals_raw_4 = document.getElementById("fcast_vals_raw_4").innerHTML; /* get coststream2 forecast values for chart from index.html */
let fcast_vals_raw_5 = document.getElementById("fcast_vals_raw_5").innerHTML; /* get coststream1 forecast values for chart from index.html */

let fcast_dates_raw = document.getElementById("fcast_dates").innerHTML; 

// let newData = []

// This is correct
// if (Array.isArray(forecast_vals_raw)) {
//   newData = forecast_vals_raw.map(item => {
//            return item 
//          });
//   }

// unhide forecast chart div if forecast(fcast_vals_raw) is returned
if (fcast_vals_raw_1 != '') {
    document.getElementById("forecast_chart").style.display = 'block'; 
    }


  // *check* use forecast_vals - and add a note how this works by getting the numbers from the string received from python (session variable) into the .js arrary needed for apexcharts
  // see else.g. for regex https://stackoverflow.com/questions/16096467/how-to-extract-array-of-numbers-from-string-in-javascript
var fcast_vals_1 = fcast_vals_raw_1.match(/-?\d+/g);
var fcast_vals_2 = fcast_vals_raw_2.match(/-?\d+/g);
var fcast_vals_3 = fcast_vals_raw_3.match(/-?\d+/g);
var fcast_vals_4 = fcast_vals_raw_4.match(/-?\d+/g);
var fcast_vals_5 = fcast_vals_raw_5.match(/-?\d+/g);
var fcast_dates = eval(fcast_dates_raw);

// debug
console.log(fcast_vals_raw_1)
console.log(typeof fcast_vals_raw_1)
console.log(fcast_vals_1)
console.log(typeof fcast_vals_1)
console.log(fcast_dates_raw)
console.log(typeof fcast_dates_raw)
console.log(fcast_dates)
console.log(typeof fcast_dates)
// console.log(newData) 

function floatchart() {
  (function () {
    var options = {
      chart: {
        type: 'line',
        height: 90,
        sparkline: {
          enabled: true
        }
      },
      dataLabels: {
        enabled: false
      },
      colors: ['#FFF'],
      stroke: {
        curve: 'smooth',
        width: 3
      },
      series: [
        {
          name: 'series1',
          data: [45, 66, 41, 89, 25, 44, 9, 54]
        }
      ],
      yaxis: {
        min: 5,
        max: 95
      },
      tooltip: {
        theme: 'dark',
        fixed: {
          enabled: false
        },
        x: {
          show: false
        },
        y: {
          title: {
            formatter: function (seriesName) {
              return 'Total Earning';
            }
          }
        },
        marker: {
          show: false
        }
      }
    };
    var chart = new ApexCharts(document.querySelector('#tab-chart-1'), options);
    chart.render();
  })();
  (function () {
    var options = {
      chart: {
        type: 'line',
        height: 90,
        sparkline: {
          enabled: true
        }
      },
      dataLabels: {
        enabled: false
      },
      colors: ['#FFF'],
      stroke: {
        curve: 'smooth',
        width: 3
      },
      series: [
        {
          name: 'series1',
          data: [35, 44, 9, 54, 45, 66, 41, 69]
        }
      ],
      yaxis: {
        min: 5,
        max: 95
      },
      tooltip: {
        theme: 'dark',
        fixed: {
          enabled: false
        },
        x: {
          show: false
        },
        y: {
          title: {
            formatter: function (seriesName) {
              return 'Total Earning';
            }
          }
        },
        marker: {
          show: false
        }
      }
    };
    var chart = new ApexCharts(document.querySelector('#tab-chart-2'), options);
    chart.render();
  })();
  (function () {
    var options = {
      chart: {
        type: 'bar',
        height: 480,
        stacked: true,
        toolbar: {
          show: false
        }
      },
      plotOptions: {
        bar: {
          horizontal: false,
          columnWidth: '50%'
        }
      },
      dataLabels: {
        enabled: false
      },
      colors: ['#d3eafd', '#2196f3', '#673ab7', '#e1d8f1'],
      series: [
        // {
        //   name: 'Investment',
        //   data: [35, 125, 35, 35, 35, 80, 35, 20, 35, 45, 15, 75]
        // },
        {
          name: 'coststream 1', // previously Loss
          // data: $.ajax({
          //   type: "GET",
          //   url: '/chart_salesfc',
          //   success: function(resp){ }

          // data: lossData

          // data: [testVar, 15, 15, 35, 65, 40, 80, 25, 15, 85, 25, 75]
          data: fcast_vals_1
        // })
        },
        // {
        //   name: 'coststream 2',
        //   data: fcast_vals_2 /* [35, 145, 35, 35, 20, 105, 100, 10, 65, 45, 30, 10] */
        // },
        // {
        //   name: 'Maintenance',
        //   data: [0, 0, 75, 0, 0, 115, 0, 0, 0, 0, 150, 0]
        // }
      ],
      responsive: [
        {
          breakpoint: 480,
          options: {
            legend: {
              position: 'bottom',
              offsetX: -10,
              offsetY: 0
            }
          }
        }
      ],
      xaxis: {
        type: 'category',
        // categories: ['Mon', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        categories: fcast_dates
      },
      grid: {
        strokeDashArray: 4
      },
      tooltip: {
        theme: 'dark'
      }
    };
    var chart = new ApexCharts(document.querySelector('#growthchart'), options);
    chart.render();

    // only show additional coststream series if available
    // NB this was a nightmare - dont use updateSeries or appendSeries, need to use updateOptions
    // after that added incremental code additions for each codestream and asked copilot to refactor
    let series = [{
      name: 'coststream 1',
      data: fcast_vals_1
    }];
    
    if (fcast_vals_2 != null) {
      series.push({
        name: 'coststream 2',
        data: fcast_vals_2
      });
    }
    
    if (fcast_vals_3 != null) {
      series.push({
        name: 'coststream 3',
        data: fcast_vals_3
      });
    }

    if (fcast_vals_4 != null) {
      series.push({
        name: 'coststream 4',
        data: fcast_vals_4
      });
    }

    if (fcast_vals_5 != null) {
      series.push({
        name: 'coststream 5',
        data: fcast_vals_5
      });
    }
    
    chart.updateOptions({
      series: series
    });


  })();
  (function () {
    var options = {
      chart: {
        type: 'area',
        height: 95,
        stacked: true,
        sparkline: {
          enabled: true
        }
      },
      colors: ['#673ab7'],
      stroke: {
        curve: 'smooth',
        width: 1
      },
      series: [
        {
          data: [0, 15, 10, 50, 30, 40, 25]
        }
      ]
    };
    var chart = new ApexCharts(document.querySelector('#bajajchart'), options);
    chart.render();
  })();
}
