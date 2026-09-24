import { defineConfig } from 'vitest/config';

/**
 * e2e testlər — REAL bazaya qoşulur.
 * Fayllar PARALEL işlədilmir: hamısı eyni bazanı dəyişir.
 */
export default defineConfig({
  test: {
    globals: true,
    environment: 'node',
    include: ['test/**/*.e2e-spec.ts'],
    fileParallelism: false,
    testTimeout: 30_000,
    hookTimeout: 30_000,
  },
});
