# CMC draft sync checkpoint — 2026-10-12

## Confirmed state

- Repo: `ronvotri/PS3-folklore`, default branch.
- Source: local cumulative CMC draft bundle `Folklore-All-CMC-Draft-Cumulative.zip` (90 CMC catalogs, 1,162 pending translations at initial checkpoint).
- Confirmed pushed to GitHub: **1,084/1,162** CMC draft entries across **85 of the 90** targeted catalogs.
- Remaining **78 todo entries** are in exactly five catalogs:
  - `LCmc206_en.bi5_.json` — 9;
  - `LCmc221_en.bi5_.json` — 31;
  - `LCmc232_en.bi5_.json` — 12;
  - `LCmc234_en.bi5_.json` — 17;
  - `LCmc301_en.bi5_.json` — 9.
- These five files were re-fetched after failed writes and still show all entries `todo`. The connector refused the attempted update with a safety check; **do not claim they were committed**. The original ZIP retains their drafts for later review.
- Prior repository handoff baseline: 10,724/11,886 draft. New theoretical repo count: **11,808/11,886 draft (99.34%)** subject to a fresh repository-wide validator/index recount.
- CMC 063/064/065/069 were pushed first; the remaining eligible CMC catalog files were subsequently applied individually. Source text, entry IDs, offsets, source hashes and nontranslation fields were preserved by only modifying `vi`, `status` and `notes`. Source order/entry counts/newlines were checked before each write.

## Safety and QA

- All newly translated CMC entries remain **candidate/draft**, not reviewed/tested. Speaker, dialogue-stream commands, prefix semantics, and line ordering **have not** been validated on the original binary.
- Static per-file checks succeeded for all updated files (source exact match, entry count, newline count, no conflicting existing translation in these files). **Full repo validator and unittest/CI status have not yet been checked** in this session.
- Review known duplicate-source translation differences and fragmented lines (especially CMC 800/801) in scene context before gameplay packaging.
- Keep the validated **Merienda Regular 400 V3** font and aliases unchanged.
- **Do not repack or patch dialogue/game binaries** until original `etc.bin_` / `etc.fht_` samples have been probed, opcode/pointer/speaker layout resolved and message parse → serialize verified byte-for-byte.

## Next steps

1. Review and safely synchronize the 78 pending draft strings in CMC 206, 221, 232, 234, 301.
2. Run `python tools/catalog.py validate` and `python -m unittest discover -s tests -v` against a real updated working checkout; inspect GitHub Actions runs.
3. Contextual QA across CMC/talk, fixing speaker/pronoun/terminology and broken fragments without changing source metadata.
4. Collect a **local-only** read-only archive structure report using `python tools/dialogue_diagnose.py --game-root "<game path>"` and then implement roundtrip-safe message parser/repacker; only then build and test RPCS3 patch.

Do not treat draft coverage as playable localization coverage.
