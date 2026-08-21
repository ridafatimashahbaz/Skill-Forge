export function ProgressBar({ label, value }: { label: string; value: number }) {
  const pct = Math.max(0, Math.min(100, value));
  return (
    <div className="mb-3">
      <div className="flex justify-between text-sm mb-1">
        <span className="capitalize text-ink/80">{label.replace("_", " ")}</span>
        <span className="text-ink/60">{pct}%</span>
      </div>
      <div className="h-2 w-full rounded-full bg-forge-light">
        <div
          className="h-2 rounded-full bg-forge transition-all"
          style={{ width: `${pct}%` }}
        />
      </div>
    </div>
  );
}
