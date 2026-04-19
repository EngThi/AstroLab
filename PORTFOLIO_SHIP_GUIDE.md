# 🚀 Ultimate Portfolio Ship Guide
**Goal:** Achieve "Zero Friction" for US Reviewers across all Hack Club Submissions.

## The "Zero Friction" Standard
Every project submitted must adhere to these 3 pillars to pass a US reviewer's test:
1.  **Global Accessibility (i18n):** All CLI output, UI, and `README.md` must be in impeccable English. No exceptions.
2.  **Instant Onboarding:** The reviewer should never have to manually create a `.env` file, generate API keys, or run `pip install -r requirements.txt`.
    *   *For Python:* Must be published on PyPI (`pip install project-name`).
    *   *For Node.js/Web:* Must have a live URL or an incredibly simple `npx` command.
3.  **Smart Fallback (Demo Mode):** If a project relies on external APIs (NASA, Gemini, OpenAI), it **must** have a local cache or mock data that loads automatically when keys are missing. The app should never crash or throw an exception on first run.

---

## 🛠️ Project-by-Project Upgrade Plan

### 1. AstroLab 🌟 (Status: SHIPPED & PERFECT)
*   **Repo:** https://github.com/EngThi/AstroLab
*   **Current State:** 100% compliant with the Zero Friction Standard. Published on PyPI, fully translated, features a rich interactive menu, and includes a `demo_cache.json` for offline review.
*   **Action Needed:** None. Ready for final evaluation.

### 2. Opportunity Aggregator
*   **Repo:** https://github.com/EngThi/opportunity-aggregator
*   **Current State:** High Friction. Entirely in Portuguese. Requires manual setup of scrapers and API keys.
*   **The "Ship" Plan (30 mins):**
    *   Translate `README.md` and terminal outputs to English.
    *   Package for PyPI as `opp-aggregator`.
    *   **Crucial Fix:** Create a `demo_jobs.json` file. If the Gemini API key is missing for the "scorer", it should output 3 high-quality fake Tech job listings automatically so the reviewer sees the UI working instantly.

### 3. CLI Problem Solver
*   **Repo:** https://github.com/EngThi/cli-problem-solver
*   **Current State:** Low Friction. Great English README and demo video. Still requires manual cloning and setup.
*   **The "Ship" Plan (20 mins):**
    *   Package for PyPI as `cli-problem-solver`.
    *   Ensure the AI explanation feature has a hardcoded, witty fallback response if the API key isn't found, rather than crashing.

### 4. AI Video Factory
*   **Repo:** https://github.com/EngThi/ai-video-factory
*   **Current State:** High Friction (Node.js). English README, but explicitly warns that TTS (Text-to-Speech) will fail without an API key.
*   **The "Ship" Plan (40 mins):**
    *   **Crucial Fix:** Include a pre-rendered 10-second `demo_audio.mp3` and `demo_video.mp4` in the repository. Modify the script so that if `--demo` is passed (or keys are missing), it bypasses the API calls and just stitches the demo assets together to prove the FFMPEG pipeline works locally.

### 5. OmniLab
*   **Repo:** https://github.com/EngThi/OmniLab
*   **Current State:** Medium Friction. Mixed PT/EN. Missing promised visual assets.
*   **The "Ship" Plan (30 mins):**
    *   Translate the entire README to English.
    *   Remove the broken placeholder GIF (`https://via.placeholder.com...`) and replace it with a real screen recording of the terminal interface.
    *   If it's Python, package it for PyPI.

### 6. Voice Task Master
*   **Repo:** https://github.com/EngThi/voice-task-master
*   **Current State:** Incomplete. One-line README.
*   **The "Ship" Plan (45 mins):**
    *   Write a complete, professional English README explaining the architecture.
    *   **Crucial Fix:** Voice recognition (Speech-to-Text) libraries are notoriously buggy across different OS audio drivers. Add a `--text-mode` or interactive fallback so a reviewer without a working microphone setup can still test the task logic by typing.

### 7. HOMES (and HOMES-Engine)
*   **Repo:** https://github.com/EngThi/HOMES
*   **Current State:** High Friction. Portuguese docs. Complex setup (`bash setup.sh`).
*   **The "Ship" Plan (1 hour):**
    *   Consolidate the documentation. Translate everything to English.
    *   Instead of making reviewers run a heavy automation suite, provide a comprehensive architectural diagram (e.g., Mermaid.js) in the README and a link to a YouTube video demonstrating the full pipeline in action. Focus the repository on being a "Showcase" rather than a 1-click install, given its complexity.

### 8. NerveOS
*   **Repo:** https://github.com/EngThi/NerveOS
*   **Current State:** Private or Empty.
*   **The "Ship" Plan:**
    *   If this is hardware/Rust related: Add a Wokwi simulation link to the README so reviewers can run the firmware directly in their browser without installing Rust or flashing a board.
