# Usa una imagen base de Node.js
FROM node:22.1-alpine

# Establece el directorio de trabajo
WORKDIR /app

# Copia los archivos del proyecto
COPY package.json pnpm-lock.yaml ./


# Instala pnpm y las dependencias
RUN npm install -g pnpm
RUN pnpm install

COPY . .
# Expone el puerto para el desarrollo
EXPOSE 3000

# Comando para iniciar el servidor de desarrollo
CMD ["pnpm", "dev"]
