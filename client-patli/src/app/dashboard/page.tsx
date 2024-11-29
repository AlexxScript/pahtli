'use client'
import Image from "next/image";
import { useAuth } from "@/hooks/useAuth"
import { useEffect } from "react";
import image1 from "/public/images/seriegraficos.png"
import image2 from "/public/images/mapadecorrelacion.png"
import image3 from "/public/images/matrisregree.png"
import image4 from "/public/images/matrizdetree.png"
// import image5 from "/public/images/matrizrandomfo.png"
import image6 from "/public/images/matrizrandompart.png"
import Table from "@/components/Table";

export const DashboardMain = () => {
    const auth = useAuth();

    useEffect(() => {
        console.log(auth?.user); // Verificar si el usuario está correctamente cargado
    }, [auth]);

    return (
        <div className="flex flex-col gap-7">
            <div className="flex flex-col gap-3 justify-center items-center w-[90%] m-auto bg-[#333333] p-5 rounded-lg">
                <h2 className="font-semibold text-[#D8A6E9]">Trazo de relaciones por pares</h2>
                <p className="text-center">
                    Es una rejilla que contiene un conjunto de gráficos 
                    de dispersión donde se muestra la relación entre todas las 
                    variables numéricas y categóricas de un conjunto de datos
                </p>
                <Image src={image1}  alt="serieGraficos"/>            
            </div>
            <div className="flex flex-col gap-3 justify-center items-center w-[90%] m-auto bg-[#333333] p-5 rounded-lg">
                <h2 className="font-semibold text-[#84D5C0]">Mapa de calor</h2>
                <p className="text-center">
                    Herramienta que muestra la correlación entre variables, 
                    representadas por filas y columnas en una cuadrícula. 
                    El color de cada celda indica la fuerza y dirección de la 
                    correlación, siendo los colores más oscuros los que representan 
                    correlaciones más fuertes.
                </p>
                <Image src={image2}  alt="serieGraficos" className="flex justify-center items-center w-[90%] m-auto"/>     
            </div>
            <div className="flex flex-col gap-3 justify-center items-center w-[90%] m-auto bg-[#333333] p-4 rounded-lg">
                <h2 className="font-semibold text-[#84D5C0]">Matrices de confusión</h2>
                <p>Matriz de confusión es simplemente 
                    una tabla que nos permite ver qué tan “confundido” está nuestro modelo al momento de la clasificación, mostrándonos tanto los aciertos como desaciertos cometidos para cada una de las categorías</p>
                <div className="flex max-w-full w-full flex-wrap gap-6 justify-center iitems-center">
                    <div className="w-[40%] flex flex-col gap-3 justify-center items-center bg-[#202020] p-5 rounded-lg">
                        <h2>Matriz de confusión de regresión logística</h2>
                        <Image src={image3}  alt="serieGraficos"/>            
                    </div>
                    <div className="w-[40%] flex flex-col gap-3 justify-center items-center bg-[#202020] p-5 rounded-lg">
                        <h2>Matriz de confusión de support vector machine</h2>
                        <Image src={image3}  alt="serieGraficos"/>            
                    </div>
                    <div className="w-[40%] flex flex-col gap-3 justify-center items-center bg-[#202020] p-5 rounded-lg">
                        <h2>Matriz de confusión de decision tree</h2>
                        <Image src={image4}  alt="serieGraficos"/>            
                    </div>
                    <div className="w-[40%] flex flex-col gap-3 justify-center items-center bg-[#202020] p-5 rounded-lg">
                        <h2>Matriz de confusión de random forest</h2>
                        <Image src={image6}  alt="serieGraficos" />            
                    </div>
                </div>    
            </div>   
                        
            <Table/>
        </div>
    );
};


export default DashboardMain