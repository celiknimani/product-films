# Brands

Verify every value on the live site each time.

## Extracting a brand from a live site

Use the repo first when there is one. Otherwise open the live site in a browser and run JavaScript to pull:

- **Fonts:** `document.fonts`, the computed `font-family` of body, h1 and h2, and the `@font-face` sources and weights actually loaded. For a face that Google Fonts does not have, embed the font file from the repo, or use the closest Google font and say so in the report.
- **Colours:** count the computed `color`, `background-color` and `border-color` across all elements and take the top values. Also collect any `background-image` gradients.
- **Shapes:** button and card border radius, shadows, pill or square buttons.
- **Logo:** the SVG from the `<img>` or inline `<svg>`, reused inline.
- **Voice:** the hero headline, section titles and button wording, so captions sound like the site.

Before any capture, press the site's own decline or "Essential only" button on the cookie banner. Hiding the banner with a broad CSS selector blanked a whole page once.

Scroll and screenshot two or three sections to see the layout rhythm. If the client also has a product app, inspect it too: the app and the marketing site often use different fonts and wording. If Figma links are given, read them with the Figma tools.

## Personal data

Mask personal data by burning it into the image (black boxes, blurred signatures) before it goes into the page. Never mask with a CSS overlay, since the original stays in the file.

For a full-page screenshot used in a scroll shot, blur client logos, names and quotes on the live page first (for example `filter: blur(8px)` on those elements through Playwright), then take the screenshot, so the blur is in the image.

## Known brands

- **Celik Nimani** (celiknimani.com, repo `celiknimani-portfolio`; verified 2026-11-20): Geist Sans and Geist Mono, ink #121212, lime accent #c9fe6e (accent text on lime is #121212), light #f1f1f1, muted #777777. Used by the ending card in `ending.md`.

Notes on client brands live in `private/brands.md`, which git ignores. Read it when it exists, and add a client there, never here, so client details stay out of the public repo.
