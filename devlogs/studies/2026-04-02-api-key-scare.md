# Devlog: Zero Friction and the "API Key Scare" 🚀

**Date:** April 2, 2026

Another piece of feedback from the Hack Club review process hit hard today.

**The Problem:**
Voter #5 said:
> "I mean I could not use it because I don't have NASA's or Gemini's API Key..."

This one hurt because **I had already built an offline demo mode precisely for this reason!** But my UX failed. When the user ran the app without a `.env` file, the very first thing I printed was a giant red warning: `⚠️ Warning: NASA_API_KEY not found. Please create a .env file...`

Of course they got scared and thought the app was broken. They didn't even try to proceed to see the demo mode kick in.

**The Fix:**
I opened `astrolab/cli.py` and completely rewrote the `check_env()` function. It no longer throws a red error. Instead, it gently informs the user:
`Notice: API keys not found in .env. Falling back to Smart Offline Demo Mode. You can test the app's full capabilities without keys!`

I also removed the warning triangle emoji to make it look less like a critical failure. The lesson here? If you build a fallback, make sure your users actually know it exists and feel encouraged to use it. UX is everything in CLI tools.