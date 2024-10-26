"use client"

import { createContext, useState } from "react"
import { PropChildrenType, AuthContextType, UserType, LoginType } from "@/types/types"

export const AuthContext = createContext<AuthContextType | null>(null)

export const AuthProvider: React.FC<PropChildrenType> = ({ children}) => {
    const [user,setUser] = useState<UserType>({
        id: null,
        email: null,
        nombres: null,
        apellido_pa: null,
        apellido_ma: null,
        numero_celular: null
    })
    const [tokenUser, setTokenUser] = useState<string | null>(null)

    const loginFunction = async ({email, password}:LoginType) => {
        try {
            const response = await fetch(process.env.NEXT_PUBLIC_RUTA_BACKEND+"usuario/login/",{
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body:JSON.stringify({email,password})
            })
            const res = await response.json() 
            if(res.user && res.token) {
                setUser(res.user)
                setTokenUser(res.token)
                localStorage.setItem("Authorization",res.token)
            }
        } catch (error) {
            console.log(error)
        }
    }

    return(
        <AuthContext.Provider value={{loginFunction, user,setUser,tokenUser,setTokenUser}} >
            {children}
        </AuthContext.Provider>
    )
}