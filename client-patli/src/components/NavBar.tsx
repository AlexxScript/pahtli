'use client';
import Image from "next/image";
import Link from "next/link";
import icon from "/public/icon.svg"
import { useAuth } from "@/hooks/useAuth";

export const NavBar = () => {
    const auth = useAuth();
    // https://dev.to/miracool/how-to-manage-user-authentication-with-react-js-3ic5
    console.log(auth?.tokenUser)
    if (!auth?.tokenUser) {
        return(
            <nav className="w-screen fixed top-0">
                <div className="lg:max-w-5xl m-auto w-full flex flex-row items-center justify-between p-2
                    max-2xl:max-w-2xl 
                ">
                    <Link href="/">
                        <Image 
                            src={icon}
                            alt="Patli brand"
                            className='h-14 w-auto'
                        />
                    </Link> 
                    <ul className="flex flex-row justify-center items-center gap-4 max-[768px]:mx-[-100%]">
                        <li><Link href="/registrar">Registrar</Link></li>
                        <li><Link href="/login">Inicio de sesión</Link></li>
                    </ul>
                </div>
            </nav> 
        )
    }

    return(
        <nav className="w-screen fixed top-0">
            <div className="lg:max-w-5xl m-auto w-full flex flex-row items-center justify-between p-2
                max-2xl:max-w-2xl 
            ">
                <Link href="/">
                    <Image 
                        src={icon}
                        alt="Patli brand"
                        className='h-14 w-auto'
                    />
                </Link> 
                <ul className="flex flex-row justify-center items-center gap-4 max-[768px]:mx-[-100%] max-[768px]:flex-col max-[768px]:absolute">
                    <li><Link href="/">Inicio</Link></li>
                    <li><Link href="/">Predecir</Link></li>
                    <li><Link href="/">Estadística</Link></li>
                    <li><Link href="/">Entrenar</Link></li>
                    <li><button onClick={() => auth.logOut()}>Cerrar sesión</button></li>
                </ul>
            </div>
        </nav>
    )
}