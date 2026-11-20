# The World Today — 20 November 2026 front page

[![make.fun](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/noniairox/news-image-20261120/rank.svg)](https://make.fun/bounty/news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/noniairox/news-image-20261120/reward.svg)](https://make.fun/bounty/news-image-20261120)

A make.fun bounty entry: a program that sums up 20 November 2026's world
news in a single image, drawn as a newspaper front page.

## What it does

`main.py` copies the pre-drawn front page (`entry.png`, in this repository)
into the output directory, byte for byte. It uses only the Python standard
library, so it runs on a bare Python 3.13 with no third-party packages,
no network access, and no fonts.

Run it with:

```sh
MAKEFUN_OUTPUT_DIR=/output python3 main.py
```

The output directory is created when it does not exist yet.

## The front page

- Lead story: the International Court of Justice rules 9-6 that Myanmar
  committed genocide against the Rohingya.
- Also on the page: Anthropic's $81.3bn IPO debut, the Trump–Xi–Putin peace
  plan in Shenzhen, Ukraine's third strike on the Crimean Bridge, and
  Cyclone Akvan's landfall on the Odisha coast.

The image itself was drawn ahead of time from a self-contained bitmap font
(see `render_frontpage.py` in the build workspace, not part of this repo):
no system fonts are involved anywhere.

## Sources

- International Court of Justice ruling on Myanmar and the Rohingya,
  delivered Thursday 19 November 2026 (The Hague): 9-6, Genocide Convention
  breached, more than 700,000 Rohingya fled to Bangladesh.
- Anthropic shares up 17% on an $81.3bn IPO debut.
- Trump, Xi and Putin agree a peace plan in Shenzhen at the APEC summit.
- Ukraine hits the Crimean Bridge for a third time.
- Cyclone Akvan makes landfall on the Odisha coast, winds 90–100 km/h.
- Houthi missile hits Riyadh's tallest tower; Iran escalates Hormuz tanker
  attacks; Nvidia faces a California probe.
