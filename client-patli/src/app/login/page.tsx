import Link from "next/link"
import Image from "next/image"
import brandP from "/public/icon.svg"

const LoginForm = () => {
    return (
        <>
            <main className="w-screen mt-[90px]">
                <section className="sectionForm max-w-[600px] h-[75vh] w-full mx-auto flex gap-4 justify-center items-center flex-col
                    rounded-lg bg-[#1d1d1d] border-[1px] border-[#E4B1F7] py-1
                ">
                    <div className="w-[30%]">
                        <Image
                            src={brandP}
                            alt="logo patli"
                        />
                    </div>
                    <h2 className="text-[#aaa] text-xl">Inciar sesión</h2>
                    <form className="flex flex-col gap-4" method="post">
                        <div className="flex flex-col">
                            <input className="rounded-md p-2 focus:border-[#7DFABB] bg-[#282A29] 
                        border-2 border-[#666666] duration-500
                        " type="email" placeholder="nombre@email.com" />
                        </div>
                        <div className="flex flex-col">
                            <input
                                className="rounded-md p-2 focus:border-[#7DFABB] bg-[#282A29] 
                        border-2 border-[#666666] duration-500"
                                type="password" placeholder="Contraseña" />
                        </div>
                        <div className="flex justify-center items-center">
                            <input type="submit" value="Iniciar sesión"
                                className="p-2 bg-[#7DFABB] rounded-md text-[#2e2e2e] hover:bg-[#4ea077]
                                duration-300 cursor-pointer" />
                        </div>
                    </form>
                        <p className="text-sm text-zinc-500">¿No tienes una cuenta? <Link href="registrar"> 
                        <b className="text-[#7dfabb] hover:text-[#4ea077] duration-300">Presiona aquí</b></Link></p>
                </section>
            </main>
        </>
    )
}

export default LoginForm