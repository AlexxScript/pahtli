import React from "react";
import { Line } from "react-chartjs-2";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";
import { Prediccion } from "@/types/types";

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

const BloodPressureChart = ({ data }: { data: Prediccion[] }) => {
  const chartData = {
    labels: data.map((item) => item.edad + " años"),
    datasets: [
      {
        label: "Presión Arterial (mmHg)",
        data: data.map((item) => parseInt(item.presionA)),
        borderColor: "#36A2EB",
        backgroundColor: "rgba(54, 162, 235, 0.2)",
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
        text: "Presión Arterial por Edad",
      },
    },
  };

  return <Line data={chartData} options={options} />;
};

export default BloodPressureChart;
