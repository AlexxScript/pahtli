'use client'
import { useAuth } from "@/hooks/useAuth";
import { Prediccion } from "@/types/types";
import React, { useState } from "react";
import CholesterolChart from "../charts/CholesterolChart";
import AnginaChart from "../charts/AnginaChart";
import CholesterolByGenderChart from "../charts/CholesterolByGenderChart";
import BloodPressureChart from "../charts/BloodPressureChart";
import CholesterolVsAgeChart from "../charts/CholesterolVsAgeChart";

export const FileUpload = () => {
  const [predicciones, setPredicciones] = useState<Prediccion[]>([]);
  const auth = useAuth()
  const [file, setFile] = useState<File | null>(null);
  const [message, setMessage] = useState<string>("");

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      setFile(e.target.files[0]); // Toma el primer archivo seleccionado
    }
  };

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    if (!file) {
      setMessage("Por favor selecciona un archivo antes de enviarlo.");
      return;
    }

    const formData = new FormData();
    formData.append("archivo", file);

    try {
      const response = await fetch(process.env.NEXT_PUBLIC_RUTA_BACKEND + "cardio/subir/", {
        method: "POST",
        body: formData,
        headers: {
          Authorization: `Token ${auth?.tokenUser}`,
        }
      });

      if (response.ok) {
        const data = await response.json();
        setPredicciones(data.predicciones);
        console.log(predicciones)
      } else {
        const error = await response.json();
        setMessage(`Error al subir el archivo: ${error.detail || "Inténtalo de nuevo."}`);
      }
    } catch (error) {
      console.error("Error de red:", error);
      setMessage("Error al conectar con el servidor. Inténtalo más tarde.");
    }
  };

  return (
    <>
      <div className="p-4 max-w-2xl overflow-x-auto mx-auto">
        <form onSubmit={handleSubmit} encType="multipart/form-data">
          <label
            className="block mb-2 text-sm font-medium text-gray-900 dark:text-white"
            htmlFor="file_input"
          >
            Subir archivo CSV para predecir serie de datos
          </label>
          <input
            className="p-2 focus:border-[#7DFABB] bg-[#282A29] 
                            border-2 border-[#666666] duration-500"
            id="file_input"
            name="archivo"
            type="file"
            accept=".csv"
            onChange={handleFileChange}
          />
          <button
            type="submit"
            className="bg-[#7DFABB] text-[#202020] p-2 border-2 hover:bg-[#7dfabbd8]"
          >
            Subir archivo
          </button>
        </form>
        {message && <div className="mt-4 text-sm font-medium text-gray-700 dark:text-gray-300">{message}</div>}
      </div>

      <div className="p-4 max-w-full overflow-x-auto mx-auto">
        <table className="max-w-full overflow-x-auto mt-6 table-auto border-collapse border border-gray-400 w-full">
          <thead>
            <tr className="bg-[#505050]">
              <th className="border border-gray-400 px-4 py-2">Edad</th>
              <th className="border border-gray-400 px-4 py-2">Género</th>
              <th className="border border-gray-400 px-4 py-2">Angina</th>
              <th className="border border-gray-400 px-4 py-2">Presión Arterial</th>
              <th className="border border-gray-400 px-4 py-2">Colesterol</th>
              <th className="border border-gray-400 px-4 py-2">Azúcar</th>
              <th className="border border-gray-400 px-4 py-2">Electrocardio</th>
              <th className="border border-gray-400 px-4 py-2">Frecuencia Máxima</th>
              <th className="border border-gray-400 px-4 py-2">Angina por Ejercicio</th>
              <th className="border border-gray-400 px-4 py-2">Viejo Pico</th>
              <th className="border border-gray-400 px-4 py-2">ST Slope</th>
              <th className="border border-gray-400 px-4 py-2">Enferemedad cardiovascular(Predicción)</th>
            </tr>
          </thead>
          <tbody>
            {predicciones.map((prediccion, index) => (
              <tr key={index} className={index % 2 === 0 ? "bg-[#303030]" : "bg-[#202020]"}>
                <td className="border border-gray-400 px-4 py-2">{prediccion.edad}</td>
                <td className="border border-gray-400 px-4 py-2">{prediccion.genero}</td>
                <td className="border border-gray-400 px-4 py-2">{prediccion.angina}</td>
                <td className="border border-gray-400 px-4 py-2">{prediccion.presionA}</td>
                <td className="border border-gray-400 px-4 py-2">{prediccion.colesterol}</td>
                <td className="border border-gray-400 px-4 py-2">{prediccion.azucar}</td>
                <td className="border border-gray-400 px-4 py-2">{prediccion.electrocardio}</td>
                <td className="border border-gray-400 px-4 py-2">{prediccion.FrecuenciaMaxima}</td>
                <td className="border border-gray-400 px-4 py-2">{prediccion.anginaEjercicio}</td>
                <td className="border border-gray-400 px-4 py-2">{prediccion.ViejoPico}</td>
                <td className="border border-gray-400 px-4 py-2">{prediccion.stslope}</td>
                <td className="border border-gray-400 px-4 py-2">{prediccion.prediccion == '1' ? "SI" : "NO"}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>


      <div className="p-4 max-w-full overflow-x-auto mx-auto">
        <div className="">
          {predicciones.length > 0 ? (
            <>
              <div className="flex justify-center items-center gap-3 max-w-full flex-wrap">
                <div className="w-[45%]">
                  <CholesterolChart data={predicciones} />
                </div>
                <div className="w-[40%]">
                  <AnginaChart data={predicciones} />
                </div>
              </div>

              <div className="flex justify-center items-center gap-3 max-w-full flex-wrap my-10">
                <div className="w-[45%]">
                  <CholesterolByGenderChart data={predicciones} />
                </div>
                <div className="w-[45%]">
                  <BloodPressureChart data={predicciones} />
                </div>
              </div>

              <div>
                <CholesterolVsAgeChart data={predicciones} />
              </div>
            </>
          ) : (
            <p>Esperando la entrada de datos...</p>
          )}
        </div>
      </div>

    </>
  );
};
