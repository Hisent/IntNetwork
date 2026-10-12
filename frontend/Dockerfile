# Node 24 = Active LTS (Node 20 ist seit 2026-04 EOL). Muss zur Node-Version
# in .github/workflows/ci.yml (Job frontend) passen.
FROM node:24-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# 1.30 = aktueller Stable-Zweig von nginx (1.27 war ein Mainline-Zweig und
# bekommt keine Korrekturen mehr).
FROM nginx:1.30-alpine
COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
# Bewusst NICHT nach conf.d/: dort wuerde die Datei zusaetzlich auf http-Ebene
# eingebunden. Sie wird nur per include aus nginx.conf gezogen.
COPY nginx-security-headers.conf /etc/nginx/security-headers.conf
EXPOSE 80
