import type { LayerId } from "../types";

type Props = {
  visiveis: Record<LayerId, boolean>;
  onToggle: (layer: LayerId, value: boolean) => void;
};

const LABELS: Record<LayerId, string> = {
  propriedades: "Imóveis",
  restricoes: "Restrições",
};

export function LayerControl({ visiveis, onToggle }: Props) {
  return (
    <div className="absolute left-4 top-4 z-10 rounded-lg bg-white/90 p-3 shadow-md backdrop-blur">
      <h2 className="mb-2 text-sm font-semibold text-gray-700">Camadas</h2>
      <div className="flex flex-col gap-1">
        {(Object.keys(LABELS) as LayerId[]).map((layer) => (
          <label
            key={layer}
            className="flex cursor-pointer items-center gap-2 text-sm text-gray-800"
          >
            <input
              type="checkbox"
              checked={visiveis[layer]}
              onChange={(e) => onToggle(layer, e.target.checked)}
            />
            {LABELS[layer]}
          </label>
        ))}
      </div>
    </div>
  );
}
