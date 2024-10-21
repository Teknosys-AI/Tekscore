var ctx2 = document.getElementById('myPieChart2').getContext('2d');
var score = 1;
var highest_value = 8;      
var lowest_value = 2;
var high_color = '#b3bf00';
var low_color = '#f8001f';
var colors = '#fb7300';
var emptyColor = '#e0e0e0';
var data = Array(8).fill(emptyColor); // Start with all segments empty
var average_valuecolors = '#e0e0e0';
var average_valuecontent = "NA";
var highest_valuecontent ="NA";
var lowest_valuecontent ="NA";





var ctx3 = document.getElementById('myPieChart3').getContext('2d');
document.addEventListener('DOMContentLoaded', function() {
    var scoreCircle3 = document.getElementById('scoreCircle3');
    
    if (scoreCircle3) {
        if (highest_value === null) {
            high_color = '#bfbfbf'; // Gray color for no data
            highest_valuecontent = "NA";  
        } else if (highest_value >= 0 && highest_value <= 2) { // Corrected logic
            high_color = '#f8001f'; // Red for 0-2
            highest_valuecontent = "HIGHRISK";  
        } else if (highest_value >= 3 && highest_value <= 4) { // Corrected logic
            high_color = '#fb7300'; // Orange for 3-4
            highest_valuecontent = "CHALLENGING";  
        } else if (highest_value >= 5 && highest_value <= 6) { // Corrected logic
            high_color = '#f3aa11'; // Yellow for 5-6
            highest_valuecontent = "RELIABLE";  
        } else if (highest_value >= 7 && highest_value <= 8) { // Corrected logic
            high_color = '#b3bf00'; // Blue for 7-8
            highest_valuecontent = "POSITIVE";  
        } else if (highest_value >= 9 && highest_value <= 10) { // Corrected logic
            high_color = '#66a44a'; // Green for 9-10
            highest_valuecontent = "OUTSTANDING";  
        } else {
            high_color = '#000000';
            highest_valuecontent = "NA"; // Handle any unexpected values
        }





        scoreCircle3.style.backgroundColor = high_color;
        scoreCircle3.textContent = highest_valuecontent;
		var myPieChart3 = new Chart(ctx3, {
    type: 'doughnut',
    data: {
        labels: Array(8).fill(content),

        datasets: [{
            data: Array(highest_value).fill(1).concat(Array(8 - highest_value).fill(1)), // Creates an array with 'score' filled segments and '8-score' empty segments
            backgroundColor: Array(highest_value).fill(high_color).concat(Array(score).fill('#e0e0e0')), // Filled parts are blue, remaining are gray
            hoverBackgroundColor: Array(score).fill(high_color).concat(Array(8 - score).fill('#bfbfbf')),
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
            ctx.fillStyle = high_color; // Set the text color
            if (width < 150) { // You can adjust the threshold value
                fontSize = (height / 70).toFixed(2);
                ctx.font = fontSize + "em Nunito";
            }
    
            var text = score !== null ? highest_value : "NA", // Show "NA" if score is null
                textX = Math.round((width - ctx.measureText(text).width) / 2),
                textY = height / 2;
    
            ctx.fillText(text, textX, textY);
    
           
    
            ctx.save();
        }
    }]
});


    } else {
        console.warn('Element with ID "scoreCircle3" not found');
    }
});




var ctx4 = document.getElementById('myPieChart4').getContext('2d');
document.addEventListener('DOMContentLoaded', function() {
    var scoreCircle4 = document.getElementById('scoreCircle4');
    

        if (scoreCircle4) {
            if (lowest_value === null) {
                low_color = '#bfbfbf'; // Gray color for no data
                lowest_valuecontent = "NA";  
            } else if (lowest_value >= 0 && lowest_value <= 2) { // Corrected logic
                low_color = '#f8001f'; // Red for 0-2
                lowest_valuecontent = "HIGHRISK";  
            } else if (lowest_value >= 3 && lowest_value <= 4) { // Corrected logic
                low_color = '#fb7300'; // Orange for 3-4
                lowest_valuecontent = "CHALLENGING";  
            } else if (lowest_value >= 5 && lowest_value <= 6) { // Corrected logic
                low_color = '#f3aa11'; // Yellow for 5-6
                lowest_valuecontent = "RELIABLE";  
            } else if (lowest_value >= 7 && lowest_value <= 8) { // Corrected logic
                low_color = '#b3bf00'; // Blue for 7-8
                lowest_valuecontent = "POSITIVE";  
            } else if (lowest_value >= 9 && lowest_value <= 10) { // Corrected logic
                low_color = '#66a44a'; // Green for 9-10
                lowest_valuecontent = "OUTSTANDING";  
            } else {
                low_color = '#000000';
                lowest_valuecontent = "NA"; // Handle any unexpected values
            }

            

        scoreCircle4.style.backgroundColor = low_color;
        scoreCircle4.textContent = lowest_valuecontent;
		var myPieChart4 = new Chart(ctx4, {
    type: 'doughnut',
    data: {
        labels: Array(8).fill(content),
        // datasets: [{
        //     data: [200, 100, 50],
        //     backgroundColor: ['#4CAF50', '#9C27B0', '#FF9800'],
        // }]

        datasets: [{
            data: Array(lowest_value).fill(1).concat(Array(8 - lowest_value).fill(1)), // Creates an array with 'score' filled segments and '8-score' empty segments
            backgroundColor: Array(lowest_value).fill(low_color).concat(Array(lowest_value).fill('#e0e0e0')), // Filled parts are blue, remaining are gray
            hoverBackgroundColor: Array(lowest_value).fill(low_color).concat(Array(8 - lowest_value).fill('#bfbfbf')),
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
            ctx.fillStyle = low_color; // Set the text color
            if (width < 150) { // You can adjust the threshold value
                fontSize = (height / 70).toFixed(2);
                ctx.font = fontSize + "em Nunito";
            }
    
            var text = score !== null ? lowest_value : "NA", // Show "NA" if score is null
                textX = Math.round((width - ctx.measureText(text).width) / 2),
                textY = height / 2;
    
            ctx.fillText(text, textX, textY);
    
           
    
            ctx.save();
        }
    }]
});
    } else {
        console.warn('Element with ID "scoreCircle" not found');
    }
});
