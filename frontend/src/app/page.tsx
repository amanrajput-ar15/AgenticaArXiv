import Link from "next/link";
import { ArrowRight, DownloadCloud, BrainCircuit } from "lucide-react";

export default function LandingPage() {
  return (
    <main className="min-h-screen flex flex-col items-center justify-center p-8 relative overflow-hidden">
      {/* Background Glow */}
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[800px] h-[800px] bg-blue-900/10 blur-[120px] rounded-full pointer-events-none -z-10" />

      <div className="text-center max-w-3xl z-10">
        <h1 className="text-5xl md:text-7xl font-bold tracking-tight mb-6">
          Research <span className="text-blue-500">Autonomous</span>.
        </h1>
        <p className="text-xl text-gray-400 mb-10 leading-relaxed">
          AgenticArXiv orchestrates five specialized AI agents to read, critique, and synthesize arXiv papers into production-grade research reports.
        </p>

        <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
          <Link href="/ingest" className="w-full sm:w-auto flex items-center justify-center gap-2 bg-[#262626] hover:bg-[#333] text-white px-8 py-4 rounded-xl font-semibold transition-colors border border-[#404040]">
            <DownloadCloud className="w-5 h-5" /> Step 1: Ingest Papers
          </Link>
          <Link href="/research" className="w-full sm:w-auto flex items-center justify-center gap-2 bg-blue-600 hover:bg-blue-500 text-white px-8 py-4 rounded-xl font-semibold transition-colors">
            <BrainCircuit className="w-5 h-5" /> Step 2: Query Agents <ArrowRight className="w-5 h-5" />
          </Link>
        </div>
      </div>
    </main>
  );
}