"use client";

import { useEffect, useState } from "react";
import { AgenticApi } from "../lib/api"; 
import { Activity, Database, Server, Search, Loader2, BookOpen, FlaskConical, BarChart2, ShieldAlert, Lightbulb } from "lucide-react";
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';

interface VectorStats {
  total_chunks: number;
  dimension: number;
}

interface AgentSection {
  analysis: string;
}

interface ResearchReport {
  query: string;
  literature_review: AgentSection;
  methods_analysis: AgentSection;
  results_analysis: AgentSection;
  critique: AgentSection;
  synthesis: AgentSection;
  num_sources: number;
}

export default function Home() {
  const [backendStatus, setBackendStatus] = useState<string>("Checking...");
  const [vectorStats, setVectorStats] = useState<VectorStats | null>(null);
  
  // New State for the Research UI
  const [query, setQuery] = useState("");
  const [isResearching, setIsResearching] = useState(false);
  const [report, setReport] = useState<ResearchReport | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const checkBackend = async () => {
      try {
        const data = await AgenticApi.checkStatus();
        setBackendStatus("Online");
        setVectorStats(data.vector_store);
      } catch (error) {
        setBackendStatus("Offline - Is FastAPI running?");
      }
    };
    checkBackend();
  }, []);

  const handleResearch = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim()) return;

    setIsResearching(true);
    setError(null);
    setReport(null);

    try {
      // Fires the agents! This takes ~1-2 minutes.
      const data = await AgenticApi.conductResearch(query);
      setReport(data);
    } catch (err: any) {
      setError(err.response?.data?.detail || "Research failed. Did you hit a rate limit?");
    } finally {
      setIsResearching(false);
    }
  };

  // Helper component to render each agent's section beautifully
  const AgentCard = ({ title, icon: Icon, content }: { title: string, icon: any, content: string }) => (
    <div className="bg-[#171717] border border-[#262626] rounded-xl p-6 shadow-lg mb-6">
      <h3 className="text-xl font-bold mb-4 flex items-center gap-3 text-blue-400">
        <Icon className="w-6 h-6" />
        {title}
      </h3>
      <div className="prose prose-invert max-w-none text-gray-300">
        <ReactMarkdown remarkPlugins={[remarkGfm]}>{content}</ReactMarkdown>
      </div>
    </div>
  );

  return (
    <main className="min-h-screen p-8 flex flex-col items-center relative overflow-y-auto">
      {/* Background Glow */}
      <div className="fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[800px] h-[800px] bg-blue-900/10 blur-[120px] rounded-full pointer-events-none -z-10" />

      <div className="w-full max-w-4xl flex flex-col gap-8 z-10 pb-20">
        
        {/* Header & Mini Diagnostics */}
        <div className="flex justify-between items-end border-b border-[#262626] pb-6 mt-4">
          <div>
            <h1 className="text-4xl font-bold tracking-tight">AgenticArXiv</h1>
            <p className="text-gray-400 mt-2">Autonomous Research Orchestration</p>
          </div>
          <div className="flex gap-4 text-sm">
            <span className={`flex items-center gap-2 px-3 py-1 rounded-full bg-black/50 border border-[#262626] ${backendStatus === 'Online' ? 'text-green-500' : 'text-red-500'}`}>
              <Server className="w-4 h-4" /> {backendStatus}
            </span>
            <span className="flex items-center gap-2 px-3 py-1 rounded-full bg-black/50 border border-[#262626] text-gray-400">
              <Database className="w-4 h-4" /> {vectorStats ? `${vectorStats.total_chunks} chunks` : 'Loading...'}
            </span>
          </div>
        </div>

        {/* The Research Input */}
        <form onSubmit={handleResearch} className="relative group">
          <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
            <Search className="h-6 w-6 text-gray-500 group-focus-within:text-blue-500 transition-colors" />
          </div>
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            disabled={isResearching || backendStatus !== 'Online'}
            placeholder="Ask your agents a complex research question..."
            className="w-full bg-[#171717] border-2 border-[#262626] text-white rounded-2xl pl-14 pr-32 py-5 text-lg focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 transition-all disabled:opacity-50"
          />
          <button
            type="submit"
            disabled={isResearching || !query.trim() || backendStatus !== 'Online'}
            className="absolute inset-y-2 right-2 px-6 bg-blue-600 hover:bg-blue-500 text-white font-semibold rounded-xl disabled:opacity-50 disabled:cursor-not-allowed transition-colors flex items-center gap-2"
          >
            {isResearching ? (
              <><Loader2 className="w-5 h-5 animate-spin" /> Orchestrating...</>
            ) : "Research"}
          </button>
        </form>

        {/* Error Handling */}
        {error && (
          <div className="p-4 bg-red-900/20 border border-red-900 text-red-400 rounded-xl flex items-start gap-3">
            <ShieldAlert className="w-5 h-5 flex-shrink-0 mt-0.5" />
            <p>{error}</p>
          </div>
        )}

        {/* Deep Thinking State */}
        {isResearching && (
          <div className="flex flex-col items-center justify-center py-20 text-gray-400 space-y-4">
            <div className="relative">
              <div className="w-16 h-16 border-4 border-blue-900/30 rounded-full animate-pulse"></div>
              <Activity className="w-8 h-8 text-blue-500 absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 animate-bounce" />
            </div>
            <p className="text-lg">Deploying 5 specialized AI agents...</p>
            <p className="text-sm text-gray-500">This usually takes 1 to 2 minutes as they read, critique, and synthesize.</p>
          </div>
        )}

        {/* The Multi-Agent Report Render */}
        {report && !isResearching && (
          <div className="animate-in fade-in slide-in-from-bottom-4 duration-700 space-y-2 mt-4">
            <div className="flex items-center gap-2 mb-6 text-gray-400 bg-blue-900/10 px-4 py-2 rounded-lg border border-blue-900/30 w-fit">
              <BookOpen className="w-4 h-4" />
              <span>Synthesized from {report.num_sources} semantic vector sources</span>
            </div>

            <AgentCard title="1. Literature Review" icon={BookOpen} content={report.literature_review.analysis} />
            <AgentCard title="2. Methodology Analysis" icon={FlaskConical} content={report.methods_analysis.analysis} />
            <AgentCard title="3. Results & Findings" icon={BarChart2} content={report.results_analysis.analysis} />
            <AgentCard title="4. Critical Review" icon={ShieldAlert} content={report.critique.analysis} />
            <AgentCard title="5. Final Synthesis" icon={Lightbulb} content={report.synthesis.analysis} />
          </div>
        )}

      </div>
    </main>
  );
}