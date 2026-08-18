import LoginTemplate from "@/components/loginTemplate";
import { createUser } from "@/app/action"

export default function Home() {
  return (
    <div className="flex flex-1 items-center justify-center font-sans bg-black">
      <div className="flex flex-col flex-1 items-center justify-center max-w-sm gap-4">
        <h1 className="text-3xl font-semibold">RailForge</h1>
        <h2 className="text-2xl font-semibold">Fazer Login</h2>
        <LoginTemplate redirect="createUser" mainButton="Logar" secundaryButton="Não tenho usuário" func={createUser} />
      </div>
    </div >
  );
}
