// Task: T014 | Shared premium backdrop for landing, auth, and dashboard shells
// Spec: @specs/1-specify/phase-2/feature-02-nextjs-todo-frontend.md (FR-001)

export function AppBackdrop() {
  return (
    <>
      <div aria-hidden="true" className="pointer-events-none absolute inset-0 app-shell-gradient" />
      <div
        aria-hidden="true"
        className="pointer-events-none absolute -left-28 top-8 h-72 w-72 rounded-full bg-primary/20 blur-3xl"
      />
      <div
        aria-hidden="true"
        className="pointer-events-none absolute -right-28 top-14 h-80 w-80 rounded-full bg-sky-300/10 blur-3xl dark:bg-sky-400/10"
      />
    </>
  )
}
