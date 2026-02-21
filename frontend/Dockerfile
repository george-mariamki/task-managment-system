
FROM node:20-alpine

# container working directory
WORKDIR /app

# copy package.json and package-lock.json to the container
COPY package*.json ./

# install dependencies
RUN npm install

#   copy the rest of the application code to the container
COPY . .

# expose the port that the development server will run on
EXPOSE 5173

# start the development server
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
