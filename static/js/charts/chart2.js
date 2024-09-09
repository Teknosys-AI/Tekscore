var ctx2 = document.getElementById('myPieChart2').getContext('2d');
var score = 1;
var average_value=1;
var highest_value = 0;      
var lowest_value = 0;
var colors = '#fb7300';
var emptyColor = '#e0e0e0';
var data = Array(8).fill(emptyColor); // Start with all segments empty
var average_valuecolors = '#e0e0e0';
var average_valuecontent = "NA";


// if (score === null) {
//     colors = ['#bfbfbf']; // Gray color for no data
//     content = "NA";       // Display "NA" if score is null
// } else if (score >= 1 && score <= 2) {
//     colors = ['#f8001f'];
//     content = "HIGHRISK";  // Red for 0-2
// } else if (score >= 3 && score <= 4) {
//     colors = ['#fb7300'];
//     content = "CHALLENGING";   // Orange for 3-4
// } else if (score >= 5 && score <= 6) {
//     colors = ['#f3aa11']; 
//     content = "RELIABLE";  // Yellow for 5-6
// } else if (score >= 7 && score <= 8) {
//     colors = ['#b3bf00']; 
//     content = "POSITIVE";  // Blue for 7
// } else if (score >= 9 && score <= 10) {
//     colors = ['#66a44a'];
//     content = "OUTSTANDING";   // Green for 8
// } else {
//     colors = ['#000000'];
//     content = "NA"; // Handle any unexpected values
// }




// if (average_value === null) {
//     average_valuecolors = '#bfbfbf'; // Gray color for no data
//     average_valuecontent = "NA";  
// console.log("average: "+average_value)
// // Display "NA" if score is null
// } else if (average_value >= 0 && score <= 2) {
//     average_valuecolors = '#f8001f';
//     average_valuecontent = "HIGHRISK";  // Red for 0-2
// console.log("average: "+average_value)

// } else if (average_value >= 3 && score <= 4) {
//     average_valuecolors = '#fb7300';
//     average_valuecontent = "CHALLENGING";   // Orange for 3-4
// console.log("average: "+average_value)

// } else if (average_value >= 5 && score <= 6) {
//     average_valuecolors = '#f3aa11'; 
//     average_valuecontent = "RELIABLE";  // Yellow for 5-6
// console.log("average: "+average_value)

// } else if (average_value >= 7 && score <= 8) {
//     average_valuecolors = '#b3bf00'; 
//     average_valuecontent = "POSITIVE";  // Blue for 7
// console.log("average: "+average_value)

// } else if (average_value >= 9 && score <= 10) {
//     average_valuecolors = '#66a44a';
//     average_valuecontent = "OUTSTANDING";   // Green for 8
// console.log("average: "+average_value)

// } else {
//     average_valuecolors = '#000000';
//     average_valuecontent = "NA"; // Handle any unexpected values
// }

// document.addEventListener('DOMContentLoaded', function() {

//     var scoreCircle2 = document.getElementById('scoreCircle2');
    
//     if (scoreCircle2) {
//         scoreCircle2.style.backgroundColor = average_valuecolors;
//         scoreCircle2.textContent = average_valuecontent;
//     } else {
//         console.warn('Element with ID "scoreCircle2" not found');
//     }

    
// });
// document.addEventListener('DOMContentLoaded', function() {
//     var dyncolor = document.getElementById('dyncolor');
    
//     if (dyncolor) {
//         dyncolor.style.color = colors;
//     } else {
//         console.warn('Element with ID "dyncolor" not found');
//     }
// });

// for (let i = 0; i < score; i++) {
//     data[i] = colors; // Fill the segments based on the score
// }
// var myPieChart2 = new Chart(ctx2, {
//     type: 'doughnut',
//     data: {
//         labels: Array(8).fill(average_value),
//         // datasets: [{
//         //     data: [200, 100, 50],
//         //     backgroundColor: ['#4CAF50', '#9C27B0', '#FF9800'],
//         // }]

//         datasets: [{
//             data: Array(average_value).fill(1).concat(Array(8 - average_value).fill(1)), // Creates an array with 'score' filled segments and '8-score' empty segments
//             backgroundColor: Array(average_value).fill(colors).concat(Array(average_value).fill('#e0e0e0')), // Filled parts are blue, remaining are gray
//             hoverBackgroundColor: Array(average_value).fill(colors).concat(Array(8 - average_value).fill('#bfbfbf')),
//             hoverBorderColor: "rgba(234, 236, 244, 1)",
//         }],
//     },
//     options: {
//         maintainAspectRatio: false,
//         tooltips: {
//             backgroundColor: "rgb(255,255,255)",
//             bodyFontColor: "#858796",
//             borderColor: '#dddfeb',
//             borderWidth: 1,
//             xPadding: 15,
//             yPadding: 15,
//             displayColors: false,
//             caretPadding: 10,
//         },
//         legend: {
//             display: false
//         },
//         responsive: true,
//         cutoutPercentage: 80, // Increase this value to make the chart thinner
//     },
//     plugins: [{
//         afterDraw: function(chart) {
//             var width = chart.chart.width,
//                 height = chart.chart.height,
//                 ctx = chart.chart.ctx;
    
//             ctx.restore();
//             var fontSize = (height / 114).toFixed(2); // Adjusted font size
//             ctx.font = fontSize + "em Nunito";
//             ctx.textBaseline = "middle";
//             ctx.fillStyle = average_valuecolors; // Set the text color
//             if (width < 150) { // You can adjust the threshold value
//                 fontSize = (height / 70).toFixed(2);
//                 ctx.font = fontSize + "em Nunito";
//             }
    
//             var text = average_value !== null ? average_value : "NA", // Show "NA" if score is null
//                 textX = Math.round((width - ctx.measureText(text).width) / 2),
//                 textY = height / 2;
    
//             ctx.fillText(text, textX, textY);
    
           
    
//             ctx.save();
//         }
//     }]
// });



var ctx3 = document.getElementById('myPieChart3').getContext('2d');
document.addEventListener('DOMContentLoaded', function() {
    var scoreCircle3 = document.getElementById('scoreCircle3');
    
    if (scoreCircle3) {
        scoreCircle3.style.backgroundColor = colors;
        scoreCircle3.textContent = content;
    } else {
        console.warn('Element with ID "scoreCircle3" not found');
    }
});
var myPieChart3 = new Chart(ctx3, {
    type: 'doughnut',
    data: {
        labels: Array(8).fill(content),

        datasets: [{
            data: Array(highest_value).fill(1).concat(Array(8 - highest_value).fill(1)), // Creates an array with 'score' filled segments and '8-score' empty segments
            backgroundColor: Array(score).fill('#f3aa11').concat(Array(score).fill('#e0e0e0')), // Filled parts are blue, remaining are gray
            hoverBackgroundColor: Array(score).fill('#f3aa11').concat(Array(8 - score).fill('#bfbfbf')),
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
            ctx.fillStyle = '#f3aa11'; // Set the text color
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





var ctx4 = document.getElementById('myPieChart4').getContext('2d');
document.addEventListener('DOMContentLoaded', function() {
    var scoreCircle3 = document.getElementById('scoreCircle4');
    
    if (scoreCircle4) {
        scoreCircle4.style.backgroundColor = colors;
        scoreCircle4.textContent = content;
    } else {
        console.warn('Element with ID "scoreCircle" not found');
    }
});
var myPieChart4 = new Chart(ctx4, {
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