
import React,{useState} from "react";
import {createRoot} from "react-dom/client";
import {Sparkles, Users, Target, MessageCircle, ArrowRight, CheckCircle2, Brain, Briefcase, ChevronRight} from "lucide-react";
import "./style.css";

const API="http://127.0.0.1:8000/api";

const sample={name:"Teja",branch:"CSE - AI & ML",year:"2nd Year",skills:["Python","Machine Learning","Java"],interests:["Generative AI","LLMs","Full Stack"],career_goal:"AI Engineer",industry:"AI",experience:"Beginner",needs:["Internship guidance","Project guidance"]};

function App(){
 const [student,setStudent]=useState(sample),[matches,setMatches]=useState([]),[tab,setTab]=useState("home"),[selected,setSelected]=useState(null),[roadmap,setRoadmap]=useState(null),[toast,setToast]=useState("");
 const [loading,setLoading]=useState(false);
 const match=async()=>{setLoading(true);let r=await fetch(API+"/match",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(student)});setMatches(await r.json());setTab("matches");setLoading(false)};
 const getRoadmap=async()=>{let r=await fetch(API+"/roadmap",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(student)});setRoadmap(await r.json());setTab("roadmap")};
 const request=async id=>{await fetch(API+"/request",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({student_name:student.name,mentor_id:id,message:"I'd like guidance on my career path and projects."})});setToast("Mentorship request sent");setTimeout(()=>setToast(""),2200)};
 return <div>
  <header><div className="brand"><div className="logo"><Sparkles size={20}/></div><b>MentorMatch</b><span>AI</span></div><nav><button onClick={()=>setTab("home")}>Home</button><button onClick={()=>setTab("matches")}>Find Mentors</button><button onClick={getRoadmap}>Career Roadmap</button></nav><div className="profile">{student.name[0]}</div></header>
  <main>
   {tab==="home"&&<section className="hero"><div><div className="pill"><Sparkles size={14}/> AI-powered mentorship</div><h1>Meet the alumni<br/><em>who can move you forward.</em></h1><p className="lead">Personalized mentor matching based on your skills, goals, interests and career direction.</p><button className="primary" onClick={match}>{loading?"Finding matches…":"Find my mentors"} <ArrowRight size={18}/></button><div className="stats"><div><b>AI Match</b><small>Skill + goal based</small></div><div><b>Verified alumni</b><small>Career experience</small></div><div><b>1:1 guidance</b><small>Structured growth</small></div></div></div><div className="hero-card"><div className="card-top"><Brain size={20}/><b>AI Profile</b><span>Ready</span></div><div className="profile-box"><div className="avatar big">{student.name[0]}</div><div><h3>{student.name}</h3><p>{student.branch} · {student.year}</p></div></div><div className="chips">{student.interests.map(x=><i key={x}>{x}</i>)}</div><div className="goal"><Target size={18}/><div><small>Career goal</small><b>{student.career_goal}</b></div></div></div></section>}
   {tab==="matches"&&<section className="page"><div className="section-head"><div><div className="pill">AI matching engine</div><h2>Your mentor matches</h2><p>Matches are explained so you can understand why each mentor fits.</p></div><button className="outline" onClick={match}>Refresh matches</button></div><div className="match-grid">{matches.map((m,i)=><article className="mentor" key={m.id}><div className="mentor-head"><div className="avatar">{m.name[0]}</div><div><h3>{m.name}</h3><p>{m.role} · {m.company}</p></div><div className="score">{m.score}%<small>match</small></div></div><div className="chips">{m.skills.slice(0,4).map(x=><i key={x}>{x}</i>)}</div><div className="why"><b>Why this mentor?</b>{m.reasons.map(x=><p key={x}><CheckCircle2 size={15}/>{x}</p>)}</div><button className="primary full" onClick={()=>{setSelected(m);request(m.id)}}>Request mentorship <ArrowRight size={16}/></button></article>)}</div>{!matches.length&&<div className="empty">Click “Find my mentors” to generate personalized matches.</div>}</section>}
   {tab==="roadmap"&&<section className="page"><div className="section-head"><div><div className="pill">AI career planner</div><h2>Your mentorship roadmap</h2><p>A practical 8-week path toward <b>{student.career_goal}</b>.</p></div></div><div className="roadmap">{(roadmap?.weeks||[]).map((w,i)=><div className="step" key={w.title}><div className="num">{i+1}</div><div><span>{w.duration}</span><h3>{w.title}</h3>{w.tasks.map(t=><p key={t}><CheckCircle2 size={15}/>{t}</p>)}</div></div>)}</div></section>}
  </main>
  {toast&&<div className="toast"><CheckCircle2 size={18}/>{toast}</div>}
  <footer><span>MentorMatch AI · Hackathon MVP</span><span>Student → Match → Mentor → Growth</span></footer>
 </div>
}
createRoot(document.getElementById("root")).render(<App/>);
