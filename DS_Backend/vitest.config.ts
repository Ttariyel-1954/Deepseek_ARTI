import { defineConfig } from 'vitest/config';

/**
 * UNIT testlər — baza və server TƏLƏB OLUNMUR.
 * e2e faylları XARİC edilir, yoxsa `npm test` onları da işə salar.
 */
export default defineConfig({
  test: {
    globals: true,
    environment: 'node',
    include: ['src/**/*.spec.ts'],
    exclude: ['**/node_modules/**', '**/dist/**', '**/*.e2e-spec.ts'],
  },
});
