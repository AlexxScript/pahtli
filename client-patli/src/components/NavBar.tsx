'use client';

import Image from "next/image";
import Link from "next/link";
import icon from "../../public/icon.svg"
// import { PatliNav } from "@/icons/PatliNav";

export const NavBar = () => {
    return(
        <ul>
            <li>
                <Link href="/" className="w-screen">
                    <Image 
                        src={icon}
                        alt="Patli brand"
                        className='w-20 h-20 fill-white'
                    />
                </Link>
            </li>
            <li><Link href="/">Registrar</Link></li>
            <li><Link href="/">Inicio de sesión</Link></li>
        </ul>
    )
}