import markdownIt from "markdown-it"
import {init} from "@github/markdownlint-github"

const overriddenOptions = init({
  "default": false,

  // GitHub's Custom A11y Rules
  "no-default-alt-text": true,   // GH001
  "no-generic-link-text": true,  // GH002
  "no-empty-alt-text": true,     // GH003

  // Standard Rules (a11y-focused)
  "heading-increment": true,     // MD001: Heading levels must only increment by one (e.g., H1 -> H2)
  "no-duplicate-heading": { "siblings_only": true }, // MD024 Multiple headings with the same content
  "single-title": true,          // MD025: One top-level heading
  "blanks-around-fences": true,  // MD031: Fenced code blocks should be surrounded by blank lines
  "fenced-code-language": true,  // MD040: Fenced code blocks should have a language specified
  "no-alt-text": true,           // MD045: Images must have alt text
  "no-empty-links": true,        // MD042: Prevents [link]()
  "no-emphasis-as-heading": true // MD036: Prevents using **Bold** instead of # Heading
})

const markdownItFactory = () => markdownIt({ html: true })
const options = {
    ignores: ["node_modules", ".gitbook", "SUMMARY.md"],
    config: overriddenOptions,
    // TODO: Reenable the customRules once we fix up the other rules. There are too many and it's overwhelming
    // customRules: ["@github/markdownlint-github"],
    markdownItFactory,
    outputFormatters: [
      ...( process.env.REPORT ? [
        [ "markdownlint-cli2-formatter-json", { "name": "./markdownlint-cli2-results.json"} ],
        [ "markdownlint-cli2-formatter-summarize", { "byRule": true } ]
      ] 
      : [[ "markdownlint-cli2-formatter-pretty", { "appendLink": true } ]]
    )]
}
export default options