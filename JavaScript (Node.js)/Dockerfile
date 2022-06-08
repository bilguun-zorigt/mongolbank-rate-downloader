FROM node:18-bullseye-slim

ENV NODE_ENV=development
ENV PATH /app/node_modules/.bin:$PATH

RUN mkdir /app && chown -R node /app
USER node
WORKDIR /app

COPY ./package.json ./
RUN npm install