const API_URL = 'http://localhost:8000'

export type FatorRestricao = {
  restricao_id: number
  tipo: string
  fonte: string
  codigo: string | null
  area_intersec_ha: number
  pct_imovel: number
}

export type Analise = {
  id: number
  propriedade_id: number
  score: number
  nivel_risco: 'BAIXO' | 'MEDIO' | 'ALTO'
  area_afetada_ha: number
  fatores: {
    versao: string
    criterio: string
    area_imovel_ha: number
    pct_afetado: number
    restricoes: FatorRestricao[]
  }
  versao_algoritmo: string
  created_at: string
}

export async function analisarPropriedade(id: number): Promise<Analise> {
  const res = await fetch(`${API_URL}/propriedades/${id}/analises`, {
    method: 'POST',
  })
  if (!res.ok) {
    throw new Error(`Falha na análise (HTTP ${res.status})`)
  }
  return res.json()
}
