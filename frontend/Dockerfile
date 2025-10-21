# frontend/Dockerfile (Simplified for Dev)
FROM node:20-alpine

WORKDIR /app

# Copy all files
COPY package*.json ./
COPY . .

# Install all dependencies (development included)
RUN npm install

# Expose the dev server port
EXPOSE 5173

# Command to start the SvelteKit development server
CMD ["npm", "run", "dev"]