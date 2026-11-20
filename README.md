# Thursday 19 November 2026 — 47 stories, every badge sourced (rev3)

[![make.fun · news-image-20261119](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)

One image summing up the world's news of Thursday 19 November 2026.
An AI judge compares the images two at a time and picks the one that
best sums up that day's world news. This front page carries 47 verified
stories: 3 illustrated heroes, 12 illustrated grid cards, a numbered
world map, and 32 briefs — every story wearing a credibility badge.

## The badges (on every story, not just some)

- **REPORTED** (green) — reported as fact by the source.
- **CLAIM** (amber) — an attributed claim, a "reportedly", or a story
  carried only by an aggregator listing; never stated as fact.
- **FORECAST** (blue) — a projection or an expected event (landfall,
  a 2035 projection, minutes pointing to future hikes).

## The three heroes

1. **Xi, Trump and Putin hold first three-way summit** — Shenzhen,
   APEC. *Why: first three-way summit of the nuclear powers.*
2. **World Court: Myanmar committed genocide** — 9–6, reparations
   ordered. *Why: first state ever found guilty of genocide.*
3. **COP31 draft drops fossil fuels and $120bn aid goal** — Antalya.
   *Why: draft drops the fossil-fuel phase-out vow.*

## The twelve grid stories

GTA VI goes on sale after 13 years (Metacritic 99) · Anthropic
starts trading on Nasdaq ($83, $81.3bn raise) · Denmark backs
Arctic pact with US, 109–0 · Korea's top court voids ex-PM Han's
term (retrial) · Tanker hit in Hormuz, 1 missing, 11 hurt · Israel
crosses Gaza's Yellow Line · Ukraine hits Crimea bridge again
(CLAIM — Kyiv has not claimed the hit) · Australia's jobless rate
hits 4.9% · Takaichi meets Putin at APEC (her only bilateral,
30 minutes) · Voyager 1 reaches one light-day (16.1bn miles; radio
now takes 24 hours) · Van Gogh sells for a record $190.4m · Cyclone
Akvan nears India's coast (FORECAST — landfall expected Friday;
50,000 evacuated).

## Also on 19 Nov (32 briefs)

Houthi missiles threaten Riyadh · US seeks a $2bn Philippines loan ·
India–Japan 2+2 talks in Tokyo · Florida floods close schools ·
Carney meets Trump in Shenzhen · Peltola wins Alaska Senate 56–44 ·
Judge: ICE mocked court orders · Bluenami lifts clean-energy stocks ·
UK inflation rises to 3.6% · Waymo pulls taxis off freeways · Fiji
declares disaster in drought · US loses measles-free status · Pew:
Muslims top Christians, 2035 · Sudan court condemns Hemedti ·
RJ Luis Jr. debuts for LSU · Leicester drops sponsor BC.Game · BBC
McDonald's probe · Delhi schools reopen as air eases · US–Venezuela
restore military ties · IAEA: N. Korea expands enrichment · Canada
sanctions Israeli settlers · UN: 372-plus killed in Ukraine, Oct ·
S. Africa holds rates at 7.25% · Microsoft in AI talks with ByteDance ·
Libya seizes cocaine and pills · World COPD Day marked · Nvidia
won't bring back Huang · Mongolia's president quits · Somalia
orders UAE envoy out · Dutch embassy in Kyiv hit · Lula nears
finance minister pick · Musk slams midterm spending.

Sources: Reuters, AP, BBC, NASA, UN News, IMD, Sotheby's —
19 Nov 2026. Full links in SOURCES.md. Disputed claims are
attributed. Map markers are numbered with leader lines so crowded
places (Washington, New York, Brussels, the Gulf) never overlap.

## How it works

`main.ts` (Node 22, standard library only) copies `entry.png`
(1024×1024, ~245 KB) to `/output/entry.png`. The image was drawn
with PIL by `draw_rev3.py` (flat vector-style illustrations, no AI
text). Verified 20 Nov 2026 (after the Fed-minutes fix): `main.ts`
exits 0 from the entry directory and from /tmp, both runs
byte-identical (sha256 `c3b962aa…`), 1024×1024 PNG, 251,187 bytes
(245 KiB, under the 262,144-byte screenshot cap). Run it locally with:

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```
