# Folklore PS3 — precedent for full fan localization (researched 14/10/2026)

## Publicly verified reference

- Folklore **BCES00050 (European build)** was translated to Russian by the **Alliance** fan group. The translation is classified as fan-made covering text and subtitles by RGdb.info: https://rgdb.info/base/rus-06024
- A contemporaneous release report dated April 2013 credits **RangerRus** for resource analysis, programming and font work: https://psjailbreak.ru/2013/04/16/sostoyalsya-reliz-russkoy-versii-folklore-ot-komandy-alliance.html
- A 2016 listing independently describes translated UI and Russian subtitles for **BCES00050**: https://nnmclub.to/forum/viewtopic.php?t=989567

**Implication:** An earlier team appears to have solved enough of the game format to localize it substantially, including subtitles; this is a valuable reverse-engineering lead. **Do not assume** the tools were published or that BCES00050 binary offsets match our **BCUS98147** original. No checked public standalone CMC re-packer or available original Alliance tool source has yet been identified. Do not distribute game binaries or copy another team's text.

## Follow-up research (developer track, not more diagnostic rounds)

1. Locate any **publicly released, legitimate, tool-only source**, documentation, scripts or direct contact for Alliance/RangerRus concerning Folklore resource containers. Examine licenses before reusing code.
2. If legally accessible, compare small **metadata-only format differences** between European original and fan-translation assets under the user's control to infer relocated sections/record lengths/pointers. Never upload or ship copyrighted game archive contents.
3. Keep this separate from the BCUS98147 checksum-verified CMC script work. The file formats/regions could differ.
4. Main blocker remains **variable-length CMC rebuilding + 23 raw talk scripts**. `tools/cmc_batch_fixed.py` is a safe intermediate multi-line tool, not the answer for 11,886 draft items.

## Negative findings

Public searches did not locate an authoritative open-source Folklore-specific CMC/BI5 repacker maintained by Alliance. Search results for other PS3 game patchers (e.g., Tales of Vesperia) should not be mistaken for tools compatible with Folklore.
