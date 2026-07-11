export type LayerId = 'propriedades' | 'restricoes'

export type SelectedFeature = {
  layer: LayerId
  id: number
  props: Record<string, unknown>
}
