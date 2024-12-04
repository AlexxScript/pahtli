'use client'
import { useAuth } from "@/hooks/useAuth";
import React, { useState } from "react";

export const DashboardEntrenar = () => {
  const [mensaje, setMensaje] = useState<string>();
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
      const response = await fetch(process.env.NEXT_PUBLIC_RUTA_BACKEND + "cardio/entrenar/", {
        method: "POST",
        body: formData,
        headers: {
          Authorization: `Token ${auth?.tokenUser}`,
        }
      });

      if (response.ok) {
        const data = await response.json();
        setMensaje(data.predicciones);
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
            Subir archivo CSV para entrenar el modelo
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
      <h1>{mensaje}</h1>

    </>
  );
};

export default DashboardEntrenar