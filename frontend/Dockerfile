FROM node:18-alpine

# Set working directory
WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci --only=production

# Copy application code
COPY . .

# Build the production bundle
RUN npm run build

# Install serve to run the production build
RUN npm install -g serve

# Expose the frontend port
EXPOSE 3000

# Serve the production build
CMD ["serve", "-s", "build", "-l", "3000"]