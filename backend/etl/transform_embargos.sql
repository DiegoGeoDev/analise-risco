BEGIN;

DELETE FROM restricoes WHERE tipo = 'EMBARGO_IBAMA' AND fonte = 'IBAMA';

WITH src AS (
    SELECT
        num_tad                              AS codigo,
        COALESCE(nome_embar, nome_imove)     AS nome,
        uf, municipio, nome_embar, num_auto_i, des_infrac,
        tipo_area, sit_desmat, dat_embarg, qtd_area_e,
        ST_Multi(ST_CollectionExtract(ST_MakeValid(geom), 3)) AS geom
    FROM staging.embargos_ibama_raw
    WHERE uf = 'MS'
      AND geom IS NOT NULL
)
INSERT INTO restricoes (tipo, fonte, codigo, nome, metadados, geom)
SELECT
    'EMBARGO_IBAMA',
    'IBAMA',
    codigo,
    nome,
    jsonb_strip_nulls(jsonb_build_object(
        'uf',                 uf,
        'municipio',          municipio,
        'nome_embargado',     nome_embar,
        'num_auto_infracao',  num_auto_i,
        'des_infracao',       des_infrac,
        'tipo_area',          tipo_area,
        'sit_desmatamento',   sit_desmat,
        'data_embargo',       dat_embarg,
        'area_embargada_ha',  qtd_area_e
    )),
    geom
FROM src
WHERE NOT ST_IsEmpty(geom);

COMMIT;
