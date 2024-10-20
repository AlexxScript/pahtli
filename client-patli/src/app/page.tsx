import Image from "next/image";
import logo from "/public/icon.svg"

export default function Home() {
  return (
    <div className="">
      <main className="max-w-5xl mx-auto grid grid-cols-6 gap-2">
        <div className="col-start-2 col-span-4 flex justify-center items-center flex-col h-screen">
          <Image 
            src={logo}
            alt="Patli"
          />
          <h1 className="font-bold">Prediciendo hoy para proteger tu mañana</h1>
        </div>

        <div className="col-start-1 col-span-3">Mision</div>
        <div className="">Vision</div>
        <div className="">Valores</div>
        <div className="">otro</div>
      </main>
    </div>
  );
}
