'use client'
import Link from "next/link";
import { useAuth } from "@/hooks/useAuth";
import { PropChildrenType } from "@/types/types";
import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import { usePathname } from 'next/navigation'
import Image from "next/image";
import icon from "/public/icon.svg"

export const DashboardLayout = ({children}:PropChildrenType) => {

    const auth = useAuth();
    const router = useRouter();
    const [loading, setLoading] = useState(true); 
    const currentePath = usePathname();
    
    console.log(currentePath)

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
        return <p>Cargando...</p>; 
    }

    return(
        <>
            <main className="">
                <aside className="ml-[-100%] fixed z-10 top-0 w-full flex flex-col h-screen border-r border-r-zinc-900 bg-[#202020] transition duration-300 md:w-4/12 lg:ml-0 lg:w-[25%] xl:w-[20%] 2xl:w-[15%]">
                    
                    <ul className="flex flex-col gap-4 my-10">
                        <li>
                            <Link href="/" className="w-full flex justify-center items-center">
                                <Image src={icon} alt="Patli brand" className='h-14 w-auto'/>
                            </Link> 
                        </li>
                        <li>
                            <Link href="/dashboard" className={currentePath === '/dashboard' ? "p-3 flex gap-2 w-full text-[#84D5C0] bg-[#84D5C022] transition-all duration-150" : "p-3 flex gap-2 w-full hover:bg-[#84D5C022] hover:text-[#84D5C0] transition-all duration-150"}>
                                <svg  xmlns="http://www.w3.org/2000/svg"  width="24"  height="24"  viewBox="0 0 24 24"  fill="none"  stroke="currentColor"  stroke-width="2"  stroke-linecap="round"  stroke-linejoin="round"  className="icon icon-tabler icons-tabler-outline icon-tabler-chart-covariate"><path stroke="none" d="M0 0h24v24H0z" fill="none"/><path d="M18 11h.009" /><path d="M14 15h.009" /><path d="M12 6h.009" /><path d="M8 10h.009" /><path d="M3 21l17 -17" /><path d="M3 3v18h18" /></svg>
                                Estadística
                            </Link>
                        </li>
                        <li>
                            <Link href="/dashboard/predecir" className={currentePath === '/dashboard/predecir' ? "p-3 flex gap-2 w-full text-[#84D5C0] bg-[#84D5C022] transition-all duration-150" : "p-3 flex gap-2 w-full hover:bg-[#84D5C022] hover:text-[#84D5C0] transition-all duration-150"}>
                                <svg  xmlns="http://www.w3.org/2000/svg"  width="24"  height="24"  viewBox="0 0 24 24"  fill="none"  stroke="currentColor"  stroke-width="2"  stroke-linecap="round"  stroke-linejoin="round"  className="icon icon-tabler icons-tabler-outline icon-tabler-heart-code"><path stroke="none" d="M0 0h24v24H0z" fill="none"/><path d="M19.5 12.572l-.536 .53m-7.91 5.96l-6.554 -6.489a5 5 0 1 1 7.5 -6.567a5 5 0 1 1 7.5 6.572" /><path d="M20 21l2 -2l-2 -2" /><path d="M17 17l-2 2l2 2" /></svg>
                                Predecir
                            </Link>
                        </li>
                        <li>
                            <Link href="/dashboard/entrenar" className={currentePath === '/dashboard/entrenar' ? "p-3 flex gap-2 w-full text-[#84D5C0] bg-[#84D5C022] transition-all duration-150" : "p-3 flex gap-2 w-full hover:bg-[#84D5C022] hover:text-[#84D5C0] transition-all duration-150"}>
                                <svg  xmlns="http://www.w3.org/2000/svg"  width="24"  height="24"  viewBox="0 0 24 24"  fill="none"  stroke="currentColor"  stroke-width="2"  stroke-linecap="round"  stroke-linejoin="round"  className="icon icon-tabler icons-tabler-outline icon-tabler-robot"><path stroke="none" d="M0 0h24v24H0z" fill="none"/><path d="M6 4m0 2a2 2 0 0 1 2 -2h8a2 2 0 0 1 2 2v4a2 2 0 0 1 -2 2h-8a2 2 0 0 1 -2 -2z" /><path d="M12 2v2" /><path d="M9 12v9" /><path d="M15 12v9" /><path d="M5 16l4 -2" /><path d="M15 14l4 2" /><path d="M9 18h6" /><path d="M10 8v.01" /><path d="M14 8v.01" /></svg>
                                Entrenar
                            </Link>
                        </li>
                        <li>
                            <button className="p-3 flex gap-2 w-full hover:bg-[#84D5C022] hover:text-[#84D5C0] transition-all duration-150" onClick={() => auth?.logOut()}>
                            <svg  xmlns="http://www.w3.org/2000/svg"  width="24"  height="24"  viewBox="0 0 24 24"  fill="none"  stroke="currentColor"  stroke-width="2"  stroke-linecap="round"  stroke-linejoin="round"  className="icon icon-tabler icons-tabler-outline icon-tabler-logout"><path stroke="none" d="M0 0h24v24H0z" fill="none"/><path d="M14 8v-2a2 2 0 0 0 -2 -2h-7a2 2 0 0 0 -2 2v12a2 2 0 0 0 2 2h7a2 2 0 0 0 2 -2v-2" /><path d="M9 12h12l-3 -3" /><path d="M18 15l3 -3" /></svg>
                                Cerrar sesión
                            </button>
                        </li>
                    </ul>
                </aside>
                <section className="my-8 ml-auto mb-6 lg:w-[75%] xl:w-[80%] 2xl:w-[85%] px-6 pt-6">
                    {children}
                </section>    
            </main>  
        </>
    )
}

export default DashboardLayout