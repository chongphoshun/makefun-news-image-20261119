# The World in One Day — Thursday, 19 November 2026 (rev2)

[![make.fun · news-image-20261119](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/chongphoshun/makefun-news-image-20261119/rank.svg)](https://make.fun/bounty/news-image-20261119/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/chongphoshun/makefun-news-image-20261119/reward.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)

One image summing up the world's news of Thursday 19 November 2026. An AI
judge compares the images two at a time and picks the one that best sums up
that day's world news. This front page carries 47 verified stories: 3 leads,
12 main stories, a numbered world map, a BY THE NUMBERS strip and 32 briefs.
A visible DATE CHECK strip states the verification: every story checked
against same-day reporting, leads and main stories double-sourced.

Rev2 changes vs the submitted v1 (rank 11,618): the ICJ Rohingya verdict is
now stated (it was read at 10:00 in The Hague on 19 Nov and verified the
same day); the COP31 fossil-fuel draft story joins the grid; five more
briefs were added (Mongolia, Somalia, Dutch embassy in Kyiv, Lula, Nvidia);
the masthead now states the story count, the 7 regions + space covered,
and the date-checking.

## The day's three leads

1. **Xi, Trump and Putin meet in Shenzhen** — First-ever trilateral at
   APEC; no deal expected.
2. **GTA VI out today, scores 99** — Vice City epic ties the all-time
   Metacritic record.
3. **Anthropic debuts at $83 a share** — AI maker raises $81.3bn in its
   Nasdaq listing today.

## The twelve main stories

4. **Jeffries nominated for Speaker, 251–11** — Democrats pick him; full
   House vote set for 3 Jan 2027.
5. **ICJ finds Myanmar guilty of genocide** — First state ever held guilty
   of genocide; reparations ordered. 9–6 vote; ~10,000 killed in the 2017
   clearance operations.
6. **Iran hits US bases in Kuwait, Bahrain** — Tehran's drones follow the
   US strike on the Qeshm missile site.
7. **Tanker hit in Hormuz; 1 missing, 11 hurt** — Navig8 Messi struck off
   Oman; second attack in 4 months.
8. **Israel crosses Gaza's Yellow Line** — First ground op since the Oct
   2025 ceasefire; 3 reported killed.
9. **Kerch Bridge hit a third time** — Blast at the 19 km crossing days
   after the road span fell.
10. **EU proposes €45bn Ukraine loan** — Covers two-thirds of Kyiv's €70bn
    2027 funding gap.
11. **Fed minutes: more hikes likely** — Almost all officials back rises;
    October hold was 10–2.
12. **COP31 draft drops fossil fuels** — Antalya text cuts the phaseout
    vow and backs carbon capture instead.
13. **Voyager 1 reaches one light-day** — 16.1bn miles out; NASA confirms
    the milestone today.
14. **Van Gogh sells for record $190.4m** — Blossoming Chestnut Trees tops
    the artist's auction record.
15. **Cyclone Akvan nears India** — Landfall expected Friday; 50,000
    evacuated in Odisha.

## Also on Nov 19

Houthi missile threat to Riyadh; US seeks a $2bn-plus loan package for the
Philippines; Takaichi meets Putin at APEC; India–Japan 2+2 dialogue in
Tokyo; Carney meets Trump; Peltola wins Alaska; US judge says ICE made a
mockery of court orders; Bluenami lifts clean-energy stocks; UK inflation
3.6%; Waymo halts freeway driverless service; Fiji declares disaster amid
El Niño drought; US loses measles-free status; Pew: Muslims to outnumber
Christians by 2035; Giannis beats his old team; RJ Luis Jr. debuts for LSU
under court order; Leicester City drops sponsor BC.Game; BBC McDonald's
probe; Delhi schools reopen; Musk on midterm spending; UN: 372-plus
civilians killed in Ukraine in October; Canada sanctions Israeli settlers;
US–Venezuela restore military cooperation; IAEA: North Korea expands
uranium enrichment; Cameron Fens sues NCAA; Microsoft reportedly in talks
to sell AI services to ByteDance; Libya seizes cocaine and millions of
pills; World COPD Day; Nvidia board won't bring back Huang; Mongolia's
president quits in railway graft scandal; Somalia orders UAE envoy out in
72 hours; Dutch embassy in Kyiv hit; Lula nears finance minister pick.

Sources: Reuters, AP, BBC, NASA, Sotheby's, IMD, Euronews, UN News —
19 Nov 2026. Full links in SOURCES.md. Disputed claims are attributed.

## How it works

`main.ts` (Node 22, standard library only) copies `entry.png` (1024×1024,
205 KB) to `/output/entry.png`. The image was drawn with PIL by
`draw_news_image_20261119_rev2.py` (flat vector-style illustrations, no AI
text). Run it locally with:

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```
