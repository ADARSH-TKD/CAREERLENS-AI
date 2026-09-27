import tempfile
from pathlib import Path
import os

_model = None

def _get_model():
    global _model
    if _model is None:
        from faster_whisper import WhisperModel
        _model = WhisperModel("tiny", device="cpu", compute_type="int8")
    return _model

def transcribe_audio(audio_file):
    """Transcribe Streamlit st.audio_input output using faster-whisper with fallbacks."""
    path = None
    try:
        data = audio_file.getvalue()
        if not data:
            return ""
        mime = getattr(audio_file, "type", "") or ""
        suffix = ".webm" if "webm" in mime else ".wav"
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as f:
            f.write(data)
            path = f.name

        # Primary engine: faster-whisper
        try:
            model = _get_model()
            segments, info = model.transcribe(
                path,
                language="en",
                beam_size=1,
                vad_filter=True,
            )
            text = " ".join(seg.text.strip() for seg in segments).strip()
            if not text:
                # Retry without VAD filter in case speech was filtered out
                segments, info = model.transcribe(
                    path,
                    language="en",
                    beam_size=1,
                    vad_filter=False,
                )
                text = " ".join(seg.text.strip() for seg in segments).strip()
            if text:
                return text
        except Exception as e_fw:
            print(f"[faster-whisper] error: {e_fw}")

        # Secondary engine: openai-whisper
        try:
            import whisper
            w_model = whisper.load_model("tiny")
            res = w_model.transcribe(path, language="en")
            w_text = res.get("text", "").strip()
            if w_text:
                return w_text
        except Exception as e_w:
            print(f"[openai-whisper] error: {e_w}")

        return ""
    except Exception as e:
        print(f"[transcribe_audio] general error: {e}")
        return ""
    finally:
        if path:
            try:
                Path(path).unlink(missing_ok=True)
            except Exception:
                pass

def speak_text_html(text, *args, **kwargs):
    """Generate HTML/JS to speak the question using the selected interviewer voice profile."""
    import json
    voice_type = "Professional Male (US)"
    if args:
        voice_type = args[0]
    elif "voice_type" in kwargs:
        voice_type = kwargs["voice_type"]
    elif "voice" in kwargs:
        voice_type = kwargs["voice"]

    safe_text = json.dumps(text or "")
    safe_voice = json.dumps(voice_type or "Professional Male (US)")
    return f"""
    <script>
    (() => {{
      try {{
        const text = {safe_text};
        const voiceType = {safe_voice};
        const synth = window.speechSynthesis || (window.top && window.top.speechSynthesis) || (window.parent && window.parent.speechSynthesis);
        if (!synth) return;

        function getBestVoice(voices, type) {{
          if (!voices || voices.length === 0) return null;
          const t = (type || "").toLowerCase();
          const isFemale = t.includes("female");

          // 1. Indian English
          if (t.includes("indian") || t.includes("(in)")) {{
            const inVoices = voices.filter(v => v.lang === "en-IN" || (v.lang && v.lang.startsWith("en-IN")) || (v.name && v.name.toLowerCase().includes("india")));
            if (inVoices.length > 0) {{
              const matched = inVoices.find(v => {{
                const n = (v.name || "").toLowerCase();
                return isFemale ? (n.includes("female") || n.includes("heera") || n.includes("neerja") || n.includes("swara"))
                                : (n.includes("male") || n.includes("ravi") || n.includes("prabhat") || n.includes("madhav"));
              }});
              if (matched) return matched;
              return inVoices[0];
            }}
          }}

          // 2. British / UK English
          if (t.includes("british") || t.includes("uk") || t.includes("(uk)")) {{
            const ukVoices = voices.filter(v => v.lang === "en-GB" || (v.lang && v.lang.startsWith("en-GB")) || (v.name && v.name.toLowerCase().includes("united kingdom")) || (v.name && v.name.toLowerCase().includes("uk")));
            if (ukVoices.length > 0) {{
              const matched = ukVoices.find(v => {{
                const n = (v.name || "").toLowerCase();
                return isFemale ? (n.includes("female") || n.includes("susan") || n.includes("hazel") || n.includes("sonia") || n.includes("libby") || n.includes("serena"))
                                : (n.includes("male") || n.includes("george") || n.includes("ryan") || n.includes("oliver") || n.includes("daniel"));
              }});
              if (matched) return matched;
              return ukVoices[0];
            }}
          }}

          // 3. Female voice (US / general)
          if (isFemale) {{
            const f = voices.find(v => {{
              const n = (v.name || "").toLowerCase();
              return (v.lang && v.lang.startsWith("en")) && (n.includes("female") || n.includes("zira") || n.includes("jenny") || n.includes("samantha") || n.includes("victoria") || n.includes("karen") || n.includes("aria") || n.includes("steffan"));
            }});
            if (f) return f;
          }}

          // 4. Male voice (US / general)
          if (t.includes("male")) {{
            const m = voices.find(v => {{
              const n = (v.name || "").toLowerCase();
              return (v.lang && v.lang.startsWith("en")) && (n.includes("male") || n.includes("david") || n.includes("guy") || n.includes("mark") || n.includes("alex") || n.includes("christopher") || n.includes("eric"));
            }});
            if (m) return m;
          }}

          // 5. Friendly AI Coach / Default English
          const anyEn = voices.find(v => v.lang && v.lang.toLowerCase().startsWith("en"));
          return anyEn || voices[0] || null;
        }}

        function speak() {{
          synth.cancel();
          const u = new SpeechSynthesisUtterance(text);
          const voices = synth.getVoices();
          const v = getBestVoice(voices, voiceType);
          if (v) {{
            u.voice = v;
            u.lang = v.lang || "en-US";
          }}

          const t = (voiceType || "").toLowerCase();
          if (t.includes("female")) {{
            u.pitch = 1.18;
            u.rate = 0.96;
          }} else if (t.includes("male")) {{
            u.pitch = 0.88;
            u.rate = 0.94;
          }} else if (t.includes("friendly") || t.includes("coach")) {{
            u.pitch = 1.05;
            u.rate = 1.0;
          }} else {{
            u.pitch = 1.0;
            u.rate = 0.96;
          }}

          synth.speak(u);
        }}

        if (synth.getVoices().length > 0) {{
          speak();
        }} else {{
          synth.onvoiceschanged = () => {{
            speak();
            synth.onvoiceschanged = null;
          }};
          setTimeout(() => {{
            if (!synth.speaking) speak();
          }}, 200);
        }}
      }} catch(e) {{}}
    }})();
    </script>
    """
