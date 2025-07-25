import js from "@eslint/js";
import globals from "globals";
import security from "eslint-plugin-security";
import { defineConfig } from "eslint/config";

export default defineConfig([
  {
    files: ["**/*.{js,mjs,cjs}"],
    plugins: {
      js,
      security,
    },
    extends: ["js/recommended", "plugin:security/recommended"],
    languageOptions: {
      globals: globals.browser,
    },
  },
  {
    files: ["**/*.js"],
    languageOptions: {
      sourceType: "commonjs",
    },
  },
]);
