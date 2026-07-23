import multer from "multer";
import path from "node:path";
import { env } from "../config/env";

// Armazenamento local em disco para o MVP.
// Em produção, trocar por um storage adapter para S3/Supabase Storage/Cloudinary.
const storage = multer.diskStorage({
  destination: env.uploadDir,
  filename: (_req, file, cb) => {
    const suffix = `${Date.now()}-${Math.round(Math.random() * 1e9)}`;
    cb(null, `${suffix}${path.extname(file.originalname)}`);
  },
});

export const uploadFotos = multer({
  storage,
  limits: { fileSize: 8 * 1024 * 1024 }, // 8MB por foto
  fileFilter: (_req, file, cb) => {
    const permitido = /jpeg|jpg|png|webp/.test(file.mimetype);
    if (!permitido) {
      cb(new Error("Formato de imagem não suportado."));
      return;
    }
    cb(null, true);
  },
});
