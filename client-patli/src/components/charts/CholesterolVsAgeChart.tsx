import React from "react";
import { Scatter } from "react-chartjs-2";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";
import { Prediccion } from "@/types/types";
import { color } from "chart.js/helpers";

ChartJS.register(CategoryScale, LinearScale, PointElement, Title, Tooltip, Legend);

const CholesterolVsAgeChart = ({ data }: { data: Prediccion[] }) => {
  const chartData = {
    datasets: [
      {
        label: "Colesterol vs. Edad",
        data: data.map((item) => ({
          x: parseInt(item.edad),
          y: parseInt(item.colesterol),
        })),
        backgroundColor: "#4BC0C0",
        borderWidth: 1,
        borderColor: '#fff'
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
        text: "Relación entre Edad y Colesterol",
      },
    },
    scales: {
      x: {
        title: {
          display: true,
          text: "Edad",
        },
        ticks: {
          color: "#999", // Color de las etiquetas en el eje X
        },
        grid: {
          color: "#999", // Color de las líneas de la grilla en el eje X
          borderColor: "#999", // Color del borde del eje X
        },
      },
      y: {
         title: {
          display: true,
          text: "Colesterol",
        },
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

  return <Scatter data={chartData} options={options} />;
};

export default CholesterolVsAgeChart;
