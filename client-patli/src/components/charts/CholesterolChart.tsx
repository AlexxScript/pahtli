import React from "react";
import { Bar } from "react-chartjs-2";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";
import { Prediccion } from "@/types/types";

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

const CholesterolChart = ({ data }: { data: Prediccion[] }) => {
  const chartData = {
    labels: data.map((item) => item.edad + " años"),
    datasets: [
      {
        label: "Colesterol (mg/dL)",
        data: data.map((item) => parseInt(item.colesterol)),
        backgroundColor: "#84D5C0",
      },
    ],
  };

  const options = {
    responsive: true,
    plugins: {
      legend: {
        position: "top" as const,
      },
      title: {
        display: true,
        text: "Colesterol por Edad",
      },
    },
    scales: {
      x: {
        ticks: {
          color: "#999", // Color de las etiquetas en el eje X
        },
        grid: {
          color: "#999", // Color de las líneas de la grilla en el eje X
          borderColor: "#999", // Color del borde del eje X
        },
      },
      y: {
        ticks: {
          color: "#999", // Color de las etiquetas en el eje Y
        },
        grid: {
          color: "#999", // Color de las líneas de la grilla en el eje Y
          borderColor: "#999", // Color del borde del eje Y
        },
      },
    },

  };

  return <Bar data={chartData} options={options} />;
};

export default CholesterolChart;