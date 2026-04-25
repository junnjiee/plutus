---
version: alpha
name: Plutus
description: Olympian dark-mode finance — where Hermes' precision meets Plutus' prosperity. A dark-first design system for expense management, built on the same near-black canvas and engineered typography as the Hermes agent dashboard, with a gold accent befitting the Greek god of wealth.
colors:
  primary: "#08090A"
  secondary: "#8A8F98"
  tertiary: "#D4A843"
  neutral: "#0F1011"
  surface: "#16181B"
  surface-elevated: "#1E2024"
  on-primary: "#F0F1F3"
  on-secondary: "#62666D"
  on-tertiary: "#08090A"
  on-surface: "#D0D6E0"
  success: "#2DA44E"
  danger: "#E23B4A"
  warning: "#D29922"
  info: "#58A6FF"
  gold-dim: "#9E7B2D"
  gold-bright: "#F5D878"
  border-subtle: "#14161A"
  border-standard: "#22252A"
  border-strong: "#33373E"
typography:
  display-xl:
    fontFamily: Inter
    fontSize: 4rem
    fontWeight: 510
    lineHeight: 1.05
    letterSpacing: "-1.28px"
  display:
    fontFamily: Inter
    fontSize: 2.5rem
    fontWeight: 510
    lineHeight: 1.1
    letterSpacing: "-0.8px"
  h1:
    fontFamily: Inter
    fontSize: 1.75rem
    fontWeight: 590
    lineHeight: 1.2
    letterSpacing: "-0.48px"
  h2:
    fontFamily: Inter
    fontSize: 1.25rem
    fontWeight: 510
    lineHeight: 1.3
    letterSpacing: "-0.2px"
  h3:
    fontFamily: Inter
    fontSize: 1rem
    fontWeight: 590
    lineHeight: 1.4
    letterSpacing: "-0.08px"
  body-lg:
    fontFamily: Inter
    fontSize: 1rem
    fontWeight: 400
    lineHeight: 1.6
  body-md:
    fontFamily: Inter
    fontSize: 0.875rem
    fontWeight: 400
    lineHeight: 1.55
  body-sm:
    fontFamily: Inter
    fontSize: 0.8125rem
    fontWeight: 400
    lineHeight: 1.5
  label-caps:
    fontFamily: Inter
    fontSize: 0.6875rem
    fontWeight: 510
    lineHeight: 1.4
    letterSpacing: "0.06em"
  mono-value:
    fontFamily: "JetBrains Mono"
    fontSize: 0.875rem
    fontWeight: 500
    lineHeight: 1.4
    letterSpacing: "0em"
  mono-caps:
    fontFamily: "JetBrains Mono"
    fontSize: 0.6875rem
    fontWeight: 500
    lineHeight: 1.5
    letterSpacing: "0.05em"
rounded:
  xs: 2px
  sm: 4px
  md: 6px
  lg: 8px
  xl: 12px
  2xl: 16px
  full: 9999px
spacing:
  xs: 4px
  sm: 8px
  md: 16px
  lg: 24px
  xl: 32px
  2xl: 48px
  3xl: 64px
