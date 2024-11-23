"use client"

import Link from "next/link"
import Image from "next/image"
import brandP from "/public/icon.svg"
import { useRouter } from "next/navigation"
import React, { useState } from "react"
import { LoginType } from "@/types/types"
import { useAuth } from "@/hooks/useAuth"

const LoginForm = () => {
    const auth = useAuth()
    const router = useRouter()
    const [values, setValues] = useState<LoginType>({
        email:"",
        password:""
    })

    const handleSubmit = async (e: React.SyntheticEvent<HTMLFormElement>) => {
        e.preventDefault()
        try {
            const response = await fetch(process.env.NEXT_PUBLIC_RUTA_BACKEND+"usuario/login/",{
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body:JSON.stringify(values)
            })
            const res = await response.json() 
            console.log(res.user.nombres)
            auth?.setUser(res.user)
            auth?.setTokenUser(res.token)
            localStorage.setItem("Authorization",res.token)   
            localStorage.setItem("User",JSON.stringify(res.user)) //convirtiendo el objeto a string  
            console.log(localStorage.getItem("User"))
            router.push('dashboard/')   
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
            <main className="w-screen mt-[90px]">
                <section className="sectionForm max-w-[600px] w-[55%] h-[75vh] mx-auto flex gap-4 justify-center items-center flex-col
                   p-10
                ">
                    <div className="w-[30%]">
                        <Image
                            src={brandP}
                            alt="logo patli"
                        />
                    </div>
                    <h2 className="text-[#aaa] text-xl">Inciar sesión</h2>
                    <form className="flex flex-col gap-4 w-full p-2" method="post" onSubmit={handleSubmit}>
                        <div className="flex flex-col">
                            <input className="rounded-md p-2 focus:border-[#7DFABB] bg-[#282A29] 
                                border-2 border-[#666666] duration-500 w-full
                                " type="email" 
                                placeholder="nombre@email.com" 
                                name="email" 
                                value={values.email}
                                onChange={handleChange}/>
                        </div>
                        <div className="flex flex-col">
                            <input
                                className="rounded-md p-2 focus:border-[#7DFABB] bg-[#282A29] 
                                border-2 border-[#666666] duration-500"
                                type="password" 
                                placeholder="Contraseña" 
                                name="password" 
                                value={values.password}
                                onChange={handleChange}/>
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