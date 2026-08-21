import { useEffect, useState } from "react";
import { api } from "../api";

export function MentorDashboard() {
  const [students, setStudents] = useState<any[]>([]);
  const [selected, setSelected] = useState<any>(null);

  useEffect(() => {
    api.listStudents().then(setStudents).catch(() => {});
  }, []);

  async function view(userId: string) {
    const p = await api.getStudent(userId);
    setSelected({ ...p, userId });
  }

  return (
    <div className="max-w-5xl mx-auto px-6 py-8 grid md:grid-cols-3 gap-8">
      <div className="md:col-span-1">
        <h2 className="text-xl font-display font-semibold mb-4">Students</h2>
        <ul className="space-y-2">
          {students.map((s) => (
            <li key={s.user_id}>
              <button
                onClick={() => view(s.user_id)}
                className="w-full text-left border border-ink/10 rounded-lg p-3 hover:border-forge"
              >
                <p className="text-sm font-medium">{s.full_name}</p>
                <p className="text-xs text-ink/50">{s.career_goal || "No career goal set"}</p>
                <p className="text-xs text-ink/40">{s.skill_count} skills logged</p>
              </button>
            </li>
          ))}
          {students.length === 0 && <p className="text-sm text-ink/50">No students yet.</p>}
        </ul>
      </div>

      <div className="md:col-span-2">
        {selected ? (
          <div>
            <h3 className="text-lg font-display font-semibold mb-1">Profile</h3>
            <p className="text-sm text-ink/60 mb-4">
              {selected.education || "No education listed"} · {selected.experience_level}
            </p>
            <div className="mb-4">
              <h4 className="text-sm font-medium mb-2">Skills</h4>
              <div className="flex flex-wrap gap-2">
                {selected.skills.map((s: any) => (
                  <span key={s.id} className="bg-forge-light text-forge-dark text-xs px-2 py-1 rounded-full">
                    {s.name} · {s.proficiency}/5
                  </span>
                ))}
              </div>
            </div>
            <div>
              <h4 className="text-sm font-medium mb-2">Projects</h4>
              <ul className="space-y-2">
                {selected.projects.map((p: any) => (
                  <li key={p.id} className="text-sm border border-ink/10 rounded-lg p-3">
                    <p className="font-medium">{p.title}</p>
                    <p className="text-ink/60">{p.description}</p>
                  </li>
                ))}
              </ul>
            </div>
          </div>
        ) : (
          <p className="text-sm text-ink/50">Select a student to view their profile.</p>
        )}
      </div>
    </div>
  );
}
