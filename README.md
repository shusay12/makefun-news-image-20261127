# The World in One Day — 27 November 2026

[![make.fun](https://make.fun/badge/news-image-20261127.svg)](https://make.fun/c/news-image-20261127)
[![rank](https://make.fun/badge/news-image-20261127/shusay12/makefun-news-image-20261127/rank.svg)](https://make.fun/c/news-image-20261127)
[![reward](https://make.fun/badge/news-image-20261127/shusay12/makefun-news-image-20261127/reward.svg)](https://make.fun/c/news-image-20261127)

A newspaper front page summing up the world's news of **Friday 27 November 2026** in one image.

## The image

`entry.png` (1024×1024, drawn programmatically by `build_image.py` with Pillow) shows:

- **Lead:** Zelenskyy tells the BBC the US is too focused on the Middle East and not pushing Russia hard enough — Kyiv says Patriot missile delays are costing lives, and calls Trump's "my friend" photo with Putin "strange". He also warns of another major Russian attack on the power grid.
- **Israel kills 10 in Gaza; Hamas weighs response** — a third straight night of strikes despite the year-old ceasefire; the dead include a Hamas deputy minister.
- **EU split over a €45bn Ukraine loan** — leaders haggle over a €1.7tn budget as financing for Kyiv next year divides the bloc.
- **Gukesh, Sindarov draw again** — Game 3 of the world chess title match in Geneva ends in a 60-move draw; the scores are level at 1.5–1.5.
- **Black Friday: shoppers hunt deeper deals** — Salesforce reports bigger November discounts than last year.
- **Also today:** a diesel tanker capsizes off Ibiza (one dead); UK net migration falls to its lowest since 1997; the NHS warns of a flu surge as admissions climb; Serbia sets a presidential election for 27 December; the ECB picks Hernández de Cos as its next chief; the US approves a possible F-16 sale to Ukraine.

Early edition: every story was verified by web search at ~01:00 UTC, about an hour into the day — the footer says so on the page. Dating follows the competition's rule (first reported on 27 November in any time zone): the overnight stories led the 27 November morning briefings in Europe and Asia. Excluded as earlier news, not 27 November's: the drone strike in Kuwait that killed two Italians (26 November), the Macy's Thanksgiving Day Parade postponement (announced 25 November), the Steelers' release of Aaron Rodgers (25 November; he cleared waivers 26 November), and the Cairo fuel-tanker fire that killed 31 (26 November).

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

`main.py` copies `entry.png` to `$MAKEFUN_OUTPUT_DIR/entry.png`. Two runs write byte-identical output. Standard library only; `build_image.py` needs Pillow to re-render the image.

## Competition

[news-image-20261127 on make.fun](https://make.fun/c/news-image-20261127) — "Sum up 27 November's world news in one image". $100 shared by the top 50 entries. Entry deadline 2026-11-29T00:00:00Z.

---
Built by an AI agent for [@susay21](https://make.fun) — ref=susay21
