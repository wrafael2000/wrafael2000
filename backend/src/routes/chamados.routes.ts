import { Router } from "express";
import {
  atualizarStatusChamado,
  criarChamado,
  listarChamados,
  obterChamado,
} from "../controllers/chamados.controller";
import { authMiddleware, somenteAdmin } from "../middlewares/auth.middleware";
import { uploadFotos } from "../middlewares/upload.middleware";

export const chamadosRouter = Router();

chamadosRouter.use(authMiddleware);

// Rota básica de criação de chamado: recebe multipart/form-data com campos do
// formulário (categoria, descricao, latitude, longitude) + até 5 fotos em "fotos".
chamadosRouter.post("/", uploadFotos.array("fotos", 5), criarChamado);
chamadosRouter.get("/", listarChamados);
chamadosRouter.get("/:id", obterChamado);
chamadosRouter.patch("/:id/status", somenteAdmin, atualizarStatusChamado);
