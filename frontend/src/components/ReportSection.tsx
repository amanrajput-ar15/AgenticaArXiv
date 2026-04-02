"use client";

import { useState } from "react";
import { ChevronDown, ChevronUp, Copy, Check } from "lucide-react";
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';

interface ReportSectionProps {
  title: string;
  icon: any;
  content: string;
  sourcesCount: number;
  defaultOpen?: boolean;
}

export default function ReportSection({ title, icon: Icon, content, sourcesCount, defaultOpen = false }: ReportSectionProps) {
  const [isOpen, setIsOpen] = useState(defaultOpen);
  const [copied, setCopied] = useState(false);

  const handleCopy = (e: React.MouseEvent) => {
    e.stopPropagation();
    navigator.clipboard.writeText(content);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="bg-[#171717] border border-[#262626] rounded-xl mb-4 overflow-hidden shadow-lg transition-all">
      <button 
        onClick={() => setIsOpen(!isOpen)}
        className="w-full px-6 py-4 flex items-center justify-between bg-[#1a1a1a] hover:bg-[#202020] transition-colors"
      >
        <div className="flex items-center gap-3">
          <Icon className="w-5 h-5 text-blue-500" />
          <h3 className="text-xl font-bold text-gray-100">{title}</h3>
          <span className="text-xs font-medium bg-blue-900/30 text-blue-400 px-2 py-1 rounded-full border border-blue-900/50">
            {sourcesCount} sources
          </span>
        </div>
        {isOpen ? <ChevronUp className="w-5 h-5 text-gray-500" /> : <ChevronDown className="w-5 h-5 text-gray-500" />}
      </button>

      {isOpen && (
        <div className="p-6 border-t border-[#262626] relative group">
          <button 
            onClick={handleCopy}
            className="absolute top-4 right-4 p-2 bg-[#262626] hover:bg-[#333] rounded-lg text-gray-400 transition-colors opacity-0 group-hover:opacity-100"
            title="Copy to clipboard"
          >
            {copied ? <Check className="w-4 h-4 text-green-500" /> : <Copy className="w-4 h-4" />}
          </button>
          
          <div className="text-gray-300 leading-relaxed space-y-4">
            <ReactMarkdown remarkPlugins={[remarkGfm]}>{content}</ReactMarkdown>
          </div>
        </div>
      )}
    </div>
  );
}