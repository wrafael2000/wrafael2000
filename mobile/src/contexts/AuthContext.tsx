import React, { createContext, useContext, useEffect, useState } from "react";
import AsyncStorage from "@react-native-async-storage/async-storage";
import * as api from "../services/api";

interface Usuario {
  id: string;
  nome: string;
  email: string;
}

interface AuthContextValue {
  usuario: Usuario | null;
  carregando: boolean;
  entrar: (email: string, senha: string) => Promise<void>;
  registrar: (nome: string, email: string, senha: string) => Promise<void>;
  sair: () => Promise<void>;
}

const AuthContext = createContext<AuthContextValue | null>(null);

const TOKEN_KEY = "@zeladoria:token";
const USUARIO_KEY = "@zeladoria:usuario";

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [usuario, setUsuario] = useState<Usuario | null>(null);
  const [carregando, setCarregando] = useState(true);

  useEffect(() => {
    AsyncStorage.getItem(USUARIO_KEY).then((raw) => {
      if (raw) setUsuario(JSON.parse(raw));
      setCarregando(false);
    });
  }, []);

  async function persistirSessao(token: string, usuarioLogado: Usuario) {
    await AsyncStorage.setItem(TOKEN_KEY, token);
    await AsyncStorage.setItem(USUARIO_KEY, JSON.stringify(usuarioLogado));
    setUsuario(usuarioLogado);
  }

  async function entrar(email: string, senha: string) {
    const { token, usuario: usuarioLogado } = await api.login(email, senha);
    await persistirSessao(token, usuarioLogado);
  }

  async function registrar(nome: string, email: string, senha: string) {
    const { token, usuario: usuarioLogado } = await api.cadastrar(nome, email, senha);
    await persistirSessao(token, usuarioLogado);
  }

  async function sair() {
    await AsyncStorage.multiRemove([TOKEN_KEY, USUARIO_KEY]);
    setUsuario(null);
  }

  return (
    <AuthContext.Provider value={{ usuario, carregando, entrar, registrar, sair }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth deve ser usado dentro de um AuthProvider");
  return ctx;
}
