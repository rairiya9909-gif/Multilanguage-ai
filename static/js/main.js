// Mapping of language dropdown values to browser BCP-47 speech recognition/synthesis codes
const langCodes = {
    "Hindi": "hi-IN",
    "Marathi": "mr-IN",
    "Bengali": "bn-IN",
    "Gujarati": "gu-IN",
    "Tamil": "ta-IN",
    "Telugu": "te-IN",
    "Kannada": "kn-IN",
    "Malayalam": "ml-IN",
    "Punjabi": "pa-IN",
    "Urdu": "ur-PK",
    "English": "en-US"
};

// UI Elements
const textInput = document.getElementById('text-input');
const srcLangSelect = document.getElementById('src-lang');
const destLangSelect = document.getElementById('dest-lang');
const swapLangsBtn = document.getElementById('swap-langs-btn');
const voiceBtn = document.getElementById('voice-btn');
const translateBtn = document.getElementById('translate-btn');
const speakBtn = document.getElementById('speak-btn');
const resultBox = document.getElementById('result-box');
const statusBar = document.getElementById('status-bar');

// Speech Recognition Init
const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
let recognition = null;
let isListening = false;

if (SpeechRecognition) {
    recognition = new SpeechRecognition();
    recognition.continuous = false;
    recognition.interimResults = false;

    recognition.onstart = () => {
        isListening = true;
        voiceBtn.classList.add('recording');
        voiceBtn.querySelector('.btn-icon').innerText = '⏹️';
        voiceBtn.querySelector('.btn-text').innerText = 'Stop';
        updateStatus('🎤 Listening... Speak now!', 'listening');
    };

    recognition.onerror = (event) => {
        console.error("Speech recognition error:", event.error);
        if (event.error === 'not-allowed') {
            updateStatus('❌ Microphone permission denied.', 'error');
        } else {
            updateStatus(`❌ Voice input error: ${event.error}`, 'error');
        }
        stopListening();
    };

    recognition.onend = () => {
        stopListening();
    };

    recognition.onresult = (event) => {
        const text = event.results[0][0].transcript;
        textInput.value = text;
        updateStatus('✅ Speech captured.');
        // Auto translate after speech capture for premium user experience
        translateText();
    };
} else {
    // Disable voice button or show error if speech recognition is not supported
    voiceBtn.title = "Speech recognition is not supported in this browser.";
    updateStatus("ℹ Voice input requires Chrome, Safari, or edge browser.");
}

// Trigger speech voices preloading for Chrome
if ('speechSynthesis' in window) {
    window.speechSynthesis.getVoices();
    if (window.speechSynthesis.onvoiceschanged !== undefined) {
        window.speechSynthesis.onvoiceschanged = () => {
            window.speechSynthesis.getVoices();
        };
    }
}

// Event Listeners
swapLangsBtn.addEventListener('click', swapLanguages);
translateBtn.addEventListener('click', translateText);
speakBtn.addEventListener('click', speakOutput);

voiceBtn.addEventListener('click', () => {
    if (isListening) {
        stopListening();
    } else {
        startListening();
    }
});

// Functions
function updateStatus(text, className = '') {
    statusBar.innerText = text;
    statusBar.className = 'status-bar ' + className;
}

function startListening() {
    if (!recognition) {
        updateStatus("❌ Speech recognition not supported in this browser.", "error");
        return;
    }
    
    // Set recording language
    const srcLangVal = srcLangSelect.value;
    recognition.lang = langCodes[srcLangVal] || 'en-US';
    
    try {
        recognition.start();
    } catch (e) {
        console.error(e);
        stopListening();
    }
}

function stopListening() {
    if (recognition && isListening) {
        recognition.stop();
    }
    isListening = false;
    voiceBtn.classList.remove('recording');
    voiceBtn.querySelector('.btn-icon').innerText = '🎤';
    voiceBtn.querySelector('.btn-text').innerText = 'Voice Input';
    if (statusBar.innerText.startsWith('🎤')) {
        updateStatus('Ready');
    }
}

function swapLanguages() {
    const temp = srcLangSelect.value;
    srcLangSelect.value = destLangSelect.value;
    destLangSelect.value = temp;
    updateStatus('Languages swapped.');
}

async function translateText() {
    const text = textInput.value.trim();
    if (!text) {
        updateStatus("⚠ Please enter some text or capture voice first.");
        return;
    }

    updateStatus("⚙ Translating...", "working");

    try {
        const response = await fetch('/translate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                text: text,
                src_lang: srcLangSelect.value,
                dest_lang: destLangSelect.value
            })
        });

        if (!response.ok) {
            throw new Error(`Server returned HTTP ${response.status}`);
        }

        const data = await response.json();
        if (data.error) {
            updateStatus(`❌ Error: ${data.error}`);
        } else {
            resultBox.innerHTML = `<span class="translated-text">${data.translated_text}</span>`;
            updateStatus("✅ Translation successful.");
        }
    } catch (error) {
        console.error("Translation error:", error);
        updateStatus(`❌ Translation failed: ${error.message}`);
    }
}

function speakOutput() {
    const textSpan = resultBox.querySelector('.translated-text');
    if (!textSpan) {
        updateStatus("⚠ No translation available to speak.");
        return;
    }
    const text = textSpan.innerText;

    if ('speechSynthesis' in window) {
        window.speechSynthesis.cancel(); // Cancel any active speech
        
        const utterance = new SpeechSynthesisUtterance(text);
        const destLangVal = destLangSelect.value;
        const code = langCodes[destLangVal] || 'en-US';
        utterance.lang = code;

        // Try to match appropriate system voice
        const voices = window.speechSynthesis.getVoices();
        const voice = voices.find(v => v.lang.toLowerCase().startsWith(code.split('-')[0].toLowerCase()));
        if (voice) {
            utterance.voice = voice;
        }

        utterance.onstart = () => {
            updateStatus("🔊 Speaking output...");
        };
        
        utterance.onend = () => {
            updateStatus("Ready");
        };

        utterance.onerror = (event) => {
            console.error("SpeechSynthesis error:", event);
            updateStatus(`❌ TTS playback error.`, 'error');
        };

        window.speechSynthesis.speak(utterance);
    } else {
        updateStatus("❌ Text-to-speech not supported in this browser.", "error");
    }
}
