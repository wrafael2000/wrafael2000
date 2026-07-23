import axios from "axios";
import AsyncStorage from "@react-native-async-storage/async-storage";
import type { CategoriaChamado, Chamado } from "../types/chamado";

export const api = axios.create({
  baseURL: process.env.EXPO_PUBLIC_API_URL ?? "http://localhost:3333",
});

api.interceptors.request.use(async (config) => {
  const token = await AsyncStorage.getItem("@zeladoria:token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

interface NovaOcorrenciaInput {
  categoria: CategoriaChamado;
  descricao: string;
  latitude: number;
  longitude: number;
  fotos: { uri: string; nome: string; tipo: string }[];
}

export async function criarChamado(input: NovaOcorrenciaInput): Promise<Chamado> {
  const formData = new FormData();
  formData.append("categoria", input.categoria);
  formData.append("descricao", input.descricao);
  formData.append("latitude", String(input.latitude));
  formData.append("longitude", String(input.longitude));

  input.fotos.forEach((foto) => {
    // @ts-expect-error — formato exigido pelo React Native para upload multipart
    formData.append("fotos", { uri: foto.uri, name: foto.nome, type: foto.tipo });
  });

  const { data } = await api.post<Chamado>("/api/chamados", formData, {
    headers: { "Content-Type": "multipart/form-data" },
  });
  return data;
}

export async function listarMeusChamados(): Promise<Chamado[]> {
  const { data } = await api.get<Chamado[]>("/api/chamados");
  return data;
}

export async function login(email: string, senha: string) {
  const { data } = await api.post("/api/auth/login", { email, senha });
  return data as { token: string; usuario: { id: string; nome: string; email: string } };
}

export async function cadastrar(nome: string, email: string, senha: string) {
  const { data } = await api.post("/api/auth/cadastro", { nome, email, senha });
  return data as { token: string; usuario: { id: string; nome: string; email: string } };
}
