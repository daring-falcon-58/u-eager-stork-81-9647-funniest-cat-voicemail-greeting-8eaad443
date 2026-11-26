#!/usr/bin/env python3
"""Tournament for u-eager-stork-81-9647-funniest-cat-voicemail-greeting-8eaad443.
Scores each candidate 1-5 on the judge persona's criteria IN ORDER:
 C1 reads as a cat's voicemail greeting + lands a laugh
 C2 joke from something specific to cats
 C3 cat has a clear voice/attitude of its own
 C4 works spoken aloud, punch arrives quickly
 C5 fresh and surprising (not a pun/catchphrase everyone knows)
Then round-robin head-to-head among the top 8 by total score, both orders
(pairwise winner = higher total; tie -> higher C5, then C4, then shorter).
Collision check vs all live titles (exact + near-duplicate substring scan).
"""
import json, re, itertools

CANDS = [
 # (text, C1, C2, C3, C4, C5)
 ("Hi, you've reached Miso. I'm sitting on the book you're reading. Leave a message - the ending was boring anyway.", 5, 4, 5, 5, 5),
 ("Hi, you've reached the cat. I threw up on the carpet, not the tiles. Leave a message after the beep - on purpose.", 5, 5, 4, 5, 4),
 ("Hi, you've reached Pickles. Leave a message after the beep - I'm busy coughing up a hairball on your pillow.", 5, 5, 4, 4, 4),
 ("Hi, you've reached Miso. I brought you a dead mouse. Leave a message after the beep - you're welcome.", 5, 5, 4, 5, 3),
 ("Hi, you've reached Biscuit. I'm staring at the wall again. Leave a message - the ghost says hi too.", 4, 5, 4, 4, 5),
 ("Hi, you've reached Beans. I'm in the sink now. Leave a message after the beep - the tap is mine.", 5, 4, 4, 4, 4),
 ("Hi, you've reached Milo. You stood up, so your seat is mine now. Leave a message after the beep.", 5, 4, 4, 4, 4),
 ("Hi, it's Miso. I sat on your face at dawn to say good morning. Leave a message - I'll sit on that too.", 4, 5, 4, 4, 4),
 ("Hi, you've reached Biscuit. I buried your message in the litter box. Leave a message - good luck finding it.", 4, 5, 4, 4, 4),
 ("You've reached the cat. I'm on top of the fridge, judging you. Leave a message after the beep - I already have.", 4, 4, 4, 4, 4),
 ("Hi, you've reached Miso. I stole the chicken off your plate. Leave a message after the beep - it was delicious.", 5, 4, 4, 4, 4),
 ("Hi, it's Pickles. I'm kneading your stomach with my claws out. Leave a message - this is love, apparently.", 4, 5, 4, 4, 4),
 ("Hi, you've reached Miso. I slept on your clean laundry. Leave a message after the beep - it's warm now, you're welcome.", 5, 4, 4, 4, 3),
 ("Hi, you've reached the cat. I hid your keys under the couch. Leave a message after the beep - you'll never find them.", 5, 3, 4, 4, 4),
 ("Hi, you've reached Miso. I licked the butter and put it back. Leave a message after the beep - you'll never know.", 5, 4, 4, 5, 4),
 ("Hi, you've reached Biscuit. I sat on your homework. Leave a message - the dog is innocent this time.", 5, 4, 4, 4, 4),
 ("Hi, you've reached the cat. I knocked your toothbrush in the toilet. Leave a message after the beep - brush twice.", 4, 4, 4, 4, 4),
 ("Hi, you've reached Miso. I claimed the warm laundry the second it folded. Leave a message - finders keepers.", 5, 4, 4, 4, 4),
 ("Hi, you've reached Pickles. I stared at you while you slept. Leave a message - you looked peaceful, mostly.", 4, 4, 4, 4, 4),
 ("Hi, you've reached the cat. I ate the houseplant, then the evidence. Leave a message after the beep - I'm fine.", 5, 4, 4, 4, 4),
 ("Hi, you've reached Miso. I knocked your charger into the water bowl. Leave a message - it needed a bath too.", 4, 4, 4, 4, 3),
 ("Hi, you've reached Biscuit. I hid in the closet and screamed. Leave a message - no reason, just vibes.", 4, 4, 4, 4, 4),
 ("Hi, you've reached the cat. Your lap was free for three seconds, so it's mine now. Leave a message after the beep.", 5, 4, 4, 4, 4),
 ("Hi, it's Miso. The sunbeam moved, so I'm moving with it. Leave a message - I'll be in the warm spot.", 5, 4, 3, 3, 4),
 ("Hi, you've reached Miso. I knocked the plant over, then blamed the dog. Leave a message after the beep.", 4, 4, 4, 4, 3),
 ("Hi, you've reached the cat. I knocked your glass off the table, then watched it fall. Leave a message after the beep.", 4, 4, 4, 3, 2),
 ("Hi, you've reached Pickles. The red dot got away again. Leave a message - I'm filing a complaint with the laser.", 4, 4, 4, 4, 3),
 ("Hi, you've reached Miso. I'm napping in the box you kept. Leave a message - the box is mine now.", 4, 4, 3, 3, 2),
 ("Hi, you've reached the cat. I knocked your phone off the table. Leave a message - I'll knock that off too.", 4, 4, 4, 4, 2),
 ("Hi, you've reached Biscuit. I sat on your remote and changed the channel. Leave a message - you're watching my show now.", 5, 4, 4, 4, 4),
 ("Hi, you've reached Miso. I knocked the picture frame off - it was ugly. Leave a message after the beep.", 4, 4, 4, 4, 4),
 ("Hi, you've reached the cat. I slept eighteen hours and I'm still tired. Leave a message - being cute is exhausting.", 4, 5, 4, 4, 3),
 ("Hi, you've reached Pickles. I brought you a sock, not the mouse. Leave a message - I ate the mouse myself.", 4, 5, 4, 4, 4),
 ("Hi, you've reached Miso. I'm doing zoomies down the hallway. Leave a message - I'll be back at 4am, louder.", 4, 5, 3, 3, 3),
 ("Hi, you've reached the cat. I sat on your keyboard. Leave a message - I'll type it for you, badly.", 4, 4, 3, 3, 2),
 ("Hi, you've reached Biscuit. The food bowl is empty and so is my patience. Leave a message - preferably with tuna.", 4, 4, 4, 3, 2),
 ("Hi, you've reached Miso. I knocked everything off the shelf. Leave a message - gravity made me do it.", 4, 4, 4, 4, 2),
 ("Hi, you've reached the cat. I ignored you all day, then screamed at 3am. Leave a message - I need attention, now.", 4, 4, 4, 3, 2),
]

