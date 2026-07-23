import { Router } from "express";
import { authRouter } from "./auth.routes";
import { chamadosRouter } from "./chamados.routes";

export const apiRouter = Router();

apiRouter.use("/auth", authRouter);
apiRouter.use("/chamados", chamadosRouter);
