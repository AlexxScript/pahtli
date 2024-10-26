import Link from "next/link"
import Image from "next/image"
import brandP from "/public/icon.svg"

const RegistrarForm = () => {
    return (
        <>
            <main className="mt-[90px]">
                <section className="sectionForm max-w-[700px] w-[75%] mx-auto flex gap-2 justify-center items-center flex-col
                p-10
                ">
                    <div className="w-[30%]">
                        <Image
                            src={brandP}
                            alt="logo patli"
                        />
                    </div>
                    <h2 className="text-[#aaa] text-xl">Registrar</h2>
                    <form className="flex flex-col gap-3 max-w-[600px]" method="post">

                        <div className="flex flex-col">
                            <input className="rounded-md p-2 focus:border-[#7DFABB] bg-[#282A29] 
                            border-2 border-[#666666] duration-500
                            " type="email" placeholder="nombre@email.com" />
                        </div>

                        <div className="flex flex-row gap-2 justify-center">
                            <input className="rounded-md p-2 focus:border-[#7DFABB] bg-[#282A29] 
                            border-2 border-[#666666] duration-500 w-1/3
                            " type="text" placeholder="Nombre" />
                            <input
                                className="rounded-md p-2 focus:border-[#7DFABB] bg-[#282A29] 
                                border-2 border-[#666666] duration-500 w-1/3"
                                type="text" placeholder="Apellido paterno" />
                            <input
                                className="rounded-md p-2 focus:border-[#7DFABB] bg-[#282A29] 
                                border-2 border-[#666666] duration-500 w-1/3"
                                type="text" placeholder="Apellido materno" />
                        </div>
                        <div className="flex flex-col">
                            <input className="rounded-md p-2 focus:border-[#7DFABB] bg-[#282A29] 
                            border-2 border-[#666666] duration-500
                            " type="text" placeholder="Número telefónico" />
                        </div>
                        <div className="flex flex-row gap-2">
                            <input className="rounded-md p-2 focus:border-[#7DFABB] bg-[#282A29] 
                            border-2 border-[#666666] duration-500 w-1/2
                            " type="password" placeholder="password" />
                            <input className="rounded-md p-2 focus:border-[#7DFABB] bg-[#282A29] 
                            border-2 border-[#666666] duration-500 w-1/2
                            " type="password" placeholder="Confirmar password"/>
                        </div>
                        <div className="flex justify-center items-center">
                            <input type="submit" value="Registrar"
                                className="p-2 bg-[#7DFABB] rounded-md text-[#2e2e2e] hover:bg-[#4ea077]
                                duration-300 cursor-pointer" />
                        </div>
                    </form>
                    <p className="text-sm text-zinc-500">¿Ya tienes una cuenta? <Link href="/login">
                        <b className="text-[#7dfabb] hover:text-[#4ea077] duration-300">Presiona aquí</b></Link></p>
                </section>
            </main>
        </>
    )
}

export default RegistrarForm