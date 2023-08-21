const page_buttons = document.querySelectorAll('.btn-year')
const canvas = document.getElementById('chart-stats-club')
let chart_distance = JSON.parse(document.getElementById('chart_distance').textContent)
let chart_colors = JSON.parse(document.getElementById('chart_colors').textContent)
const canvasContainer = document.getElementById('container-stats-club')

canvasContainer.setAttribute("style",`height: ${chart_distance.length * 40 + 50}px;`)

Chart.register(ChartDataLabels)

let chart = new Chart(canvas, {
  type: 'bar',
  data: {
    labels: chart_distance.map(row => row.y),
    datasets: [
      {
        data: chart_distance,
        backgroundColor: chart_colors,
        datalabels: {
          display: true,
          color: "#1d3652",
        }
      },
    ]
  },
  options: {
    indexAxis: 'y',
    plugins: {
      legend: {
        display: false
      },
    },
    scales: {
      x: {
        stacked: true,
      },
      y: {
        stacked: true,
      }
    },
    maintainAspectRatio: false,
    responsive: true,
  },
  scales: {
    x: {
      type: 'linear',
    },
    y: {
      type: 'linear',
    }
  }
})

function update_chart(){
  chart_distance = JSON.parse(document.getElementById('chart_distance').textContent)
  chart_colors = JSON.parse(document.getElementById('chart_colors').textContent)
  chart.data.datasets[0].backgroundColor = chart_colors
  chart.update()
}

function update_button_styles(){
  let metadata = JSON.parse(document.getElementById('metadata').textContent)

  for (let i=0; i < page_buttons.length; i++){
    page_buttons[i].classList.replace("btn-dark", "btn-light")
  }

  let target_id = "btn-year-"
  if (metadata['year'] === "None"){
    target_id += "all"
  } else {
    target_id += metadata.year
  }
  document.getElementById(target_id).classList.replace("btn-light", "btn-dark")
}

function update_all(){
  update_button_styles()
  update_chart()
}

document.addEventListener('htmx:afterSwap', update_all)

update_button_styles()