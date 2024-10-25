import { ReactNode } from "react"

export type AuthContextType = {
    tokenUser: string | object;
    setTokenUser: (tokenU: string | object) => void;
}

export type PropChildrenType = {
    children: ReactNode;
}