components:
  button-primary:
    backgroundColor: "{colors.tertiary}"
    textColor: "{colors.on-tertiary}"
    rounded: "{rounded.md}"
    padding: 8px 16px
  button-primary-hover:
    backgroundColor: "{colors.gold-bright}"
    textColor: "{colors.on-tertiary}"
  button-secondary:
    backgroundColor: "rgba(255,255,255,0.04)"
    textColor: "{colors.on-primary}"
    rounded: "{rounded.md}"
    padding: 8px 16px
  button-secondary-hover:
    backgroundColor: "rgba(255,255,255,0.08)"
  button-ghost:
    backgroundColor: transparent
    textColor: "{colors.on-surface}"
    rounded: "{rounded.md}"
    padding: 6px 10px
  button-ghost-hover:
    backgroundColor: "rgba(255,255,255,0.04)"
  button-danger:
    backgroundColor: "rgba(226,59,74,0.12)"
    textColor: "{colors.danger}"
    rounded: "{rounded.md}"
    padding: 8px 16px
  button-danger-hover:
    backgroundColor: "rgba(226,59,74,0.2)"
  card:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.on-surface}"
    rounded: "{rounded.xl}"
    padding: 20px
  card-elevated:
    backgroundColor: "{colors.surface-elevated}"
    textColor: "{colors.on-surface}"
    rounded: "{rounded.xl}"
    padding: 20px
  input:
    backgroundColor: "rgba(255,255,255,0.03)"
    textColor: "{colors.on-primary}"
    rounded: "{rounded.md}"
    padding: 10px 12px
  input-focus:
    backgroundColor: "rgba(255,255,255,0.03)"
    rounded: "{rounded.md}"
    padding: 10px
  badge-gold:
    backgroundColor: "rgba(212,168,67,0.12)"
    textColor: "{colors.tertiary}"
    rounded: "{rounded.full}"
    padding: 2px 10px
  badge-success:
    backgroundColor: "rgba(45,164,78,0.12)"
    textColor: "{colors.success}"
    rounded: "{rounded.full}"
    padding: 2px 10px
  badge-danger:
    backgroundColor: "rgba(226,59,74,0.12)"
    textColor: "{colors.danger}"
    rounded: "{rounded.full}"
    padding: 2px 10px
  badge-neutral:
    backgroundColor: "rgba(255,255,255,0.06)"
    textColor: "{colors.on-surface}"
    rounded: "{rounded.full}"
    padding: 2px 10px
  table-row:
    backgroundColor: transparent
    textColor: "{colors.on-surface}"
    padding: 12px 16px
  table-row-hover:
    backgroundColor: "rgba(255,255,255,0.03)"
  sidebar:
    backgroundColor: "{colors.neutral}"
    textColor: "{colors.on-surface}"
    padding: 16px
  nav-item:
    backgroundColor: transparent
    textColor: "{colors.on-secondary}"
    rounded: "{rounded.md}"
    padding: 8px 12px
  nav-item-active:
    backgroundColor: "rgba(212,168,67,0.08)"
    textColor: "{colors.tertiary}"
  nav-item-hover:
    backgroundColor: "rgba(255,255,255,0.04)"
    textColor: "{colors.on-primary}"
  stat-card:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.on-surface}"
    rounded: "{rounded.lg}"
    padding: 20px
---

## Overview

Plutus inherits the Olympia aesthetic from Hermes — the same near-black canvas, the same engineered precision, the same devotion to luminance hierarchy over color. Where Hermes is the messenger (speed, connectivity, interface), Plutus is the treasury (substance, accumulation, prosperity). This distinction manifests as a single chromatic shift: Hermes' indigo-violet accent becomes Plutus' gold — not decorative, but symbolic. Gold is the material of wealth; it is Plutus' domain.

The design system is dark-mode-native. Light surfaces do not exist as backgrounds — only as text, borders, and the faintest surface tints. Depth is communicated through background luminance steps (`#08090A` → `#0F1011` → `#16181B` → `#1E2024`) and semi-transparent white borders, never through heavy shadows. Typography uses Inter with `cv01` and `ss03` OpenType features, just like the Hermes dashboard — but Plutus introduces JetBrains Mono for financial figures, giving amounts the same typographic precision that code receives in the Hermes UI.

The overall mood is composed, confident, and deliberate. This is a tool for understanding where your money goes — the interface should feel like a well-organized vault, not a casino.

## Colors

The color system is achromatic by default, with gold as the sole chromatic accent. Semantic colors (success, danger, warning, info) are used only for their designated purpose — never decoratively.

