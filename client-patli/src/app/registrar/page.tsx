"use client"
import Link from "next/link"
import Image from "next/image"
import brandP from "/public/icon.svg"
import React, { useState, useEffect } from "react"
import { RegisterType } from "@/types/types"
import { useRouter } from "next/navigation"
import { useAuth } from "@/hooks/useAuth"

const RegistrarForm = () => {
    const auth = useAuth()
    const router = useRouter();
    const [values, setValues] = useState<RegisterType>({
        email:'',
        nombres:'',
        apellido_pa:'',
        apellido_ma:'',
        numero_celular:'',
        password:'',
    });
    useEffect(() => {
        if(auth?.tokenUser) router.push('/dashboard')
    },[auth, router])

    const handleSubmit = async (e: React.SyntheticEvent<HTMLFormElement>) => {
        e.preventDefault()
        try {
            const response = await fetch(process.env.NEXT_PUBLIC_RUTA_BACKEND+"usuario/registrar/",{
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body:JSON.stringify(values)
            })
            const res = await response.json()
            if (res.token) {
                router.push('/login')
            }

        } catch (error) {
            console.log(error)
        }
    }

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setValues({
            ...values,
            [e.target.name]:e.target.value
        })
    }

    return (
        <>
            <main className="mt-[90px]">
                <section className="sectionForm max-w-[600px] w-[75%] mx-auto flex gap-2 justify-center items-center flex-col
                p-10
                ">
                    <div className="w-[30%]">
                        <Image
                            src={brandP}
                            alt="logo patli"
                        />
                    </div>
                    <h2 className="text-[#aaa] text-xl">Registrar</h2>
                    <form className="flex flex-col gap-2 w-full" method="post" onSubmit={handleSubmit}>

                        <div className="flex flex-col">
                            <input className="rounded-md p-2 focus:border-[#7DFABB] bg-[#282A29] 
                            border-2 border-[#666666] duration-500
                            " type="email" placeholder="nombre@email.com" name="email" value={values.email} onChange={handleChange}/>
                        </div>

                        <div className="flex flex-row gap-2 justify-center max-[600px]:flex-col">
                            <input className="rounded-md p-2 focus:border-[#7DFABB] bg-[#282A29] 
                            border-2 border-[#666666] duration-500 w-1/3 max-[600px]:w-full
                            " type="text" placeholder="Nombre" name="nombres" value={values.nombres} onChange={handleChange}/>
                            <input
                                className="rounded-md p-2 focus:border-[#7DFABB] bg-[#282A29] 
                                border-2 border-[#666666] duration-500 w-1/3 max-[600px]:w-full"
                                type="text" placeholder="Apellido paterno" name="apellido_pa" value={values.apellido_pa} onChange={handleChange}/>
                            <input
                                className="rounded-md p-2 focus:border-[#7DFABB] bg-[#282A29] 
                                border-2 border-[#666666] duration-500 w-1/3 max-[600px]:w-full"
                                type="text" placeholder="Apellido materno" name="apellido_ma" value={values.apellido_ma} onChange={handleChange}/>
                        </div>
                        <div className="flex flex-col ">
                            <input className="rounded-md p-2 focus:border-[#7DFABB] bg-[#282A29] 
                            border-2 border-[#666666] duration-500
                            " type="text" placeholder="Número telefónico" name="numero_celular" value={values.numero_celular} onChange={handleChange}/>
                        </div>
                        <div className="flex flex-row gap-2  max-[600px]:flex-col">
                            <input className="rounded-md p-2 focus:border-[#7DFABB] bg-[#282A29] 
                            border-2 border-[#666666] duration-500 w-1/2 max-[600px]:w-full
                            " type="password" placeholder="password" name="password" value={values.password} onChange={handleChange}/>
                            <input className="rounded-md p-2 focus:border-[#7DFABB] bg-[#282A29] 
                            border-2 border-[#666666] duration-500 w-1/2 max-[600px]:w-full
                            " type="password" placeholder="Confirmar password" name="confirm_password" />
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