var ctx2 = document.getElementById('myPieChart2').getContext('2d');
var score = 1;
var colors = '#fb7300'
var emptyColor = '#e0e0e0';
var data = Array(8).fill(emptyColor); // Start with all segments empty


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


for (let i = 0; i < score; i++) {
    data[i] = colors; // Fill the segments based on the score
}
var myPieChart2 = new Chart(ctx2, {
    type: 'doughnut',
    data: {
        labels: Array(8).fill(content),
        // datasets: [{
        //     data: [200, 100, 50],
        //     backgroundColor: ['#4CAF50', '#9C27B0', '#FF9800'],
        // }]

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
        responsive: true,
        cutoutPercentage: 80, // Increase this value to make the chart thinner
    }
});