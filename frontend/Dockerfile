# Etapa 1: Build da aplicação React/Vite
FROM node:20-alpine AS builder

WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci

COPY . .
# A URL da API no frontend em produção deve ser fornecida.
# Por padrão, vamos construir com a URL relativa ou injetar depois.
RUN npm run build

# Etapa 2: Servindo com Nginx (leveza extrema)
FROM nginx:alpine

# Removemos a configuração default do nginx
RUN rm -rf /usr/share/nginx/html/*

# Copiamos o build do Vite
COPY --from=builder /app/dist /usr/share/nginx/html

# Copiamos a config customizada pro Cloud Run
COPY nginx.conf /etc/nginx/conf.d/default.conf

# A porta que o Cloud Run escuta
EXPOSE 8080

CMD ["nginx", "-g", "daemon off;"]
