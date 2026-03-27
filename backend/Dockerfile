FROM node:20-slim

WORKDIR /app

# Install dependencies first (better caching)
COPY package*.json ./
RUN npm install

# Copy app files
COPY . .

# Create uploads folder inside container
RUN mkdir -p uploads

EXPOSE 5000

CMD ["node", "server.js"]