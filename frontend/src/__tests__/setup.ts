// Task: T049 | Test setup — jest-dom matchers + MSW server lifecycle
/// <reference types="vitest/globals" />
import '@testing-library/jest-dom'
import { server } from './mocks/server'

beforeAll(() => server.listen({ onUnhandledRequest: 'warn' }))
afterEach(() => server.resetHandlers())
afterAll(() => server.close())
