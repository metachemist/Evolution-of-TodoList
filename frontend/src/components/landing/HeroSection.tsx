'use client'
// Task: T016 | Landing hero redesign with CTA hierarchy and trust indicators
// Spec: @specs/1-specify/phase-2/feature-02-nextjs-todo-frontend.md (FR-001, FR-022)

import Link from 'next/link'
import { motion } from 'framer-motion'
import { Activity, Lock, Sparkles } from 'lucide-react'
import type { LucideIcon } from 'lucide-react'
import { BRAND_BADGE_NAME, BRAND_TAGLINE } from '@/lib/brand'

import { ProductPreview } from './ProductPreview'

function TrustItem({ label, icon: Icon }: { label: string; icon: LucideIcon }) {
  return (
    <li className="inline-flex items-center gap-1.5 text-xs text-muted-foreground sm:text-sm">
      <Icon className="h-3.5 w-3.5 text-primary" />
      <span>{label}</span>
    </li>
  )
}

export function HeroSection() {
  return (
    <section className="relative pt-24 sm:pt-28">
      <div className="grid items-center gap-12 lg:grid-cols-[1.05fr_0.95fr]">
        <motion.div
          initial={{ opacity: 0, y: 16 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.55, ease: 'easeOut' }}
          className="max-w-2xl"
        >
          <p className="mb-5 inline-flex items-center gap-2 rounded-full border border-border/70 bg-muted/55 px-4 py-1.5 text-xs tracking-[0.18em] text-muted-foreground uppercase">
            <Sparkles className="h-3.5 w-3.5 text-primary" />
            {BRAND_BADGE_NAME}
          </p>

          <p className="-mt-2 mb-4 text-sm text-muted-foreground">{BRAND_TAGLINE}</p>

          <h1 className="text-balance text-4xl font-black leading-[1.05] text-foreground sm:text-5xl lg:text-6xl">
            Plan less. Focus deeper.
          </h1>

          <p className="mt-6 max-w-xl text-base leading-relaxed text-muted-foreground sm:text-lg">
            Cut through noise, keep momentum, and move with clarity from first task to final
            checkmark.
          </p>

          <div className="mt-9 flex flex-col gap-3 sm:flex-row sm:items-center">
            <Link
              href="/login"
              className="inline-flex items-center justify-center rounded-md bg-primary px-6 py-3 font-semibold text-primary-foreground transition-transform duration-200 hover:scale-[1.03] hover:opacity-95 focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
            >
              Sign in
            </Link>
            <Link
              href="/register"
              className="inline-flex items-center justify-center rounded-md border border-border bg-background/70 px-6 py-3 font-semibold text-foreground transition-transform duration-200 hover:scale-[1.02] hover:bg-muted focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
            >
              Sign up
            </Link>
          </div>

          <ul className="mt-5 flex flex-wrap items-center gap-x-4 gap-y-2">
            <TrustItem label="Secure auth" icon={Lock} />
            <TrustItem label="Real-time updates" icon={Activity} />
            <TrustItem label="Built with modern stack" icon={Sparkles} />
          </ul>
        </motion.div>

        <ProductPreview />
      </div>
    </section>
  )
}
