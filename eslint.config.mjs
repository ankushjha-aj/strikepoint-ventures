// ESLint flat config: TypeScript server code + the browser script.
import js from "@eslint/js";
import tseslint from "typescript-eslint";
import globals from "globals";

export default tseslint.config(
  { ignores: ["dist/", "node_modules/", "pages/", "tools/", "content/", "UI_Images/", "new_UI_images/"] },

  // Express server (TypeScript, Node)
  {
    files: ["src/**/*.ts"],
    extends: [js.configs.recommended, ...tseslint.configs.recommendedTypeChecked],
    languageOptions: {
      globals: globals.node,
      parserOptions: { projectService: true, tsconfigRootDir: import.meta.dirname },
    },
    rules: {
      "@typescript-eslint/no-unused-vars": ["error", { argsIgnorePattern: "^_" }],
      eqeqeq: ["error", "always"],
      "no-console": "off",
    },
  },

  // Browser script served to visitors (plain ES5-style JS in an IIFE)
  {
    files: ["assets/js/**/*.js"],
    extends: [js.configs.recommended],
    languageOptions: { ecmaVersion: 2017, sourceType: "script", globals: globals.browser },
    rules: { eqeqeq: ["error", "always"], "no-unused-vars": ["error", { caughtErrors: "none" }] },
  },

  // This config file itself
  { files: ["eslint.config.mjs"], extends: [js.configs.recommended], languageOptions: { globals: globals.node } },
);