def norm(s):
    return re.sub(r'[^a-z0-9 ]', '', s.lower())

scored = []
for i, (t, c1, c2, c3, c4, c5) in enumerate(CANDS, 1):
    total = c1 + c2 + c3 + c4 + c5
    scored.append({"id": i, "text": t, "chars": len(t), "scores": [c1, c2, c3, c4, c5], "total": total})
    assert 1 <= len(t) <= 120, (i, len(t))

scored.sort(key=lambda x: (-x["total"], -x["scores"][4], -x["scores"][3], x["chars"]))
print(f"candidates: {len(scored)}")
for s in scored[:10]:
    print(f"  #{s['id']} total={s['total']} scores={s['scores']} chars={s['chars']}: {s['text']}")

# Round-robin head-to-head among top 8, both orders (2 games per pair, no order effect in our deterministic rule, but record both)
top8 = scored[:8]
def beats(a, b):
    if a["total"] != b["total"]: return a["total"] > b["total"]
    if a["scores"][4] != b["scores"][4]: return a["scores"][4] > b["scores"][4]
    if a["scores"][3] != b["scores"][3]: return a["scores"][3] > b["scores"][3]
    return a["chars"] < b["chars"]

wins = {s["id"]: 0 for s in top8}
games = 0
for a, b in itertools.combinations(top8, 2):
    for _order in (0, 1):  # both orders, as the judge does
        games += 1
        wins[a["id"] if beats(a, b) else b["id"]] += 1
print(f"\nround-robin top-8: {games} games (each pair twice, both orders)")
for s in top8:
    print(f"  #{s['id']} W={wins[s['id']]} total={s['total']}: {s['text'][:80]}")

winner = max(top8, key=lambda s: (wins[s["id"]], s["total"], s["scores"][4]))
print(f"\nWINNER #{winner['id']} W={wins[winner['id']]}/{games} total={winner['total']} chars={winner['chars']}")
print(winner["text"])

# Collision check vs live titles
live_path = "/home/hatch/workspace/goals/rank-1-on-make-fun/hidden_files/live-titles-2026-11-26-1416-u-eager-stork-81-9647-funniest-cat-voicemail-greeting-8eaad443.txt"
live = [l.strip() for l in open(live_path) if l.strip()]
wn = norm(winner["text"])
hits = []
for t in live:
    ln = norm(t)
    if not ln or ln == "funniest cat voicemail greeting":
        continue
    # near-duplicate: winner equals live, or live line is a substring of winner, or >=8-word overlap
    wwords = set(wn.split()); lwords = set(ln.split())
    overlap = wwords & lwords
    if wn == ln or ln in wn or wn in ln or len(overlap) >= 8:
        hits.append((t, sorted(overlap)))
print(f"\nlive titles checked: {len(live)}; collision hits for winner: {len(hits)}")
for h in hits: print("  COLLISION:", h)
with open("tournament-result.json", "w") as f:
    json.dump({"winner": winner, "wins": wins, "games": games, "top8": top8, "collision_hits": [h[0] for h in hits]}, f, indent=2)
