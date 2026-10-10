# Working instructions

Read README.md, docs/STATUS.md, and docs/FORMAT.md before changing tools.

This project translates the PS3 release BCUS98147. The user confirmed the
ASCII menu prototype works in their local RPCS3 setup. Accented Vietnamese,
complete dialogue, original PS3 hardware, and Steam Deck remain unverified.

Use Python 3.10+ and the standard library for portable tooling. Run
`python -m unittest discover -s tests -v` after relevant changes. Synthetic
tests verify structure and safety; they do not establish in-game behavior.
Keep translations in translations/, tool code in tools/, and update STATUS.md
with concrete progress and the next task whenever handing off work.

Keep full game assets, extracted binary files, fonts, generated packages with
original/patched game payloads, emulator binaries, firmware, and saves local.
Use local-data/ for original assets and dist/ for generated packages.
Do not commit the legacy menu-patch.json: it contains full original menu assets.
Do not overwrite the original baseline with already patched menu files.
The extractor can recover the original bytes in memory from the user's
matching local legacy patch package; it does not restore the live game.

The current encoder supports ASCII only. Do not enable accented text merely by
switching to UTF-8. First establish the game's byte-to-glyph mapping and font
texture format, then test a small accent prototype locally. Do not claim
runtime success from structural tests alone. Preserve control sequences,
string IDs/order, and bytes outside the intended menu section.

Do not apply cloud-generated changes to the user's live game unless the task
authorizes it and the expected source hashes and a recovery path are verified.
GitHub/cloud tasks do not automatically have access to E:\Game\Folklore.
