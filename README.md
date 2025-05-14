# USAF Simulator 🎖️

_A choose-your-own-adventure RPG inspired by real military life._

This game is a story-driven, RPG-style simulation of life in the U.S. Air Force, built as a **cautionary tale**, a narrative experience, and a systems-based reflection of personal experience. It emphasizes choice, consequence, morality, and mental health — blending engaging gameplay with thematic depth.

---

## 🎮 Current Features

### ✅ Core Systems
- Modular screen architecture: main menu, backstory, pause, reenlist, chapters
- Save system with metadata and slot support
- Inventory management system (add/remove/list)
- Morality and mental state tracking
- Player stat system influenced by backstory and choices
- Dialogue system with typewriter effect, branching, and skippable lines
- Dynamic main menu and pause music
- Dev overlay (toggle with `F1`) to display inventory, stats, mental state
- Floating debug logs (for event feedback)

### ✅ Narrative Foundation
- Backstory selection influences stats and opening scenario
- First chapter and tutorial character designed to build emotional investment
- In-game consequences based on actions and mental resilience

---

## 📈 Roadmap (v1.0)

### 🎯 First Milestone
- [ ] Chapter branching with stat-based dialogue
- [ ] Rank and XP system
- [ ] Minigames for training, drills, and decisions
- [ ] Unseen mental illness trigger (player begins losing control of choices)
- [ ] Save deletion and management UI
- [ ] Moral "gray zone" choices with permanent impact
- [ ] Portrait system: subtle changes based on mental state

### 🔮 Long-Term Vision
- Full narrative arc from basic training through active duty
- Increasing psychological dissonance and consequence
- A grounded portrayal of military life — both heroic and traumatic

---

## 🛠️ How to Run

### Requirements:
- Python 3.11+
- Pygame 2.6+

### Setup:
```bash
git clone git@github.com:payhowell/USAF_Simulator.git
cd USAF_Simulator
pip install -r requirements.txt  # if you have one, or install pygame manually
python run.py
