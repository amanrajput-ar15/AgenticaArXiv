import { FileText, Layers, Hash } from "lucide-react";

interface IngestResultProps {
  papersProcessed: number;
  chunksCreated: number;
}

export default function IngestResult({ papersProcessed, chunksCreated }: IngestResultProps) {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-8 animate-in fade-in slide-in-from-bottom-4">
      <div className="bg-[#171717] border border-green-900/50 p-6 rounded-xl flex items-center gap-4">
        <div className="p-4 bg-green-900/20 rounded-lg text-green-500">
          <FileText className="w-8 h-8" />
        </div>
        <div>
          <p className="text-3xl font-bold text-white">{papersProcessed}</p>
          <p className="text-gray-400 text-sm">Papers Processed</p>
        </div>
      </div>

      <div className="bg-[#171717] border border-blue-900/50 p-6 rounded-xl flex items-center gap-4">
        <div className="p-4 bg-blue-900/20 rounded-lg text-blue-500">
          <Layers className="w-8 h-8" />
        </div>
        <div>
          <p className="text-3xl font-bold text-white">{chunksCreated}</p>
          <p className="text-gray-400 text-sm">Vector Chunks Created</p>
        </div>
      </div>
    </div>
  );
}