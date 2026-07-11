-- Regra de negócio central: DISSOLVER por cod_car. O shapefile apresenta alguns
-- imóveis em várias feições
--
-- UPSERT (ON CONFLICT cod_car): mantém o `id` ESTÁVEL entre reimportações, para
-- que as FKs de `analises` (histórico auditável) continuem válidas. Idempotente.

BEGIN;

INSERT INTO propriedades (cod_car, municipio, uf, area_ha, metadados, geom)
SELECT
    cod_car,
    municipio,
    uf,
    -- Área geodésica em hectares (geography -> m², /10000 -> ha).
    ST_Area(geom::geography) / 10000.0,
    metadados,
    geom
FROM (
    SELECT
        cod_imovel AS cod_car,
        min(municipio) AS municipio,
        min(uf)        AS uf,
        jsonb_strip_nulls(jsonb_build_object(
            'bioma',            min(bioma),
            'tipo_imovel',      min(tipo_imove),
            'situacao',         min(situacao_a),
            'status',           min(status_imo),
            'temas_ambientais', min(temas_ambi),
            'modulos_fiscais',  min(modulos_ru)
        )) AS metadados,
        -- Dissolve as partes do imóvel, sanea e força MultiPolygon válido.
        ST_Multi(ST_CollectionExtract(ST_Union(ST_MakeValid(geom)), 3)) AS geom
    FROM staging.imoveis_car_raw
    WHERE geom IS NOT NULL
    GROUP BY cod_imovel
) t
WHERE NOT ST_IsEmpty(geom)
ON CONFLICT (cod_car) DO UPDATE SET
    municipio   = EXCLUDED.municipio,
    uf          = EXCLUDED.uf,
    area_ha     = EXCLUDED.area_ha,
    metadados   = EXCLUDED.metadados,
    geom        = EXCLUDED.geom,
    imported_at = now();

-- Sincroniza remoções: imóveis que sumiram da fonte saem do curado.
-- (RESTRICT nas FKs de analises protege histórico de exclusão acidental.)
DELETE FROM propriedades p
WHERE NOT EXISTS (
    SELECT 1 FROM staging.imoveis_car_raw s WHERE s.cod_imovel = p.cod_car
);

COMMIT;
