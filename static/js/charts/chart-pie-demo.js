// Check if the score is null
if (score === null) {
    colors = ['#bfbfbf']; // Gray color for no data
    content = "NA";       // Display "NA" if score is null
} else if (score >= 1 && score <= 2) {
    colors = ['#f8001f'];
    content = "HIGHRISK";  // Red for 0-2
} else if (score >= 3 && score <= 4) {
    colors = ['#fb7300'];
    content = "CHALLENGING";   // Orange for 3-4
} else if (score >= 5 && score <= 6) {
    colors = ['#f3aa11']; 
    content = "RELIABLE";  // Yellow for 5-6
} else if (score >= 7 && score <= 8) {
    colors = ['#b3bf00']; 
    content = "POSITIVE";  // Blue for 7
} else if (score >= 9 && score <= 10) {
    colors = ['#66a44a'];
    content = "OUTSTANDING";   // Green for 8
} else {
    colors = ['#000000'];
    content = "NA"; // Handle any unexpected values
}

// Apply the circle color
document.getElementById('scoreCircle').style.backgroundColor = colors;
document.getElementById('scoreCircle').textContent = content;

// Define the data for the pie chart using the score
var ctx = document.getElementById("myPieChart");
var myPieChart = new Chart(ctx, {
    type: 'doughnut',
    data: {
        labels: Array(8).fill(content), // Use the same content for all labels
        datasets: [{
            data: Array(score).fill(1).concat(Array(8 - score).fill(1)), // Creates an array with 'score' filled segments and '8-score' empty segments
            backgroundColor: Array(score).fill(colors).concat(Array(score).fill('#e0e0e0')), // Filled parts are blue, remaining are gray
            hoverBackgroundColor: Array(score).fill(colors).concat(Array(8 - score).fill('#bfbfbf')),
            hoverBorderColor: "rgba(234, 236, 244, 1)",
        }],
    },
    options: {
        maintainAspectRatio: false,
        tooltips: {
            backgroundColor: "rgb(255,255,255)",
            bodyFontColor: "#858796",
            borderColor: '#dddfeb',
            borderWidth: 1,
            xPadding: 15,
            yPadding: 15,
            displayColors: false,
            caretPadding: 10,
        },
        legend: {
            display: false
        },
        cutoutPercentage: 80,
    },
    plugins: [{
        afterDraw: function(chart) {
            var width = chart.chart.width,
                height = chart.chart.height,
                ctx = chart.chart.ctx;

            ctx.restore();
            var fontSize = (height / 114).toFixed(2); // Adjusted font size
            ctx.font = fontSize + "em Nunito";
            ctx.textBaseline = "middle";
            ctx.fillStyle = colors; // Set the text color

            var text = score !== null ? score : "NA", // Show "NA" if score is null
                textX = Math.round((width - ctx.measureText(text).width) / 2),
                textY = height / 2;

            ctx.fillText(text, textX, textY);

            ctx.font = (fontSize * 0.5) + "em Nunito";  // Smaller font for mobile number
            var mobileText = score === null ? "NA" : mobileNumber, // Show "NA" if score is null
                mobileTextX = Math.round((width - ctx.measureText(mobileText).width) / 2),
                mobileTextY = height / 2 + 30;

            ctx.fillText(mobileText, mobileTextX, mobileTextY);

            ctx.save();
        }
    }]
});
