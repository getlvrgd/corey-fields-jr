# Corey Fields Jr. coaching landing page

Single-page, application-gated landing page for **New Build Coaching with Corey** (assumed working title). The page sells direct coaching and deal advisory for investors adding new construction. It does **not** sell the $27 Before You Build guide, the $997 New Build Orientation Program, or done-for-you building. Those appear only as a side door and in the FAQ.

## Run it

Static HTML/CSS/JS. No build step.

```bash
cd corey-fields-coaching
python3 -m http.server 8080
# open http://localhost:8080
```

Opening `index.html` straight from disk also works.

## Files

| File | Purpose |
|---|---|
| `index.html` | The page |
| `styles.css` | All styles (brand tokens at the top) |
| `script.js` | `PAGE_CONFIG` placeholder values, CTA wiring, scroll reveal, mobile sticky CTA |
| `CONTENT.md` | Every subject-specific fact on the page, with source tag and where it appears |
| `images/web/` | Source pack images (site + YouTube only, no stock) |
| `images/cut/` | Transparent WebP versions of the black-matte pack images (generated) |
| `tools/make_cutouts.py` | Regenerates `images/cut/` from `images/web/` (`python3 tools/make_cutouts.py`, needs Pillow + numpy) |
| `research-note.md`, `IMAGE-MANIFEST.md`, `claude-code-landing-page-prompt.md` | Original research pack |

## Placeholder swap list

Edit `PAGE_CONFIG` at the top of `script.js`. Nothing in the HTML needs to change.

| Key | Status | Behavior while empty | Where it shows |
|---|---|---|---|
| `PROGRAM_NAME` | **ASSUMED:** "New Build Coaching with Corey" | Uses the assumed name | Hero eyebrow, offer card title, mobile sticky bar |
| `APPLICATION_URL` | **Set:** https://www.lvrgd.co/book. **Primary CTA:** apply, then book a call | Every Apply button scrolls to the final CTA section (`#apply`) | Nav, hero, offer card, final CTA, footer, sticky bar |
| `PROGRAM_PRICE` | Not shown, per Felix. Pricing is covered on the call | Unused | Nowhere |
| `PROGRAM_DURATION` | **Set:** 8 months | | Included box header and terms |
| `CALL_CADENCE` | **Set:** whenever you need one | | Included list and terms |
| `MESSAGING_SLA` | Optional | Hidden (coaching item 07, offer row, promise sentence) | Those three spots |
| `SEAT_COUNT` | Optional, real cap only | Hidden | Offer card |
| `VSL_URL` | **Set:** https://www.lvrgd.co/book (same as Apply until a real video exists) | Hero shows `images/web/16-vsl-placeholder.jpg` with a play icon, not clickable | Hero video frame |
| `COHORT_DEADLINE` | Optional, real date only | Hidden. No fake scarcity | Offer card |

The dashed yellow chips are meant to be seen in review. Before publishing, either fill every required key or remove the row.

## Copy assumptions to confirm with Corey

- **Voice:** all page copy is written in first person as Corey Fields Jr. ("I", "my father, Corey Fields Sr., and I"). Image alt text, the "per site" note, fine print, and the footer risk line stay neutral on purpose. The program name still says "with Corey".

- The coaching is with Corey Jr. Corey Sr. is credited only as co-creator of the frameworks. He is not presented as a second coach.
- "Every application gets reviewed before a call is booked" describes the application-gated flow. Confirm it matches the real process.
- The FAQ answer for investors outside Atlanta says fit is decided on the application. Confirm Corey coaches other markets.
- "Full terms are shared before you commit to anything" (price FAQ). Confirm.
- The process guarantee: we work your pre-construction checklist until it is decision-ready, and we show up for every scheduled call. Process only. No money back, no returns promise.
- The six coaching phases reuse his public six-phase path. The bullets and "you finish with" lines under each phase are coaching-shape copy I wrote from his public themes. Confirm they match how he actually coaches.

## Image handling

- Several pack JPEGs were transparent PNGs flattened onto black. `tools/make_cutouts.py` flood-fills that black matte from the edges and writes WebP with alpha.
- `08-ten-mistakes-graphic.jpg` stays in its original form on a black card, because its black label pills connect to the matte.
- `09-six-phase-overview.jpg` crop is still generated but no longer used. The six phases are rendered as page sections instead.
- `images/cut/jobsite-measuring.jpg` is the middle print cropped out of `03-corey-on-jobsite-collage.jpg`.
- The hard cost and contingency line items in the worksheet section were read off the four cost bucket graphic inside `05-nbo-program-bundle.jpg`.
- `07` worksheet is clipped to the paper edge. The pencil tip past the paper is cut.
- `10-financials-proof-graphic.jpg` is **not used**. Illustrative profit numbers invite a student-result reading.
- `05` and `06` appear only in the "Other ways to work with us" side door.

## Hard rules (kept)

- No em dashes, en dashes, or semicolons in user-facing copy. Checked by script before handoff.
- One primary CTA (Apply). The secondary is the YouTube duplex video link.
- No invented testimonials, prices, awards, phone or WhatsApp, ROI, or student results.
- Site claims (25+ years, 500+ projects, $11M+ pipeline) are tagged "per site", with a footnote under the proof strip.
- The risk and compliance line is in the footer.

## Design

Layout follows the editorial style of kamil-mag.vercel.app (per Felix): centered serif hero with a video frame, bordered stat row, numbered problem grid, phase-by-phase coaching with line art and "you finish with" rows, an itemized worksheet, an "Included" box, and "alone vs with Corey" cards.

- Backgrounds alternate white `#FFFFFF` and beige `#F3EFE6`. Cards use `#F8F5EE` on white.
- Dark olive `#334218` is the only accent (italic headline phrases, labels, buttons, checks). Ink `#1A1A14`.
- Fonts: Instrument Serif (headlines, big numbers), Inter Tight (body), JetBrains Mono (labels). This replaces the original brief's Manrope/Inter at Felix's direction.
