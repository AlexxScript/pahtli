import { ReactNode } from "react"

export type UserType = {
    id:number | string | null;
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

export type RegisterType = {
    email:string;
    nombres:string;
    apellido_pa:string;
    apellido_ma:string;
    numero_celular:string;
    password:string;
}

export type AuthContextType = {
    user: UserType;
    setUser: ({id,email,nombres,apellido_pa,apellido_ma,numero_celular}:UserType) => void
    tokenUser: string | object | null;
    setTokenUser: (tokenU: string | null) => void;
    logOut: () => void;
}

export type PropChildrenType = {
    children: ReactNode;
}

export interface FormData {
    edad:string;
    genero:string;
    tipo_dolor_pecho: string;
    presion_arterial_reposo: string;
    colesterol: string;
    azucar_sangre_ayuno: string;
    electrogardiograma_reposo: string;
    frecuencia_cardiaca_maxima: string;
    angina_por_ejercicio: string;
    viejo_pico_ST: string;
    st_slope: string;
}

export interface Prediccion {
  edad: string;
  genero: string;
  angina: string;
  presionA: string;
  colesterol: string;
  azucar: string;
  electrocardio: string;
  FrecuenciaMaxima: string;
  anginaEjercicio: string;
  ViejoPico: string;
  stslope: string;
  prediccion: string;
}