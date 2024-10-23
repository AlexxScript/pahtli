"use client"

import { Header } from "@/components/Header";
import { QueEsSection } from "@/components/InicioUnauth/QueEsSection";

export default function Home() {


  return (
    <>
      <Header />
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1440 320"><path fill="#27272a" fill-opacity="1" d="M0,128L60,128C120,128,240,128,360,122.7C480,117,600,107,720,138.7C840,171,960,245,1080,234.7C1200,224,1320,128,1380,80L1440,32L1440,320L1380,320C1320,320,1200,320,1080,320C960,320,840,320,720,320C600,320,480,320,360,320C240,320,120,320,60,320L0,320Z"></path></svg>
      <main className="bg-[#27272a]">
        <section className="max-w-5xl w-full mx-auto grid grid-cols-6 gap-2 max-[1024px]:max-w-3xl">
          <QueEsSection/> 

          <div className="">Mision</div>
          <div className="">Vision</div>
          <div className="">Valores</div>
          <div className="">otro</div>
        </section>
      </main>
    </>
  );
}
