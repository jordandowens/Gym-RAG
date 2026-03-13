# generate_gym_rag_data.py
import json
from datetime import date, timedelta
from pathlib import Path
import random

START_DATE = date(2026, 1, 1)
DAYS = 500
OUTPUT_DIR = Path("data")
OUTPUT_DIR.mkdir(exist_ok=True)

def day_of_week(d: date):
    return d.strftime("%A")

def phase_for_day(day_index: int):
    # 0–59: strength
    # 60–89: plateau
    # 90–104: deload
    # 105–134: injury
    # 135+: recovery
    if day_index < 60:
        return "strength"
    if day_index < 90:
        return "plateau"
    if day_index < 105:
        return "deload"
    if day_index < 135:
        return "injury"
    return "recovery"

def is_rest_day(d: date):
    # 6 lifting, 1 rest: Sunday rest
    return d.weekday() == 6  # Monday=0 ... Sunday=6

def generate_meals_for_day(d: date, phase: str):
    meals = []
    # quality bias by phase
    if phase == "strength":
        qualities = ["good", "good", "average"]
    elif phase == "plateau":
        qualities = ["good", "average", "average", "bad"]
    elif phase == "deload":
        qualities = ["good", "average"]
    elif phase == "injury":
        qualities = ["average", "bad", "bad"]
    else:  # recovery
        qualities = ["good", "average", "good"]

    meal_types = ["breakfast", "lunch", "dinner"]

    for meal_type in meal_types:
        quality = random.choice(qualities)

        if quality == "good":
            calories = random.randint(550, 850)
            protein = random.randint(35, 60)
            carbs = random.randint(50, 100)
            fat = random.randint(10, 25)
            desc = "Clean, high-protein meal with complex carbs."
        elif quality == "average":
            calories = random.randint(450, 700)
            protein = random.randint(20, 40)
            carbs = random.randint(50, 90)
            fat = random.randint(15, 30)
            desc = "Decent meal, some processed food."
        else:  # bad
            calories = random.randint(800, 1500)
            protein = random.randint(10, 35)
            carbs = random.randint(80, 180)
            fat = random.randint(30, 70)
            desc = "Highly processed, low-quality meal."

        meals.append({
            "user_id": 1,
            "date": str(d),
            "name": meal_type.capitalize(),
            "description": desc,
            "calories": calories,
            "protein": protein,
            "carbs": carbs,
            "fat": fat,
            "notes": f"{quality.capitalize()} {meal_type} on {phase} phase.",
            "metadata": {
                "quality": quality,
                "meal_type": meal_type,
                "phase": phase
            }
        })

    return meals

def generate_workout_for_day(d: date, day_index: int, bench_prev: int):
    phase = phase_for_day(day_index)
    rest = is_rest_day(d)

    if rest:
        energy = random.randint(5, 7)
        text = "Rest day"
        notes = "Recovery day, no lifting."
        quality = "neutral"
        bench = bench_prev
    else:
        # nutrition/performance trend: later you can correlate with meals
        if phase == "strength":
            bench = bench_prev + random.randint(0, 5)
            energy = random.randint(7, 9)
            notes = "Pushing strength progression."
        elif phase == "plateau":
            bench = bench_prev + random.randint(-2, 1)
            energy = random.randint(5, 7)
            notes = "Hitting a plateau, lifts feel heavy."
        elif phase == "deload":
            bench = bench_prev - random.randint(10, 20)
            energy = random.randint(6, 8)
            notes = "Deload week to recover fatigue."
        elif phase == "injury":
            bench = bench_prev - random.randint(15, 30)
            energy = random.randint(2, 5)
            notes = "Training around injury, reduced load."
        else:  # recovery
            bench = bench_prev + random.randint(1, 4)
            energy = random.randint(5, 7)
            notes = "Rebuilding after injury."

        text = f"Bench press 5x5 at {bench} lbs, accessory work."
        quality = "good" if energy >= 7 else "average" if energy >= 5 else "bad"

    workout = {
        "user_id": 1,
        "date": str(d),
        "workout_text": text,
        "energy_level": energy,
        "notes": notes,
        "metadata": {
            "phase": phase if not rest else "rest",
            "day_of_week": day_of_week(d),
            "is_rest_day": rest,
            "quality": quality,
            "focus": "upper" if not rest else "recovery"
        }
    }

    return workout, bench

def main():
    workouts = []
    meals = []

    bench = 135
    for i in range(DAYS):
        d = START_DATE + timedelta(days=i)
        phase = phase_for_day(i)

        # 3 meals per day
        meals.extend(generate_meals_for_day(d, phase))

        # 1 workout per day (including rest days)
        workout, bench = generate_workout_for_day(d, i, bench)
        workouts.append(workout)

    with open(OUTPUT_DIR / "workouts.json", "w", encoding="utf-8") as f:
        json.dump(workouts, f, indent=2)

    with open(OUTPUT_DIR / "meals.json", "w", encoding="utf-8") as f:
        json.dump(meals, f, indent=2)

    print(f"Generated {len(workouts)} workouts and {len(meals)} meals.")

if __name__ == "__main__":
    main()
