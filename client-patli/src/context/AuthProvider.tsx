"use client"

import { createContext, useState } from "react"
import { PropChildrenType, AuthContextType } from "@/types/types"

export const AuthContext = createContext<AuthContextType | null>(null)

export const AuthProvider: React.FC<PropChildrenType> = ({ children}) => {
    const [tokenUser, setTokenUser] = useState<AuthContextType>()

    return(
        <AuthContext.Provider value={{tokenUser, setTokenUser}} >
            {children}
        </AuthContext.Provider>
    )
}