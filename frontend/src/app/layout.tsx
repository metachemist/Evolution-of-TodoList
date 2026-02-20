// Task: T014 | Root layout with ThemeProvider, QueryProvider, Sonner Toaster, and noscript fallback
import type { Metadata } from 'next'
import { ThemeProvider } from 'next-themes'
import { Toaster } from 'sonner'
import { QueryProvider } from '@/providers/QueryProvider'
import { BRAND_DESCRIPTION, BRAND_TITLE } from '@/lib/brand'
import './globals.css'

export const metadata: Metadata = {
  title: BRAND_TITLE,
  description: BRAND_DESCRIPTION,
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body>
        <noscript>This application requires JavaScript to run.</noscript>
        <ThemeProvider attribute="class" defaultTheme="system" enableSystem>
          <QueryProvider>
            {children}
            <Toaster richColors position="top-right" />
          </QueryProvider>
        </ThemeProvider>
      </body>
    </html>
  )
}
