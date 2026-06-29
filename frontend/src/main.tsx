import React, { FormEvent, useState } from "react";
import { createRoot } from "react-dom/client";
import { api } from "./api";
import "./styles.css";

type ApiState = { loading: boolean; result?: unknown; error?: string };

function StudentRegistration() {
  const [state, setState] = useState<ApiState>({ loading: false });

  async function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setState({ loading: true });
    try {
      const response = await api.post("/api/student/register/", new FormData(event.currentTarget), {
        headers: { "Content-Type": "multipart/form-data" },
      });
      event.currentTarget.reset();
      setState({ loading: false, result: response.data });
    } catch (error) {
      setState({ loading: false, error: "Student registration failed. Check backend and AI service logs." });
    }
  }

  return (
    <section className="card">
      <h2>Student Registration</h2>
      <form onSubmit={submit}>
        <input name="student_id" placeholder="Student ID (e.g. 101)" required />
        <input name="full_name" placeholder="Full name" required />
        <input name="email" placeholder="Email" type="email" />
        <input name="image" type="file" accept="image/*" required />
        <button disabled={state.loading}>{state.loading ? "Registering..." : "Register Face"}</button>
      </form>
      <Result state={state} />
    </section>
  );
}

function AttendanceVerification() {
  const [state, setState] = useState<ApiState>({ loading: false });

  async function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setState({ loading: true });
    try {
      const response = await api.post("/api/attendance/verify/", new FormData(event.currentTarget), {
        headers: { "Content-Type": "multipart/form-data" },
      });
      event.currentTarget.reset();
      setState({ loading: false, result: response.data });
    } catch (error) {
      setState({ loading: false, error: "Attendance verification failed. Check backend and AI service logs." });
    }
  }

  return (
    <section className="card">
      <h2>Attendance Verification</h2>
      <form onSubmit={submit}>
        <input name="image" type="file" accept="image/*" required />
        <button disabled={state.loading}>{state.loading ? "Verifying..." : "Verify Attendance"}</button>
      </form>
      <Result state={state} />
    </section>
  );
}

function Result({ state }: { state: ApiState }) {
  if (state.error) return <p className="error">{state.error}</p>;
  if (!state.result) return null;
  return <pre>{JSON.stringify(state.result, null, 2)}</pre>;
}

function App() {
  return (
    <main>
      <h1>AI Attendance System</h1>
      <p>React calls Django only; Django calls the independent FastAPI AI service.</p>
      <div className="grid">
        <StudentRegistration />
        <AttendanceVerification />
      </div>
    </main>
  );
}

createRoot(document.getElementById("root")!).render(<App />);
