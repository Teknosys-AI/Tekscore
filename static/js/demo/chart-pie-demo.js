document.getElementById("year").textContent = new Date().getFullYear();

    {% if api_data %}
        // Get api_data from Flask
        var api_data = {{ api_data | tojson }};
        // Extract the score from api_data
        var score = parseInt(api_data.score);
    {% else %}
        // Fallback in case api_data is not available
        var api_data = {};
        var score = 0; // Default score if no data is available
    {% endif %}


    var colors = [];
if (score >= 0 && score <= 4) {
    colors = ['#FF0000'];  // Red for 0-4
} else if (score === 5) {
    colors = ['#FFA500'];  // Orange for 5
} else if (score === 6) {
    colors = ['#FFFF00'];  // Yellow for 6
} else if (score === 7) {
    colors = ['#0000FF'];  // Blue for 7
} else if (score === 8) {
    colors = ['#008000'];  // Green for 8
}


    // Apply the circle color
    document.getElementById('scoreCircle').style.color = colors;
    
    // Define the data for the pie chart using the score
    var ctx = document.getElementById("myPieChart");
    var myPieChart = new Chart(ctx, {
      type: 'doughnut',
      data: {
        labels: ["Score", "Remaining"],
        datasets: [{
          data: Array(score).fill(1).concat(Array(8 - score).fill(1)), // Creates an array with 'score' filled segments and '8-score' empty segments
          backgroundColor: Array(score).fill(colors).concat(Array(score).fill('#e0e0e0')), // Filled parts are blue, remaining are gray
          hoverBackgroundColor: Array(score).fill('#2e59d9').concat(Array(8 - score).fill('#bfbfbf')),
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

          var text = score,
              textX = Math.round((width - ctx.measureText(text).width) / 2),
              textY = height / 2;

          ctx.fillText(text, textX, textY);
          ctx.save();
        }
      }]
    });