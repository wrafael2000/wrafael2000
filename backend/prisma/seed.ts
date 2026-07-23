import { CategoriaChamado, PrismaClient } from "@prisma/client";

const prisma = new PrismaClient();

const secretarias: { nome: string; categorias: CategoriaChamado[]; slaHoras: number }[] = [
  { nome: "Secretaria de Obras e Viação", categorias: [CategoriaChamado.PAVIMENTACAO], slaHoras: 120 },
  { nome: "Secretaria de Iluminação Pública", categorias: [CategoriaChamado.ILUMINACAO], slaHoras: 48 },
  { nome: "Secretaria de Meio Ambiente", categorias: [CategoriaChamado.COLETA_LIXO, CategoriaChamado.ARBORIZACAO], slaHoras: 72 },
  { nome: "Secretaria de Segurança Pública", categorias: [CategoriaChamado.RISCO_SEGURANCA], slaHoras: 24 },
  { nome: "Secretaria de Saneamento", categorias: [CategoriaChamado.SANEAMENTO], slaHoras: 96 },
  { nome: "Ouvidoria Geral", categorias: [CategoriaChamado.OUTROS], slaHoras: 120 },
];

async function main() {
  for (const secretaria of secretarias) {
    await prisma.secretaria.upsert({
      where: { nome: secretaria.nome },
      update: { categorias: secretaria.categorias, slaHoras: secretaria.slaHoras },
      create: secretaria,
    });
  }
  console.log(`Seed concluído: ${secretarias.length} secretarias.`);
}

main()
  .catch((err) => {
    console.error(err);
    process.exit(1);
  })
  .finally(() => prisma.$disconnect());
