
var months = months

var monthNames = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];

// Extract the month numbers from the months object and map them to month names
var monthLabels = [
    monthNames[months.month_1 - 1],
    monthNames[months.month_2 - 1],
    monthNames[months.month_3 - 1],
    monthNames[months.month_4 - 1],
    monthNames[months.month_5 - 1],
    monthNames[months.month_6 - 1]
].reverse();


// console.log(months)
var msisdn = chartData.msisdn;
var data = [
    chartData.month_1,
    chartData.month_2,
    chartData.month_3,
    chartData.month_4,
    chartData.month_5,
    chartData.month_6
].reverse();

// Use this data array to populate the area chart
var ctx = document.getElementById("myAreaChart");
var myLineChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: monthLabels,
        datasets: [{
            label: msisdn,
            data: data,
            lineTension: 0.3,
            backgroundColor: "rgba(78, 115, 223, 0.05)",
            borderColor: colors,
            pointRadius: 3,
            pointBackgroundColor: colors,
            pointBorderColor: colors,
            pointHoverRadius: 3,
            pointHoverBackgroundColor: colors,
            pointHoverBorderColor: colors,
            pointHitRadius: 10,
            pointBorderWidth: 2,
        }],
    },
    options: {
        maintainAspectRatio: false,
        scales: {
            xAxes: [{
              gridLines: {
                display: false,
                drawBorder: false
              },
            }],
            yAxes: [{
                ticks: {
                    min: 0,    // Set minimum value for Y-axis
                    max: 10,   // Set maximum value for Y-axis
                    stepSize: 1 // Optional: set the step size between ticks
                  },
              gridLines: {
                color: "rgb(234, 236, 244)",
                zeroLineColor: "rgb(234, 236, 244)",
                drawBorder: false,
                borderDash: [2],
                zeroLineBorderDash: [2]
              }
            }],
          },
          legend: {
            display: false
          },
    }
});

function updateChart() {
    var selectedValue = document.getElementById("dateRange").value;
    var data = [
        chartData.month_6,
        chartData.month_2,
        chartData.month_3,
        chartData.month_4,
        chartData.month_5,
        chartData.month_1
    ];

    var filteredData = [];
    var labels = monthLabels; // Use the actual month names here
    var filteredLabels = [];

    // Determine the range based on the selected option
    switch (selectedValue) {
        case "all":
            filteredData = data;  // Get all months data
            filteredLabels = labels;
            break;
        case "1": // Last Month
            filteredData = data.slice(-1); // Get last 1 month data
            filteredLabels = labels.slice(-1);
            break;
        case "2": // Last 2 Months
            filteredData = data.slice(-2); // Get last 2 months data
            filteredLabels = labels.slice(-2);
            break;
        case "3": // Last 3 Months
            filteredData = data.slice(-3); // Get last 3 months data
            filteredLabels = labels.slice(-3);
            break;
        case "4": // Last 4 Months
            filteredData = data.slice(-4); // Get last 4 months data
            filteredLabels = labels.slice(-4);
            break;
        case "5": // Last 5 Months
            filteredData = data.slice(-5); // Get last 5 months data
            filteredLabels = labels.slice(-5);
            break;
        default: // Last 6 Months (or if no match)
            filteredData = data;  // Get all months data
            filteredLabels = labels;
            break;
    }

    // Update the chart with the filtered data and labels
    myLineChart.data.labels = filteredLabels;
    myLineChart.data.datasets[0].data = filteredData;
    myLineChart.update();
}


