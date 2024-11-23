"use client"

import { createContext, useState, useEffect } from "react"
import { PropChildrenType, AuthContextType, UserType } from "@/types/types"

export const AuthContext = createContext<AuthContextType | null>(null)

export const AuthProvider: React.FC<PropChildrenType> = ({ children}) => {
    const [user,setUser] = useState<UserType>({
        id: '',
        email: '',
        nombres: '',
        apellido_pa: '',
        apellido_ma: '',
        numero_celular: ''
    })
    const [tokenUser, setTokenUser] = useState<string | null>(null)
    useEffect(() => {
        if (typeof window !== "undefined") {
            const savedToken = localStorage.getItem("Authorization");
            const savedUser = localStorage.getItem("User");
            if (savedToken && savedUser) {
                setTokenUser(savedToken);
                setUser(JSON.parse(savedUser)) //convirtiendo el string a objeto
            }
        }
    }, []);

    const logOut = () => {
        setUser({
            id: '',
            email: '',
            nombres: '',
            apellido_pa: '',
            apellido_ma: '',
            numero_celular: ''
        })
        setTokenUser(null)
        localStorage.removeItem('User')
        localStorage.removeItem('Authorization')
    }

    return(
        <AuthContext.Provider value={{user,setUser,tokenUser,setTokenUser,logOut}} >
            {children}
        </AuthContext.Provider>
    )
}