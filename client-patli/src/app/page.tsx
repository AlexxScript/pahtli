import Image from "next/image";
import logo from "/public/icon.svg"
import ilustration from "/public/ilustrationvector.svg"

export default function Home() {
  return (
    <div className="">
      <main className="max-w-5xl w-full mx-auto grid grid-cols-6 gap-2 max-[1024px]:max-w-3xl">
        <div className="col-start-2 col-span-4 flex justify-center items-center flex-col h-screen">
          <Image 
            src={logo}
            alt="Patli"
          />
          <h1 className="text-center font-bold border-b-2 pb-2 title">Prediciendo hoy para proteger tu mañana</h1>
        </div>

        <div className="col-start-1 col-end-7 flex justify-around items-center">
          <div className="w-[50%] flex justify-center">
            <h2 className="text-3xl">¿Qué es patli?</h2>
          </div>
          <div className="w-[50%]">
            <Image
              src={ilustration}
              alt="Dr ilustration"
            />
          </div> 
        </div>
        <div className="">Vision</div>
        <div className="">Valores</div>
        <div className="">otro</div>
      </main>
    </div>
  );
}
