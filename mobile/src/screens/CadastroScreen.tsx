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

export default function CadastroScreen({ navigation }: { navigation: any }) {
  const { registrar } = useAuth();
  const [nome, setNome] = useState("");
  const [email, setEmail] = useState("");
  const [senha, setSenha] = useState("");
  const [carregando, setCarregando] = useState(false);

  async function handleCadastrar() {
    if (!nome || !email || senha.length < 6) {
      Alert.alert("Verifique os dados", "Preencha nome, e-mail e uma senha com 6+ caracteres.");
      return;
    }
    setCarregando(true);
    try {
      await registrar(nome, email, senha);
    } catch {
      Alert.alert("Erro ao cadastrar", "Não foi possível concluir o cadastro. Tente novamente.");
    } finally {
      setCarregando(false);
    }
  }

  return (
    <View style={styles.container}>
      <Text style={styles.titulo}>Criar conta</Text>

      <TextInput style={styles.input} placeholder="Nome completo" value={nome} onChangeText={setNome} />
      <TextInput
        style={styles.input}
        placeholder="E-mail"
        autoCapitalize="none"
        keyboardType="email-address"
        value={email}
        onChangeText={setEmail}
      />
      <TextInput style={styles.input} placeholder="Senha" secureTextEntry value={senha} onChangeText={setSenha} />

      <TouchableOpacity style={styles.botao} onPress={handleCadastrar} disabled={carregando}>
        {carregando ? <ActivityIndicator color="#fff" /> : <Text style={styles.botaoTexto}>Cadastrar</Text>}
      </TouchableOpacity>

      <TouchableOpacity onPress={() => navigation.navigate("Login")}>
        <Text style={styles.link}>Já tem conta? Entrar</Text>
      </TouchableOpacity>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, justifyContent: "center", padding: 24, backgroundColor: "#F5F7FA" },
  titulo: { fontSize: 24, fontWeight: "700", textAlign: "center", color: "#0B6E4F", marginBottom: 32 },
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
