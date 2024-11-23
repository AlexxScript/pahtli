import type { Metadata } from "next";
import {Poppins} from 'next/font/google';
import "./globals.css";
import { NavBar } from "@/components/NavBar";
import { AuthProvider } from "@/context/AuthProvider";

const poppins = Poppins({ 
  weight:'400',
  subsets: ['latin']
})

export const metadata: Metadata = {
  title: "Patli",
  description: "Aplicación web para el análisis de datos para la predicción y descubrimiento de patrones a través de las biológicas",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body
        suppressHydrationWarning={true}
        className={`${poppins.className}`}
      >
        <AuthProvider>
          <NavBar/>
          {children}
        </AuthProvider>
        <footer>
          footer
        </footer>
      </body>
    </html>
  );
}
