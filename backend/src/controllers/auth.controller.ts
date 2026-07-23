import { Request, Response } from "express";
import bcrypt from "bcryptjs";
import jwt from "jsonwebtoken";
import { z } from "zod";
import { prisma } from "../lib/prisma";
import { env } from "../config/env";

const cadastroSchema = z.object({
  nome: z.string().min(2),
  email: z.string().email(),
  senha: z.string().min(6, "A senha deve ter pelo menos 6 caracteres."),
  telefone: z.string().optional(),
});

// POST /api/auth/cadastro
export async function cadastrar(req: Request, res: Response) {
  const parsed = cadastroSchema.safeParse(req.body);
  if (!parsed.success) {
    return res.status(400).json({ error: "Dados inválidos.", detalhes: parsed.error.flatten() });
  }

  const { nome, email, senha, telefone } = parsed.data;

  const existente = await prisma.usuario.findUnique({ where: { email } });
  if (existente) {
    return res.status(409).json({ error: "Já existe um usuário cadastrado com este e-mail." });
  }

  const senhaHash = await bcrypt.hash(senha, 10);
  const usuario = await prisma.usuario.create({
    data: { nome, email, senhaHash, telefone },
  });

  const token = gerarToken(usuario.id, usuario.role);
  return res.status(201).json({
    token,
    usuario: { id: usuario.id, nome: usuario.nome, email: usuario.email, role: usuario.role },
  });
}

const loginSchema = z.object({
  email: z.string().email(),
  senha: z.string().min(1),
});

// POST /api/auth/login
export async function login(req: Request, res: Response) {
  const parsed = loginSchema.safeParse(req.body);
  if (!parsed.success) {
    return res.status(400).json({ error: "Dados inválidos.", detalhes: parsed.error.flatten() });
  }

  const { email, senha } = parsed.data;

  const usuario = await prisma.usuario.findUnique({ where: { email } });
  const senhaValida = usuario ? await bcrypt.compare(senha, usuario.senhaHash) : false;

  if (!usuario || !senhaValida) {
    return res.status(401).json({ error: "E-mail ou senha inválidos." });
  }

  const token = gerarToken(usuario.id, usuario.role);
  return res.json({
    token,
    usuario: { id: usuario.id, nome: usuario.nome, email: usuario.email, role: usuario.role },
  });
}

function gerarToken(usuarioId: string, role: string) {
  const options: jwt.SignOptions = { expiresIn: env.jwtExpiresIn as jwt.SignOptions["expiresIn"] };
  return jwt.sign({ sub: usuarioId, role }, env.jwtSecret, options);
}