- **Primary (#08090A):** The deepest background — the vault floor. Nearly pure black with an imperceptible cool undertone, identical to the Hermes dashboard canvas.
- **Neutral (#0F1011):** Sidebar and panel backgrounds. One luminance step above primary.
- **Surface (#16181B):** Default card and container background. The primary working surface.
- **Surface Elevated (#1E2024):** Raised surfaces — modals, dropdowns, popovers. The highest luminance before chromatic color.
- **Tertiary / Gold (#D4A843):** The interaction driver — buttons, links, selected states, active navigation. A warm, muted gold that reads as "wealth" without reading as "flashy". It avoids the brashness of pure yellow or the coldness of olive.
- **Gold Dim (#9E7B2D):** De-emphasized gold for secondary accents — hover states on muted elements, subtle borders.
- **Gold Bright (#F5D878):** High-emphasis gold for primary hover states and highlight moments. Used sparingly.
- **On Primary (#F0F1F3):** Primary text — near-white with a cool cast. Not pure white, which would cause eye strain on dark backgrounds.
- **On Surface (#D0D6E0):** Secondary text — cool silver-gray for body content and descriptions.
- **On Secondary (#62666D):** Muted text — timestamps, metadata, placeholders.
- **Success (#2DA44E):** Positive financial indicators, income, budget under-limit.
- **Danger (#E23B4A):** Negative indicators, overspend, destructive actions.
- **Warning (#D29922):** Caution states, approaching budget limits.
- **Info (#58A6FF):** Informational indicators, neutral insights.
- **Border Subtle (#14161A):** Ultra-subtle dividers — the default separation. On dark backgrounds, renders visually equivalent to `rgba(255,255,255,0.05)`.
- **Border Standard (#22252A):** Standard card and input borders. Visually equivalent to `rgba(255,255,255,0.08)`.
- **Border Strong (#33373E):** Emphasized borders for focused or important elements. Visually equivalent to `rgba(255,255,255,0.12)`.

## Typography

Inter with OpenType features `cv01` (alternate lowercase 'a') and `ss03` (cleaner geometric forms) is the primary typeface — shared with the Hermes dashboard. JetBrains Mono is introduced for financial amounts and data values, giving numbers the same precision and visual weight that code receives in developer tools.

- **Display XL (4rem / 510):** Hero metrics, total spending. Aggressive negative tracking (-1.28px) creates compressed, authoritative numbers.
- **Display (2.5rem / 510):** Section totals, chart headings. Still compressed at -0.8px.
- **H1 (1.75rem / 590):** Page titles, dashboard section headers.
- **H2 (1.25rem / 510):** Card titles, sub-section headings.
- **H3 (1rem / 590):** Feature titles, small section headers.
- **Body LG (1rem / 400):** Primary reading text, descriptions.
- **Body MD (0.875rem / 400):** Standard UI text, table content, form labels.
- **Body SM (0.8125rem / 400):** Compact text, secondary table content.
- **Label Caps (0.6875rem / 510):** Navigation labels, section labels, category headers. Uppercase with 0.06em tracking.
- **Mono Value (0.875rem / 500):** Financial amounts, quantities, data values in JetBrains Mono. Tabular figures (`tnum`) for alignment.
- **Mono Caps (0.6875rem / 500):** Currency codes, technical labels. Uppercase with 0.05em tracking.

### Principles

- Weight 510 is the workhorse — between regular and medium, it provides emphasis without shouting. Shared with Hermes.
- Weight 590 replaces traditional semibold for strong emphasis — headings, active states.
- Weight 400 is for reading. Weight 300 is avoided entirely.
- Negative letter-spacing at display sizes creates the compressed, engineered feel. Tracking relaxes as size decreases.
- JetBrains Mono uses `tnum` (tabular numbers) for all financial figures — amounts align in columns.
- Label Caps and Mono Caps use uppercase to create visual hierarchy through case, not weight.

## Layout

Spacing follows an 8px base grid, consistent with the Hermes dashboard.

- **xs (4px):** Inline gaps, icon-to-text spacing.
- **sm (8px):** Tight component internal spacing, list item gaps.
- **md (16px):** Standard component padding, inter-element gaps.
- **lg (24px):** Inter-component gaps, card internal spacing.
- **xl (32px):** Section-level spacing.
- **2xl (48px):** Major section breaks.
- **3xl (64px):** Page-level vertical rhythm.

### Dashboard Layout

The expense dashboard uses a sidebar + content layout:
- **Sidebar:** 240px fixed width, collapsible to 60px icon-only on smaller screens.
- **Content:** Fluid, max-width ~1200px for readability.
- **Stat cards:** 4-column grid at desktop, 2-column at tablet, stacked on mobile.
- **Expense table:** Full-width within content area, responsive column hiding.

## Elevation & Depth

Depth is communicated through background luminance and semi-transparent borders — never heavy shadows. This mirrors the Hermes dashboard's approach.

| Level | Treatment | Use |
|-------|-----------|-----|
| Base | `#08090A` background, no shadow | Page background |
| Panel | `#0F1011` background | Sidebar, side panels |
| Surface | `#16181B` + `rgba(255,255,255,0.08)` border | Cards, containers |
| Elevated | `#1E2024` + `rgba(255,255,255,0.08)` border | Modals, dropdowns, popovers |
| Focus | `1px solid rgba(212,168,67,0.5)` outline | Keyboard focus on all interactive elements — gold ring instead of blue, befitting the treasury |

Subtle shadows are used sparingly — only for floating elements that need clear separation from the canvas:

- **Dropdown shadow:** `rgba(0,0,0,0.3) 0px 4px 16px`
- **Modal shadow:** `rgba(0,0,0,0.4) 0px 8px 32px`

## Shapes

Rounded corners follow a progressive scale. The system avoids extremes — no fully rounded cards, no sharp buttons.

- **xs (2px):** Micro elements, inline code, tiny badges.
- **sm (4px):** Small containers, tags.
- **md (6px):** Buttons, inputs, interactive elements.
- **lg (8px):** Cards, list items, table rows.
- **xl (12px):** Featured cards, panels.
- **2xl (16px):** Large panels, dialogs.
- **full (9999px):** Pills, badges, avatars, category tags.

## Components

### Buttons

- `button-primary` is gold on dark — the singular high-emphasis action per view. "Add Expense", "Save".
- `button-secondary` is translucent white on dark — secondary actions. "Cancel", "Filter".
- `button-ghost` is transparent with text — tertiary actions, toolbar buttons, icon buttons.
- `button-danger` uses a tinted red background with red text — destructive actions. "Delete".

All buttons use weight 510 at 0.875rem, matching the Hermes dashboard's button sizing.

### Cards

- `card` uses the surface background (`#16181B`) with standard border. Default container for grouped content.
- `card-elevated` uses the elevated surface (`#1E2024`) for modals and floating panels.
- Stat cards display a label (label-caps), a large value (display or display-xl), and optional change indicator.

### Inputs

- `input` uses a near-transparent background with standard border.
- `input-focus` adds a gold-tinted border to indicate active state.
- Select dropdowns and textareas follow the same pattern.

### Badges

- `badge-gold` for category labels and highlighted tags.
- `badge-success` for positive states (under budget, income).
- `badge-danger` for negative states (over budget, overspend).
- `badge-neutral` for informational tags, neutral categories.

### Table

- `table-row` is transparent by default with standard text.
- `table-row-hover` adds a faint white tint on hover for scanability.
- Column alignment: left for text, right for amounts (using mono-value).
- Zebra striping is NOT used — the dark canvas provides sufficient separation.

### Navigation

- `sidebar` is the primary navigation container at `#0F1011`.
- `nav-item` is transparent with muted text.
- `nav-item-active` shows a gold-tinted background with gold text — the active route glows.
- `nav-item-hover` adds a faint white tint.

## Do's and Don'ts

- **Do** use Inter with `cv01` and `ss03` on all text — these features are fundamental to the Olympia aesthetic.
- **Do** use JetBrains Mono for all financial amounts with `tnum` enabled — numbers must align.
- **Do** use weight 510 as the default emphasis weight — it's the shared signature between Hermes and Plutus.
- **Do** use gold (`#D4A843`) as the sole chromatic accent — it carries Plutus' identity.
- **Do** use luminance stepping for depth — darker backgrounds are deeper, lighter backgrounds are elevated.
- **Do** use semi-transparent white borders (`rgba(255,255,255,0.05–0.12)`) instead of solid borders.
- **Do** use the gold focus ring for keyboard accessibility — `rgba(212,168,67,0.5)`.
- **Don't** use pure white (`#FFFFFF`) as primary text — `#F0F1F3` prevents eye strain.
- **Don't** use heavy shadows for elevation — luminance stepping is the system.
- **Don't** apply gold decoratively — it's reserved for interaction, selection, and identity.
- **Don't** use positive letter-spacing on display text — tracking is always negative or zero.
- **Don't** use weight 700 (bold) — the system maximum is 590.
- **Don't** introduce additional chromatic colors — extend the semantic palette first if needed.
- **Don't** use zebra striping in tables — the dark canvas provides separation.
- **Don't** nest component variants — `button-primary-hover` is a sibling, not a child.
