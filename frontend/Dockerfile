FROM node:18

ENV NODE_ENV=development

RUN mkdir /app
RUN WORKDIR /app
COPY ./package.json ./package-lock.json ./
RUN npm install --development
COPY ./ .

EXPOSE 3000
CMD [ "npm", "run", "dev"]