/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  images: {
    domains: ['localhost'],
  },
  // Note: API URL is configured in .env.local
  // Default: http://localhost:8000/api
  // Production: set NEXT_PUBLIC_API_URL in Railway environment variables
}

module.exports = nextConfig