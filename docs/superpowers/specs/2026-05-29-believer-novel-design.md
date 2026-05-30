# Design Spec — *Believer* (a novel) + Kindle publication package

**Date:** 2026-05-29 · **Status:** Approved, in production · **Author of record:** Otto Quill (pen name)

## Goal
Produce an award-worthy, full-length literary novel — *Believer* — and every artifact required to publish it on Amazon Kindle (KDP), generated with maximal automation and creativity.

## Premise
Daniel Mercer, the most gifted crisis-communications fixer of his generation, wakes one morning unable to tell a lie without pain proportional to the lie — and discovers no one in his physical presence can either. The condition is never explained. It punishes deceit but not sincere error, so the only refuge is to genuinely believe one's own falsehoods: the honest suffer, the self-deceived go free. As the world learns what Daniel is, truth becomes a weapon, a sacrament, an instrument of torture, and a creed.

## Genre & tone
A deliberate blend the user chose: **literary speculative × dark satire × (inverted) superhero.** Literary realism for the protagonist's chapters; biting satire in the interstitial "dossier" documents; the escalation of a superhero origin whose "power" is a curse, whose "villain" cannot be punched, and whose climax is a confession.

## Hard creative parameters (locked)
- **Rule-rigorous and never explained.** Internal physics treated like hard SF; no origin reveal.
- **Earned-ambiguity ending.** The book never rules on whether compelled truth is good or bad.
- **Both poles live.** Good and bad consequences are explored and neither wins the argument.
- Full canon, rules, characters, timeline, themes, and style are fixed in **`/wiki`** (the world bible) and **`/manuscript/beat-sheet.md`** (34-unit spine).

## The condition (summary; full rules in `wiki/01-the-condition.md`)
1. A spoken lie causes pain proportional to the lie's magnitude/consequence (sting → seizure → death).
2. Anyone within Daniel's physical presence (~a room) is subject to the same; **not** carried by phone, writing, broadcast, or proxy. *Truth lives only where bodies are.*
3. **Belief loophole:** pain tracks *known* falsehood, not falsehood. Sincere belief is painless → the engine of the antagonist and of a society-wide self-deception epidemic.
4. Rigorous edge cases (silence, fiction/art, sarcasm, promises, opinions, bullshit) arbitrated consistently.

## Structure
Five parts, **34 units** (25 narrative chapters + 9 dossier interludes), **~86k words**. Close third-person past on Daniel, braided with found documents (news, ad copy, sermon, transcripts, memos, forum threads, an aviation report). Full beat sheet in `manuscript/beat-sheet.md`.

## Production method (maximal automation)
1. Lock the world bible + beat sheet (done).
2. Draft a **voice anchor** (ch01), then **draft all remaining units in parallel** via the Workflow tool, each agent grounded in the full bible + anchor + neighbor synopses.
3. **Continuity + line-edit pass** per unit with neighbor context (single voice, seam-smoothing, pain-calibration, canon).
4. Assemble manuscript with front/back matter; build EPUB + DOCX via pandoc.
5. Generate an original cover (1600×2560). Write the full KDP metadata pack.

## Deliverables
- `manuscript/chapters/*.md` — all 34 units.
- `build/Believer.epub` (KDP primary), `build/Believer.docx` (backup), `build/Believer.md` (assembled source).
- `art/cover.jpg` + `art/cover.png` (+ `art/make_cover.py`).
- `metadata/` — `description.html`, `kdp-metadata.md`, `kdp-metadata.json`.
- Front/back matter in `manuscript/matter/` (copyright, dedication, epigraph, about-author, acknowledgments, book-club questions).
- `wiki/` world bible; `manuscript/beat-sheet.md`.

## Out of scope
- Print/paperback interior layout (eBook-first; DOCX provided as a starting point).
- Real ISBN registration; final author bio/acknowledgments personalization (placeholders provided).
- Marketing beyond the product description and keywords.
