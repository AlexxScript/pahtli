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
      },
    ],
  };

  const options = {
    responsive: true,
    plugins: {
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
      },
      y: {
        title: {
          display: true,
          text: "Colesterol",
        },
      },
    },
  };

  return <Scatter data={chartData} options={options} />;
};

export default CholesterolVsAgeChart;
