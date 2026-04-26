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
  // Generate realistic random values
  let temp = (Math.random() * (40 - 20) + 20).toFixed(2); // 20°C to 40°C
  let hum = (Math.random() * (90 - 30) + 30).toFixed(2); // 30% to 90%
  let now = new Date();

let date = now.toLocaleDateString();     // e.g. 26/4/2026
let time = now.toLocaleTimeString();     // e.g. 10:35:21 AM

let label = date + " " + time;

  // Store data
  tempdata.push(temp);
  humdata.push(hum);
  labels.push(label);

  // Maintain max points
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
}, 5000);
