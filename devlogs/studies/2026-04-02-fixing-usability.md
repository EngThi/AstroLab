# Devlog: Fixing the "APOD Confusion" in the Quiz 🛠️

**Date:** April 2, 2026

So, I got some really honest feedback from the Hack Club reviewers on my first submission. A lot of people got confused by the Quiz flow.

**The Problem:**
Voter #12 pointed out something I completely missed:
> "My choice would be 2, wanting the space quiz, but then it'd go to fetch the picture of the day, so I'm not quite sure what's going on there..."

When you selected option 2 (Take a Space Quiz), the first thing the CLI did was print "Fetching Astronomy Picture of the Day...". To a new user, it looked like the app bugged out and ran option 1 instead!

**The Fix:**
I went into `astrolab/quiz.py` and changed the UX text. Instead of just "Fetching APOD", it now explicitly tells the user *why* it's doing that:
`"Fetching today's NASA APOD data to use as study context for your quiz..."`

It's a tiny string change, but it completely fixes the mental model for the user. They now understand the quiz is dynamically generated *from* today's picture.

I also toned down the terminal output colors and emojis a bit. Sometimes less is more when you want a tool to feel like a real developer utility rather than a toy.