export type CategoriaChamado =
  | "ILUMINACAO"
  | "PAVIMENTACAO"
  | "COLETA_LIXO"
  | "RISCO_SEGURANCA"
  | "ARBORIZACAO"
  | "SANEAMENTO"
  | "OUTROS";

export type StatusChamado = "ABERTO" | "EM_TRIAGEM" | "EM_EXECUCAO" | "RESOLVIDO" | "CANCELADO";

export const CATEGORIAS: { valor: CategoriaChamado; label: string; icone: string }[] = [
  { valor: "ILUMINACAO", label: "Iluminação", icone: "💡" },
  { valor: "PAVIMENTACAO", label: "Pavimentação", icone: "🛣️" },
  { valor: "COLETA_LIXO", label: "Coleta de Lixo", icone: "🗑️" },
  { valor: "RISCO_SEGURANCA", label: "Risco de Segurança", icone: "⚠️" },
  { valor: "ARBORIZACAO", label: "Arborização", icone: "🌳" },
  { valor: "SANEAMENTO", label: "Saneamento", icone: "🚰" },
  { valor: "OUTROS", label: "Outros", icone: "📋" },
];

export const STATUS_LABEL: Record<StatusChamado, string> = {
  ABERTO: "Aberto",
  EM_TRIAGEM: "Em Triagem",
  EM_EXECUCAO: "Em Execução",
  RESOLVIDO: "Resolvido",
  CANCELADO: "Cancelado",
};

export interface Foto {
  id: string;
  url: string;
}

export interface Chamado {
  id: string;
  protocolo: string;
  categoria: CategoriaChamado;
  descricao: string;
  status: StatusChamado;
  latitude: number;
  longitude: number;
  endereco?: string | null;
  fotos: Foto[];
  createdAt: string;
}
