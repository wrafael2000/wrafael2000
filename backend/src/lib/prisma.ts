import { PrismaClient } from "@prisma/client";

// Instância única do PrismaClient reutilizada em toda a aplicação
export const prisma = new PrismaClient();
