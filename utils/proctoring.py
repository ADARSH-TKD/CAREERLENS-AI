"""
CareerLens AI - Full-Screen & Comprehensive Proctoring Lockdown Engine
Enforces full-screen mode during active interviews and strictly restricts:
- Alt + Tab: switching to another application/window
- Ctrl + Tab: switching browser tabs
- Ctrl + C / Ctrl + V: copying or pasting
- Ctrl + F: searching within a page
- F12 / Ctrl + Shift + I: opening developer tools
- Print Screen / Win + Shift + S: taking screenshots
- Windows key: opening Start menu or leaving assessment
- Esc: exiting fullscreen or closing view
- Alt + F4: closing the browser/window
- Ctrl + W: closing the current browser tab
- Ctrl + L: moving to the browser address bar
- F11: toggling fullscreen
- Window blur / tab switching / right-click context menu
"""

def get_proctoring_html(max_warnings: int = 4) -> str:
    """
    Returns self-contained HTML/JS that attaches to window.parent to enforce
    full-screen mode, detect unauthorized keys, show warnings, and trigger cancellation.
    """
    return f"""
    <script>
    (function() {{
      try {{
        const parentWin = window.parent || window;
        const parentDoc = (window.parent && window.parent.document) ? window.parent.document : document;

        // Cleanup existing proctor if already attached
        if (parentWin.__careerLensProctorCleanup) {{
          parentWin.__careerLensProctorCleanup();
        }}

        let warningCount = parentWin.__careerLensWarningCount || 0;
        let isModalOpen = false;
        let lastTriggerTime = 0;
        const MAX_WARNINGS = {max_warnings};

        // --- Audio Alert Synthesizer ---
        function playAlertTone(isDanger = false) {{
          try {{
            const AudioCtx = parentWin.AudioContext || parentWin.webkitAudioContext;
            if (!AudioCtx) return;
            const ctx = new AudioCtx();
            const osc = ctx.createOscillator();
            const gain = ctx.createGain();
            osc.connect(gain);
            gain.connect(ctx.destination);
            
            if (isDanger) {{
              // High-low alarm
              osc.type = 'sawtooth';
              osc.frequency.setValueAtTime(440, ctx.currentTime);
              osc.frequency.linearRampToValueAtTime(220, ctx.currentTime + 0.4);
              gain.gain.setValueAtTime(0.3, ctx.currentTime);
              gain.gain.exponentialRampToValueAtTime(0.01, ctx.currentTime + 0.45);
              osc.start();
              osc.stop(ctx.currentTime + 0.45);
            }} else {{
              // Warning tone
              osc.type = 'triangle';
              osc.frequency.setValueAtTime(580, ctx.currentTime);
              osc.frequency.setValueAtTime(780, ctx.currentTime + 0.1);
              gain.gain.setValueAtTime(0.25, ctx.currentTime);
              gain.gain.exponentialRampToValueAtTime(0.01, ctx.currentTime + 0.25);
              osc.start();
              osc.stop(ctx.currentTime + 0.25);
            }}
          }} catch(e) {{}}
        }}

        // --- Fullscreen Helpers ---
        function requestFull() {{
          try {{
            const el = parentDoc.documentElement;
            if (el.requestFullscreen) {{
              el.requestFullscreen().catch(() => {{}});
            }} else if (el.webkitRequestFullscreen) {{
              el.webkitRequestFullscreen();
            }} else if (el.msRequestFullscreen) {{
              el.msRequestFullscreen();
            }}
          }} catch (e) {{}}
        }}

        function isFullscreen() {{
          return Boolean(
            parentDoc.fullscreenElement ||
            parentDoc.webkitFullscreenElement ||
            parentDoc.mozFullScreenElement ||
            parentDoc.msFullscreenElement
          );
        }}

        // Attempt initial fullscreen
        requestFull();

        // One-time click fallback in case browser policy requires user gesture
        function clickToFull() {{
          if (!isFullscreen()) {{
            requestFull();
          }}
        }}
        parentDoc.addEventListener('click', clickToFull, {{ capture: true, once: true }});

        // --- HUD Indicator Badge ---
        let hud = parentDoc.getElementById('cl-proctor-hud');
        if (!hud) {{
          hud = parentDoc.createElement('div');
          hud.id = 'cl-proctor-hud';
          hud.style.cssText = `
            position: fixed;
            top: 14px;
            right: 20px;
            z-index: 999990;
            background: rgba(15, 10, 26, 0.92);
            border: 1px solid rgba(167, 139, 250, 0.4);
            border-radius: 30px;
            padding: 6px 16px;
            display: flex;
            align-items: center;
            gap: 10px;
            font-family: Inter, sans-serif;
            font-size: 12px;
            font-weight: 600;
            color: #e9d5ff;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.45);
            backdrop-filter: blur(10px);
            pointer-events: none;
          `;
          parentDoc.body.appendChild(hud);
        }}

        function updateHud() {{
          if (!hud) return;
          const warnColor = warningCount === 0 ? '#34d399' : (warningCount < 3 ? '#fbbf24' : '#ef4444');
          hud.innerHTML = `
            <span style="display:inline-block;width:8px;height:8px;background:${{warnColor}};border-radius:50%;box-shadow:0 0 8px ${{warnColor}};"></span>
            <span>🛡️ PROCTORING ACTIVE</span>
            <span style="color:#6d28d9">|</span>
            <span style="color:${{warnColor}}">⚠️ Warnings: ${{warningCount}} / ${{MAX_WARNINGS}}</span>
          `;
        }}
        updateHud();

        // --- Modal Container ---
        function getOrCreateModal() {{
          let m = parentDoc.getElementById('cl-proctor-modal');
          if (!m) {{
            m = parentDoc.createElement('div');
            m.id = 'cl-proctor-modal';
            m.style.cssText = `
              position: fixed;
              top: 0;
              left: 0;
              width: 100vw;
              height: 100vh;
              z-index: 999999;
              background: rgba(4, 2, 8, 0.90);
              backdrop-filter: blur(15px);
              display: none;
              justify-content: center;
              align-items: center;
              font-family: Inter, sans-serif;
              padding: 20px;
              box-sizing: border-box;
            `;
            parentDoc.body.appendChild(m);
          }}
          return m;
        }}

        // --- Show Warning Modal ---
        function showWarning(reason) {{
          const now = Date.now();
          if (now - lastTriggerTime < 1200) return; // Debounce rapid multi-events
          lastTriggerTime = now;

          warningCount++;
          parentWin.__careerLensWarningCount = warningCount;
          updateHud();

          const modal = getOrCreateModal();
          isModalOpen = true;

          if (warningCount > MAX_WARNINGS) {{
            // CANCELLATION SCREEN (Occurs for more than 4 warnings)
            playAlertTone(true);
            modal.innerHTML = `
              <div style="
                max-width: 660px;
                width: 90%;
                background: linear-gradient(145deg, #240a0f, #140508);
                border: 2px solid #ef4444;
                border-radius: 24px;
                padding: 38px 34px;
                box-shadow: 0 0 75px rgba(239, 68, 68, 0.45);
                text-align: center;
              ">
                <div style="font-size: 3.8rem; margin-bottom: 8px;">⚠️</div>
                <h1 style="color: #ef4444; font-size: 26px; font-weight: 800; margin: 0 0 16px; letter-spacing: -0.02em;">
                  ⚠️ URGENT WARNING
                </h1>
                
                <div style="
                  background: rgba(239, 68, 68, 0.14);
                  border: 1.5px solid rgba(239, 68, 68, 0.45);
                  border-radius: 16px;
                  padding: 22px;
                  text-align: left;
                  margin: 18px 0;
                ">
                  <p style="color: #fee2e2; font-size: 16px; font-weight: 700; line-height: 1.6; margin: 0 0 14px;">
                    Your interview has been CANCELLED with immediate effect due to a serious issue with your application. 🚨
                  </p>
                  <p style="color: #fca5a5; font-size: 14px; line-height: 1.6; margin: 0;">
                    Failure to resolve the issue within the required time may result in permanent removal from the interview process and you may no longer be considered for this opportunity.<br>
                    <strong style="color: #ffffff;">Do not ignore this notice.</strong>
                  </p>
                </div>

                <p style="color: #94a3b8; font-size: 13px; margin: 16px 0 24px;">
                  Exceeded maximum allowed proctoring violations (${{MAX_WARNINGS}}). Last restricted action: <b>${{reason}}</b>
                </p>

                <button id="cl-proctor-cancel-btn" style="
                  background: linear-gradient(90deg, #dc2626, #ef4444);
                  color: #ffffff;
                  border: 0;
                  padding: 14px 32px;
                  border-radius: 12px;
                  font-weight: 700;
                  font-size: 15px;
                  cursor: pointer;
                  box-shadow: 0 4px 20px rgba(239, 68, 68, 0.4);
                ">Return to Dashboard</button>
              </div>
            `;
            modal.style.display = 'flex';

            const btn = modal.querySelector('#cl-proctor-cancel-btn');
            if (btn) {{
              btn.onclick = function() {{
                try {{
                  if (parentDoc.exitFullscreen) parentDoc.exitFullscreen().catch(() => {{}});
                }} catch(e) {{}}
                parentWin.location.search = '?interview_cancelled=true';
              }};
            }}
            return;
          }}

          // STANDARD WARNING (Warnings 1 to 4)
          playAlertTone(false);
          modal.innerHTML = `
            <div style="
              max-width: 590px;
              width: 90%;
              background: linear-gradient(145deg, #1d132b, #0f0a17);
              border: 2px solid #f59e0b;
              border-radius: 22px;
              padding: 32px 28px;
              box-shadow: 0 0 60px rgba(245, 158, 11, 0.35);
              text-align: center;
            ">
              <div style="font-size: 3.2rem; margin-bottom: 6px;">⚠️</div>
              <h2 style="color: #fbbf24; font-size: 22px; font-weight: 800; margin: 0 0 10px;">
                PROCTORING WARNING #${{warningCount}} / ${{MAX_WARNINGS}}
              </h2>
              
              <div style="
                background: rgba(245, 158, 11, 0.12);
                border: 1px solid rgba(245, 158, 11, 0.35);
                border-radius: 14px;
                padding: 16px;
                margin: 16px 0;
                text-align: left;
              ">
                <p style="color: #fef3c7; font-size: 14px; margin: 0 0 8px; font-weight: 700;">
                  ⚠️ Restricted key or action detected:<br>
                  <span style="color:#ffffff; font-weight: 600;">${{reason}}</span>
                </p>
                <p style="color: #cbd5e1; font-size: 13px; line-height: 1.5; margin: 0;">
                  You must remain in full-screen mode throughout the entire assessment. Do not switch tabs or applications, copy/paste, take screenshots, or press system keys.
                </p>
              </div>

              <p style="color: #ef4444; font-size: 12.5px; font-weight: 600; margin: 12px 0 20px;">
                🚨 If warnings exceed ${{MAX_WARNINGS}}, your interview will be immediately CANCELLED.
              </p>

              <button id="cl-proctor-resume-btn" style="
                background: linear-gradient(90deg, #6d28d9, #8b5cf6);
                color: #ffffff;
                border: 0;
                padding: 12px 28px;
                border-radius: 12px;
                font-weight: 700;
                font-size: 14px;
                cursor: pointer;
                box-shadow: 0 4px 20px rgba(139, 92, 246, 0.4);
              ">I Understand — Resume Full Screen</button>
            </div>
          `;
          modal.style.display = 'flex';

          const resumeBtn = modal.querySelector('#cl-proctor-resume-btn');
          if (resumeBtn) {{
            resumeBtn.onclick = function() {{
              modal.style.display = 'none';
              isModalOpen = false;
              requestFull();
            }};
          }}
        }}

        // --- Exhaustive Keydown Interceptor ---
        function onKeyDown(e) {{
          if (isModalOpen) return;

          const key = e.key || '';
          const code = e.code || '';
          const keyCode = e.keyCode || 0;
          const kLow = key.toLowerCase();
          const isCtrl = e.ctrlKey || e.metaKey;

          // 1. Windows key (Meta / OS key)
          if (key === 'Meta' || key === 'OS' || code === 'MetaLeft' || code === 'MetaRight' || keyCode === 91 || keyCode === 92) {{
            e.preventDefault();
            e.stopPropagation();
            showWarning('Windows key — opening Start menu or leaving assessment');
            return;
          }}

          // 2. Esc key
          if (key === 'Escape' || code === 'Escape' || keyCode === 27) {{
            e.preventDefault();
            e.stopPropagation();
            showWarning('Esc — exiting fullscreen or assessment view');
            return;
          }}

          // 3. Alt + Tab or Alt + F4 or Alt key combinations
          if (e.altKey && (key === 'Tab' || code === 'Tab' || keyCode === 9)) {{
            e.preventDefault();
            e.stopPropagation();
            showWarning('Alt + Tab — switching to another application/window');
            return;
          }}
          if (e.altKey && (key === 'F4' || code === 'F4' || keyCode === 115)) {{
            e.preventDefault();
            e.stopPropagation();
            showWarning('Alt + F4 — closing the browser/window');
            return;
          }}

          // 4. Ctrl + Tab (switching browser tabs)
          if (isCtrl && (key === 'Tab' || code === 'Tab' || keyCode === 9)) {{
            e.preventDefault();
            e.stopPropagation();
            showWarning('Ctrl + Tab — switching browser tabs');
            return;
          }}

          // 5. Ctrl + C / Ctrl + V / Ctrl + X (copying or pasting)
          if (isCtrl && (kLow === 'c' || kLow === 'v' || kLow === 'x' || code === 'KeyC' || code === 'KeyV' || code === 'KeyX')) {{
            e.preventDefault();
            e.stopPropagation();
            showWarning('Ctrl + C / Ctrl + V — copying or pasting');
            return;
          }}

          // 6. Ctrl + F (searching within a page)
          if (isCtrl && (kLow === 'f' || code === 'KeyF' || keyCode === 70)) {{
            e.preventDefault();
            e.stopPropagation();
            showWarning('Ctrl + F — searching within a page');
            return;
          }}

          // 7. F12 or Ctrl + Shift + I / J / C (opening developer tools)
          if (key === 'F12' || code === 'F12' || keyCode === 123) {{
            e.preventDefault();
            e.stopPropagation();
            showWarning('F12 — opening developer tools');
            return;
          }}
          if (isCtrl && e.shiftKey && (kLow === 'i' || kLow === 'j' || kLow === 'c' || code === 'KeyI' || code === 'KeyJ' || code === 'KeyC')) {{
            e.preventDefault();
            e.stopPropagation();
            showWarning('Ctrl + Shift + I — opening developer tools');
            return;
          }}

          // 8. Print Screen or Win + Shift + S (taking screenshots)
          if (key === 'PrintScreen' || code === 'PrintScreen' || keyCode === 44) {{
            e.preventDefault();
            e.stopPropagation();
            showWarning('Print Screen — taking screenshots');
            return;
          }}
          if ((e.metaKey || key === 'Meta') && e.shiftKey && (kLow === 's' || code === 'KeyS')) {{
            e.preventDefault();
            e.stopPropagation();
            showWarning('Win + Shift + S — taking screenshots');
            return;
          }}

          // 9. Ctrl + W (closing current browser tab)
          if (isCtrl && (kLow === 'w' || code === 'KeyW')) {{
            e.preventDefault();
            e.stopPropagation();
            showWarning('Ctrl + W — closing current browser tab');
            return;
          }}

          // 10. Ctrl + L (moving to browser address bar)
          if (isCtrl && (kLow === 'l' || code === 'KeyL')) {{
            e.preventDefault();
            e.stopPropagation();
            showWarning('Ctrl + L — moving to browser address bar');
            return;
          }}

          // 11. F11 (toggling fullscreen)
          if (key === 'F11' || code === 'F11' || keyCode === 122) {{
            e.preventDefault();
            e.stopPropagation();
            showWarning('F11 — toggling fullscreen');
            return;
          }}

          // 12. Other browser navigation shortcuts (Ctrl+T, Ctrl+N, Ctrl+R, F5)
          if (isCtrl && (kLow === 't' || kLow === 'n' || kLow === 'r' || code === 'KeyT' || code === 'KeyN' || code === 'KeyR')) {{
            e.preventDefault();
            e.stopPropagation();
            showWarning(`Ctrl + ${{key.toUpperCase()}} — restricted browser navigation`);
            return;
          }}
          if (key === 'F5' || keyCode === 116) {{
            e.preventDefault();
            e.stopPropagation();
            showWarning('F5 — page refresh restricted during assessment');
            return;
          }}
        }}

        // Keyup listener specifically for PrintScreen (which often triggers keyup on Windows)
        function onKeyUp(e) {{
          if (isModalOpen) return;
          if (e.key === 'PrintScreen' || e.code === 'PrintScreen' || e.keyCode === 44) {{
            showWarning('Print Screen — taking screenshots');
          }}
        }}

        // Copy / Cut / Paste native event listeners
        function onClipboard(e) {{
          if (isModalOpen) return;
          e.preventDefault();
          e.stopPropagation();
          showWarning('Ctrl + C / Ctrl + V — clipboard operation restricted');
        }}

        // Right-click Context Menu
        function onContextMenu(e) {{
          e.preventDefault();
          showWarning('Right-click context menu restricted');
        }}

        // Fullscreen exit detection
        function onFullscreenChange() {{
          if (!isFullscreen()) {{
            showWarning('Exited full-screen mode');
          }}
        }}

        // Tab visibility change
        function onVisibilityChange() {{
          if (parentDoc.hidden) {{
            showWarning('Alt + Tab / switching browser tabs (focus lost)');
          }}
        }}

        // Window blur (focus lost)
        function onWindowBlur() {{
          setTimeout(() => {{
            if (!parentDoc.hasFocus && !isModalOpen) {{
              showWarning('Alt + Tab — switching to another application/window');
            }}
          }}, 350);
        }}

        // --- Attach all event listeners to parentDoc & document ---
        parentDoc.addEventListener('keydown', onKeyDown, true);
        document.addEventListener('keydown', onKeyDown, true);

        parentDoc.addEventListener('keyup', onKeyUp, true);
        document.addEventListener('keyup', onKeyUp, true);

        parentDoc.addEventListener('copy', onClipboard, true);
        parentDoc.addEventListener('cut', onClipboard, true);
        parentDoc.addEventListener('paste', onClipboard, true);
        document.addEventListener('copy', onClipboard, true);
        document.addEventListener('cut', onClipboard, true);
        document.addEventListener('paste', onClipboard, true);

        parentDoc.addEventListener('contextmenu', onContextMenu, true);
        document.addEventListener('contextmenu', onContextMenu, true);

        parentDoc.addEventListener('fullscreenchange', onFullscreenChange);
        parentDoc.addEventListener('webkitfullscreenchange', onFullscreenChange);

        parentDoc.addEventListener('visibilitychange', onVisibilityChange);
        parentWin.addEventListener('blur', onWindowBlur);

        // --- Cleanup registration ---
        parentWin.__careerLensProctorCleanup = function() {{
          parentDoc.removeEventListener('keydown', onKeyDown, true);
          document.removeEventListener('keydown', onKeyDown, true);
          parentDoc.removeEventListener('keyup', onKeyUp, true);
          document.removeEventListener('keyup', onKeyUp, true);
          parentDoc.removeEventListener('copy', onClipboard, true);
          parentDoc.removeEventListener('cut', onClipboard, true);
          parentDoc.removeEventListener('paste', onClipboard, true);
          document.removeEventListener('copy', onClipboard, true);
          document.removeEventListener('cut', onClipboard, true);
          document.removeEventListener('paste', onClipboard, true);
          parentDoc.removeEventListener('contextmenu', onContextMenu, true);
          document.removeEventListener('contextmenu', onContextMenu, true);
          parentDoc.removeEventListener('fullscreenchange', onFullscreenChange);
          parentDoc.removeEventListener('webkitfullscreenchange', onFullscreenChange);
          parentDoc.removeEventListener('visibilitychange', onVisibilityChange);
          parentWin.removeEventListener('blur', onWindowBlur);
          parentDoc.removeEventListener('click', clickToFull, true);
          const m = parentDoc.getElementById('cl-proctor-modal');
          if (m) m.remove();
          const h = parentDoc.getElementById('cl-proctor-hud');
          if (h) h.remove();
          delete parentWin.__careerLensProctorCleanup;
        }};

      }} catch (err) {{
        console.warn('Proctoring initialization error:', err);
      }}
    }})();
    </script>
    """

def get_proctoring_exit_html() -> str:
    """
    Returns HTML/JS that cleans up proctoring listeners, HUD, and exits full screen
    when leaving the interview room.
    """
    return """
    <script>
    (function() {
      try {
        const parentWin = window.parent || window;
        const parentDoc = (window.parent && window.parent.document) ? window.parent.document : document;
        if (parentWin.__careerLensProctorCleanup) {
          parentWin.__careerLensProctorCleanup();
        }
        delete parentWin.__careerLensWarningCount;
        if (parentDoc.fullscreenElement && parentDoc.exitFullscreen) {
          parentDoc.exitFullscreen().catch(() => {});
        }
      } catch(e) {}
    })();
    </script>
    """
