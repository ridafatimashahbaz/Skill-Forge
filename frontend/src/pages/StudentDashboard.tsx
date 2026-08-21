import { useEffect, useState } from "react";
import { api } from "../api";
import { ProgressBar } from "../components/ProgressBar";

const AREAS = ["python", "web_development", "git", "devops", "ai", "database"];
const ROLES = ["ai_engineer", "backend_developer", "frontend_developer", "devops_engineer", "full_stack_developer"];

type Tab = "profile" | "skills" | "assessment" | "roadmap" | "assistant";

export function StudentDashboard() {
  const [tab, setTab] = useState<Tab>("profile");
  const [profile, setProfile] = useState<any>(null);

  useEffect(() => {
    api.getProfile().then(setProfile).catch(() => {});
  }, []);

  const tabs: { id: Tab; label: string }[] = [
    { id: "profile", label: "Profile" },
    { id: "skills", label: "Skills & projects" },
    { id: "assessment", label: "Assessment" },
    { id: "roadmap", label: "Roadmap" },
    { id: "assistant", label: "AI assistant" },
  ];

  return (
    <div className="max-w-5xl mx-auto px-6 py-8">
      <nav className="flex gap-2 mb-8 flex-wrap">
        {tabs.map((t) => (
          <button
            key={t.id}
            onClick={() => setTab(t.id)}
            className={`px-4 py-2 rounded-full text-sm font-medium border ${
              tab === t.id
                ? "bg-forge text-white border-forge"
                : "border-ink/15 text-ink/70 hover:border-forge"
            }`}
          >
            {t.label}
          </button>
        ))}
      </nav>

      {tab === "profile" && <ProfileTab profile={profile} onUpdate={setProfile} />}
      {tab === "skills" && <SkillsTab profile={profile} onUpdate={setProfile} />}
      {tab === "assessment" && <AssessmentTab />}
      {tab === "roadmap" && <RoadmapTab />}
      {tab === "assistant" && <AssistantTab />}
    </div>
  );
}

function ProfileTab({ profile, onUpdate }: any) {
  const [education, setEducation] = useState("");
  const [experienceLevel, setExperienceLevel] = useState("beginner");
  const [careerGoal, setCareerGoal] = useState("");
  const [saved, setSaved] = useState(false);

  useEffect(() => {
    if (profile) {
      setEducation(profile.education || "");
      setExperienceLevel(profile.experience_level || "beginner");
      setCareerGoal(profile.career_goal || "");
    }
  }, [profile]);

  async function save() {
    const updated = await api.updateProfile({
      education,
      experience_level: experienceLevel,
      career_goal: careerGoal,
    });
    onUpdate(updated);
    setSaved(true);
    setTimeout(() => setSaved(false), 1500);
  }

  return (
    <div className="max-w-lg space-y-4">
      <h2 className="text-xl font-display font-semibold">Your profile</h2>
      <label className="block text-sm">
        Education
        <input
          value={education}
          onChange={(e) => setEducation(e.target.value)}
          className="w-full border border-ink/20 rounded-lg px-3 py-2 mt-1"
          placeholder="e.g. BS Computer Science, COMSATS"
        />
      </label>
      <label className="block text-sm">
        Experience level
        <select
          value={experienceLevel}
          onChange={(e) => setExperienceLevel(e.target.value)}
          className="w-full border border-ink/20 rounded-lg px-3 py-2 mt-1"
        >
          <option value="beginner">Beginner</option>
          <option value="intermediate">Intermediate</option>
          <option value="advanced">Advanced</option>
        </select>
      </label>
      <label className="block text-sm">
        Career goal
        <input
          value={careerGoal}
          onChange={(e) => setCareerGoal(e.target.value)}
          className="w-full border border-ink/20 rounded-lg px-3 py-2 mt-1"
          placeholder="e.g. AI engineer"
        />
      </label>
      <button onClick={save} className="bg-forge text-white rounded-lg px-4 py-2 text-sm font-medium">
        Save
      </button>
      {saved && <span className="text-forge text-sm ml-3">Saved</span>}
    </div>
  );
}

