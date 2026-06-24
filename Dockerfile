# Frontend SPA (ninecat-web): build the CRA app, serve it with nginx and proxy
# /api/ to the in-cluster FastAPI service. react-scripts 3 runs on Node 14
# (webpack 4 breaks on OpenSSL 3 in newer Node). CI=false so build warnings
# don't fail the build.
FROM node:14-bullseye AS build
WORKDIR /app
ENV CI=false \
    GENERATE_SOURCEMAP=false
COPY package.json package-lock.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM nginx:1.27-alpine
COPY deploy/web-nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/build /usr/share/nginx/html
