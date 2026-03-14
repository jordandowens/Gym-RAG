import React, { useState } from "react";

export default function WorkoutInsert() {
  const [form, setForm] = useState({
    user_id: "",
    date: "",
    workout_text: "",
    energy_level: "",
    notes: ""
  });

  const [metadata, setMetadata] = useState({
    phase: "",
    focus: "",
    quality: "",
    is_rest_day: false,
    movements: []
  });

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const addMovement = () => {
    setMetadata({
      ...metadata,
      movements: [
        ...metadata.movements,
        { movement: "", sets: "", reps: "", weight: "" }
      ]
    });
  };

  const updateMovement = (index, field, value) => {
    const updated = [...metadata.movements];
    updated[index][field] = value;
    setMetadata({ ...metadata, movements: updated });
  };

  const removeMovement = (index) => {
    const updated = metadata.movements.filter((_, i) => i !== index);
    setMetadata({ ...metadata, movements: updated });
  };

  const submitWorkout = async () => {
    const dayOfWeek = form.date
      ? new Date(form.date).toLocaleDateString("en-US", { weekday: "long" })
      : null;

    const cleanedMovements = metadata.movements
      .map((m) => ({
        movement: m.movement || null,
        sets: m.sets ? Number(m.sets) : null,
        reps: m.reps ? Number(m.reps) : null,
        weight: m.weight ? Number(m.weight) : null
      }))
      .filter((m) => m.movement);

    const cleanedMetadata = {
      phase: metadata.phase || null,
      focus: metadata.focus || null,
      quality: metadata.quality || null,
      is_rest_day: Boolean(metadata.is_rest_day),
      day_of_week: dayOfWeek,
      movements: cleanedMovements
    };

    Object.keys(cleanedMetadata).forEach(
      (key) => cleanedMetadata[key] === null && delete cleanedMetadata[key]
    );

    const payload = {
      user_id: Number(form.user_id),
      date: form.date,
      workout_text: form.workout_text,
      energy_level: form.energy_level ? Number(form.energy_level) : 0,
      notes: form.notes || "",
      metadata: cleanedMetadata
    };

    const res = await fetch("http://localhost:5000/workouts", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });

    const data = await res.json();
    console.log("Workout Insert Response:", data);
    alert("Workout inserted!");
  };

  return (
    <div className="form-body">
      <input name="user_id" placeholder="User ID" onChange={handleChange} />
      <input name="date" type="date" onChange={handleChange} />
      <textarea name="workout_text" placeholder="Workout text" onChange={handleChange} />
      <input name="energy_level" placeholder="Energy Level" onChange={handleChange} />
      <textarea name="notes" placeholder="Notes" onChange={handleChange} />

      <select
        value={metadata.phase}
        onChange={(e) => setMetadata({ ...metadata, phase: e.target.value })}
      >
        <option value="">Select Phase</option>
        <option value="strength">Strength</option>
        <option value="hypertrophy">Hypertrophy</option>
        <option value="recovery">Recovery</option>
        <option value="deload">Deload</option>
      </select>

      <select
        value={metadata.focus}
        onChange={(e) => setMetadata({ ...metadata, focus: e.target.value })}
      >
        <option value="">Focus Area</option>
        <option value="chest">Chest</option>
        <option value="back">Back</option>
        <option value="legs">Legs</option>
        <option value="arms">Arms</option>
        <option value="shoulders">Shoulders</option>
        <option value="cardio">Cardio</option>
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

      <label style={{ color: "#e6edf3" }}>
        <input
          type="checkbox"
          checked={metadata.is_rest_day}
          onChange={(e) => setMetadata({ ...metadata, is_rest_day: e.target.checked })}
        />
        Rest Day
      </label>

      <h3 style={{ marginTop: "1rem" }}>Movements</h3>

      {metadata.movements.map((m, index) => (
        <div key={index} className="movement-row">
          <input
            placeholder="Movement"
            value={m.movement}
            onChange={(e) => updateMovement(index, "movement", e.target.value)}
          />
          <input
            placeholder="Sets"
            value={m.sets}
            onChange={(e) => updateMovement(index, "sets", e.target.value)}
          />
          <input
            placeholder="Reps"
            value={m.reps}
            onChange={(e) => updateMovement(index, "reps", e.target.value)}
          />
          <input
            placeholder="Weight"
            value={m.weight}
            onChange={(e) => updateMovement(index, "weight", e.target.value)}
          />
          <button onClick={() => removeMovement(index)}>X</button>
        </div>
      ))}

      <button className="submit-btn" onClick={addMovement}>
        Add Movement
      </button>

      <button className="submit-btn" onClick={submitWorkout}>
        Submit Workout
      </button>
    </div>
  );
}
