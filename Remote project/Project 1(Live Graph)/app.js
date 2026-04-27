$(document).ready(function () {
  $("#btn").click(function () {
    $(".content").toggleClass("hidden");
  });
});
const btn = document.getElementById("btn");

btn.addEventListener("click", function () {
  this.classList.toggle("active");

  this.textContent = this.classList.contains("active")
    ? "Remove Graph"
    : "View Graph";
});


let tempdata = [];
let humdata = [];
let labels = [];
let maxpoints = 10;

let chart;
function fetchdata() {
  $.ajax({
    url: "https://api.open-meteo.com/v1/forecast?latitude=52.52&longitude=13.41&minutely_15=temperature_2m,relative_humidity_2m&past_days=0&forecast_days=7",
    method: "GET",
    datatype: "json",
    success: function (data) {
      let temps = data.minutely_15.temperature_2m[0];
      let hums = data.minutely_15.relative_humidity_2m[0];
      let time = new Date().toLocaleTimeString();

      tempdata.push(temps);
      humdata.push(hums);
      labels.push(time);

      if (tempdata.length > maxpoints) {
        tempdata.shift();
        humdata.shift();
        labels.shift();
      }

	  updateChart();
    },
    error: function (err) {
      console.log(err);
    },
  });
}

function generateRandomData() {
  let temp = (Math.random() * (40 - 20) + 20).toFixed(2); // 20°C to 40°C
  let hum = (Math.random() * (90 - 30) + 30).toFixed(2); // 30% to 90%
  let now = new Date();

let date = now.toLocaleDateString();
let time = now.toLocaleTimeString();

let label = date + " " + time;

  tempdata.push(temp);
  humdata.push(hum);
  labels.push(label);

  if (tempdata.length > maxpoints) {
    tempdata.shift();
    humdata.shift();
    labels.shift();
  }

  updateChart(); // update graph
}

const ctx = document.getElementById("myChart");
function createGraph() {
  chart=new Chart(ctx, {
    type: "line",
    data: {
      labels: labels,
      datasets: [
        {
          label: "Temperature",
          data: tempdata,
          borderColor: "blue",
          pointStyle: "rect",
          pointRadius: 6,
          pointBackgroundColor: "blue",
          fill: false,
        },
        {
          label: "Humidity",
          data: humdata,
          borderColor: "red",
          pointStyle: "rect",
          pointRadius: 6,
          pointBackgroundColor: "red",
          fill: false,
        },
      ],
    },
    options: {
      responsive: true,
      scales: {
        x: {
          title: {
            display: true,
            text: "Time (Date & Clock)",   // X-axis label
            font: {
              size: 14,
              weight: "bold"
            }
          }
        },
        y: {
          title: {
            display: true,
            text: "Values (°C / % Humidity)",  // Y-axis label
            font: {
              size: 14,
              weight: "bold"
            }
          },
          beginAtZero: true
        }
      }
    }
  });
}

function updateChart(){
	if(chart){
		chart.data.labels=labels;
		chart.data.datasets[0].data=tempdata;
		chart.data.datasets[1].data=humdata;
		chart.update();
	}
}

createGraph();
setInterval(() => {
//   fetchdata();
	generateRandomData()
}, 5000*12); //change in every 1 minutes
