# The World on Tuesday — 24 November 2026

[![news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/marwankickup/news-image-20261124-entry/rank.svg)](https://make.fun/bounty/news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/marwankickup/news-image-20261124-entry/reward.svg)](https://make.fun/bounty/news-image-20261124)

Entry for [news-image-20261124](https://make.fun/bounty/news-image-20261124): a program
that draws one newspaper front page summing up the world news of
**Tuesday 24 November 2026** — six stories, each with a headline, a short
summary and a pictogram:

1. **Gaza** — an Israeli strike killed Hamas internal-security director
   Naeem Abu Nahel and six others.
2. **Zaporizhzhia, Ukraine** — an overnight Russian strike killed 2 people
   and wounded 40, including 4 children.
3. **South Korea** — about five Russian military aircraft entered the KADIZ
   air-defence zone near Ulleung Island; fighters scrambled, a brief
   shelter alert lifted within minutes. No territorial airspace violated.
4. **Germany–Ukraine** — Germany became the first country granted access to
   Ukraine's DELTA battlefield-management system; a letter of intent was
   signed in Berlin, alongside an interceptor-missile agreement.
5. **Iraq** — the Prime Minister ordered federal control of oilfields in
   Diyala, Kirkuk, Salahuddin and Nineveh plus Kurdish border crossings,
   after an oil-smuggling investigation.
6. **NATO / Space** — NATO chief Mark Rutte vowed the alliance will defend
   against space threats after German media reported Russia may launch a
   nuclear-armed satellite, "Sputnik-S".

`main.ts` runs `draw_image.py` (Pillow) to render `entry.png` (1024×1024,
deterministic — fixed fonts and geometry, no timestamps or randomness),
validates the PNG magic bytes and IHDR dimensions, and writes it to
`/output/entry.png`.
