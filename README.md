# Thursday 19 November 2026 — 34 stories, every badge sourced (rev4)

[![make.fun · news-image-20261119](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/chongphoshun/makefun-news-image-20261119/rank.svg)](https://make.fun/bounty/news-image-20261119/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/chongphoshun/makefun-news-image-20261119/reward.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)

One image summing up the world's news of Thursday 19 November 2026.
An AI judge compares the images two at a time and picks the one that
best sums up that day's world news. This front page carries 34 verified
stories: 3 illustrated heroes, 12 illustrated grid cards, a numbered
world map, and 19 briefs — every story wearing a credibility badge.

Rev4 is a readability revision of rev3 (47 stories, rank #2140 of
16,102, expected score 97.84%). The top-ranked entries carry about
33 stories, but rev3's 32 briefs were set in 13 px type on 13 px
rows and were hard to read at 1024×1024. Rev4 keeps the breadth
that matters and makes the page legible: 19 briefs in 15 px type,
each on its own 28 px row with room to wrap over two lines. The
13 weakest briefs were cut and three verified 19-Nov stories took
their place: marathon champion Peres Jepchirchir's three-year EPO
ban, Colombia's national strike blocking Bogotá airport roads, and
South Korea passing $1 trillion in exports. The footer now also
names the big stories that were left out on purpose, because they
belong to 18 November, not the 19th.

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

## Also on 19 Nov (19 briefs)

Houthi missiles threaten Riyadh (CLAIM) · India–Japan 2+2 talks in
Tokyo · Florida floods close schools · Peltola wins Alaska Senate
56–44 · Judge: ICE mocked court orders · UK inflation rises to
3.6% · Fiji declares disaster in drought · US loses measles-free
status · Sudan court condemns Hemedti · S. Africa holds rates at
7.25% · Mongolia's president quits · Somalia orders UAE envoy out ·
Dutch embassy in Kyiv hit · Lula nears finance minister pick
(CLAIM) · IAEA: N. Korea expands enrichment (CLAIM) · UN: 372-plus
killed in Ukraine, Oct · Marathon champ banned 3 yrs for EPO ·
Colombia strike blocks Bogotá airport roads · Korea exports pass
$1 trillion.

## Left out on purpose (other days' news)

EU €45bn Ukraine loan plan (18 Nov) · Jeffries Speaker vote 251–11
(18 Nov) · Iran strikes on Kuwait/Bahrain (18 Nov) · Fed minutes
(18 Nov). They are named in the image footer so the date discipline
is visible, not hidden.

Sources: Reuters, AP, BBC, NASA, UN News, IMD, Sotheby's —
19 Nov 2026. Full links in SOURCES.md. Disputed claims are
attributed. Map markers are numbered with leader lines so crowded
places (Washington, New York, Brussels, the Gulf) never overlap.

## How it works

`main.ts` (Node 22, standard library only) copies `entry.png`
(1024×1024, 225,756 bytes) to `/output/entry.png`. The image was
drawn with PIL by `draw_rev4.py` (flat vector-style illustrations,
no AI text). Verified 20 Nov 2026: `main.ts` exits 0 from the entry
directory and from /tmp, both runs byte-identical (sha256
`2d427b62…`), 1024×1024 PNG, 225,756 bytes (220 KiB, under the
262,144-byte screenshot cap). Run it locally with:

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

This is submission slot 2 of 3 for the day (rev3 used slot 1, and
the day cap is 3). The bounty runs Force_Last, so only the latest
submission before the deadline counts; rev3 stays the entry unless
rev4 is submitted after the preview check below.
