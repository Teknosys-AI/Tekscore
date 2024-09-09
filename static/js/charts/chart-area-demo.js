// // Assuming `score` is defined somewhere above and contains the score value
// var colors;
// var content;

// if (score === null) {
//     colors = '#bfbfbf'; // Gray color for no data
//     content = "NA";       // Display "NA" if score is null
// } else if (score >= 1 && score <= 2) {
//     colors = '#f8001f';
//     content = "HIGHRISK";  // Red for 0-2
// } else if (score >= 3 && score <= 4) {
//     colors = '#fb7300';
//     content = "CHALLENGING";   // Orange for 3-4
// } else if (score >= 5 && score <= 6) {
//     colors = '#f3aa11'; 
//     content = "RELIABLE";  // Yellow for 5-6
// } else if (score >= 7 && score <= 8) {
//     colors = '#b3bf00'; 
//     content = "POSITIVE";  // Blue for 7-8
// } else if (score >= 9 && score <= 10) {
//     colors = '#66a44a';
//     content = "OUTSTANDING";   // Green for 9-10
// } else {
//     colors = '#000000';
//     content = "NA"; // Handle any unexpected values
// }

// var ctx = document.getElementById("myAreaChart");
// var myLineChart = new Chart(ctx, {
//     type: 'line',
//     data: {
//         labels: [], // Start with an empty labels array
//         datasets: [{
//             label: "Earnings",
//             lineTension: 0.3,
//             backgroundColor: "rgba(78, 115, 223, 0.05)",
//             borderColor: colors,
//             pointRadius: 3,
//             pointBackgroundColor: colors,
//             pointBorderColor: colors,
//             pointHoverRadius: 3,
//             pointHoverBackgroundColor: colors,
//             pointHoverBorderColor: colors,
//             pointHitRadius: 10,
//             pointBorderWidth: 2,
//             data: [], // Start with an empty data array
//         }],
//     },
//     options: {
//         maintainAspectRatio: false,
//         scales: {
//             xAxes: [{
//               gridLines: {
//                 display: false,
//                 drawBorder: false
//               },
//             }],
//             yAxes: [{
//               gridLines: {
//                 color: "rgb(234, 236, 244)",
//                 zeroLineColor: "rgb(234, 236, 244)",
//                 drawBorder: false,
//                 borderDash: [2],
//                 zeroLineBorderDash: [2]
//               }
//             }],
//           },
//           legend: {
//             display: false
//           },
//     }
// });

// // Function to update the chart based on the selected date range
// function updateChart() {
//     var dateRange = document.getElementById("dateRange").value;
//     var labels = [];
//     var data = [];

//     // Generate data based on the selected date range
//     if (dateRange === "all") {
//         // Example data for all time (replace with your actual data)
//         labels = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
//         data = [0, 10000, 5000, 15000, 10000, 20000, 15000, 25000, 20000, 30000, 25000, 40000];
//     } else {
//         // Generate labels and data for the last X days
//         var days = parseInt(dateRange);
//         for (var i = 0; i < days; i++) {
//             labels.push("Day " + (days - i)); // Labels for last X days
//             data.push(Math.floor(Math.random() * 50000)); // Random data for demonstration (replace with your actual data)
//         }
//     }

//     // Update the chart data
//     myLineChart.data.labels = labels;
//     myLineChart.data.datasets[0].data = data;
//     myLineChart.update();
// }

// // Initialize the chart with default data
// updateChart();
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
];


// console.log(months)
var msisdn = chartData.msisdn;
var data = [
    chartData.month_1,
    chartData.month_2,
    chartData.month_3,
    chartData.month_4,
    chartData.month_5,
    chartData.month_6
];

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
        chartData.month_1,
        chartData.month_2,
        chartData.month_3,
        chartData.month_4,
        chartData.month_5,
        chartData.month_6
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


