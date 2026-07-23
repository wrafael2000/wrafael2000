import React, { useEffect, useState } from "react";
import {
  ActivityIndicator,
  Alert,
  Image,
  ScrollView,
  StyleSheet,
  Text,
  TextInput,
  TouchableOpacity,
  View,
} from "react-native";
import * as Location from "expo-location";
import * as ImagePicker from "expo-image-picker";
import { CATEGORIAS, CategoriaChamado } from "../types/chamado";
import { criarChamado } from "../services/api";

type Coordenadas = { latitude: number; longitude: number };
type FotoSelecionada = { uri: string; nome: string; tipo: string };

export default function NovaOcorrenciaScreen({ navigation }: { navigation: any }) {
  const [categoria, setCategoria] = useState<CategoriaChamado | null>(null);
  const [descricao, setDescricao] = useState("");
  const [fotos, setFotos] = useState<FotoSelecionada[]>([]);
  const [coordenadas, setCoordenadas] = useState<Coordenadas | null>(null);
  const [buscandoLocalizacao, setBuscandoLocalizacao] = useState(true);
  const [erroLocalizacao, setErroLocalizacao] = useState<string | null>(null);
  const [enviando, setEnviando] = useState(false);

  useEffect(() => {
    capturarLocalizacao();
  }, []);

  async function capturarLocalizacao() {
    setBuscandoLocalizacao(true);
    setErroLocalizacao(null);
    try {
      const { status } = await Location.requestForegroundPermissionsAsync();
      if (status !== "granted") {
        setErroLocalizacao("Permita o acesso à localização para registrar a ocorrência.");
        return;
      }

      const posicao = await Location.getCurrentPositionAsync({
        accuracy: Location.Accuracy.High,
      });
      setCoordenadas({
        latitude: posicao.coords.latitude,
        longitude: posicao.coords.longitude,
      });
    } catch {
      setErroLocalizacao("Não foi possível obter sua localização. Tente novamente.");
    } finally {
      setBuscandoLocalizacao(false);
    }
  }

  async function adicionarFoto() {
    if (fotos.length >= 5) {
      Alert.alert("Limite atingido", "Você pode anexar até 5 fotos por ocorrência.");
      return;
    }

    const { status } = await ImagePicker.requestCameraPermissionsAsync();
    if (status !== "granted") {
      Alert.alert("Permissão necessária", "Permita o acesso à câmera para anexar fotos.");
      return;
    }

    const resultado = await ImagePicker.launchCameraAsync({
      quality: 0.6,
      allowsEditing: false,
    });

    if (!resultado.canceled && resultado.assets[0]) {
      const asset = resultado.assets[0];
      setFotos((atual) => [
        ...atual,
        { uri: asset.uri, nome: `foto-${Date.now()}.jpg`, tipo: "image/jpeg" },
      ]);
    }
  }

  function removerFoto(uri: string) {
    setFotos((atual) => atual.filter((foto) => foto.uri !== uri));
  }

  function validar(): string | null {
    if (!categoria) return "Selecione uma categoria para o problema.";
    if (descricao.trim().length < 10) return "Descreva o problema com pelo menos 10 caracteres.";
    if (!coordenadas) return "Aguarde a captura da localização ou tente novamente.";
    return null;
  }

  async function enviarOcorrencia() {
    const erro = validar();
    if (erro) {
      Alert.alert("Verifique os dados", erro);
      return;
    }

    setEnviando(true);
    try {
      await criarChamado({
        categoria: categoria!,
        descricao: descricao.trim(),
        latitude: coordenadas!.latitude,
        longitude: coordenadas!.longitude,
        fotos,
      });

      Alert.alert("Ocorrência registrada!", "Você pode acompanhar o status no histórico.", [
        { text: "OK", onPress: () => navigation.navigate("Historico") },
      ]);
    } catch (err) {
      Alert.alert("Erro ao enviar", "Não foi possível registrar a ocorrência. Tente novamente.");
    } finally {
      setEnviando(false);
    }
  }

  return (
    <ScrollView style={styles.container} contentContainerStyle={styles.conteudo}>
      <Text style={styles.titulo}>Nova Ocorrência</Text>
      <Text style={styles.subtitulo}>
        Relate um problema de zeladoria urbana. Sua localização é capturada automaticamente.
      </Text>

      <Text style={styles.rotulo}>Categoria</Text>
      <View style={styles.categoriasGrid}>
        {CATEGORIAS.map((item) => (
          <TouchableOpacity
            key={item.valor}
            style={[styles.categoriaChip, categoria === item.valor && styles.categoriaChipAtiva]}
            onPress={() => setCategoria(item.valor)}
          >
            <Text style={styles.categoriaIcone}>{item.icone}</Text>
            <Text
              style={[
                styles.categoriaLabel,
                categoria === item.valor && styles.categoriaLabelAtiva,
              ]}
            >
              {item.label}
            </Text>
          </TouchableOpacity>
        ))}
      </View>

      <Text style={styles.rotulo}>Descrição do problema</Text>
      <TextInput
        style={styles.textarea}
        multiline
        numberOfLines={4}
        placeholder="Descreva o que está acontecendo, ex: poste apagado há 3 dias na esquina da rua..."
        value={descricao}
        onChangeText={setDescricao}
        maxLength={500}
      />

      <Text style={styles.rotulo}>Localização</Text>
      <View style={styles.localizacaoBox}>
        {buscandoLocalizacao && (
          <View style={styles.localizacaoLinha}>
            <ActivityIndicator size="small" />
            <Text style={styles.localizacaoTexto}>Obtendo sua localização via GPS...</Text>
          </View>
        )}
        {!buscandoLocalizacao && coordenadas && (
          <Text style={styles.localizacaoTexto}>
            📍 Lat {coordenadas.latitude.toFixed(6)}, Lng {coordenadas.longitude.toFixed(6)}
          </Text>
        )}
        {!buscandoLocalizacao && erroLocalizacao && (
          <View>
            <Text style={styles.localizacaoErro}>{erroLocalizacao}</Text>
            <TouchableOpacity onPress={capturarLocalizacao}>
              <Text style={styles.tentarNovamente}>Tentar novamente</Text>
            </TouchableOpacity>
          </View>
        )}
      </View>

      <Text style={styles.rotulo}>Fotos ({fotos.length}/5)</Text>
      <View style={styles.fotosGrid}>
        {fotos.map((foto) => (
          <View key={foto.uri} style={styles.fotoPreview}>
            <Image source={{ uri: foto.uri }} style={styles.fotoImagem} />
            <TouchableOpacity style={styles.fotoRemover} onPress={() => removerFoto(foto.uri)}>
              <Text style={styles.fotoRemoverTexto}>✕</Text>
            </TouchableOpacity>
          </View>
        ))}
        {fotos.length < 5 && (
          <TouchableOpacity style={styles.adicionarFoto} onPress={adicionarFoto}>
            <Text style={styles.adicionarFotoTexto}>+ Foto</Text>
          </TouchableOpacity>
        )}
      </View>

      <TouchableOpacity
        style={[styles.botaoEnviar, enviando && styles.botaoDesabilitado]}
        onPress={enviarOcorrencia}
        disabled={enviando}
      >
        {enviando ? (
          <ActivityIndicator color="#fff" />
        ) : (
          <Text style={styles.botaoEnviarTexto}>Registrar Ocorrência</Text>
        )}
      </TouchableOpacity>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: "#F5F7FA" },
  conteudo: { padding: 20, paddingBottom: 40 },
  titulo: { fontSize: 24, fontWeight: "700", color: "#1A1A1A" },
  subtitulo: { fontSize: 14, color: "#666", marginTop: 4, marginBottom: 20 },
  rotulo: { fontSize: 14, fontWeight: "600", color: "#333", marginBottom: 8, marginTop: 12 },
  categoriasGrid: { flexDirection: "row", flexWrap: "wrap", gap: 8 },
  categoriaChip: {
    flexDirection: "row",
    alignItems: "center",
    borderWidth: 1,
    borderColor: "#DDD",
    borderRadius: 20,
    paddingVertical: 8,
    paddingHorizontal: 12,
    backgroundColor: "#fff",
  },
  categoriaChipAtiva: { backgroundColor: "#0B6E4F", borderColor: "#0B6E4F" },
  categoriaIcone: { marginRight: 6, fontSize: 14 },
  categoriaLabel: { fontSize: 13, color: "#333" },
  categoriaLabelAtiva: { color: "#fff", fontWeight: "600" },
  textarea: {
    backgroundColor: "#fff",
    borderWidth: 1,
    borderColor: "#DDD",
    borderRadius: 10,
    padding: 12,
    minHeight: 100,
    textAlignVertical: "top",
    fontSize: 14,
  },
  localizacaoBox: {
    backgroundColor: "#fff",
    borderWidth: 1,
    borderColor: "#DDD",
    borderRadius: 10,
    padding: 12,
  },
  localizacaoLinha: { flexDirection: "row", alignItems: "center", gap: 8 },
  localizacaoTexto: { fontSize: 13, color: "#333" },
  localizacaoErro: { fontSize: 13, color: "#C0392B" },
  tentarNovamente: { fontSize: 13, color: "#0B6E4F", fontWeight: "600", marginTop: 6 },
  fotosGrid: { flexDirection: "row", flexWrap: "wrap", gap: 10 },
  fotoPreview: { width: 80, height: 80, borderRadius: 10, overflow: "hidden" },
  fotoImagem: { width: "100%", height: "100%" },
  fotoRemover: {
    position: "absolute",
    top: 2,
    right: 2,
    backgroundColor: "rgba(0,0,0,0.6)",
    borderRadius: 10,
    width: 20,
    height: 20,
    alignItems: "center",
    justifyContent: "center",
  },
  fotoRemoverTexto: { color: "#fff", fontSize: 12 },
  adicionarFoto: {
    width: 80,
    height: 80,
    borderRadius: 10,
    borderWidth: 1,
    borderColor: "#BBB",
    borderStyle: "dashed",
    alignItems: "center",
    justifyContent: "center",
  },
  adicionarFotoTexto: { color: "#666", fontSize: 12 },
  botaoEnviar: {
    backgroundColor: "#0B6E4F",
    borderRadius: 12,
    paddingVertical: 16,
    alignItems: "center",
    marginTop: 28,
  },
  botaoDesabilitado: { opacity: 0.6 },
  botaoEnviarTexto: { color: "#fff", fontSize: 16, fontWeight: "700" },
});
