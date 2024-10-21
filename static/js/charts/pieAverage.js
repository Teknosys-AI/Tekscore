

  var ctx2av = document.getElementById('myPieChart2').getContext('2d');
var score = 5; // Example score
var average_value = 5; // Example average value

var colorsav = '#fb7300'; // Default color
var emptyColorav = '#e0e0e0';
var dataav = Array(8).fill(emptyColorav); // Start with all segments empty
var average_valuecolorsav = '#f8001f';
var average_valuecontent = "NA";


document.addEventListener('DOMContentLoaded', function() {
    var scoreCircle2 = document.getElementById('scoreCircle2');
    if (scoreCircle2) {


        if (average_value === null) {
            average_valuecolorsav = '#bfbfbf'; // Gray color for no data
            average_valuecontent = "NA";  
        } else if (average_value >= 0 && average_value <= 2) { // Corrected logic
            average_valuecolorsav = '#f8001f'; // Red for 0-2
            average_valuecontent = "HIGHRISK";  
        } else if (average_value >= 3 && average_value <= 4) { // Corrected logic
            average_valuecolorsav = '#fb7300'; // Orange for 3-4
            average_valuecontent = "CHALLENGING";  
        } else if (average_value >= 5 && average_value <= 6) { // Corrected logic
            average_valuecolorsav = '#f3aa11'; // Yellow for 5-6
            average_valuecontent = "RELIABLE";  
        } else if (average_value >= 7 && average_value <= 8) { // Corrected logic
            average_valuecolorsav = '#b3bf00'; // Blue for 7-8
            average_valuecontent = "POSITIVE";  
        } else if (average_value >= 9 && average_value <= 10) { // Corrected logic
            average_valuecolorsav = '#66a44a'; // Green for 9-10
            average_valuecontent = "OUTSTANDING";  
        } else {
            average_valuecolorsav = '#000000';
            average_valuecontent = "NA"; // Handle any unexpected values
        }

        scoreCircle2.style.backgroundColor = average_valuecolorsav;
        scoreCircle2.textContent = average_valuecontent;

        if (dyncolor) {
            dyncolor.style.color = colors;
        } else {
            console.warn('Element with ID "dyncolor" not found');
        }



        

//added inside
var myPieChart2 = new Chart(ctx2av, {
    type: 'doughnut',
    data: {
        labels: Array(8).fill(''), // Empty labels to avoid clutter
        datasets: [{
            data: Array(average_value).fill(1).concat(Array(8 - average_value).fill(1)), // Fill segments
            backgroundColor: Array(average_value).fill(average_valuecontent).concat(Array(8 - average_value).fill(emptyColorav)), // Filled segments colored, rest empty
            hoverBackgroundColor: Array(average_value).fill(average_valuecontent).concat(Array(8 - average_value).fill('#bfbfbf')),
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
            displaycolorsav: false,
            caretPadding: 10,
        },
        legend: {
            display: false
        },
        responsive: true,
        cutoutPercentage: 80, // Increase this value to make the chart thinner
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
            ctx.fillStyle = average_valuecolorsav; // Set the text color
            if (width < 150) { // You can adjust the threshold value
                fontSize = (height / 70).toFixed(2);
                ctx.font = fontSize + "em Nunito";
            }

            var text = average_value, // Show content based on average value
                textX = Math.round((width - ctx.measureText(text).width) / 2),
                textY = height / 2;

            ctx.fillText(text, textX, textY);
            ctx.save();
        }
    }]
});




    } else {
        console.warn('Element with ID "scoreCircle2" not found');
    }

    var dyncolor = document.getElementById('dyncolor');
    if (dyncolor) {
        dyncolor.style.color = colorsav;
    } else {
        console.warn('Element with ID "dyncolor" not found');
    }
});

for (let i = 0; i < score; i++) {
    dataav[i] = colorsav; // Fill the segments based on the score
}