function SkillsTab({ profile, onUpdate }: any) {
  const [skillName, setSkillName] = useState("");
  const [proficiency, setProficiency] = useState(3);
  const [projectTitle, setProjectTitle] = useState("");
  const [projectDesc, setProjectDesc] = useState("");
  const [projectTech, setProjectTech] = useState("");

  async function refresh() {
    const p = await api.getProfile();
    onUpdate(p);
  }

  async function addSkill() {
    if (!skillName.trim()) return;
    await api.addSkill({ name: skillName, proficiency });
    setSkillName("");
    refresh();
  }

  async function addProject() {
    if (!projectTitle.trim()) return;
    await api.addProject({ title: projectTitle, description: projectDesc, tech_stack: projectTech });
    setProjectTitle("");
    setProjectDesc("");
    setProjectTech("");
    refresh();
  }

  if (!profile) return <p className="text-ink/60">Loading...</p>;

  return (
    <div className="grid md:grid-cols-2 gap-8">
      <div>
        <h3 className="font-display font-semibold mb-3">Skills</h3>
        <div className="flex flex-wrap gap-2 mb-4">
          {profile.skills.map((s: any) => (
            <span
              key={s.id}
              className="bg-forge-light text-forge-dark text-sm px-3 py-1 rounded-full flex items-center gap-2"
            >
              {s.name} · {s.proficiency}/5
              <button onClick={async () => { await api.deleteSkill(s.id); refresh(); }} className="text-forge-dark/50 hover:text-ember">
                ×
              </button>
            </span>
          ))}
          {profile.skills.length === 0 && <p className="text-sm text-ink/50">No skills added yet.</p>}
        </div>
        <div className="flex gap-2">
          <input
            value={skillName}
            onChange={(e) => setSkillName(e.target.value)}
            placeholder="e.g. Python"
            className="border border-ink/20 rounded-lg px-3 py-2 text-sm flex-1"
          />
          <select value={proficiency} onChange={(e) => setProficiency(Number(e.target.value))} className="border border-ink/20 rounded-lg px-2 text-sm">
            {[1, 2, 3, 4, 5].map((n) => <option key={n} value={n}>{n}</option>)}
          </select>
          <button onClick={addSkill} className="bg-forge text-white rounded-lg px-3 text-sm">Add</button>
        </div>
      </div>

      <div>
        <h3 className="font-display font-semibold mb-3">Projects</h3>
        <ul className="space-y-2 mb-4">
          {profile.projects.map((p: any) => (
            <li key={p.id} className="border border-ink/10 rounded-lg p-3 text-sm">
              <div className="flex justify-between">
                <span className="font-medium">{p.title}</span>
                <button onClick={async () => { await api.deleteProject(p.id); refresh(); }} className="text-ink/40 hover:text-ember">×</button>
              </div>
              {p.tech_stack && <p className="text-ink/50 text-xs mt-1">{p.tech_stack}</p>}
              {p.description && <p className="text-ink/70 mt-1">{p.description}</p>}
            </li>
          ))}
          {profile.projects.length === 0 && <p className="text-sm text-ink/50">No projects added yet.</p>}
        </ul>
        <div className="space-y-2">
          <input value={projectTitle} onChange={(e) => setProjectTitle(e.target.value)} placeholder="Project title"
            className="w-full border border-ink/20 rounded-lg px-3 py-2 text-sm" />
          <input value={projectTech} onChange={(e) => setProjectTech(e.target.value)} placeholder="Tech stack (e.g. React, FastAPI)"
            className="w-full border border-ink/20 rounded-lg px-3 py-2 text-sm" />
          <textarea value={projectDesc} onChange={(e) => setProjectDesc(e.target.value)} placeholder="Short description"
            className="w-full border border-ink/20 rounded-lg px-3 py-2 text-sm" rows={2} />
          <button onClick={addProject} className="bg-forge text-white rounded-lg px-3 py-2 text-sm">Add project</button>
        </div>
      </div>
    </div>
  );
}

