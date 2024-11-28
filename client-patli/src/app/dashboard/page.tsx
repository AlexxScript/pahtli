'use client'
import Image from "next/image";
import { useAuth } from "@/hooks/useAuth"
import { useEffect } from "react";
import image1 from "/public/images/seriegraficos.png"
import image2 from "/public/images/mapadecorrelacion.png"

export const DashboardMain = () => {
    const auth = useAuth();

    useEffect(() => {
        console.log(auth?.user); // Verificar si el usuario está correctamente cargado
    }, [auth]);

    return (
        <>
            <h1>Hola en Dashboard</h1>
            <Image src={image1}  alt="serieGraficos" />            
            <Image src={image2}  alt="serieGraficos" />            
            <p>Bienvenido, {auth?.user.nombres}</p>
        </>
    );
};


export default DashboardMain