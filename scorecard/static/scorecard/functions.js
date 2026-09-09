import { Chart, LineController, LineElement, CategoryScale, LinearScale, PointElement, Filler, Tooltip, Legend } from "chart.js";
import chroma from "chroma-js";
import CrosshairPlugin from "chartjs-plugin-crosshair";
import html2pdf from "html2pdf.js";

Chart.register(LineController, LineElement, CategoryScale, LinearScale, PointElement, Filler, CrosshairPlugin, Legend, Tooltip);
const colorScale = chroma.scale("Set3");
window.chartConfigs = {};

function configureChartVisuals(data) {
  const configuredDatasets = data.datasets.map((dataset, index) => {
    const color = colorScale(index / data.datasets.length)
      .alpha(0.6)
      .css();
    return {
      ...dataset,
      fill: true,
      backgroundColor: color,
      tension: 0.1,
      pointRadius: 0
    };
  });

  return {
    ...data,
    datasets: configuredDatasets
  };
}

function humanize(value) {
  let size = Number(value || 0);
  let i;
  const maxIterations = 9; // Because there are 9 units in the array
  for (i = 0; size >= 1000 && i < maxIterations; i++) size /= 1000;

  const units = ["bps", "Kbps", "Mbps", "Gbps", "Tbps", "Pbps", "Ebps", "Zbps", "Ybps"];
  return {
    value: parseFloat(size.toFixed(2)),
    unit: units[i]
  };
}

function getRoundedMax(value) {
  const increasedValue = value * 1.1; // Increment by 10%
  const magnitude = Math.pow(10, Math.floor(Math.log10(increasedValue)));
  return Math.ceil(increasedValue / magnitude) * magnitude;
}

function createChart(elementId, data) {
  const configuredData = configureChartVisuals(data);
  chartConfig = {
    type: "line",
    data: {
      labels: configuredData.originalLabels,
      datasets: configuredData.datasets
    },
    options: {
      layout: {
        padding: {
          left: 10,
          right: 10
        }
      },
      scales: {
        y: {
          min: 0,
          max: getRoundedMax(configuredData.maxValue),
          ticks: {
            callback: function (value) {
              const humanizedValue = humanize(value);
              return `${humanizedValue.value} ${humanizedValue.unit}`;
            }
          }
        },
        x: {
          ticks: {
            maxRotation: 0,
            minRotation: 0,
            autoSkip: true,
            autoSkipPadding: 50
          }
        }
      },
      plugins: {
        crosshair: {
          line: {
            color: "#000000",
            width: 1,
            dashPattern: [5, 5] // specify dash pattern (5px dash, 5px space)
          },
          sync: {
            enabled: false // Disable trace line syncing with other charts
          },
          zoom: {
            enabled: false // Disable zooming
          }
        },
        legend: {
          display: true,
          position: "bottom",
          labels: {
            boxWidth: 12,
            usePointStyle: true,
            padding: 5,
            font: {
              size: 10,
              family: "Helvetica"
            },
            color: "#333"
          }
        },
        tooltip: {
          align: "start",
          enabled: true,
          mode: "index", // This will cause all tooltips from that index to be displayed
          intersect: false, // This will prevent the tooltip from being displayed only when the cursor is hovered over the point
          callbacks: {
            title: function (context) {
              const tooltipItem = context[0];
              const dataset = context[0].dataset;
              return configuredData.groupedData[dataset.label].detailedLabels[tooltipItem.parsed.x]; // Display the time with seconds in the tooltip title
            },
            label: function (context) {
              const tooltipItem = context.parsed;
              const dataset = context.dataset;
              const datasetName = dataset.label;
              const value = tooltipItem.y;
              const humanizedValue = humanize(value);
              return `${datasetName}: ${humanizedValue.value} ${humanizedValue.unit}`;
            }
          }
        }
      },
      interaction: {
        mode: "nearest",
        axis: "x",
        intersect: false
      }
    }
  };

  const chart = new Chart(document.getElementById(elementId), chartConfig);
  chartConfigs[elementId] = chartConfig;

  return chart;
}

function exportChartToPdf(elementId) {
  const element = document.getElementById(elementId);
  const options = {
    margin: 1,
    filename: "grafica.pdf",
    image: { type: "jpeg", quality: 0.98 },
    html2canvas: { scale: 2 },
    jsPDF: { unit: "in", format: "letter", orientation: "landscape" }
  };

  html2pdf().from(element).set(options).save();
}

window.createChart = createChart;
window.exportChartToPdf = exportChartToPdf;
