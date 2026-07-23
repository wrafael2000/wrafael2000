import { useEffect, useState } from "react";

interface Metricas {
  totalAberto: number;
  totalEmTriagem: number;
  totalEmExecucao: number;
  totalResolvido: number;
  chamadosForaDoPrazo: number;
}

// MVP: dados mockados. Próxima iteração: agregar via endpoint dedicado,
// ex. GET /api/chamados/metricas, calculado a partir de Chamado + StatusHistorico.
const METRICAS_MOCK: Metricas = {
  totalAberto: 42,
  totalEmTriagem: 18,
  totalEmExecucao: 25,
  totalResolvido: 137,
  chamadosForaDoPrazo: 6,
};

export default function Dashboard() {
  const [metricas, setMetricas] = useState<Metricas>(METRICAS_MOCK);

  useEffect(() => {
    // Placeholder para a integração real com a API:
    // fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/chamados/metricas`)
    //   .then((res) => res.json())
    //   .then(setMetricas);
  }, []);

  const cards = [
    { label: "Abertos", valor: metricas.totalAberto, cor: "#F0AD4E" },
    { label: "Em Triagem", valor: metricas.totalEmTriagem, cor: "#5BC0DE" },
    { label: "Em Execução", valor: metricas.totalEmExecucao, cor: "#0275D8" },
    { label: "Resolvidos", valor: metricas.totalResolvido, cor: "#0B6E4F" },
    { label: "Fora do prazo", valor: metricas.chamadosForaDoPrazo, cor: "#D9534F" },
  ];

  return (
    <main style={{ fontFamily: "system-ui, sans-serif", padding: 32, background: "#F5F7FA", minHeight: "100vh" }}>
      <h1 style={{ color: "#1A1A1A" }}>Painel de Gestão — Zeladoria SJP</h1>
      <p style={{ color: "#666" }}>Visão geral dos chamados registrados pelos cidadãos.</p>

      <section style={{ display: "flex", gap: 16, flexWrap: "wrap", marginTop: 24 }}>
        {cards.map((card) => (
          <div
            key={card.label}
            style={{
              background: "#fff",
              borderRadius: 12,
              padding: 20,
              minWidth: 160,
              borderTop: `4px solid ${card.cor}`,
              boxShadow: "0 1px 3px rgba(0,0,0,0.08)",
            }}
          >
            <div style={{ fontSize: 32, fontWeight: 700, color: "#1A1A1A" }}>{card.valor}</div>
            <div style={{ fontSize: 13, color: "#666" }}>{card.label}</div>
          </div>
        ))}
      </section>
    </main>
  );
}
