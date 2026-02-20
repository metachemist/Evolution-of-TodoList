'use client'
// Task: T016 | Landing feature reinforcement strip
// Spec: @specs/1-specify/phase-2/feature-02-nextjs-todo-frontend.md (FR-001, FR-020)

import { motion } from 'framer-motion'
import { LayoutDashboard, ShieldCheck, Zap } from 'lucide-react'
import type { LucideIcon } from 'lucide-react'

type Feature = {
  title: string
  description: string
  icon: LucideIcon
}

const features: Feature[] = [
  {
    title: 'Fast & Lightweight',
    description: 'Instant interactions and smooth workflows that keep your day moving.',
    icon: Zap,
  },
  {
    title: 'Secure Authentication',
    description: 'Protected account sessions designed for confident daily usage.',
    icon: ShieldCheck,
  },
  {
    title: 'Clean Focused Dashboard',
    description: 'A distraction-free space to prioritize what matters most.',
    icon: LayoutDashboard,
  },
]

function FeatureCard({ feature, index }: { feature: Feature; index: number }) {
  const Icon = feature.icon
  return (
    <motion.article
      initial={{ opacity: 0, y: 14 }}
      whileInView={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.35, delay: index * 0.08 }}
      viewport={{ once: true, amount: 0.5 }}
      whileHover={{ y: -4 }}
      className="rounded-xl border border-border/70 bg-muted/35 p-5 backdrop-blur-md transition-shadow hover:shadow-[0_14px_30px_-18px_rgba(56,189,248,0.45)]"
    >
      <div className="mb-3 inline-flex h-10 w-10 items-center justify-center rounded-lg border border-border/70 bg-background/70">
        <Icon className="h-5 w-5 text-primary" />
      </div>
      <h3 className="text-base font-semibold text-foreground">{feature.title}</h3>
      <p className="mt-1.5 text-sm leading-relaxed text-muted-foreground">{feature.description}</p>
    </motion.article>
  )
}

export function FeatureStrip() {
  return (
    <section className="pb-16 pt-6 sm:pb-24">
      <div className="grid gap-4 md:grid-cols-3">
        {features.map((feature, index) => (
          <FeatureCard key={feature.title} feature={feature} index={index} />
        ))}
      </div>
    </section>
  )
}
