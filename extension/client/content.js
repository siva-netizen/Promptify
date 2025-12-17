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
            return el.textContent || el.innerText || '';
        },
        setValue: (el, val) => {
            el.textContent = val;
            el.dispatchEvent(new Event('input', { bubbles: true }));
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
    },
    PERPLEXITY: {
        inputSelector: 'textarea, input[placeholder*="Ask"], div[contenteditable="true"]',
        containerSelector: 'div.relative',
        getValue: (el) => {
            if (el.tagName === 'TEXTAREA' || el.tagName === 'INPUT') {
                return el.value || '';
            }
            return el.textContent || el.innerText || '';
        },
        setValue: (el, val) => {
            el.focus();

            try {
                // Case 1: Textarea/Input (Native React Control)
                if (el.tagName === 'TEXTAREA' || el.tagName === 'INPUT') {
                    const proto = el.tagName === 'TEXTAREA'
                        ? window.HTMLTextAreaElement.prototype
                        : window.HTMLInputElement.prototype;

                    const nativeSetter = Object.getOwnPropertyDescriptor(proto, 'value').set;

                    if (nativeSetter) {
                        nativeSetter.call(el, val);
                    } else {
                        el.value = val;
                    }

                    el.dispatchEvent(new Event('input', { bubbles: true }));
                    el.dispatchEvent(new Event('change', { bubbles: true }));
                }
                // Case 2: ContentEditable Div (Slate.js / Complex Editor)
                else {
                    // Modern editors (Slate) listen to 'beforeinput'
                    const beforeInputEvent = new InputEvent('beforeinput', {
                        bubbles: true,
                        cancelable: true,
                        inputType: 'insertText',
                        data: val
                    });
                    el.dispatchEvent(beforeInputEvent);

                    // Strategy 1: execCommand 'insertText'
                    // Select all content safely
                    const range = document.createRange();
                    range.selectNodeContents(el);
                    const sel = window.getSelection();
                    sel.removeAllRanges();
                    sel.addRange(range);

                    const success = document.execCommand('insertText', false, val);

                    // Strategy 2: Simulate Paste (if insertText failed or didn't change text)
                    if (!success || (el.textContent !== val && el.innerText !== val)) {
                        console.warn('[Promptify] execCommand failed. Attempting synthetic PASTE event.');

                        const dataTransfer = new DataTransfer();
                        dataTransfer.setData('text/plain', val);

                        const pasteEvent = new ClipboardEvent('paste', {
                            bubbles: true,
                            cancelable: true,
                            clipboardData: dataTransfer
                        });

                        el.dispatchEvent(pasteEvent);

                        // Give it a moment, then check if we need to force it
                        // (Note: we can't wait async inside this sync block easily, but the event is sync)

                        // If execCommand return false or didn't update text, try fallback
                        if (!success || (el.textContent !== val && el.innerText !== val)) {
                            console.warn('[Promptify] execCommand failed/ignored. Trying direct Text node replacement.');
                            // Last resort: Nuke the contents and replace with text node.
                            // This might break editor state but is worth a try.
                            el.textContent = val;
                            el.dispatchEvent(new Event('input', { bubbles: true }));
                        }
                    }
                }
            } catch (err) {
                console.error('[Promptify] SetValue failed:', err);
                // Fallback: Copy to clipboard
                navigator.clipboard.writeText(val).then(() => {
                    alert('Could not auto-update input (security restriction). Refined prompt copied to clipboard!');
                }).catch(() => {
                    prompt("Could not auto-update. Please copy the prompt:", val);
                });
            }
        }
    },
    GEMINI: {
        inputSelector: 'div.ql-editor[contenteditable="true"]',
        containerSelector: null, // Let the fallback logic find the container with the send button
        getValue: (el) => el.textContent || el.innerText || '',
        setValue: (el, val) => {
            el.focus();
            el.textContent = val;
            el.dispatchEvent(new Event('input', { bubbles: true, composed: true }));
            el.dispatchEvent(new Event('change', { bubbles: true, composed: true }));
            el.dispatchEvent(new InputEvent('input', { bubbles: true, inputType: 'insertText', data: val }));
        }
    },
    COPILOT: {
        inputSelector: 'textarea[id*="searchbox"], textarea[class*="searchbox"], .show-placeholder[contenteditable="true"]',
        containerSelector: '.input-container, .cib-serp-main', // Try to find a stable container
        getValue: (el) => el.value || el.textContent || '',
        setValue: (el, val) => {
            el.focus();
            if (el.tagName === 'TEXTAREA' || el.tagName === 'INPUT') {
                el.value = val;
                el.dispatchEvent(new Event('input', { bubbles: true }));
                el.dispatchEvent(new Event('change', { bubbles: true }));
            } else {
                el.textContent = val;
                el.dispatchEvent(new Event('input', { bubbles: true }));
            }
        }
    }
};

