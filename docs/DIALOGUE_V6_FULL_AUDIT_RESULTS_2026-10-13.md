# Folklore V6 — Full CMC candidate audit (13 October 2026)

**Input:** user-provided, redacted `GUI_CHO_CHATGPT_cmc-frame-audit.json` generated on original BCUS98147 archive. The report contains aggregate classifications, not bytes or dialogue text. This is evidence of candidate framing, **not** proof of message grammar, script control flow, speaker IDs, pointer relocation or a working dialogue repacker.

## Marker parity check across all 134 catalogs

Readback via connected GitHub checked every candidate with an ASCII-printable first character at file offset `mod4=3` against its draft Vietnamese first character. **Exactly one mismatch was found:** CMC800 at decimal offset `12071`, English source begins `beautiful...` but Vietnamese begins `đẹp...`. This is *not* automatically an error: if the first letter is on-screen text, forcing the letter `b` into the Vietnamese draft would corrupt the translation. If it is an engine field, it needs to be preserved out of band by a proven serializer. **No translation was changed.**

In response, the experimental tokenizer uses neutral names `fourth_byte`, `remaining_ascii`, `fourth_byte_in_source`, not `speaker`, `selector` or `visible_text`. It reconstructs original bytes only. This avoids prematurely declaring that the fourth byte is invisible metadata.

## Verified observations

- **134/134 CMC catalog files were source-verified by V6** before the redacted report was written. The tool checks archive size, per-CMC SHA, catalog IDs, ASCII source and NUL at each catalog offset.
- **1,744/1,795 candidates match `00 04 00 XX` (97.16%).** Split: 1,001 candidate sources appear to start with an ASCII selector byte; 743 have a separate preceding control selector byte. These classifications are hypotheses, not display-string definitions.
- **51 candidates across 27 CMC catalogs do not match**, with 24 `not_000400_frame`, 12 `unexpected_mod1`, 12 `unexpected_mod2`, and 3 `mod3_nonprintable_source_prefix`. The report makes no claims that these are bad game files.
- **107 of 134** catalog files have all candidate prefixes recognized by this signature. Excluding CMC800 and CMC801, **1,728/1,763 candidates match (98.01%)**.
- **CMC800 (4/14) and CMC801 (12/18)** contribute **16 of the 51 mismatches**; these catalogs contain split-line and unusual prefix cases and need separate parsing investigation.
- V6 checks **only cataloged candidate ASCII-NUL strings**, not all on-screen text and not raw `talk/en/*.bin_` script grammar. This is not an in-game validation.

## Mismatching catalogs (all remain untouched)

| CMC | Candidate mismatch count | Reasons |
|---|---:|---|
| 008 | 1 | `not_000400_frame` ×1 |
| 020 | 2 | `unexpected_mod1` ×1, `unexpected_mod2` ×1 |
| 021 | 2 | `unexpected_mod1` ×1, `unexpected_mod2` ×1 |
| 032 | 1 | `unexpected_mod1` ×1 |
| 042 | 1 | `not_000400_frame` ×1 |
| 050 | 1 | `unexpected_mod2` ×1 |
| 104 | 1 | `unexpected_mod1` ×1 |
| 113 | 1 | `not_000400_frame` ×1 |
| 116 | 2 | `not_000400_frame` ×1, `unexpected_mod2` ×1 |
| 128 | 1 | `unexpected_mod2` ×1 |
| 129 | 3 | `not_000400_frame` ×1, `unexpected_mod2` ×2 |
| 130 | 1 | `not_000400_frame` ×1 |
| 131 | 1 | `not_000400_frame` ×1 |
| 132 | 1 | `unexpected_mod2` ×1 |
| 138 | 1 | `not_000400_frame` ×1 |
| 139 | 2 | `not_000400_frame` ×1, `unexpected_mod2` ×1 |
| 140 | 3 | `not_000400_frame` ×2, `unexpected_mod2` ×1 |
| 143 | 3 | `mod3_nonprintable_source_prefix` ×1, `unexpected_mod1` ×2 |
| 146 | 1 | `not_000400_frame` ×1 |
| 153 | 1 | `not_000400_frame` ×1 |
| 163 | 1 | `not_000400_frame` ×1 |
| 203 | 1 | `unexpected_mod1` ×1 |
| 208 | 1 | `not_000400_frame` ×1 |
| 210 | 1 | `not_000400_frame` ×1 |
| 213 | 1 | `unexpected_mod2` ×1 |
| 800 | 10 | `not_000400_frame` ×7, `unexpected_mod1` ×2, `unexpected_mod2` ×1 |
| 801 | 6 | `mod3_nonprintable_source_prefix` ×2, `not_000400_frame` ×1, `unexpected_mod1` ×3 |

## Static triage on GitHub catalogs

From catalog source offsets alone, 24 candidates start at `offset % 4` = 1 or 2, inconsistent with the two V5 frame forms. Many of these source strings begin with a space, comma, exclamation mark or newline; some may be fragments of a larger record or extractor overcaptures. **Do not drop or rewrite them automatically.**

| CMC | Candidate offset(s) (`decimal`) at mod1/mod2 |
|---|---|
| 020 | `13734`, `13893` |
| 021 | `14765`, `14806` |
| 032 | `11289` |
| 050 | `9414` |
| 104 | `11605` |
| 116 | `11594` |
| 128 | `10606` |
| 129 | `12502`, `13146` |
| 132 | `11262` |
| 139 | `13362` |
| 140 | `15022` |
| 143 | `11737`, `12281` |
| 203 | `11549` |
| 213 | `11270` |
| 800 | `12253`, `12530`, `12837` |
| 801 | `11417`, `11933`, `12009` |

Three `mod3_nonprintable_source_prefix` candidates are newline-leading source strings: CMC143 offset 12387 and CMC801 offsets 11767, 12227. Their original strings and Vietnamese draft must not be changed until a grammar has been proven.

The other 24 `not_000400_frame` mismatches cannot be localized precisely from this aggregate report alone. Investigate on a local original archive with a safe read-only exception report; never infer their bytes/offsets from aggregate counts.

## Experimental code (read-only, no patch functionality)

- `tools/cmc_readonly_tokens.py` classifies **only confidently matching** candidate frame spans as a neutral fourth byte plus remaining ASCII bytes, retains *all other byte ranges* in opaque chunks and reassembles them byte-for-byte. It fails closed on any source SHA or reconstructed-byte mismatch.
- `tests/test_cmc_readonly_tokens.py` covers synthetic mod0/mod3 framing, opaque exception preservation, source mismatches and invalid NUL tokens. New tokenizer tests ran **4/4 PASS on synthetic fixtures**; no original game archive was present in this environment. Tokenization must not be described as a complete message parser.
- A real full-archive tokenizer run (when ready) should require original local `etc.bin_` and `etc.fht_`, process all 134 catalogs, and report only counts. No support for Vietnamese replacements, archive writes, or pointer updates is included.

## Next technical gates

1. Byte-exact **candidate tokenization on original CMC archives**, preserving 51 unknown candidates as opaque. Confirm source hash, frame count, and no overlapping spans across all 134 files.
2. Identify framing exceptions and whether printable selectors are visible characters or metadata. Resolve meaningful record control/choice/speaker structure with positive and negative checks.
3. Study raw talk scripts separately; do not apply CMC grammar to `tk100/tk101` without evidence.
4. Only after documented message grammar and byte-exact command-stream roundtrip design relocation-safe rebuild with backups and RPCS3 tests. Keep Merienda V3 unchanged.

**Translation data:** 11,886/11,886 draft entries (158 catalogs) are available in GitHub; **game dialogue patch remains unbuilt**.