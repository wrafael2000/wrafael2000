import { Router } from "express";
import { cadastrar, login } from "../controllers/auth.controller";

export const authRouter = Router();

authRouter.post("/cadastro", cadastrar);
authRouter.post("/login", login);
