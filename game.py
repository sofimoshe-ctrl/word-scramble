#!/usr/bin/env python3
import random
import time
import os
import json

LOG_FILE = os.path.join(os.path.dirname(__file__), "scores.json")

COLORS = {
    "red": "\033[91m", "green": "\033[92m", "yellow": "\033[93m",
    "blue": "\033[94m", "magenta": "\033[95m", "cyan": "\033[96m",
    "bold": "\033[1m", "reset": "\033[0m",
}
def c(text, *styles):
    return "".join(COLORS[s] for s in styles) + text + COLORS["reset"]

WORD_SETS = {
    "ცხოველები 🐾": [
        ("LION", "ლომი"), ("TIGER", "ვეფხვი"), ("ELEPHANT", "სპილო"),
        ("MONKEY", "მაიმუნი"), ("DOLPHIN", "დელფინი"), ("GIRAFFE", "ჟირაფი"),
        ("PENGUIN", "პინგვინი"), ("CHEETAH", "გეპარდი"), ("WOLF", "მგელი"),
        ("EAGLE", "არწივი"), ("SHARK", "ზვიგენი"), ("PANDA", "პანდა"),
    ],
    "ქალაქები 🌍": [
        ("PARIS", "პარიზი"), ("TOKYO", "ტოკიო"), ("LONDON", "ლონდონი"),
        ("BERLIN", "ბერლინი"), ("ROME", "რომი"), ("CAIRO", "კაირო"),
        ("DUBAI", "დუბაი"), ("SYDNEY", "სიდნეი"), ("ATHENS", "ათენი"),
        ("TBILISI", "თბილისი"), ("MOSCOW", "მოსკოვი"), ("VIENNA", "ვენა"),
    ],
    "საჭმელი 🍕": [
        ("PIZZA", "პიცა"), ("SUSHI", "სუში"), ("BURGER", "ბურგერი"),
        ("PASTA", "პასტა"), ("SALAD", "სალათი"), ("BREAD", "პური"),
        ("CHEESE", "ყველი"), ("APPLE", "ვაშლი"), ("COFFEE", "ყავა"),
        ("CHOCOLATE", "შოკოლადი"), ("ORANGE", "ფორთოხალი"), ("MANGO", "მანგო"),
    ],
}

def scramble(word):
    letters = list(word)
    while True:
        random.shuffle(letters)
        if "".join(letters) != word:
            return "".join(letters)

def load_scores():
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE) as f:
            return json.load(f)
    return []

def save_score(name, score, total, theme):
    scores = load_scores()
    scores.append({"name": name, "score": score, "total": total, "theme": theme,
                   "date": time.strftime("%Y-%m-%d")})
    scores.sort(key=lambda x: x["score"], reverse=True)
    with open(LOG_FILE, "w") as f:
        json.dump(scores[:20], f, indent=2, ensure_ascii=False)

def show_leaderboard():
    scores = load_scores()
    if not scores:
        print(c("  ლიდერბორდი ცარიელია.", "yellow"))
        return
    print(c("\n  ── 🏆 ლიდერბორდი ──", "bold", "yellow"))
    for i, s in enumerate(scores[:10], 1):
        medal = ["🥇","🥈","🥉"][i-1] if i <= 3 else f"  {i}."
        print(f"  {medal} {c(s['name'], 'bold', 'cyan')}  —  "
              f"{c(str(s['score']), 'green', 'bold')}/{s['total']}  ({s['theme']}, {s['date']})")

def play(theme, words):
    os.system("clear")
    print(c(f"\n  🎮 თემა: {theme}", "bold", "yellow"))
    print(c("  თითოეულ სიტყვას 15 წამი აქვს. მოამზადდი!\n", "cyan"))
    input(c("  Enter — დასაწყებად...", "green"))

    sample = random.sample(words, min(8, len(words)))
    score = 0

    for idx, (word, geo) in enumerate(sample, 1):
        scrambled = scramble(word)
        os.system("clear")
        print(c(f"\n  სიტყვა {idx}/{len(sample)}   ქულა: {score}", "bold", "cyan"))
        print(c(f"\n  ქართულად: {geo}", "bold"))
        print(c(f"\n  გაშლილი:  ", "yellow") + c(scrambled, "bold", "magenta", ))

        deadline = time.time() + 15
        answered = False
        while time.time() < deadline:
            remaining = int(deadline - time.time())
            print(f"\r  ⏱  {c(str(remaining), 'bold', 'red')} წამი   ", end="", flush=True)
            try:
                import select
                if select.select([__import__('sys').stdin], [], [], 0.5)[0]:
                    guess = input("\n  პასუხი: ").strip().upper()
                    if guess == word:
                        print(c("  ✓ სწორია!", "bold", "green"))
                        score += 1
                    else:
                        print(c(f"  ✗ არასწორი. სიტყვა იყო: {word}", "red"))
                    answered = True
                    time.sleep(1)
                    break
            except Exception:
                time.sleep(0.5)

        if not answered:
            print(c(f"\n\n  ⏰ დრო ამოიწურა! სიტყვა იყო: {word}", "red"))
            time.sleep(1.5)

    return score, len(sample)

def main():
    os.system("clear")
    print(c("""
  ╔══════════════════════════════════════╗
  ║   🔤  სიტყვების გაშლის რბოლა       ║
  ╚══════════════════════════════════════╝
""", "bold", "cyan"))

    print(c("  1", "bold", "yellow") + "  — თამაში")
    print(c("  2", "bold", "yellow") + "  — ლიდერბორდი")
    print(c("  q", "bold", "red")    + "  — გასვლა\n")

    choice = input(c("  არჩევანი: ", "cyan")).strip().lower()

    if choice == "q":
        print(c("\n  ნახვამდის! 👋\n", "yellow"))
        return
    elif choice == "2":
        show_leaderboard()
        input(c("\n  Enter — გასასვლელად...", "cyan"))
        return
    elif choice != "1":
        return

    name = input(c("\n  შეიყვანე სახელი: ", "green")).strip() or "სტუმარი"

    themes = list(WORD_SETS.keys())
    print(c("\n  თემა:", "bold"))
    for i, t in enumerate(themes, 1):
        print(f"  {c(str(i), 'bold', 'yellow')} — {t}")
    t_choice = input(c("\n  აირჩიე (1-3): ", "cyan")).strip()
    try:
        theme = themes[int(t_choice) - 1]
    except (ValueError, IndexError):
        theme = random.choice(themes)
        print(c(f"  შემთხვევითი თემა: {theme}", "cyan"))

    score, total = play(theme, WORD_SETS[theme])

    pct = int(100 * score / total)
    os.system("clear")
    print(c(f"""
  ╔══════════════════════════╗
  ║      🏁 თამაში დასრულდა  ║
  ╚══════════════════════════╝

  მოთამაშე:  {name}
  თემა:      {theme}
  შედეგი:    {score}/{total}  ({pct}%)
""", "bold"))

    if pct == 100:
        print(c("  🏆 სრულყოფილი! ბრავო!", "bold", "yellow"))
    elif pct >= 70:
        print(c("  🎉 კარგი შედეგი!", "green"))
    else:
        print(c("  💪 კიდევ სცადე, გამოვა!", "cyan"))

    save_score(name, score, total, theme)
    print(c("\n  ქულა შენახულია ლიდერბორდში!\n", "cyan"))

if __name__ == "__main__":
    main()
