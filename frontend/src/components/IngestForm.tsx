"use client";

import { useState } from "react";
import { Search, Loader2 } from "lucide-react";

interface IngestFormProps {
  onIngest: (query: string, maxResults: number) => Promise<void>;
  isLoading: boolean;
}

export default function IngestForm({ onIngest, isLoading }: IngestFormProps) {
  const [query, setQuery] = useState("");
  const [maxResults, setMaxResults] = useState(5);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (query.trim()) onIngest(query, maxResults);
  };

  return (
    <form onSubmit={handleSubmit} className="bg-[#171717] border border-[#262626] p-6 rounded-xl shadow-lg flex flex-col gap-4">
      <div>
        <label className="block text-sm font-medium text-gray-400 mb-2">Research Topic</label>
        <div className="relative">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-500" />
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            disabled={isLoading}
            placeholder="e.g., transformer attention mechanisms"
            className="w-full bg-[#0a0a0a] border border-[#262626] text-white rounded-lg pl-10 pr-4 py-3 focus:outline-none focus:border-blue-500"
            required
          />
        </div>
      </div>
      
      <div>
        <label className="block text-sm font-medium text-gray-400 mb-2">Max Papers to Download: {maxResults}</label>
        <input
          type="range"
          min="1"
          max="20"
          value={maxResults}
          onChange={(e) => setMaxResults(Number(e.target.value))}
          disabled={isLoading}
          className="w-full accent-blue-600"
        />
      </div>

      <button
        type="submit"
        disabled={isLoading || !query.trim()}
        className="mt-2 w-full bg-blue-600 hover:bg-blue-500 disabled:bg-blue-900/50 text-white font-bold py-3 rounded-lg flex justify-center items-center gap-2 transition-colors"
      >
        {isLoading ? <><Loader2 className="w-5 h-5 animate-spin" /> Downloading & Chunking PDFs...</> : "Ingest Papers"}
      </button>
      <p className="text-xs text-gray-500 text-center mt-2">
        Ingestion downloads PDFs directly from arXiv. This takes about 10 seconds per paper.
      </p>
    </form>
  );
}