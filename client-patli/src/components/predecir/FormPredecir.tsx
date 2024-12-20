import { useAuth } from "@/hooks/useAuth"
import { useEffect, useState } from "react";
import { FormData } from "@/types/types";


export const FormPredecir = () => {
    const auth = useAuth();
    const [formData, setFormData] = useState<FormData>({
        edad: "",
        genero: "F",
        tipo_dolor_pecho: "0",
        presion_arterial_reposo: "",
        colesterol: "",
        azucar_sangre_ayuno: "",
        electrogardiograma_reposo: "1",
        frecuencia_cardiaca_maxima: "",
        angina_por_ejercicio: "0",
        viejo_pico_ST: "",
        st_slope: "2",
    });
    const [resultado, setResultado] = useState<string | null>(null);

    useEffect(() => {
        console.log(auth?.user); // Verificar si el usuario está correctamente cargado
    }, [auth]);

    const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        try {
            const response = await fetch(process.env.NEXT_PUBLIC_RUTA_BACKEND + "cardio/predecir/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    Authorization: `Token ${auth?.tokenUser}`,
                },
                body: JSON.stringify(formData),
            });

            if (response.ok) {
                const data = await response.json();
                console.log(data.prediccion)
                setResultado(`Predicción: ${data.prediccion}`);
            } else {
                const errorData = await response.json();
                console.error("Errores:", errorData);
                alert("Error al realizar la predicción. Revisa los datos ingresados.");
            }
        } catch (error) {
            console.error("Error:", error);
            alert("Hubo un problema al conectar con el servidor.");
        }
    };


    return (
        <>
            <div className="max-w-3xl mx-auto p-4">
                <h1 className="text-xl font-bold mb-4">Formulario de Predicción Cardio</h1>
                <form onSubmit={handleSubmit} className="space-y-4">
                    <div>
                        <label htmlFor="st_slope" className="block text-sm font-medium text-[#aaaaa]">
                            Edad
                        </label>
                        <input
                            type="number"
                            id="edad"
                            name="edad"
                            value={formData.edad}
                            onChange={handleChange}
                            className="rounded-md w-full p-2 focus:border-[#7DFABB] bg-[#282A29] 
                                border-2 border-[#666666] duration-500"
                            required
                        />
                    </div>
                    <div>
                        <label htmlFor="st_slope" className="block text-sm font-medium text-[#aaaaa]">
                            Género
                        </label>
                        <select
                            id="st_slope"
                            name="genero"
                            value={formData.genero}
                            onChange={handleChange}
                            className="rounded-md w-full p-2 focus:border-[#7DFABB] bg-[#282A29] 
                                border-2 border-[#666666] duration-500"
                        >
                            <option value="F">Femenino</option>
                            <option value="M">Masculino</option>
                        </select>
                    </div>
                    <div>
                        <label htmlFor="tipo_dolor_pecho" className="block text-sm font-medium text-[#aaaaa]">
                            Tipo de Dolor de Pecho
                        </label>
                        <select
                            id="tipo_dolor_pecho"
                            name="tipo_dolor_pecho"
                            value={formData.tipo_dolor_pecho}
                            onChange={handleChange}
                            className="rounded-md p-2 w-full focus:border-[#7DFABB] bg-[#282A29] 
                                border-2 border-[#666666] duration-500"
                        >
                            <option value="ASINTOMATICO">Asintomático</option>
                            <option value="ANGINA ATIPICA">Angina Atípica</option>
                            <option value="SIN DOLOR ANGINAL">Sin Dolor Anginal</option>
                            <option value="ANGINA TIPICA">Angina Típica</option>
                        </select>
                    </div>


                    <div>
                        <label htmlFor="presion_arterial_reposo" className="block text-sm font-medium text-[#aaaaa]">
                            Presión Arterial en Reposo (mm Hg)
                        </label>
                        <input
                            type="number"
                            step="0.01"
                            id="presion_arterial_reposo"
                            name="presion_arterial_reposo"
                            value={formData.presion_arterial_reposo}
                            onChange={handleChange}
                            className="rounded-md p-2 w-full focus:border-[#7DFABB] bg-[#282A29] 
                                border-2 border-[#666666] duration-500"
                            required
                        />
                    </div>
                    <div>
                        <label htmlFor="colesterol" className="block text-sm font-medium text-[#aaaaa]">
                            Colesterol (mm/dl)
                        </label>
                        <input
                            type="number"
                            step="0.01"
                            id="colesterol"
                            name="colesterol"
                            value={formData.colesterol}
                            onChange={handleChange}
                            className="rounded-md p-2 w-full focus:border-[#7DFABB] bg-[#282A29] 
                                border-2 border-[#666666] duration-500"
                            required
                        />
                    </div>
                    <div>
                        <label htmlFor="azucar_sangre_ayuno" className="block text-sm font-medium text-[#aaaaa]">
                            Azúcar en Sangre en Ayuno (mg/dl)
                        </label>
                        <input
                            type="number"
                            step="0.01"
                            id="azucar_sangre_ayuno"
                            name="azucar_sangre_ayuno"
                            value={formData.azucar_sangre_ayuno}
                            onChange={handleChange}
                            className="rounded-md p-2 w-full focus:border-[#7DFABB] bg-[#282A29] 
                                border-2 border-[#666666] duration-500"
                            required
                        />
                    </div>

                    <div>
                        <label htmlFor="electrogardiograma_reposo" className="block text-sm font-medium text-[#aaaaa]">
                            Resultado del Electrocardiograma en Reposo
                        </label>
                        <select
                            id="electrogardiograma_reposo"
                            name="electrogardiograma_reposo"
                            value={formData.electrogardiograma_reposo}
                            onChange={handleChange}
                            className="rounded-md w-full p-2 focus:border-[#7DFABB] bg-[#282A29] 
                                border-2 border-[#666666] duration-500"
                        >
                            <option value="ANOMALIA DEL SEGMENTO ST">Anomalía del Segmento ST</option>
                            <option value="NORMAL">Normal</option>
                            <option value="HIPERTROFIA VENTRICULAR IZQUIERDA">Hipertrofia Ventricular Izquierda</option>
                        </select>
                    </div>
                    <div>
                        <label htmlFor="frecuencia_cardiaca_maxima" className="block text-sm font-medium text-[#aaaaa]">
                            Frecuencia Cardíaca Máxima
                        </label>
                        <input
                            type="number"
                            id="frecuencia_cardiaca_maxima"
                            name="frecuencia_cardiaca_maxima"
                            value={formData.frecuencia_cardiaca_maxima}
                            onChange={handleChange}
                            className="rounded-md p-2 w-full focus:border-[#7DFABB] bg-[#282A29] 
                                border-2 border-[#666666] duration-500"
                            required
                        />
                    </div>

                    <div>
                        <label htmlFor="angina_por_ejercicio" className="block text-sm font-medium text-[#aaaaa]">
                            ¿Presentó Angina por Ejercicio?
                        </label>
                        <select
                            id="angina_por_ejercicio"
                            name="angina_por_ejercicio"
                            value={formData.angina_por_ejercicio}
                            onChange={handleChange}
                            className="rounded-md p-2 w-full focus:border-[#7DFABB] bg-[#282A29] 
                                    border-2 border-[#666666] duration-500"
                        >
                            <option value="0">No</option>
                            <option value="1">Sí</option>
                        </select>
                    </div>
                    <div>
                        <label htmlFor="viejo_pico_ST" className="block text-sm font-medium text-[#aaaaa]">
                            Viejo Pico ST
                        </label>
                        <input
                            type="number"
                            step="0.01"
                            id="viejo_pico_ST"
                            name="viejo_pico_ST"
                            value={formData.viejo_pico_ST}
                            onChange={handleChange}
                            className="rounded-md p-2 w-full focus:border-[#7DFABB] bg-[#282A29] 
                                border-2 border-[#666666] duration-500"
                            required
                        />
                    </div>
                    <div>
                        <label htmlFor="st_slope" className="block text-sm font-medium text-[#aaaaa]">
                            Pendiente del ST
                        </label>
                        <select
                            id="st_slope"
                            name="st_slope"
                            value={formData.st_slope}
                            onChange={handleChange}
                            className="rounded-md p-2 w-full focus:border-[#7DFABB] bg-[#282A29] 
                                border-2 border-[#666666] duration-500"
                        >
                            <option value="DESCENDENTE">Descendente</option>
                            <option value="PLANO">Plano</option>
                            <option value="ASCENDENTE">Ascendente</option>
                        </select>
                    </div>
                    <button
                        type="submit"
                        className="w-full bg-[#7DFABB] text-[#202020] py-2 px-4 rounded-md hover:bg-[#7dfabbd8]"
                    >
                        Predecir
                    </button>
                </form>
                {resultado && <div className="mt-4 text-green-600 font-bold">{resultado}</div>}
            </div>
        </>
    )
}