function AssessmentTab() {
  const [area, setArea] = useState(AREAS[0]);
  const [questions, setQuestions] = useState<any[]>([]);
  const [answers, setAnswers] = useState<Record<string, string>>({});
  const [result, setResult] = useState<any>(null);
  const [scores, setScores] = useState<Record<string, number>>({});

  useEffect(() => {
    api.getScores().then(setScores).catch(() => {});
  }, [result]);

  async function loadQuestions() {
    setResult(null);
    setAnswers({});
    const qs = await api.getQuestions(area, 5);
    setQuestions(qs);
  }

  async function submit() {
    const payload = {
      area,
      answers: Object.entries(answers).map(([question_id, selected_option]) => ({ question_id, selected_option })),
    };
    const res = await api.submitAssessment(payload);
    setResult(res);
  }

  return (
    <div className="max-w-2xl">
      <h2 className="text-xl font-display font-semibold mb-4">Skill assessment</h2>

      <div className="mb-6">
        <h3 className="text-sm font-medium text-ink/70 mb-2">Your latest scores</h3>
        {AREAS.map((a) => <ProgressBar key={a} label={a} value={scores[a] || 0} />)}
      </div>

      <div className="flex gap-2 mb-4">
        <select value={area} onChange={(e) => setArea(e.target.value)} className="border border-ink/20 rounded-lg px-3 py-2 text-sm">
          {AREAS.map((a) => <option key={a} value={a}>{a.replace("_", " ")}</option>)}
        </select>
        <button onClick={loadQuestions} className="bg-forge text-white rounded-lg px-4 py-2 text-sm">Start assessment</button>
      </div>

      {questions.length > 0 && !result && (
        <div className="space-y-4">
          {questions.map((q) => (
            <div key={q.id} className="border border-ink/10 rounded-lg p-4">
              <p className="text-sm font-medium mb-2">{q.question}</p>
              {Object.entries(q.options).map(([key, text]) => (
                <label key={key} className="flex items-center gap-2 text-sm py-1">
                  <input
                    type="radio"
                    name={q.id}
                    checked={answers[q.id] === key}
                    onChange={() => setAnswers({ ...answers, [q.id]: key })}
                  />
                  {text as string}
                </label>
              ))}
            </div>
          ))}
          <button onClick={submit} className="bg-forge text-white rounded-lg px-4 py-2 text-sm">Submit answers</button>
        </div>
      )}

      {result && (
        <div className="border border-forge/30 bg-forge-light rounded-lg p-4 text-sm">
          Score for {result.area.replace("_", " ")}: <strong>{result.score}%</strong> ({result.correct}/{result.total} correct)
        </div>
      )}
    </div>
  );
}

