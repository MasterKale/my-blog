+++
title = "An AI-skeptical senior engineer's guide to making the most of Claude"
date = "2026-03-02T23:35:24.203Z"
description = "I'm reluctantly coming around to AI. Here's some ideas that Claude gave me on how best to use it while keeping a human (me) in the loop."
categories = ["ai", "claude"]
keywords = []
hasCode = false
+++

I've been largely hands-off with LLMs after testing the waters from time to time and not finding much utility in [tech that can inherently lie to you](https://en.wikipedia.org/wiki/Hallucination_(artificial_intelligence)). Anthropic's Claude series of models became unexpectedly, incredibly capable sometime back in November or December (just as my second kid was born so no wonder I missed the news), especially compared to previous times I'd used it.

After vibe-coding an iOS passkey provider app into existence at work last week with Claude Opus 4.6 and just a few hours of effort, it seemed worthwhile to finally put some skin in the game for my own personal use. It also felt prudent to explore this as leadership across the tech industry demands more and more adoption of AI, even if [there are lots of signs of it being a bubble](https://www.wired.com/story/ai-bubble-will-burst/)...

So one of the first things I did after ponying up $20 to Anthropic was to ask **Claude Sonnet 4.6** about how to "make the most of my Claude Pro subscription."

One of my goals of adopting Claude is not for automating the creation of code but to use it as a tool to augment my expertise. When I talked with Claude I wanted to validate the idea that I might use it as an elaborate rubber duck. Could I use it to, say, analyze a higher-level feature proposal I'd draft first in response to a GitHub issue, and then have Claude draft a plan of what parts of the codebase need to change to solve the issue? Then I could actually implement the plan to remain hands-on-keyboard and stave off what's being deemed "[cognitive debt](https://margaretstorey.com/blog/2026/02/09/cognitive-debt/)" (i.e. the inability to explain how "the system" works because you're no longer involved in its authoring) for as long as possible.

I got what _I_ think were some decent tips out of it, about how I could shift my mindset to think of Claude as "a force multiplier rather than a replacement for \[my\] thinking." And when I asked, Claude generated a somewhat-janky-but-serviceable one-pager PDF with a summary of its advice that I could print out and stick on the wall at my desk. I'll be exploring most of these ideas as I explore Claude further, and having a visual reminder like this off-screen will be useful for me as I make progress.

When I showed the PDF to a few people, they quickly asked if they could share it with others in their orbit to help them with their own LLM adoption journeys. I decided then to post the PDF publicly if it really could help other skeptical senior software engineers to reluctantly embrace AI. So here is the PDF for everyone's enjoyment:

## Claude for Software Engineers (PDF)

Presented exactly as Claude created it:

<object data="claude-for-software-engineers-cheatsheet-sonnet-4.6.pdf" type="application/pdf" width="100%" height="500px">
  <p>Couldn't render PDF.</p>
</object>

<p style="text-align: center; margin-top: 0;">
<a href="claude-for-software-engineers-cheatsheet-sonnet-4.6.pdf" style="display: inline-block; margin: auto">(Click to download PDF)</a>
</p>


## Full Chat Transcript

Here's the full chat I had with Claude Sonnet 4.6 that led to the generation of the PDF above, for those who are interested in reading the entire conversation that occurred beforehand.

Link: https://claude.ai/share/07194ef9-cd71-41b4-a72d-229cbda5dbad

> **Me**
>
> I'm an AI skeptic who has reluctantly come around to the idea of using AI as a tool for software engineering. As far as skill level goes, I've got 16 years writing web apps primarily, but have also spent most of my life programming as a hobby. What are some tips on how to make the most of my Claude Pro subscription? I'm looking for workflow suggestions that will keep me involved in the actual code because I'm terrified of eventually not being able to understand my own open-source library codebases if I start liberally vibe coding when I make changes to them.

<p></p>

> **Claude**
>
> Your concern is legitimate and well-founded — the "skill atrophy through delegation" problem is real. Here's how I'd approach Claude as a force multiplier rather than a replacement for your thinking:
> 
> **Use Claude for the tedious, not the thoughtful**
>
> With 16 years of web app experience, your most valuable asset is your architectural intuition and domain knowledge. Protect that. Let Claude handle:
> 
> - Boilerplate and scaffolding you already know how to write
> - Writing tests for code you wrote
> - Converting types/interfaces between formats
> - Writing documentation and changelogs from your diffs
> - Regex and string manipulation one-offs
> 
> **Treat Claude like a very fast junior dev, not an oracle**
> 
> Your mental model matters here. Don't ask "how should I architect this?" Ask "implement X using approach Y, with these constraints." You stay the decision-maker. Claude executes. If you let Claude make architectural choices in your open-source libraries, you'll end up maintaining code you didn't design and don't fully trust.
> 
> **Require explanations for anything non-obvious**
> 
> When Claude produces something you don't immediately understand — ask it to walk through the logic. Don't accept code that surprises you. If you can't explain every line in a PR to a contributor, it shouldn't go in. This also catches hallucinated APIs before they bite you.
> 
> **Write the hard parts yourself first, then ask for help**
> 
> For core logic changes, write your own rough implementation first, even if it's ugly. Then ask Claude to review it, suggest improvements, or help you refactor. This keeps the thinking yours and uses Claude's strength (pattern recognition, syntax, edge case awareness) without outsourcing your reasoning.
> 
> **Use Claude heavily for context-switching tax**
> 
> Coming back to a codebase after two weeks away? Paste in the relevant files and ask Claude to summarize the current state, recent decisions, or how a particular module works. This is low-risk and high-value — Claude is reading code you wrote, synthesizing it for you.
> 
> **Code review your own Claude output, seriously**
> 
> Read everything Claude writes as if it were a PR from someone you don't yet trust. Ask: does this fit the existing patterns in my codebase? Is this idiomatic? Does this handle errors the way I handle errors? Your library's code style and philosophy is something Claude doesn't know — you do.
> 
> **Keep a "Claude touched this" commit discipline**
> 
> Some people find it useful to either note in commits when Claude was heavily involved, or to review those PRs with extra scrutiny before merging. This helps you stay accountable and keeps you reading the code carefully.
> <hr>
> The underlying principle: Claude should make you faster at what you already know how to do, not a stranger in your own codebase. The moment you feel like you're merging code you wouldn't have been able to write yourself, that's the line to pull back from.

<p></p>

> **Me**
>
> Can I meaningfully solicit feedback from Claude on a potential solution I've brainstormed? Or will I get sycophantic validation whether the solution is good or not?

<p></p>

> **Claude**
>
> You can get genuine critical feedback, but you have to ask for it correctly — the sycophancy risk is real and your skepticism is warranted.
> 
> **The default behavior leans validating.** If you say "I'm thinking of doing X, what do you think?" you'll often get "Great approach! Here are a few minor considerations..." even when X has serious problems. This is a known failure mode, not a feature.
> 
> **What actually works:**
> 
> Ask adversarially. Instead of "what do you think of this approach?" try:
> 
> - "What are the strongest arguments against this approach?"
> - "Steelman the case for doing this a completely different way."
> - "What would have to be true for this to be a bad idea?"
> - "What are the non-obvious failure modes here?"
> 
> Separate the phases. First ask for critique only, explicitly telling Claude not to offer solutions yet. Once you've heard the objections, you can decide whether they're fatal. If you ask for feedback and alternatives in one shot, Claude tends to bury the critique inside a helpful reframe.
> 
> Give Claude something to push against. The more specific your proposal, the better the feedback. Vague ideas get vague encouragement. A concrete design with actual constraints and tradeoffs gives Claude enough to find real problems.
>
> Tell Claude your prior. If you say "I'm pretty confident this is right" you'll get more pushback than if you say "I think this might work" — counterintuitively. Stating confidence signals that you want your certainty tested.
>
> **The honest ceiling:** Claude is better at finding problems with concrete technical proposals than evaluating subtler things like "is this the right abstraction for this library's philosophy?" — that requires knowing your codebase, your users, and your taste in ways Claude doesn't. For that kind of judgment, your skepticism about AI feedback is probably correct and human reviewers who know your project are worth more.
>
> But for "here's my proposed algorithm / data structure / API shape / error handling strategy — what's wrong with it?" Claude can be a genuinely useful devil's advocate if you frame it that way explicitly.

<p></p>

> **Me**
>
> Can you generate a single-page PDF of this advice, bullet point style as a kind of Claude cheat sheet I could print out and stick on the wall?

<p></p>

> **Claude**
>
> There's your wall-ready cheat sheet — two-column layout covering all eight principles from our conversation, print it at 100% for a clean letter-size sheet.
>
> [Claude cheatsheet (PDF)](claude-for-software-engineers-cheatsheet-sonnet-4.6.pdf)
