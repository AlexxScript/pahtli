'use client'
import { useAuth } from "@/hooks/useAuth"
import { useEffect } from "react";

export const DashboardMain = () => {
    const auth = useAuth();

    useEffect(() => {
        console.log(auth?.user); // Verificar si el usuario está correctamente cargado
    }, [auth]);

    return (
        <>
            <h1>Hola en Dashboard</h1>
            <p>Bienvenido, {auth?.user.nombres}</p>
        </>
    );
};


export default DashboardMain