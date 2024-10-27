import { ReactNode } from "react"

export type UserType = {
    id:number | null;
    email: string | null;
    nombres: string | null;
    apellido_pa: string | null;
    apellido_ma: string | null;
    numero_celular: string | null;
}

export type LoginType = {
    email: string;
    password: string;
} 

export type AuthContextType = {
    user: UserType;
    setUser: ({id,email,nombres,apellido_pa,apellido_ma,numero_celular}:UserType) => void
    tokenUser: string | object | null;
    setTokenUser: (tokenU: string | null) => void;
}

export type PropChildrenType = {
    children: ReactNode;
}