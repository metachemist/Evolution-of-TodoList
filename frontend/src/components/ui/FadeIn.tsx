'use client'
// Task: T014 | Shared subtle page/section fade-in animation utility
// Spec: @specs/1-specify/phase-2/feature-02-nextjs-todo-frontend.md (FR-022)

import { motion } from 'framer-motion'

interface FadeInProps {
  children: React.ReactNode
  className?: string
  delay?: number
}

export function FadeIn({ children, className, delay = 0 }: FadeInProps) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 12 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4, ease: 'easeOut', delay }}
      className={className}
    >
      {children}
    </motion.div>
  )
}
