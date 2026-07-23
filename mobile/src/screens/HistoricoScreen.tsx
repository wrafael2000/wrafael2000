import React, { useCallback, useState } from "react";
import { useFocusEffect } from "@react-navigation/native";
import {
  ActivityIndicator,
  FlatList,
  RefreshControl,
  StyleSheet,
  Text,
  View,
} from "react-native";
import { listarMeusChamados } from "../services/api";
import { CATEGORIAS, Chamado, STATUS_LABEL, StatusChamado } from "../types/chamado";

const CORES_STATUS: Record<StatusChamado, string> = {
  ABERTO: "#F0AD4E",
  EM_TRIAGEM: "#5BC0DE",
  EM_EXECUCAO: "#0275D8",
  RESOLVIDO: "#0B6E4F",
  CANCELADO: "#999",
};

export default function HistoricoScreen() {
  const [chamados, setChamados] = useState<Chamado[]>([]);
  const [carregando, setCarregando] = useState(true);

  async function carregar() {
    try {
      const dados = await listarMeusChamados();
      setChamados(dados);
    } finally {
      setCarregando(false);
    }
  }

  useFocusEffect(
    useCallback(() => {
      carregar();
    }, [])
  );

  if (carregando) {
    return (
      <View style={styles.centro}>
        <ActivityIndicator size="large" color="#0B6E4F" />
      </View>
    );
  }

  return (
    <FlatList
      style={styles.container}
      contentContainerStyle={styles.lista}
      data={chamados}
      keyExtractor={(item) => item.id}
      refreshControl={<RefreshControl refreshing={false} onRefresh={carregar} />}
      ListEmptyComponent={
        <View style={styles.centro}>
          <Text style={styles.vazioTexto}>Você ainda não registrou nenhuma ocorrência.</Text>
        </View>
      }
      renderItem={({ item }) => {
        const categoria = CATEGORIAS.find((c) => c.valor === item.categoria);
        return (
          <View style={styles.card}>
            <View style={styles.cardTopo}>
              <Text style={styles.categoria}>
                {categoria?.icone} {categoria?.label}
              </Text>
              <View style={[styles.statusBadge, { backgroundColor: CORES_STATUS[item.status] }]}>
                <Text style={styles.statusTexto}>{STATUS_LABEL[item.status]}</Text>
              </View>
            </View>
            <Text style={styles.descricao} numberOfLines={2}>
              {item.descricao}
            </Text>
            <Text style={styles.protocolo}>Protocolo: {item.protocolo}</Text>
          </View>
        );
      }}
    />
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: "#F5F7FA" },
  lista: { padding: 16 },
  centro: { flex: 1, alignItems: "center", justifyContent: "center", padding: 40 },
  vazioTexto: { color: "#666", textAlign: "center" },
  card: {
    backgroundColor: "#fff",
    borderRadius: 12,
    padding: 16,
    marginBottom: 12,
    borderWidth: 1,
    borderColor: "#EEE",
  },
  cardTopo: { flexDirection: "row", justifyContent: "space-between", alignItems: "center" },
  categoria: { fontSize: 15, fontWeight: "600", color: "#1A1A1A" },
  statusBadge: { borderRadius: 12, paddingVertical: 4, paddingHorizontal: 10 },
  statusTexto: { color: "#fff", fontSize: 11, fontWeight: "700" },
  descricao: { fontSize: 13, color: "#555", marginTop: 8 },
  protocolo: { fontSize: 11, color: "#999", marginTop: 10 },
});
