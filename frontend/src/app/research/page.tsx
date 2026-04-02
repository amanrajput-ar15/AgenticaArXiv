"use client";

import { useEffect, useState } from "react";
import { AgenticApi } from "@/lib/api";
import ResearchForm from "@/components/ResearchForm";
import ReportSkeleton from "@/components/ReportSkeleton";
import ReportSection from "@/components/ReportSection";
import SourceCard from "@/components/SourceCard";
import Link from "next/link";
import { AlertTriangle, FileQuestion, BookOpen, FlaskConical, BarChart2, ShieldAlert, Lightbulb, Download } from "lucide-react";

export default function ResearchPage() {
  const [totalChunks, setTotalChunks] = useState<number>(-1);
  const [query, setQuery] = useState("");
  const [isResearching, setIsResearching] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [report, setReport] = useState<any | null>(null); // State for the report

  useEffect(() => {
    AgenticApi.checkStatus()
      .then(data => setTotalChunks(data.vector_store.total_chunks))
      .catch(() => setTotalChunks(0));
  }, []);

  const handleResearch = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim()) return;
    
    setIsResearching(true);
    setError(null);
    setReport(null);
    
    try {
      const data = await AgenticApi.conductResearch(query);
      setReport(data);
    } catch (err: any) {
      setError(err.response?.data?.detail || "Research failed. Did you hit a rate limit?");
    } finally {
      setIsResearching(false);
    }
  };

  const handleExport = () => {
    if (!report) return;
    const textContent = `Research Query: ${report.query}\n\n` +
      `1. Literature Review\n${report.literature_review.analysis}\n\n` +
      `2. Methods Analysis\n${report.methods_analysis.analysis}\n\n` +
      `3. Results Analysis\n${report.results_analysis.analysis}\n\n` +
      `4. Critical Analysis\n${report.critique.analysis}\n\n` +
      `5. Final Synthesis\n${report.synthesis.analysis}\n`;
      
    const blob = new Blob([textContent], { type: "text/plain" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `AgenticArXiv-Report-${Date.now()}.txt`;
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <main className="max-w-4xl mx-auto p-8 pt-24 min-h-screen">
      <div className="mb-8">
        <h1 className="text-4xl font-bold mb-2">Autonomous Research</h1>
        <p className="text-gray-400">Query your ingested papers using the multi-agent orchestrator.</p>
      </div>

      {totalChunks === 0 ? (
        <div className="bg-[#171717] border border-[#262626] rounded-xl p-12 text-center flex flex-col items-center">
          <FileQuestion className="w-16 h-16 text-gray-600 mb-4" />
          <h2 className="text-2xl font-bold mb-2">No papers indexed yet</h2>
          <p className="text-gray-400 mb-6">You need to ingest arXiv papers before querying the agents.</p>
          <Link href="/ingest" className="bg-white text-black px-6 py-2 rounded-lg font-bold hover:bg-gray-200 transition-colors">
            Go to Ingest →
          </Link>
        </div>
      ) : (
        <>
          {error && (
             <div className="mb-6 p-4 bg-red-900/20 border border-red-900 rounded-lg flex items-center gap-3 text-red-400">
               <AlertTriangle className="w-5 h-5 flex-shrink-0" />
               <p>{error}</p>
             </div>
          )}

          <ResearchForm query={query} setQuery={setQuery} onResearch={handleResearch} isResearching={isResearching} totalChunks={totalChunks} />

          {isResearching && <ReportSkeleton />}

          {report && !isResearching && (
            <div className="mt-8 animate-in fade-in slide-in-from-bottom-4">
              <div className="flex justify-between items-end mb-6">
                <h2 className="text-2xl font-bold">Research Report</h2>
                <button onClick={handleExport} className="flex items-center gap-2 text-sm bg-[#262626] hover:bg-[#333] text-gray-300 px-4 py-2 rounded-lg transition-colors">
                  <Download className="w-4 h-4" /> Export .txt
                </button>
              </div>

              <ReportSection title="1. Literature Review" icon={BookOpen} content={report.literature_review.analysis} sourcesCount={report.literature_review.sources_used} defaultOpen={true} />
              <ReportSection title="2. Methodology Analysis" icon={FlaskConical} content={report.methods_analysis.analysis} sourcesCount={report.methods_analysis.sources_used} />
              <ReportSection title="3. Results & Findings" icon={BarChart2} content={report.results_analysis.analysis} sourcesCount={report.results_analysis.sources_used} />
              <ReportSection title="4. Critical Review" icon={ShieldAlert} content={report.critique.analysis} sourcesCount={report.critique.sources_used} />
              <ReportSection title="5. Final Synthesis" icon={Lightbulb} content={report.synthesis.analysis} sourcesCount={report.synthesis.sources_used} />

              <div className="mt-12 mb-20">
                <h3 className="text-xl font-bold mb-4 flex items-center gap-2 border-b border-[#262626] pb-2">
                  <BookOpen className="w-5 h-5 text-gray-400" /> {report.num_sources} Sources Utilized
                </h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {report.sources.map((source: any) => (
                    <SourceCard key={source.paper_id} {...source} />
                  ))}
                </div>
              </div>
            </div>
          )}
        </>
      )}
    </main>
  );
}