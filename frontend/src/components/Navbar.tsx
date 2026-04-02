"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useEffect, useState } from "react";
import { AgenticApi } from "@/lib/api";
import { Database, Server } from "lucide-react";

export default function Navbar() {
  const pathname = usePathname();
  const [status, setStatus] = useState<string>("Checking...");

  useEffect(() => {
    const checkBackend = async () => {
      try {
        const data = await AgenticApi.checkStatus();
        setStatus(`${data.vector_store.total_chunks} chunks`);
      } catch (error) {
        setStatus("Offline");
      }
    };
    checkBackend();
    // Poll every 30 seconds
    const interval = setInterval(checkBackend, 30000);
    return () => clearInterval(interval);
  }, []);

  const navLinks = [
    { href: "/ingest", label: "Ingest" },
    { href: "/research", label: "Research" },
  ];

  return (
    <nav className="fixed top-0 w-full bg-[#0a0a0a]/80 backdrop-blur-md border-b border-[#262626] z-50">
      <div className="max-w-6xl mx-auto px-6 h-16 flex items-center justify-between">
        <div className="flex items-center gap-8">
          <Link href="/" className="text-xl font-bold tracking-tight flex items-center gap-2">
            <span className="bg-blue-600 text-white px-2 py-0.5 rounded">A</span>genticArXiv
          </Link>
          <div className="hidden md:flex items-center gap-1">
            {navLinks.map((link) => (
              <Link
                key={link.href}
                href={link.href}
                className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                  pathname === link.href ? "bg-[#262626] text-white" : "text-gray-400 hover:text-white hover:bg-[#1a1a1a]"
                }`}
              >
                {link.label}
              </Link>
            ))}
          </div>
        </div>

        <div className={`flex items-center gap-2 px-3 py-1.5 rounded-full text-xs font-medium border ${
          status === "Offline" ? "bg-red-900/20 text-red-400 border-red-900/50" : "bg-[#171717] text-gray-300 border-[#262626]"
        }`}>
          {status === "Offline" ? <Server className="w-3.5 h-3.5" /> : <Database className="w-3.5 h-3.5 text-blue-500" />}
          {status}
        </div>
      </div>
    </nav>
  );
}