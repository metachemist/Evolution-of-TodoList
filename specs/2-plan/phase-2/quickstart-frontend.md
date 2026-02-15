# Quickstart: Next.js Todo Frontend

**Feature**: 006-nextjs-todo-frontend | **Date**: 2026-02-13

## Prerequisites

- Node.js 22+ (LTS)
- The FastAPI backend running at `http://localhost:8000` (see `backend/` directory)
- A Neon PostgreSQL database configured for the backend

## 1. Project Setup

```bash
# From the repository root
cd frontend

# Create Next.js 16 project (if not already scaffolded)
npx create-next-app@latest . --typescript --tailwind --app --src-dir --no-import-alias

# Install dependencies
npm install @tanstack/react-query @radix-ui/react-dialog react-hook-form @hookform/resolvers zod sonner next-themes

# Install dev dependencies
npm install -D vitest @vitejs/plugin-react @testing-library/react @testing-library/jest-dom @testing-library/user-event jsdom playwright @playwright/test
```

## 2. Environment Configuration

```bash
# Copy example env
cp .env.example .env.local
```

**`.env.example`** contents:
```
# Backend API URL (FastAPI server)
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## 3. Project Structure After Setup

```
frontend/
├── CLAUDE.md                     # Frontend-specific agent instructions
├── package.json
├── next.config.ts
├── tsconfig.json                 # strict: true
├── vitest.config.ts
├── playwright.config.ts
├── .env.example
├── .env.local                    # Git-ignored
├── tailwind.css                  # Tailwind v4 CSS-first config
├── public/
├── src/
│   ├── app/                      # Next.js App Router
│   ├── components/               # React components
│   ├── lib/                      # API client, query client, validations
│   ├── hooks/                    # Custom React hooks
│   ├── providers/                # Context providers
│   └── types/                    # TypeScript types
├── e2e/                          # Playwright E2E tests
└── src/__tests__/                # Vitest unit/component tests
```

## 4. Running the Application

```bash
# Start the backend first (from repo root)
cd backend && uvicorn src.main:app --reload --port 8000

# In a separate terminal, start the frontend
cd frontend && npm run dev
```

The frontend runs at `http://localhost:3000`.

## 5. Key Configuration Files

### next.config.ts
```typescript
import type { NextConfig } from 'next'

const nextConfig: NextConfig = {
  // No special config needed — App Router is default in Next.js 16
}

export default nextConfig
```

### tsconfig.json (key settings)
```json
{
  "compilerOptions": {
    "strict": true,
    "target": "ES2022",
    "lib": ["dom", "dom.iterable", "esnext"],
    "jsx": "preserve",
    "module": "esnext",
    "moduleResolution": "bundler",
    "paths": {
      "@/*": ["./src/*"]
    }
  }
}
```

### vitest.config.ts
```typescript
import { defineConfig } from 'vitest/config'
import react from '@vitejs/plugin-react'
import { resolve } from 'path'

export default defineConfig({
  plugins: [react()],
  test: {
    environment: 'jsdom',
    globals: true,
    setupFiles: ['./src/__tests__/setup.ts'],
    coverage: {
      provider: 'v8',
      include: ['src/lib/**', 'src/hooks/**', 'src/components/**'],
      exclude: ['src/types/**', 'src/app/**/layout.tsx', 'src/app/**/page.tsx'],
      thresholds: {
        statements: 60,
      },
    },
  },
  resolve: {
    alias: {
      '@': resolve(__dirname, './src'),
    },
  },
})
```

### tailwind.css (Tailwind v4 CSS-first)
```css
@import "tailwindcss";

@custom-variant dark (&:where(.dark, .dark *));

@theme inline {
  --color-background: #ffffff;
  --color-foreground: #0a0a0a;
  --color-muted: #737373;
  --color-border: #e5e5e5;
  --color-primary: #2563eb;
  --color-primary-foreground: #ffffff;
  --color-destructive: #dc2626;
  --color-success: #16a34a;
}

.dark {
  --color-background: #0a0a0a;
  --color-foreground: #ededed;
  --color-muted: #a3a3a3;
  --color-border: #262626;
  --color-primary: #3b82f6;
  --color-primary-foreground: #ffffff;
  --color-destructive: #ef4444;
  --color-success: #22c55e;
}
```

## 6. Running Tests

```bash
# Unit and component tests
npm run test

# Unit tests with coverage
npm run test:coverage

# E2E tests (requires both backend and frontend running)
npx playwright test

# E2E tests with UI
npx playwright test --ui
```

## 7. Development Workflow

1. **Start backend**: `cd backend && uvicorn src.main:app --reload --port 8000`
2. **Start frontend**: `cd frontend && npm run dev`
3. **Open browser**: Navigate to `http://localhost:3000`
4. **Register**: Create an account at `/register`
5. **Manage tasks**: Create, edit, toggle, delete tasks on `/dashboard`

## 8. Dependency Summary

| Package | Purpose | Version |
|---|---|---|
| next | Framework (App Router) | 16+ |
| react / react-dom | UI library | 19+ |
| typescript | Type safety | 5.x |
| @tanstack/react-query | Server state + optimistic updates | 5.x |
| @radix-ui/react-dialog | Accessible modal dialogs | latest |
| react-hook-form | Form state management | 7.x |
| @hookform/resolvers | Zod integration for RHF | latest |
| zod | Schema validation | 4.x |
| sonner | Toast notifications | latest |
| next-themes | Dark/light mode persistence | latest |
| tailwindcss | Styling (constitution mandate) | 4.x |
| vitest | Test runner | latest |
| @testing-library/react | Component testing | latest |
| @playwright/test | E2E browser testing | latest |
