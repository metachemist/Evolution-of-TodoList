# ADR-0009: Accessible UI Component Primitives

> **Scope**: Document decision clusters, not individual technology choices. Group related decisions that work together.

- **Status:** Accepted
- **Date:** 2026-02-13
- **Feature:** Phase 2 — Next.js Todo Frontend
- **Context:** The spec mandates WCAG 2.1 Level AA compliance (FR-022, FR-023, SC-013) and defines specific interactive patterns: three modal dialogs (create, edit, delete confirmation), three forms with per-field validation (login, register, task create/edit), and non-blocking toast notifications (success 3s, error 5s dismissible). These three concerns work together as an integrated UX layer — a change in modal strategy affects form rendering; a change in form library affects validation error display. They are chosen and maintained as a cluster.

<!-- Significance checklist: PASS — WCAG AA compliance requirement, affects all modals and forms, multiple alternatives with tradeoffs -->

## Decision

- **Modal/Dialog**: Radix UI Dialog (`@radix-ui/react-dialog`) — unstyled headless primitive styled with Tailwind. Provides focus trap, Escape-close, focus-return-to-trigger, scroll lock, portal rendering, and ARIA attributes (`role="dialog"`, `aria-modal="true"`) automatically.
- **Forms**: react-hook-form v7 with `@hookform/resolvers` and Zod v4. Uncontrolled inputs minimise re-renders; Zod schemas are shared across client and server; `zodResolver` wires schema to form in one line.
- **Toasts**: Sonner — imperative API callable outside React components, ~2KB gzipped, supports auto-dismiss duration and close button natively.
- These three are chosen together: Radix modal contains react-hook-form; form errors use Zod messages; Sonner toasts fire on mutation success/error from the same hooks.

## Consequences

### Positive

- All WCAG 2.1 AA modal requirements (focus trap, screen reader announcement, keyboard nav) are handled automatically by Radix — no custom implementation risk
- Zod schemas are the single source of validation truth — same schema validates on client blur/submit and could validate in server actions in future phases
- Sonner's imperative `toast()` API can be called from the API client layer (outside React) — toast fires on network error without needing component state
- The three libraries compose cleanly: Radix renders the Dialog, react-hook-form manages field state inside it, Sonner fires on close

### Negative

- Three additional runtime dependencies (Radix, react-hook-form, Sonner) where one monolithic UI library might cover all three
- Radix Dialog is unstyled — requires Tailwind classes for every visual aspect (intentional but adds boilerplate)
- Zod v4 has breaking changes from v3 — team must be aware of the version in use

## Alternatives Considered

**Alternative A — Headless UI (Tailwind team) + react-hook-form + Sonner**: Strong alternative. Headless UI has excellent Tailwind integration and Dialog/Transition primitives. Rejected: Radix UI has a broader component ecosystem (Tooltip, DropdownMenu, Popover) available for Phases III+ without changing the primitive library.

**Alternative B — Native HTML `<dialog>` element + Constraint Validation API + custom toasts**: Rejected — native `<dialog>` has inconsistent focus-trap behaviour across Safari versions in the spec's required browser list. The Constraint Validation API cannot produce the exact error messages the spec defines. Custom toasts require reimplementing accessible ARIA live regions.

**Alternative C — shadcn/ui component library (pre-built Radix + Tailwind components)**: Rejected for this phase — shadcn/ui is a code-generation approach (copies component source into the project). Adds ~50 files of generated code for features we don't use. Acceptable for future phases with more complex UI requirements.

**Alternative D — Formik + Yup + react-hot-toast**: Rejected — Formik uses controlled inputs (every keystroke causes a re-render, risking >200ms validation latency from spec SC-006). Yup is heavier than Zod (~45KB vs ~21KB combined). react-hot-toast is functionally equivalent to Sonner but Sonner's close button support is cleaner.

## References

- Feature Spec: @specs/1-specify/phase-2/feature-02-nextjs-todo-frontend.md (FR-008, FR-010, FR-013, FR-022, FR-023, FR-025, SC-006, SC-013)
- Implementation Plan: @specs/2-plan/phase-2/phase-2-nextjs-todo-frontend.md (ADR-004, Phase C components)
- UI Design: @specs/2-plan/phase-2/ui-design/components.md (Modal, LoginForm, RegisterForm, TaskCreateModal, TaskEditModal, TaskDeleteModal)
- Research: @specs/2-plan/phase-2/research-frontend.md (§6 Toast Notifications, §7 Modal/Dialog, §8 Form Validation)
- Related ADRs: ADR-0008 (state/mutation strategy — modals fire Sonner toasts from mutation hooks)
- Evaluator Evidence: @history/prompts/006-nextjs-todo-frontend/0004-frontend-implementation-plan.plan.prompt.md
