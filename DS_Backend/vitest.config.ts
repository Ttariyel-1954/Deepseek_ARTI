import { defineConfig } from 'vitest/config';

export default defineConfig({
  test: {
    globals: true,
    environment: 'node',
    include: ['**/*.spec.ts'],
    // e2e testleri ayri isledilir
    exclude: ['**/*.e2e-spec.ts', 'node_modules/**'],
  },
});
