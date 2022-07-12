FROM node:lts-alpine

RUN npm install -g http-server

WORKDIR /app

COPY package*.json ./

RUN npm install

COPY . .

RUN npm run build

CMD ["http-server", "--proxy", "http://localhost:8080?", "dist"]

#CMD ["npm", "run", "serve"]