# Usa una imagen base de Node.js
FROM node:22.1-alpine

# Establece el directorio de trabajo
WORKDIR /app

# Copia únicamente los archivos necesarios para instalar dependencias
COPY package.json pnpm-lock.yaml ./

# Instala pnpm y las dependencias
RUN npm install -g pnpm
RUN pnpm install --frozen-lockfile

# Copia el resto del proyecto
COPY . .

# Expone el puerto para el desarrollo
EXPOSE 3000

# Comando para iniciar el servidor de desarrollo
CMD ["pnpm", "dev"]

