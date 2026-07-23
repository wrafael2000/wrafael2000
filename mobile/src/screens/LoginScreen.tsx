import React, { useState } from "react";
import {
  ActivityIndicator,
  Alert,
  StyleSheet,
  Text,
  TextInput,
  TouchableOpacity,
  View,
} from "react-native";
import { useAuth } from "../contexts/AuthContext";

export default function LoginScreen({ navigation }: { navigation: any }) {
  const { entrar } = useAuth();
  const [email, setEmail] = useState("");
  const [senha, setSenha] = useState("");
  const [carregando, setCarregando] = useState(false);

  async function handleEntrar() {
    if (!email || !senha) {
      Alert.alert("Preencha os campos", "Informe e-mail e senha para continuar.");
      return;
    }
    setCarregando(true);
    try {
      await entrar(email, senha);
    } catch {
      Alert.alert("Erro ao entrar", "E-mail ou senha inválidos.");
    } finally {
      setCarregando(false);
    }
  }

  return (
    <View style={styles.container}>
      <Text style={styles.titulo}>Zeladoria SJP</Text>
      <Text style={styles.subtitulo}>Entre para registrar e acompanhar suas ocorrências</Text>

      <TextInput
        style={styles.input}
        placeholder="E-mail"
        autoCapitalize="none"
        keyboardType="email-address"
        value={email}
        onChangeText={setEmail}
      />
      <TextInput
        style={styles.input}
        placeholder="Senha"
        secureTextEntry
        value={senha}
        onChangeText={setSenha}
      />

      <TouchableOpacity style={styles.botao} onPress={handleEntrar} disabled={carregando}>
        {carregando ? <ActivityIndicator color="#fff" /> : <Text style={styles.botaoTexto}>Entrar</Text>}
      </TouchableOpacity>

      <TouchableOpacity onPress={() => navigation.navigate("Cadastro")}>
        <Text style={styles.link}>Ainda não tem conta? Cadastre-se</Text>
      </TouchableOpacity>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, justifyContent: "center", padding: 24, backgroundColor: "#F5F7FA" },
  titulo: { fontSize: 28, fontWeight: "700", textAlign: "center", color: "#0B6E4F" },
  subtitulo: { fontSize: 14, color: "#666", textAlign: "center", marginTop: 8, marginBottom: 32 },
  input: {
    backgroundColor: "#fff",
    borderWidth: 1,
    borderColor: "#DDD",
    borderRadius: 10,
    padding: 14,
    marginBottom: 12,
  },
  botao: { backgroundColor: "#0B6E4F", borderRadius: 12, paddingVertical: 16, alignItems: "center", marginTop: 8 },
  botaoTexto: { color: "#fff", fontWeight: "700", fontSize: 16 },
  link: { textAlign: "center", color: "#0B6E4F", marginTop: 20, fontSize: 13 },
});
