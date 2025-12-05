// --- DOM elements ---
const statusDiv = document.getElementById("status");

// Steps
const step1 = document.getElementById("step1");
const step2 = document.getElementById("step2");
const step3 = document.getElementById("step3");

// Step 1
const agentMessageP = document.getElementById("agent-message");
const recordBtn = document.getElementById("record-btn");

// Step 2
const originalSentenceP = document.getElementById("original-sentence");
const correctedSentenceP = document.getElementById("corrected-sentence");
const explanationTextP = document.getElementById("explanation-text");
const continueBtn = document.getElementById("continue-btn");
const finishBtn = document.getElementById("finish-btn");

// Step 3
const summaryMistakesUl = document.getElementById("summary-mistakes");
const summaryActivitiesUl = document.getElementById("summary-activities");
const newSessionBtn = document.getElementById("new-session-btn");

// --- State ---
let currentFollowUpMessage = "Hello, I am your personal English teacher.";
let mediaRecorder = null;
let audioChunks = [];
let mediaStream = null;

// --- Helpers ---
function showStep(stepId) {
  [step1, step2, step3].forEach((el) => el.classList.remove("active"));
  if (stepId === "step1") step1.classList.add("active");
  if (stepId === "step2") step2.classList.add("active");
  if (stepId === "step3") step3.classList.add("active");
}

function setStatus(message) {
  statusDiv.textContent = message || "";
}

// --- Audio recording ---
async function ensureMediaRecorder() {
  if (mediaRecorder) return;

  if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
    setStatus("Your browser does not support audio recording.");
    throw new Error("getUserMedia not supported");
  }

  try {
    mediaStream = await navigator.mediaDevices.getUserMedia({ audio: true });
    mediaRecorder = new MediaRecorder(mediaStream);

    mediaRecorder.addEventListener("dataavailable", (event) => {
      if (event.data.size > 0) {
        audioChunks.push(event.data);
      }
    });

    mediaRecorder.addEventListener("stop", () => {
      const audioBlob = new Blob(audioChunks, { type: "audio/webm" });
      audioChunks = [];
      sendAudioToBackend(audioBlob);
    });
  } catch (err) {
    console.error(err);
    setStatus("Could not access microphone. Please check permissions.");
    throw err;
  }
}

async function startRecording(event) {
  event.preventDefault();

  try {
    await ensureMediaRecorder();
  } catch {
    return;
  }

  if (mediaRecorder.state === "inactive") {
    audioChunks = [];
    mediaRecorder.start();
    recordBtn.classList.add("recording");
    setStatus("Recording... release the button when you finish speaking.");
  }
}

function stopRecording(event) {
  event.preventDefault();

  if (mediaRecorder && mediaRecorder.state === "recording") {
    mediaRecorder.stop();
    recordBtn.classList.remove("recording");
    setStatus("Processing your sentence...");
  }
}

// --- Backend calls ---
async function sendAudioToBackend(audioBlob) {
  const formData = new FormData();
  formData.append("audio", audioBlob, "recording.webm");

  try {
    const response = await fetch("/api/voice-turn", {
      method: "POST",
      body: formData,
    });

    if (!response.ok) {
      throw new Error(`Backend error: ${response.status}`);
    }

    const data = await response.json();

    // Update Step 2 content
    originalSentenceP.textContent = data.original_sentence;
    correctedSentenceP.textContent = data.corrected_sentence;
    explanationTextP.textContent = data.explanation;

    // Update follow-up message for future Step 1 visits
    currentFollowUpMessage = data.reply;
    agentMessageP.textContent = currentFollowUpMessage;

    // Go to Step 2
    showStep("step2");
    setStatus("Feedback ready.");
  } catch (err) {
    console.error(err);
    setStatus("Error contacting backend. Please try again.");
  }
}

async function requestSummary() {
  setStatus("Requesting summary...");

  try {
    const response = await fetch("/api/summary", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ dummy: true }),
    });

    if (!response.ok) {
      throw new Error(`Backend error: ${response.status}`);
    }

    const data = await response.json();

    // Populate lists
    summaryMistakesUl.innerHTML = "";
    summaryActivitiesUl.innerHTML = "";

    (data.main_mistakes || []).forEach((m) => {
      const li = document.createElement("li");
      li.textContent = m;
      summaryMistakesUl.appendChild(li);
    });

    (data.activities || []).forEach((a) => {
      const li = document.createElement("li");
      li.textContent = a;
      summaryActivitiesUl.appendChild(li);
    });

    showStep("step3");
    setStatus("Summary loaded.");
  } catch (err) {
    console.error(err);
    setStatus("Error fetching summary. Please try again.");
  }
}

// --- Event listeners ---
// Click & hold behavior (mouse + touch)
recordBtn.addEventListener("mousedown", startRecording);
recordBtn.addEventListener("mouseup", stopRecording);
recordBtn.addEventListener("mouseleave", stopRecording);
recordBtn.addEventListener("touchstart", startRecording);
recordBtn.addEventListener("touchend", stopRecording);

// Step 2 buttons
continueBtn.addEventListener("click", () => {
  // Go back to Step 1 with latest follow-up message
  agentMessageP.textContent = currentFollowUpMessage;
  showStep("step1");
  setStatus("");
});

finishBtn.addEventListener("click", () => {
  requestSummary();
});

// Step 3 button
newSessionBtn.addEventListener("click", () => {
  // Reset minimal state for a new session if you want
  currentFollowUpMessage = "Hello, I am your personal English teacher.";
  agentMessageP.textContent = currentFollowUpMessage;
  showStep("step1");
  setStatus("");
});

// Initial step
showStep("step1");
setStatus("");
