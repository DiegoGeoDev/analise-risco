-- Seed de restrições SIMULADAS (fonte='SIMULADO') — NÃO são dado oficial.
--
-- Motivo: em Três Lagoas não há sobreposição real com ÁREA entre imóveis e
-- embargos (só slivers de fronteira). Para demonstrar um caso POSITIVO de risco,
-- eu criei embargos fictícios como buffers métricos sobre imóveis reais.
--
-- Rastreabilidade: fonte='SIMULADO'.

BEGIN;

DELETE FROM restricoes WHERE fonte = 'SIMULADO';

-- Cenário 1: embargo INTERNO ao imóvel (parte da propriedade embargada).
WITH alvo AS (
    SELECT cod_car, geom
    FROM propriedades
    WHERE area_ha BETWEEN 200 AND 400
    ORDER BY area_ha
    LIMIT 1
)
INSERT INTO restricoes (tipo, fonte, codigo, nome, metadados, geom)
SELECT
    'EMBARGO_IBAMA', 'SIMULADO', 'SIM-001',
    'Embargo simulado (interno ao imóvel) — demonstração',
    jsonb_build_object(
        'descricao', 'Cenário fictício para demonstrar a análise de risco.',
        'alvo_cod_car', cod_car
    ),
    ST_Multi(ST_Transform(
        ST_Buffer(ST_PointOnSurface(geom)::geography, 400)::geometry, 4674
    ))
FROM alvo;

-- Cenário 2: embargo na BORDA do imóvel (sobreposição parcial).
WITH alvo AS (
    SELECT cod_car, geom
    FROM propriedades
    WHERE area_ha BETWEEN 40 AND 100
    ORDER BY area_ha
    LIMIT 1
)
INSERT INTO restricoes (tipo, fonte, codigo, nome, metadados, geom)
SELECT
    'EMBARGO_IBAMA', 'SIMULADO', 'SIM-002',
    'Embargo simulado (na borda do imóvel) — demonstração',
    jsonb_build_object(
        'descricao', 'Cenário fictício para demonstrar a análise de risco.',
        'alvo_cod_car', cod_car
    ),
    ST_Multi(ST_Transform(
        ST_Buffer(
            ST_PointN(ST_ExteriorRing(ST_GeometryN(geom, 1)), 1)::geography, 300
        )::geometry, 4674
    ))
FROM alvo;

COMMIT;
