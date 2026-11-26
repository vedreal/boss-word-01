#!/usr/bin/env python3
"""One Word for the Boss — make.fun entry.

Writes exactly one word describing the boss to /output/entry.txt.
The word is the whole entry: 1-30 characters, no phrase, no caption.

Judge (z-ai/glm-5.3-flash, pairwise) weighs, in order:
  1. a single word that describes a boss, the sort of word a person
     would actually use about the one they report to
  2. funny on its own, the kind of word a colleague repeats at lunch
  3. rings true, catching a real habit of bosses
  4. fresh, not the first word anyone would reach for
  5. travels, working for a boss in a kitchen, a warehouse or an
     office without the industry needing to be explained

Ten candidate words, each scored 1-5 per criterion with weights
5/4/3/2/1 following the judge's order. Highest score wins;
ties go to the shorter word, then to the earlier candidate.
"""

CANDIDATES = [
    # (word, rationale, scores [on-subject, funny, true, fresh, travels])
    (
        "Seagull",
        "The seagull manager: swoops in, squawks loudly, craps all over "
        "the work, then flies off. A complete joke in one word — arrival, "
        "noise, mess, departure — and a real, named management trope "
        "every office worker recognises. Works in any industry because "
        "seagulls are everywhere.",
        [5, 5, 5, 4, 5],
    ),
    (
        "Helicopter",
        "The hovering boss: always overhead, loud, watching everything, "
        "never landing. Instantly clear even to someone who never heard "
        "the term 'helicopter manager', and the single most common bad-boss "
        "complaint. Slightly less fresh because helicopter parenting is "
        "so well known.",
        [5, 4, 5, 3, 5],
    ),
    (
        "Ostrich",
        "Head in the sand while the problems pile up. One visual, "
        "universally understood, and true of the boss who ignores every "
        "warning until it explodes. Travels anywhere; everyone knows an "
        "ostrich.",
        [5, 4, 4, 4, 5],
    ),
    (
        "Omniscient",
        "The boss who believes they know everything and acts on it. "
        "The grandeur of the word is the joke: the all-knowing boss is "
        "usually the least informed person in the room. People do say it "
        "ironically about a boss; slightly formal, so it travels a touch "
        "less well at lunch.",
        [5, 4, 4, 4, 4],
    ),
    (
        "Vampire",
        "Drains the energy and life out of the room, then asks why "
        "everyone looks tired. True and vivid, works in any workplace. "
        "A little generic as an insult, which costs it freshness.",
        [5, 4, 4, 3, 5],
    ),
    (
        "Bottleneck",
        "Every decision, approval and piece of work queues up behind one "
        "person and stops there. The truest word on the list and it "
        "travels everywhere, but it reads more descriptive than funny.",
        [5, 3, 5, 3, 5],
    ),
    (
        "Delegator",
        "Delegates everything, including their own job, then keeps the "
        "credit. True of a whole species of boss and funny because the "
        "delegation never stops upward. Reads a little flat as a bare word.",
        [5, 3, 5, 3, 5],
    ),
    (
        "Parrot",
        "Repeats whatever the higher-ups just said and presents it as "
        "their own idea. True, travels, and everyone has met one. The "
        "joke is a touch thin: a parrot only repeats, it never leads.",
        [5, 3, 4, 3, 5],
    ),
    (
        "Clockwatcher",
        "Watches the clock, never the work: in at 9:00 sharp, out at "
        "5:00 sharp, and furious if you are a minute late while the "
        "project burns. True and it travels, but it is a familiar office "
        "word, not a surprise.",
        [5, 3, 4, 3, 5],
    ),
    (
        "Micromanager",
        "The control case: the first word anyone reaches for about a bad "
        "boss. Undeniably true, but it loses on freshness by definition — "
        "it is the word everyone already uses, so it earns a shrug, "
        "not a laugh.",
        [5, 2, 5, 1, 5],
    ),
]

WEIGHTS = [5, 4, 3, 2, 1]


def score(candidate):
    """Weighted rubric score for one candidate."""
    _, _, scores = candidate
    return sum(s * w for s, w in zip(scores, WEIGHTS))


def rank(candidates):
    """Rank candidates by score, then shorter word, then earlier order."""
    scored = [(score(c), len(c[0]), -i, c) for i, c in enumerate(candidates)]
    scored.sort(key=lambda t: (t[0], -t[1], t[2]), reverse=True)
    return [(s, c) for s, _, _, c in scored]


def main():
    ranked = rank(CANDIDATES)
    print("Candidate ranking (score, word):")
    for s, (word, rationale, _) in ranked:
        print(f"  {s:3d}  {word}")
    winner = ranked[0][1][0]
    print(f"Winner: {winner}")
    return winner


if __name__ == "__main__":
    main()


# --- part 2: pick the winner, validate it, write the entry ---

def write_entry(output_path="/output/entry.txt"):
    """Write the winning word to the entry file.

    Gate: /output/entry.txt must be UTF-8 text of 1 to 30 characters,
    not only white space, and the entry is exactly one word, so the
    file holds the word alone with no spaces and no trailing newline.
    """
    ranked = rank(CANDIDATES)
    word = ranked[0][1][0]
    if not word or not (1 <= len(word) <= 30):
        raise ValueError(f"word fails the 1-30 character gate: {word!r}")
    if any(ch.isspace() for ch in word):
        raise ValueError(f"entry must be a single word, no spaces: {word!r}")
    import os

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(word)
    with open(output_path, "r", encoding="utf-8") as f:
        written = f.read()
    assert written == word, f"read-back mismatch: {written!r} != {word!r}"
    print(f"Wrote entry to {output_path}: {written!r} ({len(written)} chars)")
    return written


if __name__ == "__main__":
    write_entry()
