import type { Metadata } from 'next'
import { Inter, Poppins } from 'next/font/google'
import './globals.css'
import { Toaster } from 'react-hot-toast'

const inter = Inter({
  subsets: ['latin'],
  variable: '--font-inter',
  display: 'swap',
})

const poppins = Poppins({
  subsets: ['latin'],
  weight: ['400', '500', '600', '700', '800'],
  variable: '--font-poppins',
  display: 'swap',
})

export const metadata: Metadata = {
  title: 'AquaFlow Pro - Sistema de Gestão Aquática',
  description: 'Sistema profissional de gestão para centros aquáticos e academias de natação',
  keywords: ['natação', 'piscina', 'gestão', 'aquático', 'academia'],
  authors: [{ name: 'AquaFlow Pro' }],
  openGraph: {
    title: 'AquaFlow Pro',
    description: 'Sistema profissional de gestão aquática',
    type: 'website',
  },
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="pt-BR" className={`${inter.variable} ${poppins.variable}`}>
      <body className={`${inter.className} antialiased`}>
        {children}
        <Toaster
          position="top-right"
          toastOptions={{
            duration: 4000,
            style: {
              background: 'hsl(var(--card))',
              color: 'hsl(var(--card-foreground))',
              border: '1px solid hsl(var(--border))',
              borderRadius: 'var(--radius)',
              boxShadow: 'var(--shadow-medium)',
            },
            success: {
              iconTheme: {
                primary: 'hsl(var(--success))',
                secondary: 'white',
              },
              style: {
                background: 'hsl(var(--success))',
                color: 'hsl(var(--success-foreground))',
              },
            },
            error: {
              iconTheme: {
                primary: 'hsl(var(--error))',
                secondary: 'white',
              },
              style: {
                background: 'hsl(var(--error))',
                color: 'hsl(var(--error-foreground))',
              },
            },
          }}
        />
      </body>
    </html>
  )
}