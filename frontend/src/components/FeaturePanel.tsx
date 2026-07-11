import { useEffect, useState } from "react";
import type { LayerId, SelectedFeature } from "../types";
import { analisarPropriedade, type Analise } from "../api";

type Props = {
  selected: SelectedFeature | null;
  onClose: () => void;
};

const CAMPOS: Record<LayerId, [string, string][]> = {
  propriedades: [
    ["Código CAR", "cod_car"],
    ["Município", "municipio"],
    ["UF", "uf"],
    ["Área (ha)", "area_ha"],
  ],
  restricoes: [
    ["Tipo", "tipo"],
    ["Fonte", "fonte"],
    ["Código", "codigo"],
    ["Nome", "nome"],
  ],
};

const TITULOS: Record<LayerId, string> = {
  propriedades: "Imóvel",
  restricoes: "Restrição",
};

const COR_NIVEL: Record<Analise["nivel_risco"], string> = {
  BAIXO: "bg-green-100 text-green-800",
  MEDIO: "bg-amber-100 text-amber-800",
  ALTO: "bg-red-100 text-red-800",
};

function formatar(v: unknown): string {
  if (v == null) return "—";
  if (typeof v === "number")
    return v.toLocaleString("pt-BR", { maximumFractionDigits: 2 });
  return String(v);
}

export function FeaturePanel({ selected, onClose }: Props) {
  const [analise, setAnalise] = useState<Analise | null>(null);
  const [carregando, setCarregando] = useState(false);
  const [erro, setErro] = useState<string | null>(null);

  useEffect(() => {
    setAnalise(null);
    setErro(null);
  }, [selected?.id, selected?.layer]);

  if (!selected) return null;

  const handleAnalisar = async () => {
    setCarregando(true);
    setErro(null);
    try {
      setAnalise(await analisarPropriedade(selected.id));
    } catch (e) {
      setErro(e instanceof Error ? e.message : "Erro desconhecido");
    } finally {
      setCarregando(false);
    }
  };

  return (
    <div className="absolute right-4 top-4 z-10 flex max-h-[85vh] w-80 flex-col overflow-auto rounded-lg bg-white/95 p-4 shadow-lg">
      <div className="mb-3 flex items-center justify-between">
        <h2 className="text-sm font-semibold text-gray-700">
          {TITULOS[selected.layer]}
        </h2>
        <button
          type="button"
          onClick={onClose}
          aria-label="Fechar"
          className="text-gray-400 hover:text-gray-700"
        >
          ✕
        </button>
      </div>

      <dl className="flex flex-col gap-2">
        {CAMPOS[selected.layer].map(([label, key]) => (
          <div key={key} className="flex justify-between gap-3 text-sm">
            <dt className="text-gray-500">{label}</dt>
            <dd className="text-right font-medium text-gray-900 truncate">
              {formatar(selected.props[key])}
            </dd>
          </div>
        ))}
      </dl>

      {selected.layer === "propriedades" && (
        <div className="mt-4 border-t border-gray-200 pt-3">
          <button
            type="button"
            onClick={handleAnalisar}
            disabled={carregando}
            className="w-full rounded-md bg-blue-600 px-3 py-2 text-sm font-medium text-white hover:bg-blue-700 disabled:opacity-50"
          >
            {carregando ? "Analisando…" : "Analisar risco"}
          </button>

          {erro && <p className="mt-2 text-sm text-red-600">{erro}</p>}

          {analise && <ResultadoAnalise analise={analise} />}
        </div>
      )}
    </div>
  );
}

function ResultadoAnalise({ analise }: { analise: Analise }) {
  return (
    <div className="mt-3 flex flex-col gap-3">
      <div className="flex items-center justify-between">
        <span className="text-3xl font-bold text-gray-900">
          {analise.score}
        </span>
        <span
          className={`rounded-full px-2.5 py-1 text-xs font-semibold ${COR_NIVEL[analise.nivel_risco]}`}
        >
          {analise.nivel_risco}
        </span>
      </div>

      <p className="text-sm text-gray-600">
        Área afetada: <strong>{formatar(analise.area_afetada_ha)} ha</strong> (
        {formatar(analise.fatores.pct_afetado)}% do imóvel)
      </p>

      {/* Explicabilidade: os fatores que geraram o score. */}
      {analise.fatores.restricoes.length > 0 && (
        <div>
          <h3 className="mb-1 text-xs font-semibold uppercase text-gray-500">
            Fatores
          </h3>
          <ul className="flex flex-col gap-1">
            {analise.fatores.restricoes.map((r) => (
              <li
                key={r.restricao_id}
                className="rounded bg-gray-50 px-2 py-1 text-xs text-gray-700"
              >
                <span className="font-medium">{r.tipo}</span> - {r.fonte} -{" "}
                {r.codigo ?? "—"} - {formatar(r.area_intersec_ha)} ha (
                {formatar(r.pct_imovel)}%)
              </li>
            ))}
          </ul>
        </div>
      )}

      <p className="text-right text-[10px] text-gray-400">
        regra {analise.versao_algoritmo}
      </p>
    </div>
  );
}
