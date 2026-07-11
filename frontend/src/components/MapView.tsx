import { useState } from "react";
import { Map, Source, Layer } from "@vis.gl/react-maplibre";
import type { MapLayerMouseEvent } from "@vis.gl/react-maplibre";
import type { FilterSpecification, StyleSpecification } from "maplibre-gl";
import "maplibre-gl/dist/maplibre-gl.css";
import { LayerControl } from "./LayerControl";
import { FeaturePanel } from "./FeaturePanel";
import type { LayerId, SelectedFeature } from "../types";

const MARTIN_URL = "http://localhost:3000";

const BASE_STYLE: StyleSpecification = {
  version: 8,
  sources: {
    osm: {
      type: "raster",
      tiles: ["https://tile.openstreetmap.org/{z}/{x}/{y}.png"],
      tileSize: 256,
      attribution: "© OpenStreetMap",
    },
  },
  layers: [{ id: "osm", type: "raster", source: "osm" }],
};

// Martin expõe o id como ATRIBUTO (get), não como id de feição do MVT.
const FILTRO_VAZIO: FilterSpecification = ["==", ["get", "id"], -1];

export function MapView() {
  const [visiveis, setVisiveis] = useState<Record<LayerId, boolean>>({
    propriedades: true,
    restricoes: true,
  });
  const [selected, setSelected] = useState<SelectedFeature | null>(null);

  const onToggle = (layer: LayerId, value: boolean) =>
    setVisiveis((v) => ({ ...v, [layer]: value }));

  const onClick = (e: MapLayerMouseEvent) => {
    const f = e.features?.[0];
    if (!f) {
      setSelected(null);
      return;
    }
    setSelected({
      layer: f.sourceLayer as LayerId,
      id: Number(f.properties?.id),
      props: f.properties ?? {},
    });
  };

  const visibility = (layer: LayerId) =>
    (visiveis[layer] ? "visible" : "none") as "visible" | "none";

  const highlightFilter = (layer: LayerId): FilterSpecification =>
    selected?.layer === layer
      ? ["==", ["get", "id"], selected.id]
      : FILTRO_VAZIO;

  return (
    <>
      <Map
        initialViewState={{ longitude: -51.7, latitude: -20.78, zoom: 10 }}
        style={{ width: "100%", height: "100%" }}
        mapStyle={BASE_STYLE}
        interactiveLayerIds={["propriedades-fill", "restricoes-fill"]}
        onClick={onClick}
      >
        <Source
          id="propriedades"
          type="vector"
          url={`${MARTIN_URL}/propriedades`}
        >
          <Layer
            id="propriedades-fill"
            type="fill"
            source-layer="propriedades"
            layout={{ visibility: visibility("propriedades") }}
            paint={{ "fill-color": "#3b82f6", "fill-opacity": 0.08 }}
          />
          <Layer
            id="propriedades-line"
            type="line"
            source-layer="propriedades"
            layout={{ visibility: visibility("propriedades") }}
            paint={{ "line-color": "#2563eb", "line-width": 0.8 }}
          />
          <Layer
            id="propriedades-highlight"
            type="line"
            source-layer="propriedades"
            filter={highlightFilter("propriedades")}
            paint={{ "line-color": "#f59e0b", "line-width": 3 }}
          />
        </Source>

        <Source id="restricoes" type="vector" url={`${MARTIN_URL}/restricoes`}>
          <Layer
            id="restricoes-fill"
            type="fill"
            source-layer="restricoes"
            layout={{ visibility: visibility("restricoes") }}
            paint={{ "fill-color": "#ef4444", "fill-opacity": 0.35 }}
          />
          <Layer
            id="restricoes-line"
            type="line"
            source-layer="restricoes"
            layout={{ visibility: visibility("restricoes") }}
            paint={{ "line-color": "#b91c1c", "line-width": 1 }}
          />
          <Layer
            id="restricoes-highlight"
            type="line"
            source-layer="restricoes"
            filter={highlightFilter("restricoes")}
            paint={{ "line-color": "#f59e0b", "line-width": 3 }}
          />
        </Source>
      </Map>

      <LayerControl visiveis={visiveis} onToggle={onToggle} />
      <FeaturePanel selected={selected} onClose={() => setSelected(null)} />
    </>
  );
}