function RoadmapTab() {
  const [targetRole, setTargetRole] = useState(ROLES[0]);
  const [roadmap, setRoadmap] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    api.getLatestRoadmap().then(setRoadmap).catch(() => {});
  }, []);

  async function generate() {
    setLoading(true);
    try {
      const r = await api.generateRoadmap(targetRole);
      setRoadmap(r);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="max-w-2xl">
      <h2 className="text-xl font-display font-semibold mb-4">Career roadmap</h2>
      <div className="flex gap-2 mb-6">
        <select value={targetRole} onChange={(e) => setTargetRole(e.target.value)} className="border border-ink/20 rounded-lg px-3 py-2 text-sm">
          {ROLES.map((r) => <option key={r} value={r}>{r.replace("_", " ")}</option>)}
        </select>
        <button onClick={generate} disabled={loading} className="bg-forge text-white rounded-lg px-4 py-2 text-sm">
          {loading ? "Generating..." : "Generate roadmap"}
        </button>
      </div>

      {roadmap && (
        <div className="space-y-6">
          <div className="flex gap-4 text-sm">
            <span className="bg-forge-light text-forge-dark px-3 py-1 rounded-full">
              Current level: {roadmap.current_level}
            </span>
            <span className="bg-forge-light text-forge-dark px-3 py-1 rounded-full">
              Target: {roadmap.target_role.replace("_", " ")}
            </span>
          </div>

          <div>
            <h3 className="text-sm font-medium text-ink/70 mb-2">Skill gaps</h3>
            <ul className="space-y-2">
              {roadmap.skill_gaps.map((g: any) => (
                <li key={g.topic} className="text-sm border-l-2 border-ember pl-3">
                  <strong className="capitalize">{g.topic.replace("_", " ")}</strong> — current {g.current_score}%, gap size {g.gap_size}
                </li>
              ))}
              {roadmap.skill_gaps.length === 0 && <p className="text-sm text-ink/50">No major gaps detected — take assessments to refine this.</p>}
            </ul>
          </div>

          <div>
            <h3 className="text-sm font-medium text-ink/70 mb-2">Recommended topics</h3>
            <div className="space-y-3">
              {roadmap.recommended_topics.map((t: any) => (
                <div key={t.topic} className="border border-ink/10 rounded-lg p-3">
                  <div className="flex justify-between text-sm font-medium capitalize">
                    <span>{t.topic.replace("_", " ")}</span>
                    <span className={t.priority === "high" ? "text-ember" : "text-ink/50"}>{t.priority} priority</span>
                  </div>
                  <ul className="list-disc list-inside text-sm text-ink/70 mt-1">
                    {t.subtopics.map((s: string) => <li key={s}>{s}</li>)}
                  </ul>
                </div>
              ))}
            </div>
          </div>

          <div>
            <h3 className="text-sm font-medium text-ink/70 mb-2">Suggested projects</h3>
            <ul className="list-disc list-inside text-sm text-ink/70">
              {roadmap.suggested_projects.map((p: string) => <li key={p}>{p}</li>)}
            </ul>
          </div>
        </div>
      )}
    </div>
  );
}

function AssistantTab() {
  const [mode, setMode] = useState<"chat" | "agent">("agent");
  const [message, setMessage] = useState("");
  const [history, setHistory] = useState<{ role: string; text: string }[]>([]);
  const [loading, setLoading] = useState(false);

  async function send() {
    if (!message.trim()) return;
    const userMsg = message;
    setHistory((h) => [...h, { role: "user", text: userMsg }]);
    setMessage("");
    setLoading(true);
    try {
      const res = mode === "agent" ? await api.runAgent(userMsg) : await api.chat(userMsg);
      setHistory((h) => [...h, { role: "assistant", text: res.reply }]);
    } catch (err: any) {
      setHistory((h) => [...h, { role: "assistant", text: `Error: ${err.message}` }]);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="max-w-2xl">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-xl font-display font-semibold">AI career assistant</h2>
        <select value={mode} onChange={(e) => setMode(e.target.value as any)} className="border border-ink/20 rounded-lg px-2 py-1 text-sm">
          <option value="agent">Career agent (uses your profile)</option>
          <option value="chat">Knowledge base chat</option>
        </select>
      </div>

      <div className="border border-ink/10 rounded-lg p-4 h-80 overflow-y-auto space-y-3 mb-4 bg-white">
        {history.length === 0 && (
          <p className="text-sm text-ink/40">
            Try: "I know Python and basic web development. I want to become an AI engineer. What should I learn next?"
          </p>
        )}
        {history.map((m, i) => (
          <div key={i} className={m.role === "user" ? "text-right" : "text-left"}>
            <span className={`inline-block rounded-lg px-3 py-2 text-sm max-w-[85%] ${
              m.role === "user" ? "bg-forge text-white" : "bg-forge-light text-ink"
            }`}>
              {m.text}
            </span>
          </div>
        ))}
        {loading && <p className="text-sm text-ink/40">Thinking...</p>}
      </div>

      <div className="flex gap-2">
        <input
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && send()}
          placeholder="Ask about your next learning steps..."
          className="flex-1 border border-ink/20 rounded-lg px-3 py-2 text-sm"
        />
        <button onClick={send} className="bg-forge text-white rounded-lg px-4 py-2 text-sm">Send</button>
      </div>
    </div>
  );
}
