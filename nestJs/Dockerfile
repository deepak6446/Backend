# node.js base image
FROM node:18-alpine
RUN apk add ca-certificates
ARG NPM_TOKEN
RUN test -n "$NPM_TOKEN" || (echo "NPM_TOKEN  not set" && false)
# server info
RUN node -v
RUN npm -v

# working directory
RUN mkdir /app
RUN chown -R node:node /app
WORKDIR /app
RUN npm install -g npm@7
RUN chmod 757 /etc/ssl/certs
# switch to user node
USER node
# ADD --chown=node:node ./.env ./.env
ADD --chown=node:node ./src ./src
COPY --chown=node:node ./*.json ./
COPY --chown=node:node ./start.sh ./
RUN chmod 757 ./start.sh
RUN echo "//npm.pkg.github.com/:_authToken=$NPM_TOKEN" > .npmrc
RUN echo "@<repo>:registry=https://npm.pkg.github.com/<repo>" >> .npmrc
# install dependencies for build
RUN npm install --development
RUN npm install @nestjs/cli@10.0.5
RUN npm run build
RUN rm -r ./src ./node_modules ./tsconfig*.json ./nest-cli.json

# install prod dependencies
RUN npm install --production

#start server
CMD [ "npm", "run", "start:prod" ]
