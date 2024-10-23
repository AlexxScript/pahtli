'use client';

import Image from "next/image";
import Link from "next/link";
import icon from "/public/icon.svg"

export const NavBar = () => {
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
                {/* <ul className="flex flex-row justify-center items-center gap-4 max-[768px]:mx-[-100%]">
                    <li><Link href="/">Registrar</Link></li>
                    <li><Link href="/">Inicio de sesión</Link></li>
                </ul> */}
                <ul className="flex flex-row justify-center items-center gap-4 max-[768px]:mx-[-100%] max-[768px]:flex-col max-[768px]:absolute">
                    <li><Link href="/">Inicio</Link></li>
                    <li><Link href="/">Predecir</Link></li>
                    <li><Link href="/">Estadística</Link></li>
                    <li><Link href="/">Entrenar</Link></li>
                    <li><Link href="/">Cerrar sesión</Link></li>
                </ul>
            </div>
        </nav>
        
    )
}