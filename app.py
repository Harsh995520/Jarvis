from datetime import datetime
from urllib.parse import quote

import wikipedia
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field

app = FastAPI(title="JARVIS Web Assistant", version="1.0.0")

PAGE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="theme-color" content="#070b16">
<title>JARVIS — AI Web Assistant</title>
<style>
:root{color-scheme:dark;--bg:#070b16;--panel:#101a2b;--line:#223451;--cyan:#58d9ff;--muted:#9aabc4}
*{box-sizing:border-box}body{margin:0;min-height:100vh;background:radial-gradient(circle at 50% 0%,#122b49 0,#070b16 52%);color:#eef7ff;font:16px Inter,system-ui,Segoe UI,sans-serif;display:flex;justify-content:center;padding:28px 14px}
main{width:min(900px,100%)}header{text-align:center;margin:12px 0 24px}.orb{width:92px;height:92px;border-radius:50%;margin:0 auto 15px;border:1px solid #58d9ff88;box-shadow:0 0 35px #2ebeff55,inset 0 0 24px #2ebeff33;display:grid;place-items:center;color:var(--cyan);font-size:38px;animation:pulse 3s infinite}
@keyframes pulse{50%{box-shadow:0 0 55px #2ebeff88,inset 0 0 30px #2ebeff55}}h1{letter-spacing:7px;margin:0;font-size:clamp(28px,6vw,42px)}.sub{color:var(--muted);margin-top:8px}
.panel{background:#0d1728eF;border:1px solid var(--line);border-radius:20px;overflow:hidden;box-shadow:0 18px 70px #0007}.top{display:flex;justify-content:space-between;align-items:center;padding:15px 18px;border-bottom:1px solid var(--line);color:var(--muted);font-size:13px}.status{color:#8cf0bd}.chat{height:390px;overflow:auto;padding:20px;display:flex;flex-direction:column;gap:14px}.msg{max-width:85%;padding:13px 16px;border-radius:15px;line-height:1.5;white-space:pre-wrap;overflow-wrap:anywhere}.bot{background:#142640;border:1px solid #24496a;align-self:flex-start}.user{background:#07577a;align-self:flex-end}.actions{display:flex;gap:9px;flex-wrap:wrap;padding:0 18px 16px}.chip,button{border:1px solid #2a5473;background:#10243a;color:#c8f2ff;border-radius:999px;padding:9px 13px;cursor:pointer}.chip:hover,button:hover{border-color:var(--cyan);background:#153552}.compose{display:flex;gap:10px;padding:16px;border-top:1px solid var(--line)}input{min-width:0;flex:1;background:#081322;border:1px solid #29415e;color:white;border-radius:12px;padding:14px;font-size:15px;outline:none}input:focus{border-color:var(--cyan)}.send{background:#087ca5;color:white;border:0;border-radius:12px;padding:0 20px}.mic.listening{background:#8a2638;color:white;border-color:#f77}.foot{text-align:center;color:#8193aa;font-size:12px;margin:15px 0}.hint{color:var(--muted);font-size:13px;padding:0 18px 17px}
@media(max-width:540px){.chat{height:55vh}.compose{flex-wrap:wrap}.compose input{flex-basis:100%}.send{flex:1;padding:13px}}
</style>
</head>
<body><main>
<header><div class="orb">✧</div><h1>J.A.R.V.I.S</h1><div class="sub">Just A Rather Very Intelligent System · Web Edition</div></header>
<section class="panel">
<div class="top"><span>ASSISTANT CONSOLE</span><span class="status" id="status">● ONLINE</span></div>
<div class="chat" id="chat" aria-live="polite"><div class="msg bot">Hello! I am JARVIS. You can type a command or use the microphone. Try “What time is it?”, “Wikipedia artificial intelligence”, “Open YouTube”, or “Open Google”.</div></div>
<div class="actions"><button class="chip" data-command="What time is it?">Time</button><button class="chip" data-command="Wikipedia artificial intelligence">Wikipedia</button><button class="chip" data-command="Open Google">Google</button><button class="chip" data-command="Open YouTube">YouTube</button></div>
<form class="compose" id="form"><input id="command" maxlength="500" autocomplete="off" placeholder="Type a command for JARVIS…" aria-label="Command"><button type="button" class="mic" id="mic" title="Speak command">🎙</button><button class="send" type="submit">Send</button></form>
<div class="hint">Voice input depends on browser support and microphone permission. Speech output uses your browser. This public demo does not access your computer files or send emails.</div>
</section><div class="foot">Built with Python · FastAPI · Browser Speech APIs</div>
</main>
<script>
const chat=document.getElementById('chat'),form=document.getElementById('form'),input=document.getElementById('command'),statusEl=document.getElementById('status'),mic=document.getElementById('mic');
function add(text,who){const el=document.createElement('div');el.className='msg '+who;el.textContent=text;chat.appendChild(el);chat.scrollTop=chat.scrollHeight;}
function speak(text){if('speechSynthesis'in window){speechSynthesis.cancel();const u=new SpeechSynthesisUtterance(text);u.rate=1; speechSynthesis.speak(u);}}
async function sendCommand(command){const clean=command.trim();if(!clean)return;add(clean,'user');input.value='';statusEl.textContent='● THINKING';try{const res=await fetch('/api/command',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({command:clean})});const data=await res.json();if(!res.ok)throw new Error(data.detail||'Request failed');add(data.response,'bot');speak(data.response);if(data.open_url){window.open(data.open_url,'_blank','noopener,noreferrer');}}catch(e){add('I could not process that request: '+e.message,'bot');}finally{statusEl.textContent='● ONLINE';}}
form.addEventListener('submit',e=>{e.preventDefault();sendCommand(input.value);});
document.querySelectorAll('[data-command]').forEach(b=>b.addEventListener('click',()=>sendCommand(b.dataset.command)));
const SpeechRecognition=window.SpeechRecognition||window.webkitSpeechRecognition;
if(SpeechRecognition){const recognition=new SpeechRecognition();recognition.lang='en-IN';recognition.interimResults=false;recognition.maxAlternatives=1;mic.addEventListener('click',()=>{try{recognition.start();}catch(e){}});recognition.onstart=()=>{mic.classList.add('listening');statusEl.textContent='● LISTENING'};recognition.onend=()=>{mic.classList.remove('listening');statusEl.textContent='● ONLINE'};recognition.onerror=e=>{add('Microphone error: '+e.error+'. You can type your command instead.','bot')};recognition.onresult=e=>sendCommand(e.results[0][0].transcript);}else{mic.disabled=true;mic.title='Speech recognition is not supported in this browser';}
</script></body></html>"""

class CommandRequest(BaseModel):
    command: str = Field(min_length=1, max_length=500)

@app.get("/", response_class=HTMLResponse)
async def home():
    return HTMLResponse(PAGE)

@app.get("/health")
async def health():
    return {"status": "ok", "app": "JARVIS Web Assistant"}

@app.post("/api/command")
async def process_command(payload: CommandRequest, request: Request):
    command = payload.command.strip().lower()
    if not command:
        raise HTTPException(status_code=400, detail="Please enter a command.")

    if any(term in command for term in ("what time", "current time", "tell me the time", "the time")):
        return {"response": "The server time is " + datetime.now().astimezone().strftime("%I:%M %p %Z") + "."}

    if any(term in command for term in ("what date", "today's date", "current date", "what is the date")):
        return {"response": "Today's date is " + datetime.now().astimezone().strftime("%A, %d %B %Y") + "."}

    if "open youtube" in command or command.strip() == "youtube":
        return {"response": "Opening YouTube in a new browser tab.", "open_url": "https://www.youtube.com/"}

    if "open google" in command or command.strip() == "google":
        return {"response": "Opening Google in a new browser tab.", "open_url": "https://www.google.com/"}

    if "wikipedia" in command:
        topic = command.replace("wikipedia", "", 1).strip()
        if not topic:
            return {"response": "Please add a topic, for example: Wikipedia artificial intelligence."}
        try:
            summary = wikipedia.summary(topic, sentences=2, auto_suggest=True, redirect=True)
            return {"response": "According to Wikipedia: " + summary}
        except wikipedia.exceptions.DisambiguationError as exc:
            choices = ", ".join(exc.options[:5])
            return {"response": "That topic has multiple meanings. Please be more specific. Possible topics: " + choices}
        except wikipedia.exceptions.PageError:
            return {"response": "I couldn't find a Wikipedia page for that topic."}
        except Exception:
            return {"response": "Wikipedia is temporarily unavailable. Please try again shortly."}

    if command in {"help", "what can you do", "commands"}:
        return {"response": "I can tell you the time and date, summarize a Wikipedia topic, and open Google or YouTube. Try: Wikipedia machine learning, Open Google, or What time is it?"}

    return {"response": "I don't recognize that command yet. I can tell the time or date, search Wikipedia, and open Google or YouTube. Type “help” to see examples."}
