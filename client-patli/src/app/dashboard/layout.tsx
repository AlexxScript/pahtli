'use client'
import { useAuth } from "@/hooks/useAuth";
import { PropChildrenType } from "@/types/types";
import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";

export const DashboardLayout = ({children}:PropChildrenType) => {

    const auth = useAuth();
    const router = useRouter();
    const [loading, setLoading] = useState(true); 

    useEffect(() => {
        const verifyAuth = async () => {
            const token = auth?.tokenUser || localStorage.getItem("Authorization");
            if (!token) {
                router.push('login/');
            } else {
                setLoading(false);
            }
        };
        verifyAuth();
    }, [auth, router]);

    if (loading) {
        return <p>Cargando...</p>; // Muestra un estado de carga mientras se verifica la autenticación.
    }

    return(
        <>
            <section className="my-[90px]">
                <h1>hola {auth?.tokenUser} </h1>
                {children}
            </section>
        </>
    )
}

export default DashboardLayout