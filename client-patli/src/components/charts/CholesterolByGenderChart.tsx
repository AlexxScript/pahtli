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

const CholesterolByGenderChart = ({ data }: { data: Prediccion[] }) => {
  // Separar por género
  const maleData = data.filter((item) => item.genero === "M");
  const femaleData = data.filter((item) => item.genero === "F");

  const chartData = {
    labels: ["Hombres", "Mujeres"],
    datasets: [
      {
        label: "Colesterol Promedio",
        data: [
          maleData.reduce((sum, item) => sum + parseInt(item.colesterol), 0) /
            maleData.length,
          femaleData.reduce((sum, item) => sum + parseInt(item.colesterol), 0) /
            femaleData.length,
        ],
        backgroundColor: ["#4BC0C0", "#FF6384"],
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
        text: "Colesterol Promedio por Género",
      },
    },
  };

  return <Bar data={chartData} options={options} />;
};

export default CholesterolByGenderChart;
