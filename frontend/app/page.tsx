"use client"

import { Button } from "@/components/ui/button";
import { useState } from "react";
import ElementForm from "./createEntities/createEntities";
import { formEstacao as fe, formLine as fl, FormConfig } from "./createEntities/forms";


export default function Home() {
  const [formEstacao, setFormEstacao] = useState<FormConfig>(fe);
  const [formLinha, setFormLinha] = useState<FormConfig>(fl);
  const [forms, setForms] = useState<number>(-1);

  const states = [
    [formEstacao, setFormEstacao],
    [formLinha, setFormLinha],
  ] as const;


  function findAtual() {
    return (states[forms])
  }


  function handleChange(nome: string, value: string) {
    const set = findAtual()[1];

    set((previous) => ({
      ...previous,
      result: {
        ...(previous.result),
        [nome]: value,
      }
    }));
  }

  return (
    <div className="flex h-dvh">
      <div className="flex h-full w-full flex-col">
        <header className="w-full shrink-0 border-b p-4 border-white">
          <h1>
            Sistema de Gestão de Trens
          </h1>
        </header>

        <svg className="min-h-0 flex-1">
        </svg>
      </div>
      <div className="h-full flex flex-col justify-center border-l border-white p-4">
        {forms === -1 && (
          <>
            <Button className="w-full" onClick={() => setForms(0)}>
              Criar Estação
            </Button>
            <Button className="w-full" onClick={() => setForms(1)}>
              Criar Linha
            </Button>
          </>
        )}

        {forms !== -1 && (
          <ElementForm
            form={findAtual()[0]}
            close={() => setForms(-1)}
            handleChange={handleChange}
          />)}
      </div>
    </div>
  );
}
