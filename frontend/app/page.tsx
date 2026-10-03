"use client"

import { Button } from "@/components/ui/button";
import { useEffect, useState } from "react";
import ElementForm from "./createEntities/createEntities";
import { formEstacao as fe, formLine as fl, formConections as fc, FormConfig } from "./createEntities/forms";
import { type MapLine, url } from "./constrants";
import RailMap from "@/components/railMap";


export default function Home() {
  const [lines, setLines] = useState<MapLine[]>([]);
  const [mapMessage, setMapMessage] = useState("Carregando mapa...");
  const [formEstacao, setFormEstacao] = useState<FormConfig>(fe);
  const [formLinha, setFormLinha] = useState<FormConfig>(fl);
  const [formConeccao, setFormConeccao] = useState<FormConfig>(fc);
  const [forms, setForms] = useState<number>(-1);

  const states = [
    [formEstacao, setFormEstacao],
    [formLinha, setFormLinha],
    [formConeccao, setFormConeccao]
  ] as const;

  useEffect(() => {
    const controller = new AbortController();

    async function loadMap() {
      try {
        const result = await fetch(`${url}map`, { signal: controller.signal });
        if (!result.ok) throw new Error(`HTTP ${result.status}`);
        const data: { lines: MapLine[] } = await result.json();
        if (controller.signal.aborted) return;
        setLines(data.lines);
        setMapMessage("");
      } catch {
        if (!controller.signal.aborted) {
          setMapMessage("Não foi possível carregar o mapa.");
        }
      }
    }

    loadMap();
    return () => controller.abort();
  }, []);


  function findAtual() {
    return (states[forms])
  }


  function handleChange(nome: string, value: string | number) {
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

        <RailMap lines={lines} message={mapMessage} />
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
            <Button className="w-full" onClick={() => setForms(2)}>
              Criar Conexão
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
