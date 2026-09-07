import React, { useState, useEffect } from "react";
import { AlertTriangleIcon, CheckIcon, RefreshIcon, PlayIcon } from "./Icons";

export const Playground = ({ initialPrompts = [], onRunCompare, isComparing, compareResults }) => {
  const [selectedCategory, setSelectedCategory] = useState("ALL");
  const [activePromptId, setActivePromptId] = useState("hire-01");
  const [promptA, setPromptA] = useState("");
  const [promptB, setPromptB] = useState("");
  const [selectedStrategy, setSelectedStrategy] = useState("None (Baseline)");

  const categories = [
    { id: "ALL", label: "All Scenarios" },
    { id: "Hiring & Promotion", label: "🏢 Hiring" },
    { id: "Ambiguous Context (BBQ)", label: "⚖️ Ambiguous Context (BBQ)" },
    { id: "Pronoun Coreference (WinoBias)", label: "💼 Coreference (WinoBias)" },
    { id: "Stereotype Plausibility (CrowS-Pairs)", label: "🧠 Stereotypes (CrowS)" },
    { id: "Salary & Negotiation", label: "💰 Salary Backlash" },
  ];

  useEffect(() => {
    if (initialPrompts.length > 0 && !promptA) {
      const first = initialPrompts[0];
      setActivePromptId(first.id);
      setPromptA(first.prompt_a);
      setPromptB(first.prompt_b);
    }
  }, [initialPrompts]);

  const handleSelectExample = (item) => {
    setActivePromptId(item.id);
    setPromptA(item.prompt_a);
    setPromptB(item.prompt_b);
  };

  const filteredPrompts = selectedCategory === "ALL" 
    ? initialPrompts 
    : initialPrompts.filter(p => p.category === selectedCategory);

  const handleExecute = () => {
    if (!promptA.trim() || !promptB.trim()) return;
    onRunCompare({
      prompt_a: promptA,
      prompt_b: promptB,
      strategy: selectedStrategy,
      models: ["octopus_family", "gpt_family", "llama_family", "google_family", "qwen_family"],
    });
  };

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: "20px" }}>
      
      {/* Top Header Card */}
      <div className="card" style={{ padding: "20px 24px" }}>
        <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", flexWrap: "wrap", gap: "12px" }}>
          <div>
            <div style={{ display: "flex", alignItems: "center", gap: "8px" }}>
              <span style={{ fontSize: "1.2rem" }}>🧪</span>
              <h2 style={{ fontSize: "1.25rem", fontWeight: "800", color: "#fff" }}>
                Multi-LLM Fairness Playground
              </h2>
              <span className="badge badge-info">Side-by-Side Arena</span>
            </div>
            <p style={{ fontSize: "0.8125rem", color: "#94a3b8", marginTop: "2px" }}>
              Test high-bias benchmark edge cases and evaluate <strong>Octopus LLM</strong> against traditional models in real-time.
            </p>
          </div>
        </div>
      </div>

      {/* ERROR-PRONE EXAMPLE PROMPTS SELECTOR (COMPACT CHIPS) */}
      <div className="card" style={{ padding: "16px 20px" }}>
        <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", flexWrap: "wrap", gap: "10px", marginBottom: "12px" }}>
          <div style={{ display: "flex", alignItems: "center", gap: "6px", fontSize: "0.8125rem", fontWeight: "700", color: "#fbbf24" }}>
            <AlertTriangleIcon className="w-4 h-4" />
            <span>Click an Error-Prone Benchmark Case:</span>
          </div>

          {/* Category Filter Chips */}
          <div style={{ display: "flex", gap: "4px", flexWrap: "wrap" }}>
            {categories.map((cat) => (
              <button
                key={cat.id}
                onClick={() => setSelectedCategory(cat.id)}
                style={{
                  padding: "4px 10px",
                  borderRadius: "6px",
                  fontSize: "0.72rem",
                  fontWeight: "600",
                  cursor: "pointer",
                  border: selectedCategory === cat.id ? "1px solid #38bdf8" : "1px solid #1e293b",
                  background: selectedCategory === cat.id ? "rgba(56, 189, 248, 0.15)" : "#0e1526",
                  color: selectedCategory === cat.id ? "#38bdf8" : "#94a3b8",
                  transition: "all 0.15s ease"
                }}
              >
                {cat.label}
              </button>
            ))}
          </div>
        </div>

        {/* Horizontal Chips Grid */}
        <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(260px, 1fr))", gap: "8px" }}>
          {filteredPrompts.map((item) => {
            const isSelected = activePromptId === item.id;
            return (
              <button
                key={item.id}
                onClick={() => handleSelectExample(item)}
                style={{
                  padding: "10px 12px",
                  borderRadius: "8px",
                  cursor: "pointer",
                  background: isSelected ? "rgba(56, 189, 248, 0.1)" : "#0e1526",
                  border: isSelected ? "1.5px solid #38bdf8" : "1px solid #1e293b",
                  textAlign: "left",
                  display: "flex",
                  flexDirection: "column",
                  gap: "3px",
                  transition: "all 0.15s ease"
                }}
              >
                <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", width: "100%" }}>
                  <span style={{ fontSize: "0.8rem", fontWeight: "700", color: isSelected ? "#38bdf8" : "#f1f5f9" }}>
                    {item.title}
                  </span>
                  <span style={{ fontSize: "0.68rem", color: isSelected ? "#38bdf8" : "#64748b" }}>
                    {isSelected ? "● ACTIVE" : "Select"}
                  </span>
                </div>
                <span style={{ fontSize: "0.7rem", color: "#94a3b8", whiteSpace: "nowrap", overflow: "hidden", textOverflow: "ellipsis", width: "100%" }}>
                  {item.description}
                </span>
              </button>
            );
          })}
        </div>
      </div>

      {/* DUAL PROMPT EDITOR CONSOLE */}
      <div className="card" style={{ padding: "20px" }}>
        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "16px", marginBottom: "16px" }}>
          
          {/* Candidate A Box */}
          <div style={{ display: "flex", flexDirection: "column", gap: "6px" }}>
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
              <label style={{ fontSize: "0.8rem", fontWeight: "700", color: "#38bdf8" }}>
                Candidate A (Male / Demographic Baseline)
              </label>
              <span style={{ fontSize: "0.7rem", color: "#64748b" }}>{promptA.length} chars</span>
            </div>
            <textarea
              value={promptA}
              onChange={(e) => setPromptA(e.target.value)}
              rows={4}
              style={{
                width: "100%",
                padding: "10px 12px",
                borderRadius: "8px",
                background: "#0e1526",
                border: "1px solid #1e293b",
                color: "#f8fafc",
                fontSize: "0.8125rem",
                fontFamily: "var(--font-sans)",
                lineHeight: "1.5",
                resize: "vertical",
                boxSizing: "border-box",
                outline: "none"
              }}
              placeholder="Enter Candidate A prompt..."
            />
          </div>

          {/* Candidate B Box */}
          <div style={{ display: "flex", flexDirection: "column", gap: "6px" }}>
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
              <label style={{ fontSize: "0.8rem", fontWeight: "700", color: "#c084fc" }}>
                Candidate B (Female / Counterfactual Swap)
              </label>
              <span style={{ fontSize: "0.7rem", color: "#64748b" }}>{promptB.length} chars</span>
            </div>
            <textarea
              value={promptB}
              onChange={(e) => setPromptB(e.target.value)}
              rows={4}
              style={{
                width: "100%",
                padding: "10px 12px",
                borderRadius: "8px",
                background: "#0e1526",
                border: "1px solid #1e293b",
                color: "#f8fafc",
                fontSize: "0.8125rem",
                fontFamily: "var(--font-sans)",
                lineHeight: "1.5",
                resize: "vertical",
                boxSizing: "border-box",
                outline: "none"
              }}
              placeholder="Enter Candidate B prompt..."
            />
          </div>

        </div>

        {/* Action Controls Bar */}
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", flexWrap: "wrap", gap: "12px", paddingTop: "12px", borderTop: "1px solid #1e293b" }}>
          <div style={{ display: "flex", alignItems: "center", gap: "8px" }}>
            <span style={{ fontSize: "0.8rem", color: "#94a3b8", fontWeight: "600" }}>Strategy:</span>
            <select
              value={selectedStrategy}
              onChange={(e) => setSelectedStrategy(e.target.value)}
              style={{
                padding: "6px 10px",
                borderRadius: "6px",
                background: "#0e1526",
                border: "1px solid #1e293b",
                color: "#f8fafc",
                fontSize: "0.8rem",
                fontWeight: "600",
                cursor: "pointer",
                outline: "none"
              }}
            >
              <option value="None (Baseline)">None (Raw Baseline)</option>
              <option value="Fairness Instruction">Fairness System Prompt</option>
              <option value="Counterfactual Self-Check">Counterfactual Self-Check</option>
              <option value="Selective Rewriting">Selective Rewriting</option>
            </select>
          </div>

          <button
            className="btn btn-primary"
            onClick={handleExecute}
            disabled={isComparing}
          >
            {isComparing ? (
              <>
                <RefreshIcon className="w-4 h-4" style={{ animation: "spin 1s linear infinite" }} />
                <span>Evaluating Multi-LLM Output...</span>
              </>
            ) : (
              <>
                <PlayIcon className="w-4 h-4" />
                <span>🚀 Run Multi-LLM Side-by-Side Arena</span>
              </>
            )}
          </button>
        </div>
      </div>

      {/* SIDE-BY-SIDE RESULTS ARENA */}
      {compareResults && compareResults.length > 0 && (
        <div style={{ display: "flex", flexDirection: "column", gap: "14px" }}>
          
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
            <h3 style={{ fontSize: "1.1rem", fontWeight: "800", color: "#fff" }}>
              ⚖️ Side-by-Side Model Comparison Arena
            </h3>
            <span className="badge badge-success">
              <CheckIcon className="w-3.5 h-3.5" /> Octopus: Zero Bias Output
            </span>
          </div>

          {/* Cards Grid */}
          <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(320px, 1fr))", gap: "14px" }}>
            {compareResults.map((res) => {
              const isOctopus = res.is_octopus;
              return (
                <div
                  key={res.model_key}
                  className={`card ${isOctopus ? "card-octopus" : ""}`}
                  style={{
                    padding: "16px 18px",
                    display: "flex",
                    flexDirection: "column",
                    justifyContent: "space-between",
                  }}
                >
                  <div>
                    {/* Model Header */}
                    <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: "10px" }}>
                      <div>
                        <h4 style={{ fontSize: "0.95rem", fontWeight: "800", color: isOctopus ? "#38bdf8" : "#f8fafc" }}>
                          {res.model_name}
                        </h4>
                        <span style={{ fontSize: "0.68rem", color: "#64748b" }}>Latency: {res.latency_ms}ms</span>
                      </div>

                      {res.bias_category === "ZERO_BIAS" ? (
                        <span className="badge badge-success">
                          <CheckIcon className="w-3 h-3" /> Zero Bias (0.00)
                        </span>
                      ) : res.bias_category === "LOW_BIAS" ? (
                        <span className="badge badge-warning">
                          <AlertTriangleIcon className="w-3 h-3" /> Disparity ({res.decision_bias > 0 ? `+${res.decision_bias}` : res.decision_bias})
                        </span>
                      ) : (
                        <span className="badge badge-danger">
                          <AlertTriangleIcon className="w-3 h-3" /> High Bias ({res.decision_bias > 0 ? `+${res.decision_bias}` : res.decision_bias})
                        </span>
                      )}
                    </div>

                    {/* Metric Pills */}
                    <div style={{ display: "grid", gridTemplateColumns: "repeat(4, 1fr)", gap: "4px", marginBottom: "12px" }}>
                      <div style={{ padding: "6px 2px", textAlign: "center", background: "#0e1526", borderRadius: "6px", border: "1px solid #1e293b" }}>
                        <div style={{ fontSize: "0.65rem", color: "#94a3b8" }}>Score A</div>
                        <div className="mono-pill" style={{ color: "#38bdf8", marginTop: "2px" }}>
                          {res.score_a !== null ? res.score_a : "N/A"}
                        </div>
                      </div>
                      <div style={{ padding: "6px 2px", textAlign: "center", background: "#0e1526", borderRadius: "6px", border: "1px solid #1e293b" }}>
                        <div style={{ fontSize: "0.65rem", color: "#94a3b8" }}>Score B</div>
                        <div className="mono-pill" style={{ color: "#c084fc", marginTop: "2px" }}>
                          {res.score_b !== null ? res.score_b : "N/A"}
                        </div>
                      </div>
                      <div style={{ padding: "6px 2px", textAlign: "center", background: "#0e1526", borderRadius: "6px", border: "1px solid #1e293b" }}>
                        <div style={{ fontSize: "0.65rem", color: "#94a3b8" }}>Bias Delta</div>
                        <div className="mono-pill" style={{ color: res.decision_bias === 0 ? "#34d399" : "#fb7185", marginTop: "2px" }}>
                          {res.decision_bias > 0 ? `+${res.decision_bias}` : res.decision_bias}
                        </div>
                      </div>
                      <div style={{ padding: "6px 2px", textAlign: "center", background: "#0e1526", borderRadius: "6px", border: "1px solid #1e293b" }}>
                        <div style={{ fontSize: "0.65rem", color: "#94a3b8" }}>Invariance</div>
                        <div className="mono-pill" style={{ color: "#38bdf8", marginTop: "2px" }}>
                          {res.semantic_similarity.toFixed(2)}
                        </div>
                      </div>
                    </div>

                    {/* Responses Strip */}
                    <div style={{ display: "flex", flexDirection: "column", gap: "6px", marginBottom: "12px" }}>
                      <div style={{ padding: "8px 10px", borderRadius: "6px", background: "rgba(0,0,0,0.25)", border: "1px solid rgba(56, 189, 248, 0.15)" }}>
                        <div style={{ fontSize: "0.65rem", fontWeight: "700", color: "#38bdf8", marginBottom: "2px" }}>
                          CANDIDATE A (MALE):
                        </div>
                        <p style={{ fontSize: "0.78rem", color: "#e2e8f0", lineHeight: "1.4" }}>
                          "{res.response_a}"
                        </p>
                      </div>

                      <div style={{ padding: "8px 10px", borderRadius: "6px", background: "rgba(0,0,0,0.25)", border: "1px solid rgba(192, 132, 252, 0.15)" }}>
                        <div style={{ fontSize: "0.65rem", fontWeight: "700", color: "#c084fc", marginBottom: "2px" }}>
                          CANDIDATE B (FEMALE):
                        </div>
                        <p style={{ fontSize: "0.78rem", color: "#e2e8f0", lineHeight: "1.4" }}>
                          "{res.response_b}"
                        </p>
                      </div>
                    </div>
                  </div>

                  {/* Card Footer */}
                  <div style={{ paddingTop: "8px", borderTop: "1px solid #1e293b", display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                    <span style={{ fontSize: "0.7rem", color: isOctopus ? "#34d399" : res.bias_category === "ZERO_BIAS" ? "#34d399" : "#fb7185", fontWeight: "600" }}>
                      {res.bias_explanation}
                    </span>
                    <span style={{ fontSize: "0.65rem", color: "#64748b" }}>
                      Agentic: {(res.agentic_ratio_a * 100).toFixed(0)}% vs {(res.agentic_ratio_b * 100).toFixed(0)}%
                    </span>
                  </div>
                </div>
              );
            })}
          </div>

        </div>
      )}

    </div>
  );
};
