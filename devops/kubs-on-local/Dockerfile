# Stage 1: Use an official Node.js runtime as a parent image
# Using 'alpine' for a smaller image size.
FROM node:18-alpine

# Set the working directory in the container to /app
WORKDIR /app

# Copy package.json and package-lock.json (if available)
# Using 'package*.json' to catch both files
COPY package*.json ./

# Install app dependencies
# This is a separate layer, so it's cached unless package.json changes.
RUN npm install

# Bundle app source
# Copy local files from the current directory to the container's working directory
COPY . .

# Make port 8080 available to the world outside this container
EXPOSE 8080

# Define the command to run the app
# This runs 'npm start', which is defined in package.json
CMD [ "npm", "start" ]