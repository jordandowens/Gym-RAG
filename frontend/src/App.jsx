import ChatSidebar from "./components/ChatSidebar";
import WorkoutInsert from "./components/WorkoutInsert";
import MealInsert from "./components/MealInsert";
import "./styles/main.css";

export default function App() {
  return (
    <div className="app-container">
      {/* Main content */}
      <div className="main-panel">
        <h1 className="page-title">GymRAG Dashboard</h1>

        <div className="forms-grid">
          <div className="form-card">
            <h2>Insert Workout</h2>
            <WorkoutInsert />
          </div>

          <div className="form-card">
            <h2>Insert Meal</h2>
            <MealInsert />
          </div>
        </div>
      </div>

      {/* Chat sidebar */}
      <div className="chat-sidebar">
        <ChatSidebar />
      </div>
    </div>
  );
}
