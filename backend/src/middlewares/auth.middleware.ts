import { NextFunction, Request, Response } from "express";
import jwt from "jsonwebtoken";
import { env } from "../config/env";

export interface AuthPayload {
  sub: string;
  role: "CIDADAO" | "ADMIN" | "SECRETARIA";
}

declare global {
  // eslint-disable-next-line @typescript-eslint/no-namespace
  namespace Express {
    interface Request {
      user?: AuthPayload;
    }
  }
}

export function authMiddleware(req: Request, res: Response, next: NextFunction) {
  const header = req.headers.authorization;
  if (!header?.startsWith("Bearer ")) {
    return res.status(401).json({ error: "Token de autenticação ausente." });
  }

  const token = header.replace("Bearer ", "");

  try {
    req.user = jwt.verify(token, env.jwtSecret) as AuthPayload;
    return next();
  } catch {
    return res.status(401).json({ error: "Token inválido ou expirado." });
  }
}

export function somenteAdmin(req: Request, res: Response, next: NextFunction) {
  if (req.user?.role !== "ADMIN" && req.user?.role !== "SECRETARIA") {
    return res.status(403).json({ error: "Acesso restrito à gestão municipal." });
  }
  return next();
}
