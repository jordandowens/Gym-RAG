import React, { useState } from "react";

export default function MealInsert() {
  const [form, setForm] = useState({
    user_id: "",
    date: "",
    name: "",
    description: "",
    calories: "",
    protein: "",
    carbs: "",
    fat: "",
    notes: ""
  });

  const [metadata, setMetadata] = useState({
    quality: "",
    meal_type: "",
    phase: ""
  });

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const submitMeal = async () => {
    const dayOfWeek = form.date
      ? new Date(form.date).toLocaleDateString("en-US", { weekday: "long" })
      : null;

    const cleanedMetadata = {
      meal_type: metadata.meal_type || null,
      phase: metadata.phase || null,
      quality: metadata.quality || null,
      day_of_week: dayOfWeek
    };

    Object.keys(cleanedMetadata).forEach(
      (key) => cleanedMetadata[key] === null && delete cleanedMetadata[key]
    );

    const payload = {
      user_id: Number(form.user_id),
      date: form.date,
      name: form.name,
      description: form.description,
      calories: Number(form.calories) || 0,
      protein: Number(form.protein) || 0,
      carbs: Number(form.carbs) || 0,
      fat: Number(form.fat) || 0,
      notes: form.notes || "",
      metadata: cleanedMetadata
    };

    const res = await fetch("http://localhost:5000/meals", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });

    const data = await res.json();
    console.log("Meal Insert Response:", data);
    alert("Meal inserted!");
  };

  return (
    <div className="form-body">
      <input name="user_id" placeholder="User ID" onChange={handleChange} />
      <input name="date" type="date" onChange={handleChange} />
      <input name="name" placeholder="Meal Name" onChange={handleChange} />
      <textarea name="description" placeholder="Description" onChange={handleChange} />

      <input name="calories" placeholder="Calories" onChange={handleChange} />
      <input name="protein" placeholder="Protein" onChange={handleChange} />
      <input name="carbs" placeholder="Carbs" onChange={handleChange} />
      <input name="fat" placeholder="Fat" onChange={handleChange} />

      <textarea name="notes" placeholder="Notes" onChange={handleChange} />

      <select
        value={metadata.meal_type}
        onChange={(e) => setMetadata({ ...metadata, meal_type: e.target.value })}
      >
        <option value="">Meal Type</option>
        <option value="breakfast">Breakfast</option>
        <option value="lunch">Lunch</option>
        <option value="dinner">Dinner</option>
        <option value="snack">Snack</option>
      </select>

      <select
        value={metadata.phase}
        onChange={(e) => setMetadata({ ...metadata, phase: e.target.value })}
      >
        <option value="">Phase</option>
        <option value="strength">Strength</option>
        <option value="hypertrophy">Hypertrophy</option>
        <option value="recovery">Recovery</option>
        <option value="cutting">Cutting</option>
      </select>

      <select
        value={metadata.quality}
        onChange={(e) => setMetadata({ ...metadata, quality: e.target.value })}
      >
        <option value="">Quality</option>
        <option value="great">Great</option>
        <option value="good">Good</option>
        <option value="average">Average</option>
        <option value="poor">Poor</option>
      </select>

      <button className="submit-btn" onClick={submitMeal}>
        Submit Meal
      </button>
    </div>
  );
}
