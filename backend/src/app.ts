import express from "express";
import cors from "cors";
import { apiRouter } from "./routes";
import { env } from "./config/env";

export const app = express();

app.use(cors());
app.use(express.json());
app.use("/uploads", express.static(env.uploadDir));

app.get("/health", (_req, res) => res.json({ status: "ok" }));
app.use("/api", apiRouter);

// Handler de erro genérico (ex: falhas de upload/multer)
app.use((err: Error, _req: express.Request, res: express.Response, _next: express.NextFunction) => {
  console.error(err);
  res.status(500).json({ error: err.message ?? "Erro interno do servidor." });
});
