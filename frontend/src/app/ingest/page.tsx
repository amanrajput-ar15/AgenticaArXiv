"use client";

import { useState } from "react";
import { AgenticApi } from "@/lib/api";
import IngestForm from "@/components/IngestForm";
import IngestResult from "@/components/IngestResult";
import Link from "next/link";
import { ArrowRight, AlertTriangle } from "lucide-react";

export default function IngestPage() {
  const [isLoading, setIsLoading] = useState(false);
  const [result, setResult] = useState<{ papers: number; chunks: number } | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleIngest = async (query: string, maxResults: number) => {
    setIsLoading(true);
    setError(null);
    setResult(null);

    try {
      const data = await AgenticApi.ingestPapers(query, maxResults);
      setResult({ papers: data.papers_processed, chunks: data.chunks_created });
    } catch (err: any) {
      setError(err.response?.data?.detail || "Failed to ingest papers. Check backend logs.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <main className="max-w-3xl mx-auto p-8 pt-24 min-h-screen">
      <div className="mb-8">
        <h1 className="text-4xl font-bold mb-2">Ingest Knowledge</h1>
        <p className="text-gray-400">Search arXiv and populate the FAISS vector database.</p>
      </div>

      {error && (
        <div className="mb-6 p-4 bg-red-900/20 border border-red-900 rounded-lg flex items-center gap-3 text-red-400">
          <AlertTriangle className="w-5 h-5 flex-shrink-0" />
          <p>{error}</p>
        </div>
      )}

      <IngestForm onIngest={handleIngest} isLoading={isLoading} />

      {result && (
        <>
          <IngestResult papersProcessed={result.papers} chunksCreated={result.chunks} />
          <div className="mt-8 flex justify-center">
            <Link href="/research" className="flex items-center gap-2 text-blue-400 hover:text-blue-300 font-semibold transition-colors">
              Proceed to Research <ArrowRight className="w-5 h-5" />
            </Link>
          </div>
        </>
      )}
    </main>
  );
}