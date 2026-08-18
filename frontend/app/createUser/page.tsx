import LoginTemplate from "@/components/loginTemplate";
import { login } from "@/app/action"

export default function Home() {
  return (
    <div className="flex flex-1 items-center justify-center font-sans bg-black">
      <div className="flex flex-col flex-1 items-center justify-center max-w-sm gap-4">
        <h1 className="text-3xl font-semibold tracking-tight">RailForge</h1>
        <h2 className="text-2xl font-semibold tracking-tight">Criar Usuário</h2>
        <LoginTemplate redirect="" mainButton="Criar Usuário" secundaryButton="Já tenho Login" func={login} />
      </div>
    </div >
  );
}
