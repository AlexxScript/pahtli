"use client"

import { createContext, useState } from "react"
import { PropChildrenType, AuthContextType, UserType } from "@/types/types"

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
    return(
        <AuthContext.Provider value={{user,setUser,tokenUser,setTokenUser}} >
            {children}
        </AuthContext.Provider>
    )
}