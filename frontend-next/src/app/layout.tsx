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
  title: {
    default: 'AquaFlow Pro - Sistema de Gestão Aquática',
    template: '%s | AquaFlow Pro',
  },
  description: 'Sistema profissional de gestão para centros aquáticos e academias de natação. Controle alunos, horários, pagamentos e professores.',
  keywords: ['natação', 'piscina', 'gestão', 'aquático', 'academia', 'alunos', 'mensalidade', 'horários'],
  authors: [{ name: 'AquaFlow Pro' }],
  creator: 'AquaFlow Pro',
  publisher: 'AquaFlow Pro',
  robots: {
    index: true,
    follow: true,
  },
  openGraph: {
    title: 'AquaFlow Pro - Sistema de Gestão Aquática',
    description: 'Sistema profissional de gestão para centros aquáticos e academias de natação. Controle alunos, horários, pagamentos e professores.',
    type: 'website',
    locale: 'pt_BR',
    siteName: 'AquaFlow Pro',
  },
  twitter: {
    card: 'summary_large_image',
    title: 'AquaFlow Pro - Sistema de Gestão Aquática',
    description: 'Sistema profissional de gestão para centros aquáticos e academias de natação.',
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