---
name: هدايا سلمى — Salma Gifts
description: Names first — the couple's names on a pearl-rimmed mirror tray, on ivory, gold and warm brown.
colors:
  ivory-ground: "#FBF7F0"
  warm-surface: "#FFFDF9"
  ivory-tint: "#F4ECDF"
  brown-ink: "#3B2A1C"
  brown-muted: "#6B5A4C"
  gold: "#C9A266"
  gold-soft: "#E9D3A2"
  gold-deep: "#A8813F"
  gold-text: "#8A6428"
  hairline: "#E8DCC6"
typography:
  display:
    fontFamily: "Aref Ruqaa, El Messiri, serif"
    fontSize: "clamp(32px, 6vw, 54px)"
    fontWeight: 700
    lineHeight: 1.4
  names:
    fontFamily: "Amiri, Aref Ruqaa, serif"
    fontSize: "clamp(30px, 9.4vw, 46px)"
    fontWeight: 700
    lineHeight: 1.35
  body:
    fontFamily: "El Messiri, Tajawal, system-ui, sans-serif"
    fontSize: "17px"
    fontWeight: 400
    lineHeight: 1.85
  small:
    fontFamily: "Tajawal, El Messiri, system-ui, sans-serif"
    fontSize: "14px"
    fontWeight: 500
    lineHeight: 1.6
rounded:
  label: "14px"
  field: "16px"
  photo: "20px"
  feature: "26px"
  pill: "999px"
spacing:
  gutter: "20px"
  section: "52px"
  section-wide: "76px"
components:
  button-primary:
    backgroundColor: "{colors.gold}"
    textColor: "{colors.brown-ink}"
    rounded: "{rounded.pill}"
    padding: "10px 30px"
    height: "52px"
  button-quiet:
    backgroundColor: "{colors.warm-surface}"
    textColor: "{colors.brown-ink}"
    rounded: "{rounded.pill}"
    padding: "10px 30px"
  name-field:
    backgroundColor: "{colors.warm-surface}"
    textColor: "{colors.brown-ink}"
    rounded: "{rounded.field}"
    padding: "10px 14px"
  photo-label:
    backgroundColor: "{colors.warm-surface}"
    textColor: "{colors.brown-ink}"
    rounded: "{rounded.label}"
    padding: "8px 14px"
---

# Design System: هدايا سلمى

## Overview

**Creative North Star: "Your names, on the tray."** Every Salma piece carries the couple's names, so the site opens on them: the visitor types two names and sees them stretched with kashida on a round mirror tray with a pearl rim, exactly how the workshop writes them, then books with one button. Everything after that is calm and short: real product photos, a boutique-style price menu, a brief story, the promise (inspect and pay on delivery, two days, all governorates).

**Key Characteristics:**
- Ivory ground, gold as hairlines, rims and price numbers, warm brown text. No dark sections.
- Real photos stay clear; text on a photo sits in a small ivory label card.
- One authored motion: the kashida grows into the names, then one light sweep crosses the mirror.
- Copy in Modern Standard Arabic; the slogan «لتبقى ذكرياتكم الجميلة، خالدة.» sits directly under the H1 and in the footer.

## Colors

### Primary
- **Gold** `#C9A266`: rules, the diamond divider, rims, active borders, the primary button gradient (`#EBD7AA → #C9A266`). Never body text.
- **Gold deep** `#A8813F`: large price numbers, the slogan, the H1 accent word (large text only).
- **Gold text** `#8A6428`: links and any small gold text (meets 4.5:1 on ivory).

### Neutral
- **Ivory ground** `#FBF7F0`, **warm surface** `#FFFDF9` (fields, labels), **ivory tint** `#F4ECDF` (alternate sections, footer), **hairline** `#E8DCC6`.
- **Brown ink** `#3B2A1C` for text, **brown muted** `#6B5A4C` for secondary text. Never pure black.

### Named Rules
- **No Fog Rule:** never lay a white haze over a photo; use an ivory label card instead (owner's explicit rule).
- **Gold Is Line, Not Field:** gold fills only the primary button and selected states; elsewhere it is a 1–1.5px line or a number.

## Typography

- **Display (Aref Ruqaa 700):** H1, H2, brand name, slogan, closing title.
- **Names (Amiri 700):** only the names on the tray and tag preview. Aref Ruqaa renders the tatweel at zero width, so it cannot show kashida; Amiri can.
- **Body (El Messiri 400–700):** paragraphs, buttons, prices.
- **Small (Tajawal 500):** labels, captions, breadcrumb, notes.
- Prices use Western digits with `tabular-nums`. All fonts are self-hosted in `/assets/fonts/`.

## Layout

- Container 1160px with a 20px gutter; reading columns 740px.
- Sections are 52px tall in padding on mobile and 76px from 900px up; alternate sections use the ivory tint.
- Home, mobile: H1 → slogan → tray (~296px) → name fields → product toggle → primary button, all inside 844px. Desktop: the name fields flank the tray as place cards.
- Bouquet styles: a horizontal snap rail on mobile and five columns on desktop.
- Product pages: breadcrumb → H1, lead, price, button → photo mosaic (one large, two stacked) → about → FAQ.

## Elevation & Depth

- One soft shadow, `0 14px 34px -18px rgba(70,48,22,.35)`, used for place cards, photos and the toast. The tray carries its own deeper drop shadow.
- No hard offset shadows and no glass, except the sticky header blur.

## Shapes

- Rounded rectangles for photos (20–26px), fields (16px) and labels (14px). Pill buttons.
- Diamonds (rotated squares) for bullets, breadcrumb separators and the divider.
- Circles only for the tray, tag and step numbers. No arches.

## Components

- **Name maker** (`#maker`): the tray (CSS mirror, SVG pearl ring, ring boxes with the first letters), the tag scene (a bouquet photo with an acrylic name tag), two name fields, a collapsed date control, the product toggle (tray 15 / bouquet with tag 20) and the submit button. Submitting copies the order text to the clipboard, opens Instagram DM and shows a toast.
- **Photo label:** an ivory card at the bottom of a photo, with the style name in display type and the price in gold text.
- **Price menu:** rows with a thumbnail, name and line, and a gold price; two columns on desktop.
- **FAQ:** hairline-separated `details`, with a drawn plus/minus. Every FAQ also ships as FAQPage JSON-LD.

## Do's and Don'ts

- Do keep every existing URL; add style pages under `/masakat-arayes/<style>/`.
- Do use the words people actually search in titles and H1s (مسكة عروس، صينية خطوبة), with فصحى body copy.
- Don't add kickers or eyebrow labels above headings, gradient text, or glyph icons.
- Don't invent reviews, ratings or customer names.
- Don't use dark backgrounds or put text directly on photos.
- Not canonized: the CSS-drawn mirror is an interim stand-in. The finish review asked for a real photographic cutout of an empty tray, pending a photo from the owner.
