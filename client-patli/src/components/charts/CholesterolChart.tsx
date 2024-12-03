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
  };

  return <Bar data={chartData} options={options} />;
};

export default CholesterolChart;