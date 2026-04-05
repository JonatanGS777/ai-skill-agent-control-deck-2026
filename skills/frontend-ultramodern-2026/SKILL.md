---
name: "frontend-ultramodern-2026"
description: "Diseña interfaces frontend ultramodernas, adaptables al brief, con lenguaje visual distintivo y sin patrones genéricos de IA."
version: "1.2.0"
domain: "frontend"
quality_tier: "expert"
compatibility:
  - claude-code
  - codex
owner: "yonatanguerrerosoriano"
tags:
  - "frontend"
  - "ui-design"
  - "design-systems"
  - "ultramodern"
  - "2026"
  - "anti-generic-ai"
foundation_skills:
  - "logic-propositional-reasoning"
  - "algorithm-correctness-invariants"
  - "testing-verification-foundations"
  - "security-threat-modeling-foundations"
---

# Frontend Ultramodern 2026 Skill

## Mission
Construir interfaces frontend de nivel premium (2026) con un lenguaje visual intencional, memorable y contextual, evitando cualquier apariencia de plantilla generica de IA.

## When to use
- When the user asks for a new page, section, component library, landing, dashboard, or app shell.
- When the brief demands visual originality, stronger branding, or premium product feel.
- When previous outputs feel generic and need a fully art-directed redesign.

## Inputs expected
- Product goal, audience, conversion intent, and tone.
- Technical stack (HTML/CSS/JS, React, Vue, Next.js, etc.).
- Constraints: accessibility level, performance budget, deadlines.
- Existing design system (if any) and what must remain unchanged.

## Workflow
1. Brief decoding and design direction:
   - Summarize product, audience, and desired emotion in one sentence.
   - Choose exactly one dominant art direction (not a mix).
   - Define 3 style pillars that will guide typography, color, layout, and motion.
2. Style selection framework (2026):
   - `Editorial Brutalist Precision`: bold type, hard contrast, asymmetric rhythm.
   - `Neo-Glass Depth`: frosted layers, depth hierarchy, subtle spectral accents.
   - `Kinetic Typography`: type-first storytelling with motion-led reading flow.
   - `Soft Industrial`: utility visuals + refined spacing + tactile controls.
   - `Retro-Future 2.5D`: modernized Y2K cues with strict spacing discipline.
   - `Organic Tech Atmosphere`: mesh gradients, natural curves, scientific UI tone.
   Pick one based on brand/audience fit and justify it briefly.
3. Implementation (production code):
   - Build responsive layouts for mobile + desktop from the first pass.
   - Use expressive typography with deliberate pairings (display + body + mono if needed).
   - Define CSS variables/tokens for color, spacing, radius, shadows, and motion.
   - Use meaningful animation (entry sequence, hover states, state transitions), not random effects.
4. Anti-generic AI audit:
   - Check for predictable block patterns and replace with intentional composition.
   - Remove cliche palettes and overused gradients that do not match the brief.
   - Ensure the interface has one memorable signature element.
5. Quality and validation:
   - Accessibility: semantic HTML, keyboard support, visible focus, contrast checks.
   - Performance: avoid heavy paint storms, reduce unnecessary blur/filters.
   - Consistency: spacing, rhythm, component states, and token reuse.

## Output contract
Respond in this order:
1. Design direction chosen and why it fits the brief.
2. Concrete implementation summary (tokens, layout, typography, motion).
3. Files/components changed with key behaviors.
4. Validation status (responsive, accessibility, performance, anti-generic audit).
5. Optional next iteration ideas.

## Guardrails
- Never default to common generic font stacks (Inter/Roboto/Arial/system) unless explicitly required by the user/system.
- Never ship cookie-cutter layouts (hero + three cards + CTA) without custom composition and brand-specific decisions.
- Never rely on visual noise to fake sophistication.
- Always keep accessibility, responsiveness, and performance as non-negotiable constraints.
- If the project already has a design system, evolve within that system instead of breaking consistency.

## Foundations
- `logic-propositional-reasoning`
- `algorithm-correctness-invariants`
- `testing-verification-foundations`
- `security-threat-modeling-foundations`

## Logical reliability checklist
- Assumptions from the brief are explicit and separated from verified constraints.
- The selected visual direction is justified with user and product context.
- Accessibility and performance checks are verifiable before final output.
- Trade-offs are documented so the design can be audited and iterated safely.

## Anti-generic checklist (must pass before finalizing)
- Unique typographic voice selected and applied consistently.
- Color system aligned to the chosen direction; no random rainbow accents.
- Layout has intentional hierarchy and at least one distinctive compositional move.
- Motion supports comprehension and brand tone.
- UI does not look like an interchangeable template from another product.

## Example prompts
- "Apply `frontend-ultramodern-2026` and redesign this SaaS landing with a premium editorial-tech direction."
- "Use `frontend-ultramodern-2026` to build a dashboard shell that feels futuristic but enterprise-ready."
- "Run `frontend-ultramodern-2026` and refactor this generic UI into a distinctive 2026 visual system."
