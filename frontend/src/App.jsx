import { useState } from "react";

const apiBase = import.meta.env.VITE_API_URL || "";

async function predictPrice(productName) {
  const url = apiBase ? `${apiBase.replace(/\/$/, "")}/predict` : "/api/predict";
  const res = await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ product_name: productName }),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    const d = err.detail;
    const message =
      typeof d === "string"
        ? d
        : Array.isArray(d) && d[0]?.msg
          ? d.map((x) => x.msg).join("; ")
          : res.statusText;
    throw new Error(message);
  }
  return res.json();
}

export default function App() {
  const [name, setName] = useState("");
  const [price, setPrice] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  async function onSubmit(e) {
    e.preventDefault();
    setError(null);
    setPrice(null);
    const trimmed = name.trim();
    if (!trimmed) {
      setError("Enter a product name.");
      return;
    }
    setLoading(true);
    try {
      const data = await predictPrice(trimmed);
      setPrice(data.price_etb);
    } catch (err) {
      setError(err.message || "Request failed");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div
      style={{
        maxWidth: 520,
        margin: "0 auto",
        padding: "3rem 1.25rem",
      }}
    >
      <h1 style={{ fontSize: "1.75rem", fontWeight: 600, marginBottom: "0.25rem" }}>
        Suggested listing price
      </h1>
      <p style={{ color: "#555", marginTop: 0, marginBottom: "1.75rem" }}>
        Trained on your <code>market_data.csv</code> (text only). Enter a phone listing title.
      </p>

      <form onSubmit={onSubmit}>
        <label htmlFor="product" style={{ display: "block", fontWeight: 500, marginBottom: 6 }}>
          Product name
        </label>
        <input
          id="product"
          value={name}
          onChange={(e) => setName(e.target.value)}
          placeholder="e.g. Samsung Galaxy S21 128 GB"
          style={{
            width: "100%",
            padding: "0.65rem 0.75rem",
            fontSize: "1rem",
            border: "1px solid #ccc",
            borderRadius: 8,
            marginBottom: 12,
          }}
        />
        <button
          type="submit"
          disabled={loading}
          style={{
            padding: "0.6rem 1.1rem",
            fontSize: "1rem",
            borderRadius: 8,
            border: "none",
            background: loading ? "#9a9a9a" : "#2563eb",
            color: "#fff",
            cursor: loading ? "default" : "pointer",
          }}
        >
          {loading ? "Predicting…" : "Get suggested price"}
        </button>
      </form>

      {error && (
        <p style={{ color: "#b91c1c", marginTop: "1.25rem" }} role="alert">
          {error}
        </p>
      )}

      {price != null && (
        <div
          style={{
            marginTop: "1.5rem",
            padding: "1rem 1.25rem",
            background: "#fff",
            borderRadius: 10,
            border: "1px solid #e5e2dc",
          }}
        >
          <div style={{ fontSize: "0.9rem", color: "#555" }}>Suggested price</div>
          <div style={{ fontSize: "1.75rem", fontWeight: 600, marginTop: 4 }}>
            ETB {price.toLocaleString("en-ET", { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
          </div>
        </div>
      )}
    </div>
  );
}
