import type { Metadata } from "next";
import { Poppins } from 'next/font/google';
import "./globals.css";
import { AuthProvider } from "@/context/AuthProvider";

const poppins = Poppins({
  weight: '400',
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
          {children}
        </AuthProvider>
        <footer className="max-w-[75vw] w-full mx-auto flex justify-center items-center p-20">
          <ul className="flex gap-5">
            <li>
              <a href="" className="flex flex-col justify-center items-center">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="currentColor" className="icon icon-tabler icons-tabler-filled icon-tabler-brand-facebook"><path stroke="none" d="M0 0h24v24H0z" fill="none" /><path d="M18 2a1 1 0 0 1 .993 .883l.007 .117v4a1 1 0 0 1 -.883 .993l-.117 .007h-3v1h3a1 1 0 0 1 .991 1.131l-.02 .112l-1 4a1 1 0 0 1 -.858 .75l-.113 .007h-2v6a1 1 0 0 1 -.883 .993l-.117 .007h-4a1 1 0 0 1 -.993 -.883l-.007 -.117v-6h-2a1 1 0 0 1 -.993 -.883l-.007 -.117v-4a1 1 0 0 1 .883 -.993l.117 -.007h2v-1a6 6 0 0 1 5.775 -5.996l.225 -.004h3z" /></svg>
                <p>
                  Facebook
                </p>
              </a>
            </li>
            <li>
              <a href="" className="flex flex-col justify-center items-center">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="currentColor" className="icon icon-tabler icons-tabler-filled icon-tabler-brand-instagram"><path stroke="none" d="M0 0h24v24H0z" fill="none" /><path d="M16 3a5 5 0 0 1 5 5v8a5 5 0 0 1 -5 5h-8a5 5 0 0 1 -5 -5v-8a5 5 0 0 1 5 -5zm-4 5a4 4 0 0 0 -3.995 3.8l-.005 .2a4 4 0 1 0 4 -4m4.5 -1.5a1 1 0 0 0 -.993 .883l-.007 .127a1 1 0 0 0 1.993 .117l.007 -.127a1 1 0 0 0 -1 -1" /></svg>
                <p>
                  Instagram
                </p>
              </a>
            </li>
            <li>
              <a href="" className="flex flex-col justify-center items-center gap-2">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" className="bi bi-twitter-x" viewBox="0 0 16 16">
                  <path d="M12.6.75h2.454l-5.36 6.142L16 15.25h-4.937l-3.867-5.07-4.425 5.07H.316l5.733-6.57L0 .75h5.063l3.495 4.633L12.601.75Zm-.86 13.028h1.36L4.323 2.145H2.865z" />
                </svg>
                <p>
                  Twitter-X
                </p>
              </a>
            </li>
          </ul>
        </footer>
      </body>
    </html>
  );
}
