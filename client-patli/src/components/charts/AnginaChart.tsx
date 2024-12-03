import { Prediccion } from "@/types/types";
import { Pie } from "react-chartjs-2";
import {
  Chart as ChartJS,
  ArcElement,
  Tooltip,
  Legend,
} from "chart.js";

ChartJS.register(ArcElement, Tooltip, Legend);

const AnginaChart = ({ data }: { data: Prediccion[] }) => {
  const anginaTypes = Array.from(new Set(data.map((item) => item.angina)));
  const chartData = {
    labels: anginaTypes,
    datasets: [
      {
        data: anginaTypes.map(
          (type) => data.filter((item) => item.angina === type).length
        ),
        backgroundColor: ["#FF6384", "#36A2EB", "#FFCE56", "#4BC0C0"],
      },
    ],
  };

  return (
    <div>
      <h3>Distribución de Tipos de Dolor Torácico</h3>
      <Pie data={chartData} />
    </div>
  );
};

export default AnginaChart;
