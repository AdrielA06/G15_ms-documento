# ESTE ARCHIVO SIRVE PARA CREAR LA IMAGEN DE DOCKER DE NUESTRO PROYECTO



# 1. ETAPA DE PRECONSTRUCCIÓN

# Definimos la imagen de base que va a utilizar nuestro contenedor backend
FROM node:22-alpine AS build

# Definimos el directorio del contenedor en el cual va a estar nuestra aplicación
WORKDIR /app

# Instalamos Chromium y otras dependencias de sistema operativo necesarias
RUN apk add --no-cache \
    chromium \
    nss \
    freetype \
    freetype-dev \
    harfbuzz \
    ca-certificates \
    ttf-freefont

# Configuramos las variables de entorno para Puppeteer
ENV PUPPETEER_SKIP_CHROMIUM_DOWNLOAD=true
ENV PUPPETEER_EXECUTABLE_PATH=/usr/bin/chromium-browser

# Copiamos todos los archivos package+algo.json al directorio de trabajo
COPY package*.json ./

# Ejecutamos npm installa para generar el archivo package.json
RUN npm install

# Instalación limpia de todas las dependencias necesarias.
# La primer flag evita que los scripts de instalación se ejecuten con permisos de superusario 
# La segunda flag evita que se hagan reportes de auditoría durante la instalación
RUN npm ci --unsafe-perm=false --no-audit --no-fund

# Copiamos el archivo de configiración de Typescript (define reglas de escritura y compilación a JS) al directorio de trabajo
COPY tsconfig.json ./

# Copiamos todos los schemas y migraciones de Prisma ORM
COPY prisma ./prisma

# Copiamos la carpeta con archivos públicos
COPY public ./public

# Copiamos el código fuente del proyecto de '/src' (escrito en TS) al directorio de trabajo
COPY src ./src

# Generamos todos los tipos de Prisma ORM necesarios para la compilación También migramos la base de datos.
RUN npx prisma generate

# Compilamos todo el proyecto contenido '/src' a un código equivalente en JS en el directorio '/dist' 
RUN npm run build

# Realizamos una instalación limpia de las dependencias que únicamente se van a usar en producción
# Elininamos el código fuente escrito en Typescript y también el archivo de configuración de TS
RUN npm ci --only=production --no-audit --no-fund && \
    rm -rf src tsconfig.json



# 2. ETAPA DE CONSTRUCCIÓN

# Utilizamos como base una imagen de Node v22 sin shell, ni gestores. Más liviana y menos vulnerable.
FROM gcr.io/distroless/nodejs22:nonroot

WORKDIR /app

# Copiamos desde la imagen de preconstrucción a la imagen de construcción, únicamente las carpetas y archivos necesarios 
COPY --from=build /app/prisma ./prisma
COPY --from=build /app/public ./public
COPY --from=build /app/dist ./dist
COPY --from=build /app/package*.json ./
COPY --from=build /app/node_modules ./node_modules


# Indicamos que la aplicación de node (y sus dependencias) se ejecute en modo producción, en forma optimizanda
# Tambien indicamos que la variable de entorno del puerto sea 3000
ENV NODE_ENV=production \
    PORT=3000

# Definimos el puerto interno del contenedor donde la aplicación se va a ejecutar
EXPOSE 3000

USER nonroot

# Comando que se ejecuta automáticamente cuando se levanta el contenedor
CMD ["dist/index.js"]