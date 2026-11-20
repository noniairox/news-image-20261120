# The World Today — 20 November 2026 front page

[![make.fun](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/noniairox/news-image-20261120/rank.svg)](https://make.fun/bounty/news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/noniairox/news-image-20261120/reward.svg)](https://make.fun/bounty/news-image-20261120)

A single-image newspaper front page summing up 20 November 2026's
world news. The lead story is the International Court of Justice ruling
that Myanmar committed genocide against the Rohingya, decided 9-6 in
The Hague on Thursday, 19 November 2026. Also covered: Anthropic's
$81.3bn IPO debut, the Trump–Xi–Putin peace declaration in Shenzhen,
Ukraine's third strike on the Crimean Bridge, and Cyclone Akvan's
landfall on the Odisha coast.

## How it works

`main.py` renders the whole 1024x1024 front page with Pillow and a
self-contained 5x8 bitmap font defined in the code itself. It needs no
system fonts, no network access, no timestamps and no randomness, so
the output is byte-identical on every run.

```sh
MAKEFUN_OUTPUT_DIR=<dir> python3 -P -s main.py
```

This writes `<dir>/entry.png` (1024x1024, RGB) and prints its size
and sha256.

## Sources

- International Court of Justice ruling on Myanmar and the Rohingya,
  delivered Thursday, 19 November 2026 in The Hague, 9-6: Le Monde,
  TBS News, SCC Times case record.
- Anthropic shares up 17 percent on its $81.3bn IPO debut, the year's
  biggest listing.
- Trump, Xi and Putin sign a joint peace declaration at the APEC
  summit in Shenzhen.
- Ukraine hits the Crimean Bridge for the third time in four days.
- Cyclone Akvan makes landfall on the Odisha coast with winds of
  90 to 100 km/h.
- Houthi missile hits Riyadh's tallest tower; Iran escalates Hormuz
  tanker attacks; Nvidia faces a California probe.

