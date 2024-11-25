'use client'
import Link from "next/link";
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
            <main className="">
                <aside className="ml-[-100%] fixed z-10 top-0 pb-3 px-6 w-full flex flex-col justify-between h-screen border-r border-r-zinc-800 bg-zinc-800 transition duration-300 md:w-4/12 lg:ml-0 lg:w-[25%] xl:w-[20%] 2xl:w-[15%]">
                    <ul>
                        <li><Link href="/dashboard">Predecir</Link></li>
                        <li><Link href="/">Estadística</Link></li>
                        <li><Link href="/">Entrenar</Link></li>
                    </ul>
                </aside>
                <section className="my-[90px] ml-auto mb-6 lg:w-[75%] xl:w-[80%] 2xl:w-[85%]">
                    {children}
                </section>    
            </main>  
        </>
    )
}

export default DashboardLayout