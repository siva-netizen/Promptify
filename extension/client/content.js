// content.js

function log(msg) {
    console.log(`[Promptify] ${msg}`);
}

const PROMPTIFY_ICON = `<svg width="20" height="20" viewBox="0 0 128 128" xmlns="http://www.w3.org/2000/svg">
  <circle cx="64" cy="64" r="64" fill="#7C3AED"/>
  <path d="M44 30 H72 C85 30 94 38 94 52 C94 66 85 74 72 74 H58 V98 H44 V30 Z M58 42 V62 H70 C77 62 80 58 80 52 C80 46 77 42 70 42 H58 Z" fill="white"/>
  <path d="M98 24 L102 36 L114 40 L102 44 L98 56 L94 44 L82 40 L94 36 Z" fill="white"/>
</svg>`;

const PLATFORMS = {
    CHATGPT: {
        inputSelector: 'div#prompt-textarea',
        containerSelector: 'div.relative.flex.h-full.max-w-full.flex-1',
        getValue: (el) => {
            // ChatGPT uses contenteditable div, get textContent or innerText
            return el.textContent || el.innerText || '';
        },
        setValue: (el, val) => {
            // For contenteditable, set textContent
            el.textContent = val;
            // Trigger input event
            el.dispatchEvent(new Event('input', { bubbles: true }));
            // Also trigger change for good measure
            el.dispatchEvent(new Event('change', { bubbles: true }));
        }
    },
    CLAUDE: {
        inputSelector: 'div.ProseMirror[contenteditable="true"]',
        containerSelector: 'div.cursor-text',
        getValue: (el) => el.textContent || el.innerText || '',
        setValue: (el, val) => {
            el.textContent = val;
            el.dispatchEvent(new Event('input', { bubbles: true }));
        }
    }
};

function detectPlatform() {
    const host = window.location.hostname;
    if (host.includes('chatgpt.com')) return PLATFORMS.CHATGPT;
    if (host.includes('claude.ai')) return PLATFORMS.CLAUDE;
    return null;
}

const platform = detectPlatform();

if (platform) {
    log(`Detected platform: ${window.location.hostname}`);
    initObserver();
} else {
    log("Platform not supported.");
}

function initObserver() {
    const observer = new MutationObserver((mutations) => {
        const input = document.querySelector(platform.inputSelector);
        if (input && !document.getElementById('promptify-btn')) {
            injectButton(input);
        }
    });

    observer.observe(document.body, { childList: true, subtree: true });
}

function injectButton(inputEl) {
    const btn = document.createElement('button');
    btn.id = 'promptify-btn';
    btn.innerHTML = `<span style="display:flex;align-items:center;gap:6px;">
        ${PROMPTIFY_ICON}
        <span>Refine</span>
    </span>`;

    btn.style.cssText = `
        position: absolute;
        bottom: 8px;
        right: 60px;
        z-index: 1000;
        background: linear-gradient(90deg, #7C3AED, #5B21B6);
        color: white;
        border: none;
        border-radius: 6px;
        padding: 6px 12px;
        font-size: 13px;
        font-weight: 500;
        cursor: pointer;
        opacity: 0.95;
        transition: all 0.2s ease;
        box-shadow: 0 2px 8px rgba(124, 58, 237, 0.3);
    `;

    // Find the proper container - look for parent that contains both input and send button
    let container = inputEl.parentElement;

    // For ChatGPT, traverse up to find the form container with send button
    let attempts = 0;
    while (container && attempts < 10) {
        if (container.querySelector('[data-testid="send-button"]') ||
            container.querySelector('button[aria-label*="Send"]')) {
            break;
        }
        container = container.parentElement;
        attempts++;
    }

    // Fallback to immediate parent if we went too far
    if (!container || container === document.body) {
        container = inputEl.parentElement;
    }

    if (container) {
        container.style.position = 'relative';
        container.appendChild(btn);
    }

    btn.addEventListener('click', async (e) => {
        e.preventDefault();
        e.stopPropagation();

        const currentText = platform.getValue(inputEl);
        log(`Retrieved text: "${currentText}" (length: ${currentText ? currentText.length : 0})`);

        if (!currentText || !currentText.trim()) {
            alert("Please type a prompt first!");
            return;
        }

        btn.textContent = "⏳ Refining...";
        btn.disabled = true;

        try {
            const resp = await chrome.runtime.sendMessage({
                type: 'REFINE_PROMPT',
                prompt: currentText
            });

            if (resp.success) {
                showConfirmation(resp.refined, inputEl);
            } else {
                alert(`Error: ${resp.error}`);
            }
        } catch (err) {
            alert(`Error: ${err.message}`);
        } finally {
            btn.textContent = "✨ Refine";
            btn.disabled = false;
        }
    });
}

function showConfirmation(newText, inputEl) {
    // Create Modal
    const modal = document.createElement('div');
    modal.style.cssText = `
        position: fixed;
        top: 0; left: 0; right: 0; bottom: 0;
        background: rgba(0,0,0,0.7);
        z-index: 10000;
        display: flex;
        align-items: center;
        justify-content: center;
    `;

    const content = document.createElement('div');
    content.style.cssText = `
        background: #1a1a1a;
        color: white;
        padding: 20px;
        border-radius: 8px;
        width: 80%;
        max-width: 600px;
        max-height: 80vh;
        overflow-y: auto;
        font-family: sans-serif;
        border: 1px solid #333;
    `;

    content.innerHTML = `
        <h3 style="margin-top:0">Refined Prompt Preview</h3>
        <textarea style="width:100%; height: 300px; background: #000; color: #fff; border: 1px solid #444; padding: 10px;">${newText}</textarea>
        <div style="margin-top: 15px; text-align: right;">
            <button id="pfy-cancel" style="background:#444; color:white; border:none; padding:8px 16px; border-radius:4px; margin-right:10px; cursor:pointer;">Cancel</button>
            <button id="pfy-confirm" style="background:#00BFFF; color:white; border:none; padding:8px 16px; border-radius:4px; cursor:pointer;">Update Input</button>
        </div>
    `;

    modal.appendChild(content);
    document.body.appendChild(modal);

    document.getElementById('pfy-cancel').onclick = () => {
        document.body.removeChild(modal);
    };

    document.getElementById('pfy-confirm').onclick = () => {
        platform.setValue(inputEl, newText);
        document.body.removeChild(modal);
    };
}
