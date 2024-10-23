import Image from "next/image"
import logo from "/public/icon.svg"

export const Header = () => {
    return (
        <header className="mt-[90px] flex justify-center items-center flex-col h-[50vh]">
            <Image
                src={logo}
                alt="Patli"
            />
            <h1 className="text-center font-bold border-b-2 pb-2 title">Prediciendo hoy para proteger tu mañana</h1>
        </header>
    )
}