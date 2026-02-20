// Task: T016 | Root page — premium landing page with hero, preview, and feature reinforcement
import { FeatureStrip } from '@/components/landing/FeatureStrip'
import { HeroSection } from '@/components/landing/HeroSection'
import { AppBackdrop } from '@/components/ui/AppBackdrop'

export default function RootPage() {
  return (
    <main className="app-shell">
      <AppBackdrop />
      <div className="relative mx-auto w-full max-w-6xl px-6">
        <HeroSection />
        <FeatureStrip />
      </div>
    </main>
  )
}
