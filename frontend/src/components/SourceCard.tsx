import { ExternalLink } from "lucide-react";

interface SourceCardProps {
  paper_id: string;
  title: string;
  authors: string[];
  published: string;
}

export default function SourceCard({ paper_id, title, authors, published }: SourceCardProps) {
  // Format date to just Year-Month
  const dateStr = new Date(published).toLocaleDateString('en-US', { year: 'numeric', month: 'short' });
  const authorStr = authors.length > 3 ? `${authors.slice(0, 3).join(", ")} et al.` : authors.join(", ");

  return (
    <div className="p-4 bg-[#0a0a0a] border border-[#262626] rounded-lg">
      <div className="flex justify-between items-start gap-4">
        <div>
          <h4 className="font-semibold text-gray-200 line-clamp-2" title={title}>{title}</h4>
          <p className="text-sm text-gray-500 mt-1">{authorStr} • {dateStr}</p>
        </div>
        <a 
          href={`https://arxiv.org/abs/${paper_id}`} 
          target="_blank" 
          rel="noopener noreferrer"
          className="flex-shrink-0 p-2 text-blue-400 hover:bg-blue-900/20 rounded-lg transition-colors"
          title="View on arXiv"
        >
          <ExternalLink className="w-4 h-4" />
        </a>
      </div>
    </div>
  );
}