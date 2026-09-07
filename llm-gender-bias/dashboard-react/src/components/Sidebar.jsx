import React from "react";
import { BrainIcon, ChartIcon, SparklesIcon, ShieldIcon, SearchIcon, LayersIcon } from "./Icons";

export const Sidebar = ({ activeTab, setActiveTab, apiStatus }) => {
  const navItems = [
    { id: "playground", label: "Live Playground", icon: <SparklesIcon size={16} />, badge: "Side-by-Side" },
    { id: "training", label: "Model Training", icon: <BrainIcon size={16} />, badge: "DPO Telemetry" },
    { id: "octopus", label: "Octopus Architecture", icon: <LayersIcon size={16} /> },
    { id: "benchmarks", label: "3.5K+ Benchmarks", icon: <ChartIcon size={16} />, badge: "5 Datasets" },
    { id: "mitigation", label: "Mitigation Suite", icon: <ShieldIcon size={16} /> },
    { id: "quality", label: "Data Quality Audit", icon: <SearchIcon size={16} /> },
  ];

  return (
    <aside style={{
      width: "250px",
      minWidth: "250px",
      background: "#0d1322",
      borderRight: "1px solid #1e293b",
      display: "flex",
      flexDirection: "column",
      justifyContent: "space-between",
      height: "100vh",
      position: "sticky",
      top: 0,
      padding: "20px 16px",
      boxSizing: "border-box"
    }}>
      {/* Top Brand */}
      <div>
        <div style={{ display: "flex", alignItems: "center", gap: "10px", padding: "0 8px 20px 8px", borderBottom: "1px solid #1e293b", marginBottom: "16px" }}>
          <div style={{
            width: "36px",
            height: "36px",
            borderRadius: "8px",
            background: "linear-gradient(135deg, #0284c7 0%, #a855f7 100%)",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            fontSize: "18px",
            boxShadow: "0 2px 8px rgba(2, 132, 199, 0.4)"
          }}>
            🐙
          </div>
          <div>
            <div style={{ fontSize: "1.05rem", fontWeight: "800", color: "#fff", lineHeight: "1.2" }}>
              Octopus <span style={{ color: "#38bdf8" }}>AI</span>
            </div>
            <div style={{ fontSize: "0.7rem", color: "#64748b" }}>
              Bias-Free LLM Platform
            </div>
          </div>
        </div>

        {/* Navigation Links */}
        <nav style={{ display: "flex", flexDirection: "column", gap: "4px" }}>
          {navItems.map((item) => {
            const isActive = activeTab === item.id;
            return (
              <button
                key={item.id}
                onClick={() => setActiveTab(item.id)}
                style={{
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "space-between",
                  width: "100%",
                  padding: "10px 12px",
                  borderRadius: "8px",
                  border: isActive ? "1px solid #2a3754" : "1px solid transparent",
                  background: isActive ? "#16223b" : "transparent",
                  color: isActive ? "#fff" : "#94a3b8",
                  fontWeight: isActive ? "600" : "500",
                  fontSize: "0.85rem",
                  cursor: "pointer",
                  transition: "all 0.15s ease",
                  textAlign: "left"
                }}
              >
                <div style={{ display: "flex", alignItems: "center", gap: "10px" }}>
                  <span style={{ color: isActive ? "#38bdf8" : "#64748b" }}>{item.icon}</span>
                  <span>{item.label}</span>
                </div>
                {item.badge && (
                  <span style={{
                    fontSize: "0.65rem",
                    padding: "2px 6px",
                    borderRadius: "4px",
                    background: isActive ? "rgba(56, 189, 248, 0.2)" : "rgba(255,255,255,0.06)",
                    color: isActive ? "#38bdf8" : "#64748b",
                    fontWeight: "600"
                  }}>
                    {item.badge}
                  </span>
                )}
              </button>
            );
          })}
        </nav>
      </div>

      {/* Bottom Model Info Card */}
      <div style={{
        padding: "12px",
        borderRadius: "8px",
        background: "#111a2e",
        border: "1px solid #1e293b",
        display: "flex",
        flexDirection: "column",
        gap: "8px"
      }}>
        <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between" }}>
          <span style={{ fontSize: "0.72rem", color: "#64748b", fontWeight: "600" }}>ACTIVE ENGINE</span>
          <span style={{
            fontSize: "0.65rem",
            padding: "2px 6px",
            borderRadius: "4px",
            background: apiStatus === "online" ? "rgba(16, 185, 129, 0.15)" : "rgba(245, 158, 11, 0.15)",
            color: apiStatus === "online" ? "#34d399" : "#fbbf24",
            fontWeight: "700"
          }}>
            {apiStatus === "online" ? "● ONLINE" : "● CLIENT"}
          </span>
        </div>

        <div style={{ fontSize: "0.8rem", color: "#e2e8f0", fontWeight: "600" }}>
          🐙 Octopus-v1-Causal
        </div>
        <div style={{ fontSize: "0.7rem", color: "#34d399" }}>
          ✓ CrowS: 0.00 | BBQ: 100%
        </div>
      </div>
    </aside>
  );
};
