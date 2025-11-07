import React, {useState} from "react";
export default function App(){
  const [q,setQ] = useState("");
  const [res,setRes] = useState(null);
  async function submit(){
    const r = await fetch((process.env.REACT_APP_API_URL || "") + "/recommend", {
      method:"POST",
      headers: {"Content-Type":"application/json"},
      body: JSON.stringify({query:q, max_results:10})
    });
    const j = await r.json();
    setRes(j.recommendations || []);
  }
  return (<div className="p-4">
    <h1>SHL Recommender</h1>
    <textarea value={q} onChange={e=>setQ(e.target.value)} rows={6} cols={80}/>
    <div><button onClick={submit}>Recommend</button></div>
    <table>
      <thead><tr><th>Name</th><th>URL</th><th>Type</th><th>Score</th></tr></thead>
      <tbody>
        {res && res.map((r,i)=>(
          <tr key={i}><td>{r.assessment_name}</td><td><a href={r.assessment_url} target="_blank" rel="noreferrer">{r.assessment_url}</a></td><td>{r.test_type}</td><td>{r.score.toFixed(3)}</td></tr>
        ))}
      </tbody>
    </table>
  </div>);
}