function detectPlatform() {
    const host = window.location.hostname;
    if (host.includes('chatgpt.com')) return PLATFORMS.CHATGPT;
    if (host.includes('claude.ai')) return PLATFORMS.CLAUDE;
    if (host.includes('perplexity.ai')) return PLATFORMS.PERPLEXITY;
    if (host.includes('gemini.google.com')) return PLATFORMS.GEMINI;
    if (host.includes('copilot.microsoft.com') || host.includes('bing.com')) return PLATFORMS.COPILOT;
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
    const tryInject = () => {
        // Use the new robust finder
        const input = findTargetElement(platform.inputSelector);
        if (input && !document.getElementById('promptify-btn')) {
            log(`Found input via robust search`);
            injectButton(input);
            return true;
        }
        return false;
    };

    if (!tryInject()) {
        log('Input not found initially, setting up observer...');
    }

    const observer = new MutationObserver((mutations) => {
        if (!document.getElementById('promptify-btn')) {
            tryInject();
        }
    });

    observer.observe(document.body, { childList: true, subtree: true });
}

/**
 * Robustly find an element, including traversing open Shadow DOMs.
 * Useful for platforms like Copilot/Bing that use custom elements.
 */
function findTargetElement(selectors) {
    if (!selectors) return null;
    const selectorList = selectors.split(',').map(s => s.trim());

    // 1. Try standard query first
    for (const selector of selectorList) {
        const el = document.querySelector(selector);
        if (el) return el;
    }

    // 2. Try Shadow DOM traversal for specific platforms (like Copilot)
    // This is a simplified traversal targeting common shadow hosts
    const shadowHosts = document.querySelectorAll('cib-serp, cib-action-bar, cib-text-input, sh-input-field');
    for (const host of shadowHosts) {
        if (host.shadowRoot) {
            for (const selector of selectorList) {
                const el = host.shadowRoot.querySelector(selector);
                if (el) return el;

                // Deep traversal (one level deeper for now)
                const nestedHosts = host.shadowRoot.querySelectorAll('*');
                for (const nested of nestedHosts) {
                    if (nested.shadowRoot) {
                        const deepEl = nested.shadowRoot.querySelector(selector);
                        if (deepEl) return deepEl;
                    }
                }
            }
        }
    }

    return null;
}

function injectButton(inputEl) {
    const btn = document.createElement('button');
    btn.id = 'promptify-btn';
    btn.innerHTML = `<span style="display:flex;align-items:center;gap:6px;">
        ${PROMPTIFY_ICON}
        <span>Refine</span>
    </span>`;

    btn.style.cssText = `
        display: inline-flex;
        align-items: center;
        gap: 6px;
        margin-top: 8px;
        margin-left: auto;
        background: linear-gradient(90deg, #7C3AED, #5B21B6);
        color: white;
        border: none;
        border-radius: 6px;
        padding: 8px 16px;
        font-size: 13px;
        font-weight: 500;
        cursor: pointer;
        opacity: 0.95;
        transition: all 0.2s ease;
        box-shadow: 0 2px 8px rgba(124, 58, 237, 0.3);
    `;

    btn.onmouseenter = () => {
        btn.style.opacity = '1';
        btn.style.transform = 'translateY(-1px)';
        btn.style.boxShadow = '0 4px 12px rgba(124, 58, 237, 0.4)';
    };

    btn.onmouseleave = () => {
        btn.style.opacity = '0.95';
        btn.style.transform = 'translateY(0)';
        btn.style.boxShadow = '0 2px 8px rgba(124, 58, 237, 0.3)';
    };

    // Find the container that holds the input area
    let container = null;

    // 1. Try platform-specific container selector first
    if (platform.containerSelector) {
        container = inputEl.closest(platform.containerSelector);
    }

    // 2. Fallback to generic traversal if no specific container found
    if (!container) {
        container = inputEl.parentElement;
        let attempts = 0;
        while (container && attempts < 10) {
            if (container.querySelector('[data-testid="send-button"]') ||
                container.querySelector('button[aria-label*="Send"]') ||
                container.tagName === 'FORM') {
                break;
            }
            container = container.parentElement;
            attempts++;
        }
    }

    // 3. Ultimate fallback
    if (!container || container === document.body) {
        container = inputEl.parentElement;
    }

    log(`Injecting button after container: ${container.tagName} (Class: ${container.className})`);

    // Create a wrapper div to hold the button
    const buttonWrapper = document.createElement('div');
    buttonWrapper.id = 'promptify-btn-wrapper';
    buttonWrapper.style.cssText = `
        display: flex;
        justify-content: flex-end;
        align-items: center; 
        padding: 4px 12px 8px 12px;
        width: 100%;
        position: relative;
        z-index: 9999;
        pointer-events: auto;
    `;

    buttonWrapper.appendChild(btn);

    // Insert the button wrapper after the container for all platforms
    if (container && container.parentElement) {
        container.parentElement.insertBefore(buttonWrapper, container.nextSibling);
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
            btn.innerHTML = `<span style="display:flex;align-items:center;gap:6px;">
        ${PROMPTIFY_ICON}
        <span>Refine</span>
    </span>`;
            btn.disabled = false;
        }
    });
}

function showConfirmation(newText, inputEl) {
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
