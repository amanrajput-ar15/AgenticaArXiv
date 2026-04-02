export default function ReportSkeleton() {
  const sections = ["Literature Review", "Methods Analysis", "Results Analysis", "Critical Analysis", "Research Synthesis"];
  
  return (
    <div className="mt-8 space-y-4">
      <div className="flex flex-col items-center justify-center py-8 text-blue-400">
        <div className="w-12 h-12 border-4 border-blue-900/30 border-t-blue-500 rounded-full animate-spin mb-4"></div>
        <p className="animate-pulse">Agents are analyzing papers...</p>
      </div>
      
      {sections.map((title, i) => (
        <div key={i} className="bg-[#171717] border border-[#262626] p-6 rounded-xl opacity-70">
          <div className="h-6 w-1/3 bg-[#262626] rounded animate-pulse mb-4"></div>
          <div className="space-y-2">
            <div className="h-4 w-full bg-[#262626] rounded animate-pulse"></div>
            <div className="h-4 w-5/6 bg-[#262626] rounded animate-pulse"></div>
            <div className="h-4 w-4/6 bg-[#262626] rounded animate-pulse"></div>
          </div>
        </div>
      ))}
    </div>
  );
}