var ctx = document.getElementById("myAreaChart");
var myLineChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: [], // Start with an empty labels array
        datasets: [{
            label: "Earnings",
            lineTension: 0.3,
            backgroundColor: "rgba(78, 115, 223, 0.05)",
            borderColor: "rgba(78, 115, 223, 1)",
            pointRadius: 3,
            pointBackgroundColor: "rgba(78, 115, 223, 1)",
            pointBorderColor: "rgba(78, 115, 223, 1)",
            pointHoverRadius: 3,
            pointHoverBackgroundColor: "rgba(78, 115, 223, 1)",
            pointHoverBorderColor: "rgba(78, 115, 223, 1)",
            pointHitRadius: 10,
            pointBorderWidth: 2,
            data: [], // Start with an empty data array
        }],
    },
    options: {
        maintainAspectRatio: false,
        // ... other options
    }
});

// Function to update the chart based on the selected date range
function updateChart() {
    var dateRange = document.getElementById("dateRange").value;
    var labels = [];
    var data = [];

    // Generate data based on the selected date range
    if (dateRange === "all") {
        // Example data for all time (replace with your actual data)
        labels = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
        data = [0, 10000, 5000, 15000, 10000, 20000, 15000, 25000, 20000, 30000, 25000, 40000];
    } else {
        // Generate labels and data for the last X days
        var days = parseInt(dateRange);
        for (var i = 0; i < days; i++) {
            labels.push("Day " + (days - i)); // Labels for last X days
            data.push(Math.floor(Math.random() * 50000)); // Random data for demonstration (replace with your actual data)
        }
    }

    // Update the chart data
    myLineChart.data.labels = labels;
    myLineChart.data.datasets[0].data = data;
    myLineChart.update();
}

// Initialize the chart with default data
updateChart();
