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

## Default translation work

When asked to continue translating, work immediately on the existing catalogs.
Use translations/index.json and docs/QUEUE.md to pick approximately 200 verified
menu entries per work session (or all remaining if fewer), checking in logical
subgroups of about 50 for consistency, metadata invariants and control codes.
Do not stop after the first 50 entries unless a real blocker appears; report
progress and commit once the larger batch is checked. For long narrative or
context-sensitive dialogue, choose a smaller batch only when necessary for
translation quality. Prefer verified menu entries first. Do not request a ROM just to translate.
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
