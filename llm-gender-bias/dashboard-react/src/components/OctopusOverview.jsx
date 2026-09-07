import React from "react";
import { SparklesIcon, CheckIcon, LayersIcon } from "./Icons";

export const OctopusOverview = ({ onTryPlayground }) => {
  const kpiStats = [
    { label: "CrowS-Pairs Disparity", value: "0.00", badge: "Zero Bias", note: "Exact plausibility parity", color: "#10b981" },
    { label: "BBQ Disambiguation", value: "100%", badge: "State-of-the-Art", note: "Zero ambiguous stereotyping", color: "#38bdf8" },
    { label: "WinoBias Coreference", value: "0.00", badge: "Invariant", note: "0% occupational bias", color: "#a855f7" },
    { label: "Utility Retention", value: "98.5%", badge: "High Quality", note: "+12.4% vs post-edit baseline", color: "#3b82f6" },
  ];

  const pipelineStages = [
    {
      step: "01",
      title: "Causal Demographic Normalization",
      desc: "Isolates gender-loaded pronouns and demographic tokens. Builds canonical counterfactual representations in latent feature space.",
      tag: "Pre-Inference",
    },
    {
      step: "02",
      title: "Invariance Backbone Core",
      desc: "Evaluates factual qualifications, technical skills, and context independently of gender conditioning, eliminating implicit associations.",
      tag: "Latent Core",
    },
    {
      step: "03",
      title: "Calibrated Output Synthesis",
      desc: "Synthesizes high-utility responses. Automatically enforces objective neutrality ('Cannot be determined') under ambiguous context.",
      tag: "Post-Inference",
    },
  ];

  const models = [
    { name: "🐙 Octopus AI", crows: "0.00", bbq: "100%", wino: "0.00", utility: "98.5%", status: "SOTA Leader", isOctopus: true },
    { name: "GPT-4 / GPT-3.5", crows: "0.17", bbq: "40.0%", wino: "1.75", utility: "88.2%", status: "Coreference Bias", isOctopus: false },
    { name: "Llama 3.3 70B", crows: "0.00", bbq: "0.0%", wino: "0.00", utility: "91.0%", status: "BBQ Blindspot", isOctopus: false },
    { name: "Google Gemini 2.5", crows: "0.00", bbq: "0.0%", wino: "0.00", utility: "92.4%", status: "BBQ Blindspot", isOctopus: false },
    { name: "Qwen 2.5 32B", crows: "1.50", bbq: "80.0%", wino: "1.00", utility: "86.5%", status: "High Stereotyping", isOctopus: false },
  ];

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: "24px" }}>
      
      {/* Hero Banner */}
      <div className="card card-octopus" style={{ padding: "32px", position: "relative" }}>
        <div style={{ maxWidth: "880px" }}>
          <div style={{ display: "inline-flex", alignItems: "center", gap: "6px", padding: "4px 10px", borderRadius: "6px", background: "rgba(56, 189, 248, 0.15)", border: "1px solid rgba(56, 189, 248, 0.3)", marginBottom: "14px" }}>
            <SparklesIcon className="w-3.5 h-3.5" style={{ color: "#38bdf8" }} />
            <span style={{ fontSize: "0.75rem", fontWeight: "700", color: "#38bdf8", textTransform: "uppercase", letterSpacing: "0.05em" }}>
              Causal Architecture Flagship
            </span>
          </div>

          <h1 style={{ fontSize: "2.1rem", fontWeight: "800", color: "#fff", lineHeight: "1.25", marginBottom: "12px" }}>
            Octopus: The First Truly <span style={{ color: "#38bdf8" }}>Bias-Free & Causal LLM</span>
          </h1>

          <p style={{ fontSize: "0.95rem", color: "#94a3b8", lineHeight: "1.6", marginBottom: "24px" }}>
            Traditional LLMs consistently exhibit demographic disparities across counterfactual name swaps and collapse into stereotyping under uninformative contexts. 
            <strong> Octopus</strong> achieves mathematical invariance across <strong>CrowS-Pairs</strong>, <strong>BBQ</strong>, and <strong>WinoBias</strong> while maintaining <strong>98.5% utility retention</strong>.
          </p>

          <div style={{ display: "flex", gap: "12px", flexWrap: "wrap" }}>
            <button className="btn btn-primary" onClick={onTryPlayground}>
              <SparklesIcon className="w-4 h-4" />
              <span>Open Side-by-Side Playground</span>
            </button>
            <a href="#pipeline" className="btn btn-secondary" style={{ textDecoration: "none" }}>
              <LayersIcon className="w-4 h-4" />
              <span>View 3-Stage Pipeline</span>
            </a>
          </div>
        </div>
      </div>

      {/* KPI 4-Card Row */}
      <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(240px, 1fr))", gap: "16px" }}>
        {kpiStats.map((kpi, idx) => (
          <div key={idx} className="card" style={{ padding: "20px", display: "flex", flexDirection: "column", justifyContent: "space-between", borderTop: `3px solid ${kpi.color}` }}>
            <div>
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "10px" }}>
                <span style={{ fontSize: "0.8125rem", fontWeight: "600", color: "#94a3b8" }}>{kpi.label}</span>
                <span className="badge" style={{ background: "rgba(255,255,255,0.06)", color: kpi.color }}>
                  {kpi.badge}
                </span>
              </div>
              <div style={{ fontSize: "2.25rem", fontWeight: "800", color: kpi.color, fontFamily: "var(--font-mono)", lineHeight: "1", marginBottom: "6px" }}>
                {kpi.value}
              </div>
            </div>
            <span style={{ fontSize: "0.75rem", color: "#64748b" }}>{kpi.note}</span>
          </div>
        ))}
      </div>

      {/* 3-Stage Pipeline Architecture */}
      <div id="pipeline" className="card" style={{ padding: "28px" }}>
        <div style={{ marginBottom: "20px" }}>
          <h2 style={{ fontSize: "1.25rem", fontWeight: "700", color: "#fff", marginBottom: "4px" }}>
            ⚡ 3-Stage Causal Normalization Architecture
          </h2>
          <p style={{ fontSize: "0.85rem", color: "#94a3b8" }}>
            How Octopus achieves guaranteed counterfactual invariance and eliminates hallucinated demographic associations.
          </p>
        </div>

        <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(280px, 1fr))", gap: "16px" }}>
          {pipelineStages.map((stage) => (
            <div key={stage.step} style={{ padding: "20px", borderRadius: "10px", background: "var(--bg-surface)", border: "1px solid var(--border-subtle)" }}>
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "12px" }}>
                <span style={{ fontSize: "0.8125rem", fontWeight: "800", color: "#38bdf8", fontFamily: "var(--font-mono)" }}>
                  STAGE {stage.step}
                </span>
                <span className="badge badge-info">{stage.tag}</span>
              </div>
              <h3 style={{ fontSize: "1rem", fontWeight: "700", color: "#f8fafc", marginBottom: "8px" }}>
                {stage.title}
              </h3>
              <p style={{ fontSize: "0.8125rem", color: "#94a3b8", lineHeight: "1.5" }}>
                {stage.desc}
              </p>
            </div>
          ))}
        </div>
      </div>

      {/* Head-to-Head Comparison Table */}
      <div className="card" style={{ padding: "28px" }}>
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "16px", flexWrap: "wrap", gap: "12px" }}>
          <div>
            <h2 style={{ fontSize: "1.25rem", fontWeight: "700", color: "#fff", marginBottom: "4px" }}>
              🏆 Head-to-Head Multi-LLM Benchmark Matrix
            </h2>
            <p style={{ fontSize: "0.85rem", color: "#94a3b8" }}>
              Independent evaluation across CrowS-Pairs, BBQ Disambiguation, and WinoBias Coreference.
            </p>
          </div>
          <span className="badge badge-success">
            <CheckIcon className="w-3.5 h-3.5" /> Audited & Verified
          </span>
        </div>

        <div style={{ overflowX: "auto" }}>
          <table style={{ width: "100%", borderCollapse: "collapse", textAlign: "left", fontSize: "0.875rem" }}>
            <thead>
              <tr style={{ borderBottom: "1px solid var(--border-subtle)", color: "#94a3b8", background: "var(--bg-surface)" }}>
                <th style={{ padding: "12px 16px", fontWeight: "600" }}>Model Family</th>
                <th style={{ padding: "12px 16px", fontWeight: "600" }}>CrowS-Pairs Bias</th>
                <th style={{ padding: "12px 16px", fontWeight: "600" }}>BBQ Unbiased Rate</th>
                <th style={{ padding: "12px 16px", fontWeight: "600" }}>WinoBias Bias</th>
                <th style={{ padding: "12px 16px", fontWeight: "600" }}>Utility Retention</th>
                <th style={{ padding: "12px 16px", fontWeight: "600" }}>Evaluation Verdict</th>
              </tr>
            </thead>
            <tbody>
              {models.map((m, idx) => (
                <tr
                  key={idx}
                  style={{
                    borderBottom: "1px solid var(--border-subtle)",
                    background: m.isOctopus ? "rgba(56, 189, 248, 0.06)" : "transparent",
                  }}
                >
                  <td style={{ padding: "14px 16px", fontWeight: m.isOctopus ? "700" : "500", color: m.isOctopus ? "#38bdf8" : "#f8fafc" }}>
                    {m.name}
                  </td>
                  <td style={{ padding: "14px 16px", fontFamily: "var(--font-mono)", color: m.crows === "0.00" ? "#34d399" : "#fb7185", fontWeight: "600" }}>
                    {m.crows}
                  </td>
                  <td style={{ padding: "14px 16px", fontFamily: "var(--font-mono)", color: m.bbq === "100%" ? "#34d399" : m.bbq === "80.0%" ? "#fbbf24" : "#fb7185", fontWeight: "600" }}>
                    {m.bbq}
                  </td>
                  <td style={{ padding: "14px 16px", fontFamily: "var(--font-mono)", color: m.wino === "0.00" ? "#34d399" : "#fb7185", fontWeight: "600" }}>
                    {m.wino}
                  </td>
                  <td style={{ padding: "14px 16px", fontFamily: "var(--font-mono)", color: "#94a3b8" }}>
                    {m.utility}
                  </td>
                  <td style={{ padding: "14px 16px" }}>
                    {m.isOctopus ? (
                      <span className="badge badge-success">Zero Bias SOTA</span>
                    ) : m.status.includes("Blindspot") ? (
                      <span className="badge badge-danger">{m.status}</span>
                    ) : (
                      <span className="badge badge-warning">{m.status}</span>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

    </div>
  );
};
