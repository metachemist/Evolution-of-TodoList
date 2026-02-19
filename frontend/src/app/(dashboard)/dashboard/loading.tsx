// Task: T047 | Loading skeleton for dashboard — covers RSC hydration phase (~50-150ms)
export default function DashboardLoading() {
  return (
    <div className="surface-panel p-5 sm:p-7">
      <div className="mb-7 flex items-center justify-between">
        <div className="space-y-2">
          <div className="h-3 w-20 animate-pulse rounded bg-muted" />
          <div className="h-8 w-36 animate-pulse rounded bg-muted" />
        </div>
        <div className="h-10 w-32 animate-pulse rounded-xl bg-muted" />
      </div>
      <ul className="flex flex-col gap-3" aria-label="Loading tasks">
        {[1, 2, 3].map((n) => (
          <li
            key={n}
            className="surface-card flex items-start gap-3 p-4 animate-pulse"
          >
            <div className="mt-1 h-4 w-4 shrink-0 rounded-full bg-muted" />
            <div className="flex-1 space-y-2">
              <div className="h-3 w-3/5 rounded bg-muted" />
              <div className="h-3 w-2/5 rounded bg-muted" />
            </div>
          </li>
        ))}
      </ul>
    </div>
  )
}
