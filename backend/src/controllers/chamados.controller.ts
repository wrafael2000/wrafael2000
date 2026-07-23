import { Request, Response } from "express";
import { z } from "zod";
import { CategoriaChamado, StatusChamado } from "@prisma/client";
import { prisma } from "../lib/prisma";

const criarChamadoSchema = z.object({
  categoria: z.nativeEnum(CategoriaChamado),
  descricao: z.string().min(10, "Descreva o problema com pelo menos 10 caracteres."),
  latitude: z.coerce.number().min(-90).max(90),
  longitude: z.coerce.number().min(-180).max(180),
  endereco: z.string().optional(),
});

/**
 * Resolve a secretaria responsável por uma categoria de chamado.
 * Ponto de extensão para a futura triagem automática via IA (ver README > Roadmap).
 */
async function resolveSecretariaPorCategoria(categoria: CategoriaChamado) {
  return prisma.secretaria.findFirst({
    where: { categorias: { has: categoria } },
  });
}

// POST /api/chamados — cria um novo chamado (entregável principal desta iteração)
export async function criarChamado(req: Request, res: Response) {
  const parsed = criarChamadoSchema.safeParse(req.body);
  if (!parsed.success) {
    return res.status(400).json({ error: "Dados inválidos.", detalhes: parsed.error.flatten() });
  }

  const { categoria, descricao, latitude, longitude, endereco } = parsed.data;
  const cidadaoId = req.user!.sub;

  const secretaria = await resolveSecretariaPorCategoria(categoria);
  const prazoLimite = secretaria
    ? new Date(Date.now() + secretaria.slaHoras * 60 * 60 * 1000)
    : null;

  const arquivos = (req.files as Express.Multer.File[] | undefined) ?? [];

  const chamado = await prisma.chamado.create({
    data: {
      categoria,
      descricao,
      latitude,
      longitude,
      endereco,
      cidadaoId,
      secretariaId: secretaria?.id,
      prazoLimite,
      fotos: {
        create: arquivos.map((file) => ({ url: `/uploads/${file.filename}` })),
      },
      historico: {
        create: { statusNovo: StatusChamado.ABERTO, alteradoPorId: cidadaoId },
      },
    },
    include: { fotos: true, secretaria: true },
  });

  return res.status(201).json(chamado);
}

// GET /api/chamados — lista chamados do cidadão autenticado (ou todos, se admin)
export async function listarChamados(req: Request, res: Response) {
  const { status } = req.query;
  const isGestao = req.user!.role === "ADMIN" || req.user!.role === "SECRETARIA";

  const chamados = await prisma.chamado.findMany({
    where: {
      status: status ? (status as StatusChamado) : undefined,
      cidadaoId: isGestao ? undefined : req.user!.sub,
    },
    include: { fotos: true, secretaria: true },
    orderBy: { createdAt: "desc" },
  });

  return res.json(chamados);
}

// GET /api/chamados/:id — detalhe de um chamado, incluindo histórico de status
export async function obterChamado(req: Request, res: Response) {
  const chamado = await prisma.chamado.findUnique({
    where: { id: req.params.id },
    include: { fotos: true, secretaria: true, historico: { orderBy: { createdAt: "asc" } } },
  });

  if (!chamado) {
    return res.status(404).json({ error: "Chamado não encontrado." });
  }

  return res.json(chamado);
}

const atualizarStatusSchema = z.object({
  status: z.nativeEnum(StatusChamado),
  observacao: z.string().optional(),
});

// PATCH /api/chamados/:id/status — uso da gestão municipal para avançar o chamado no fluxo
export async function atualizarStatusChamado(req: Request, res: Response) {
  const parsed = atualizarStatusSchema.safeParse(req.body);
  if (!parsed.success) {
    return res.status(400).json({ error: "Dados inválidos.", detalhes: parsed.error.flatten() });
  }

  const chamadoAtual = await prisma.chamado.findUnique({ where: { id: req.params.id } });
  if (!chamadoAtual) {
    return res.status(404).json({ error: "Chamado não encontrado." });
  }

  const { status, observacao } = parsed.data;

  const chamado = await prisma.chamado.update({
    where: { id: req.params.id },
    data: {
      status,
      historico: {
        create: {
          statusAnterior: chamadoAtual.status,
          statusNovo: status,
          observacao,
          alteradoPorId: req.user!.sub,
        },
      },
    },
    include: { fotos: true, secretaria: true },
  });

  return res.json(chamado);
}
