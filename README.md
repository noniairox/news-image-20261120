# The World Today — 20 November 2026 front page

[![make.fun](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/noniairox/news-image-20261120/rank.svg)](https://make.fun/bounty/news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/noniairox/news-image-20261120/reward.svg)](https://make.fun/bounty/news-image-20261120)

A one-page newspaper front page that sums up the world news of
20 November 2026 in a single image. The lead story is the
International Court of Justice ruling that Myanmar committed genocide
against the Rohingya, with the day's other big stories below it:
Anthropic's record $81.3 billion IPO, the Trump–Xi–Putin summit in
Shenzhen, Ukraine's third strike on the Crimean Bridge in four days,
and Cyclone Akvan's landfall on India's east coast.

## How it is made

`main.py` draws the whole front page with Pillow — masthead, dateline,
lead story in two columns, and four secondary stories — and writes
`entry.png` (1024×1024). The script is fully deterministic: no network
calls, no timestamps, no randomness. Running it twice produces a
byte-identical image.

```sh
python3 main.py
# writes entry.png into the current directory
# or set MAKEFUN_OUTPUT_DIR to choose the output folder
MAKEFUN_OUTPUT_DIR=/tmp/out python3 main.py
```

## Files

- `main.py` — the deterministic front-page renderer
- `entry.png` — the finished front page, 1024×1024
- `LICENSE` — MIT

## Sources

Every story on the page comes from reporting published on
19–20 November 2026:

- International Court of Justice ruling on Myanmar and the Rohingya —
  ICJ, BBC, The New York Times, The Hindu
- Anthropic's record IPO and the S&P 500's fifth straight loss —
  BBC, Reuters, AP
- Trump, Xi and Putin's first three-way summit and the APEC Shenzhen
  Outlook — BBC, AP, The New York Times
- Ukraine's strikes on the Crimean Bridge — BBC, Reuters
- Cyclone Akvan's landfall on the Odisha coast — The Hindu, IMD
- Houthi missile strike on Riyadh, Iran's Hormuz tanker attacks,
  Nvidia's California probe — Reuters, BBC
