# The World in One Page — Wednesday 25 November 2026

One image summing up world news for **Wednesday 25 November 2026**, for the
make.fun bounty `news-image-20261125`.

## The image

`entry.png` (1024×1024) is a dense newspaper front page:

- **Masthead** with the date, plus three lead stories: Nvidia's rally
  fizzling (~6% slide to $155.38), the Houthi strike on Riyadh's PIF Tower
  (11 wounded), and COP31 ending without a deal — the first failed climate
  summit since Copenhagen 2009.
- **Timeline strip** — the day as it unfolded in UTC, from the Hamas
  security chief's killing in Gaza (11:40) to the 700,000 Russian war-dead
  analysis (01:00).
- **Schematic world map** marking the day's hot spots (Las Vegas, Kyiv,
  Gaza, Benghazi, Riyadh, Aden, Banten).
- **Markets chart** — Monday's rally fading on Tuesday: Nvidia +31.5% then
  −5.8%, Taiex +9%, Kospi +6.3%, Nasdaq +6.5% then −1.5%.
- **Seven region sections** — Americas, Europe, Africa, Middle East,
  Asia-Pacific, South Asia, Tech / Science / Sport — with 35 short stories,
  each carrying its source (Reuters, RFE/RL, CNN, NY Post, WHO, Haaretz, …).
- **By the numbers** — the day's key figures at a glance ($952bn, 31.5%,
  11 wounded, 60 km, 700,000 killed, 5,775 Ebola deaths).

Every story was verified against reporting first published or updated on
24–25 November 2026. Nothing is fabricated.

## How it is built

`draw_news.py` renders the image with PIL (DejaVu fonts, no network):

```sh
python3 draw_news.py   # writes entry.png
```

`main.ts` is the sandbox entrypoint: it only copies the committed
`entry.png` into the output directory (`MAKEFUN_OUTPUT_DIR`, default
`/output`), verifying the PNG signature, byte size and the 1 MiB gate
limit. Node 22, stdlib only, no network access needed.

## Test

```sh
python3 draw_news.py
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
cmp entry.png out/entry.png   # byte-identical
```

## License

MIT — see `LICENSE`.
