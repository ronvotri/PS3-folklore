# Folklore translation workspace

Read README.md, docs/STATUS.md, docs/TRANSLATION.md, docs/QUEUE.md and docs/CLOUD.md first.
For format/font changes also read docs/FORMAT.md, docs/FONT.md, fonts/choice.json
and fonts/aliases.json. Respond to the user in Vietnamese.

## Verified result

BCUS98147 uses Merienda Regular 400 for the menu prototype. On 2026-10-10
user confirmed V3 fixed extra gaps after Vietnamese letters such as ấ and ớ.
V3 has 25 two-byte UTF-8 aliases pointing to the same Vietnamese glyphs.
Human translations remain Vietnamese NFC. Do not replace the font, remove
aliases, or return to direct three-byte encoding for these characters.
This is a small menu test, not a full-game or full-alphabet verification.

## Current priority (confirmed 2026-10-11)

User prioritizes a **playable Vietnamese game over raw draft coverage**. For the
next continuation, start with `docs/DIALOGUE_BINARY_PROBE.md` and the
`tools/dialogue_probe.py` read-only forensic path for talk/CMC. Validate
original binary/sections/pointer hypotheses on local backups, then prove a
lossless parse→serialize roundtrip BEFORE implementing a write-capable repacker.
Do not treat `draft` count as game-completion percentage. Keep translation
work as a secondary track, and NEVER overwrite original dialogue offsets with
UTF-8 variable-length strings. There are no original game binaries in the
GitHub repo, so the forensic probe has only synthetic test coverage so far.
Do not mark dialogue `reviewed`/`tested` from heuristic string order/speaker.
Preserve confirmed Merienda V3 assets and all local patches.

## Default translation work

When asked to continue translating, work immediately on the existing catalogs.
Use translations/index.json and docs/QUEUE.md to choose a coherent batch and
translate as many entries as can be checked reliably in the current session;
**there is no fixed 200-entry cap or required batch size** (updated at user's
request 2026-10-11). Prefer finishing a catalog and reusing identical source
translations across catalogs, but never sacrifice context, natural address or
metadata safety for raw numbers. QA in logical chunks (~50 or any suitable size),
then commit a checked, coherent batch. When large batches risk interrupted tool sessions,
prefer smaller independently verified commits (e.g. 50–100 dialogue entries) over
trying to maximize a single request. Never claim unsaved changes are complete.
Menu drafts are already complete.
For long narrative or context-sensitive dialogue, reduce or expand the batch
as evidence and quality justify. Do not request a ROM just to translate.
Edit vi, status, notes; update source_review only after actual source review.
Keep IDs, English sources, hashes, offsets, metadata and order unchanged.
Read neighboring entries for context. Use translations/glossary.json.
Preserve control tokens, placeholders and newline blocks. Scanned candidates
can include binary metadata as leading symbols/digits: retain source and
uncertain prefixes in drafts and record uncertainty. Do not invent speakers.
Do not mark tested without local in-game confirmation. Do not retranslate
completed entries unless requested or a concrete error is found.
Record the completed batch and next task in QUEUE.md and STATUS.md. Review
changes, commit or open a PR as supported/authorized by the cloud task.

## Required checks

Text work needs Python 3.10+ and the standard library only:
python tools/catalog.py validate
python -m unittest discover -s tests -v
Run both after relevant changes. Optional font tools need Pillow/fonttools;
do not install those for plain translation. Legacy tools/folklore.py supports
ASCII only and must not build or apply V3 accented translations.
Dialogue repacking is not implemented. Never overwrite catalog offsets with
variable-length text. Preserve alias assignments when adding glyph coverage;
reject missing glyphs, occupied slots and incorrect source hashes.

## Local/cloud boundary

Cloud has text catalogs and tooling, not E:\Game\Folklore. Build and runtime
checks happen locally. User wants to control/open the game themselves and
report screenshots. Do not launch/control RPCS3 unless later explicitly asked.
Pause writes while RPCS3 runs. Preserve originals and recovery packages.
Do not infer runtime success from synthetic tests or font preview images.
Keep ROM/ISO, firmware, saves, binary assets, extracted font textures, downloaded
TTFs and payload patch packages local in ignored local-data/ and dist/.
Text-only catalogs are authorized translation material and belong in
translations/catalogs/. Never upload font-demo-patch.json or menu-patch.json.
