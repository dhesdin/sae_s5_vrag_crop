import { globalIgnores } from 'eslint/config'
import { defineConfigWithVueTs, vueTsConfigs } from '@vue/eslint-config-typescript'
import pluginVue from 'eslint-plugin-vue'
import pluginOxlint from 'eslint-plugin-oxlint'
import skipFormatting from 'eslint-config-prettier/flat'

export default defineConfigWithVueTs(
  {
    name: 'app/files-to-lint',
    files: ['**/*.{vue,ts,mts,tsx}'],
  },

  globalIgnores([
    '**/dist/**',
    '**/dist-ssr/**',
    '**/coverage/**',
    '**/node_modules/**',
    '*.d.ts'
  ]),

  // Utilisation des règles recommandées complètes (inclut les bonnes pratiques)
  ...pluginVue.configs['flat/recommended'],
  vueTsConfigs.recommendedTypeChecked,

  {
    name: 'app/custom-rules',
    rules: {
      // Conventions de nommage des composants (exige des noms multi-mots)
      'vue/multi-word-component-names': ['error', {
        ignores: ['App', 'Help', 'PopUp'] // Permet d'ignorer vos composants actuels si nécessaire
      }],

      // Bonnes pratiques TypeScript strictes
      '@typescript-eslint/no-unused-vars': ['error', {
        argsIgnorePattern: '^_',
        varsIgnorePattern: '^_'
      }],
      '@typescript-eslint/consistent-type-imports': ['error', {
        prefer: 'type-imports'
      }],
      '@typescript-eslint/no-explicit-any': 'warn',

      // Sécurité & Qualité de code Vue
      'vue/no-v-html': 'warn',
      'vue/require-default-prop': 'off', // Optionnel selon vos préférences avec TypeScript
      'vue/block-order': ['error', {
        order: ['script', 'template', 'style']
      }],

      // Console et Debug
      'no-console': process.env.NODE_ENV === 'production' ? 'warn' : 'off',
      'no-debugger': process.env.NODE_ENV === 'production' ? 'error' : 'off',
    },
  },

  // Intégration Oxlint pour des performances de linter fulgurantes
  ...pluginOxlint.buildFromOxlintConfigFile('.oxlintrc.json'),

  // Désactivation des règles de style gérées par Prettier en dernier
  skipFormatting,
)
