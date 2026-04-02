import { Loader2 } from "lucide-react";

interface ResearchFormProps {
  query: string;
  setQuery: (q: string) => void;
  onResearch: (e: React.FormEvent) => void;
  isResearching: boolean;
  totalChunks: number;
}

export default function ResearchForm({ query, setQuery, onResearch, isResearching, totalChunks }: ResearchFormProps) {
  return (
    <form onSubmit={onResearch} className="bg-[#171717] border border-[#262626] p-6 rounded-xl shadow-lg">
      <textarea
        rows={4}
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        disabled={isResearching || totalChunks === 0}
        placeholder={totalChunks === 0 ? "Ingest papers first..." : "e.g., How do different attention mechanisms compare?"}
        className="w-full bg-[#0a0a0a] border border-[#262626] text-white rounded-lg p-4 mb-4 focus:outline-none focus:border-blue-500 resize-none disabled:opacity-50"
        required
      />
      <div className="flex justify-between items-center">
        <p className="text-sm text-gray-500">
          Takes 30–50 seconds — 5 specialized agents will analyze your query.
        </p>
        <button
          type="submit"
          disabled={isResearching || totalChunks === 0 || !query.trim()}
          className="bg-blue-600 hover:bg-blue-500 disabled:bg-blue-900/50 text-white font-bold py-2 px-6 rounded-lg flex items-center gap-2 transition-colors"
        >
          {isResearching ? <><Loader2 className="w-4 h-4 animate-spin" /> Orchestrating...</> : "Generate Report"}
        </button>
      </div>
    </form>
  );
}