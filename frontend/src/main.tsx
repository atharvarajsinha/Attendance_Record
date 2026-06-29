import React, { FormEvent, useState } from "react";
import { createRoot } from "react-dom/client";
import { api } from "./api";
import "./styles.css";

interface AttendanceRecord {
  student_id: string;
  full_name: string;
  status: string;
  created_at: string;
}

interface AttendanceResponse {
  id: number;
  image: string;
  detected_faces: number;
  created_at: string;
  records: AttendanceRecord[];
}

type ApiState = {
  loading: boolean;
  result?: AttendanceResponse;
  error?: string;
};

function StudentRegistration() {
  const [state, setState] = useState<ApiState>({
    loading: false,
  });

  async function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();

    const form = event.currentTarget;   // ✅ Save reference first

    setState({ loading: true });

    try {
        const response = await api.post(
            "/api/attendance/verify/",
            new FormData(form),
            {
                headers: {
                    "Content-Type": "multipart/form-data",
                },
            }
        );

        form.reset();    // ✅ Safe

        setState({
            loading: false,
            result: response.data,
        });

    } catch (err) {
        console.error(err);

        setState({
            loading: false,
            error: "Attendance verification failed.",
        });
    }
  }

  return (
    <section className="card">
      <h2>Student Registration</h2>

      <form onSubmit={submit}>
        <input
          name="student_id"
          placeholder="Student ID"
          required
        />

        <input
          name="full_name"
          placeholder="Full Name"
          required
        />

        <input
          name="email"
          type="email"
          placeholder="Email"
        />

        <input
          name="image"
          type="file"
          accept="image/*"
          required
        />

        <button disabled={state.loading}>
          {state.loading ? "Registering..." : "Register Face"}
        </button>
      </form>

      <Result state={state} />
    </section>
  );
}

function AttendanceVerification() {
  const [state, setState] = useState<ApiState>({
    loading: false,
  });

  async function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();

    setState({ loading: true });

    try {
      console.log("Uploading classroom image...");

      const response = await api.post(
        "/api/attendance/verify/",
        new FormData(event.currentTarget),
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        }
      );

      console.log(response.data);

      event.currentTarget.reset();

      setState({
        loading: false,
        result: response.data,
      });
    } catch (err) {
      console.error(err);

      setState({
        loading: false,
        error: "Attendance verification failed.",
      });
    }
  }

  return (
    <section className="card">
      <h2>Attendance Verification</h2>

      <form onSubmit={submit}>
        <input
          name="image"
          type="file"
          accept="image/*"
          required
        />

        <button disabled={state.loading}>
          {state.loading ? "Verifying..." : "Verify Attendance"}
        </button>
      </form>

      <Result state={state} />
    </section>
  );
}

function Result({ state }: { state: ApiState }) {
  if (state.loading) {
    return <p>Processing...</p>;
  }

  if (state.error) {
    return (
      <p
        style={{
          color: "red",
          marginTop: 20,
        }}
      >
        {state.error}
      </p>
    );
  }

  if (!state.result) {
    return null;
  }

  const data = state.result;

  return (
    <div
      style={{
        marginTop: 20,
      }}
    >
      <h3>Attendance Result</h3>

      <p>
        <strong>Attendance ID:</strong> {data.id}
      </p>

      <p>
        <strong>Detected Faces:</strong>{" "}
        {data.detected_faces}
      </p>

      <p>
        <strong>Created At:</strong>{" "}
        {new Date(data.created_at).toLocaleString()}
      </p>

      {data.image && (
        <>
          <h4>Uploaded Classroom Image</h4>

          <img
            src={`http://localhost:8000${data.image}`}
            alt="Attendance"
            style={{
              maxWidth: "500px",
              width: "100%",
              borderRadius: "10px",
              border: "1px solid #ccc",
            }}
          />
        </>
      )}

      <h4
        style={{
          marginTop: 20,
        }}
      >
        Recognized Students
      </h4>

      <table
        style={{
          width: "100%",
          borderCollapse: "collapse",
        }}
      >
        <thead>
          <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Status</th>
            <th>Time</th>
          </tr>
        </thead>

        <tbody>
          {data.records.map((student) => (
            <tr key={student.student_id}>
              <td>{student.student_id}</td>

              <td>{student.full_name}</td>

              <td>
                <span
                  style={{
                    color:
                      student.status === "Present"
                        ? "green"
                        : "red",
                    fontWeight: "bold",
                  }}
                >
                  {student.status}
                </span>
              </td>

              <td>
                {new Date(
                  student.created_at
                ).toLocaleTimeString()}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

function App() {
  return (
    <main
      style={{
        maxWidth: "900px",
        margin: "30px auto",
        padding: "20px",
      }}
    >
      <h1>AI Attendance System</h1>

      <p>
        React → Django → FastAPI AI Service
      </p>

      <div
        style={{
          display: "grid",
          gap: "30px",
        }}
      >
        <StudentRegistration />

        <AttendanceVerification />
      </div>
    </main>
  );
}

createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);