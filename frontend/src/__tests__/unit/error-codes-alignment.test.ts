// Task: T008 | Ensure frontend shared error codes stay aligned with backend definitions
import { describe, it, expect } from 'vitest'
import { readFileSync } from 'node:fs'
import { resolve } from 'node:path'
import { BACKEND_ERROR_CODES } from '@/shared/error-codes'

function extractCodes(pattern: RegExp, source: string): Set<string> {
  const codes = new Set<string>()
  for (const match of source.matchAll(pattern)) {
    const code = match[1]
    if (code) codes.add(code)
  }
  return codes
}

describe('shared backend error code catalog', () => {
  it('contains all codes defined in backend error mapper and HTTP exception map', () => {
    const backendRoot = resolve(process.cwd(), '../backend/src')
    const mapperSource = readFileSync(resolve(backendRoot, 'utils/error_mapper.py'), 'utf8')
    const mainSource = readFileSync(resolve(backendRoot, 'main.py'), 'utf8')

    const mapperCodes = extractCodes(/code\s*=\s*"([A-Z_]+)"/g, mapperSource)
    const httpMapCodes = extractCodes(/:\s*"([A-Z_]+)"/g, mainSource)
    httpMapCodes.add('HTTP_ERROR')

    const backendDefinedCodes = new Set<string>([...mapperCodes, ...httpMapCodes])
    const sharedCodes = new Set<string>(Object.values(BACKEND_ERROR_CODES))

    for (const code of backendDefinedCodes) {
      expect(sharedCodes.has(code)).toBe(true)
    }
  })
})
