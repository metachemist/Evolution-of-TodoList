// Task: T056 | Component tests for Modal
import { describe, it, expect, vi } from 'vitest'
import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { Modal } from '@/components/ui/Modal'

function ModalWrapper({
  open = true,
  onOpenChange = vi.fn(),
}: {
  open?: boolean
  onOpenChange?: (v: boolean) => void
}) {
  return (
    <Modal open={open} onOpenChange={onOpenChange} title="Test Modal" description="Test description">
      <p>Modal content</p>
      <button>Trigger</button>
    </Modal>
  )
}

describe('Modal', () => {
  it('renders title and description when open', () => {
    render(<ModalWrapper />)
    expect(screen.getByText('Test Modal')).toBeInTheDocument()
    expect(screen.getByText('Test description')).toBeInTheDocument()
  })

  it('renders children', () => {
    render(<ModalWrapper />)
    expect(screen.getByText('Modal content')).toBeInTheDocument()
  })

  it('does not render when closed', () => {
    render(<ModalWrapper open={false} />)
    expect(screen.queryByText('Test Modal')).not.toBeInTheDocument()
  })

  it('calls onOpenChange(false) when Escape is pressed', async () => {
    const user = userEvent.setup()
    const onOpenChange = vi.fn()
    render(<ModalWrapper onOpenChange={onOpenChange} />)
    await user.keyboard('{Escape}')
    expect(onOpenChange).toHaveBeenCalledWith(false)
  })
})
