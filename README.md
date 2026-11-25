# The World in One Page — 25 November 2026

[![make.fun · news-image-20261125](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![rank](https://make.fun/badge/news-image-20261125/aldi235/news-image-20261125/rank.svg)](https://make.fun/bounty/news-image-20261125/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![reward](https://make.fun/badge/news-image-20261125/aldi235/news-image-20261125/reward.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)

A single 1024×1024 newspaper front page that sums up Wednesday
25 November 2026's world news in one image, for the
`news-image-20261125` bounty ($100).

## What's on the page

- **Masthead** — "THE WORLD IN ONE PAGE", dated Wednesday 25 November 2026.
- **Three lead stories** — the Nvidia rally fizzling after Monday's
  +31.5% surge, the Houthis hitting Riyadh's PIF Tower a second time,
  and COP31 ending without a deal.
- **Timeline strip** — the day as it unfolded, from the Gaza strike at
  11:40 UTC to the 700,000 Russian war dead figure at 01:00 UTC.
- **Schematic world map** — the hot spots marked: Las Vegas, Kyiv, Gaza,
  Benghazi, Riyadh, Aden and Banten.
- **Markets chart** — Monday's rally (Nasdaq +6.5%, Nvidia +31.5%)
  against Tuesday's fade (Nvidia −5.8%), plus Asia's Tuesday surge.
- **Seven region sections, 35 stories** — Americas (7), Europe (6),
  Middle East (6), Africa (3), Asia-Pacific (4), South Asia (3) and
  Tech / Science / Sport (6). Every story is one short headline plus a
  one-line summary, ending with its source in red.
- **By the numbers** — $952bn, +31.5%, 11 wounded, 60 km, 700,000 and
  5,775: the day's six figures that matter most.

38 stories in total (3 leads + 35 region stories), all drawn from real
reporting dated 24–25 November 2026.

## How it is built

`draw_news.py` renders the whole page with Pillow and the system DejaVu
fonts — no network, no downloaded assets. `main.ts` (Node standard
library only) copies the finished `entry.png` into the output directory
and checks the copy is byte-identical, a valid PNG, and under 1 MiB.

```sh
python3 draw_news.py
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts && cmp entry.png out/entry.png
```

The image is 1024×1024 and the PNG is well under the 1 MiB limit.
