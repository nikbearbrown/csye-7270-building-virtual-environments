# Releasing Games in 2026: Channels, AI Rules, and Who Actually Gets Paid

*Current as of November 3, 2026. Several of these policies changed in the past year, so re-check the live terms before any submission. Not legal advice.*

## The short version

You framed this as two AI questions (code and assets), but the stores split it three ways: AI that helps you **write code**, AI that **makes assets you ship**, and AI that **generates content while the game runs**. AI-written code is now a non-issue on almost every storefront. Shipped AI assets need disclosure on Steam, on itch.io (strictly for asset packs), and on Fab, and essentially nowhere else. Runtime generation, such as an LLM character or live image or voice synthesis, is where every platform that has rules puts its strictest ones.

On money: the median Steam game released in 2025 grossed a few hundred dollars, two in three grossed under $1,000, and roughly one in twelve cleared $100,000.

## 1. Where you can release

| Channel | What it is | Store cut | Gate to entry |
|---|---|---|---|
| Steam (Valve) | Dominant PC store | 30%, dropping to 25% after $10M and 20% after $50M | $100 Steam Direct fee per game, refunded once the game reaches $1,000 in adjusted gross revenue |
| Epic Games Store | Second-largest PC store | 0% on the first $1M per app per year (since June 2025), then 12% | Self-publishing portal with review |
| itch.io | Open indie store, also a major asset-pack market | Developer chooses; default 10%, can be 0% | Essentially open |
| GOG | Curated, DRM-free PC store | Typically 30% | Must be accepted by GOG's curation |
| Microsoft Store (PC) / Xbox | Windows store; Xbox console via ID@Xbox | 12% for PC games; console typically 30% | Partner Center account; ID@Xbox application for console |
| PlayStation Store | Console | Typically 30%; terms under NDA | Partner program approval, dev kits, certification |
| Nintendo eShop | Console | Typically 30%; terms under NDA | Developer portal approval, dev kits, lot check |
| Google Play | Android | 15% on the first $1M per year, then 30% | One-time registration fee; policy review |
| Apple App Store | iOS/macOS | 15% under the Small Business Program, otherwise 30% | Annual developer fee; App Review |
| Meta Horizon Store | Standalone VR | Typically 30% | Curated |
| Fab (Epic) | **Asset** marketplace, not a game store | 88/12 split | Seller account |

**On "Unreal Marketplace":** it no longer exists. Fab replaced it in October 2024 and also absorbed the Sketchfab store, ArtStation Marketplace, and Quixel. Fab is where you'd sell Blender models, environments, or code templates, not games. If you ship a *game* built in Unreal, the engine royalty is a separate obligation from any store cut. As far as I know it's 5% of lifetime gross above $1M per product, with a reduced rate if you also launch on the Epic Games Store; verify against the current Unreal EULA before relying on that.

**On Godot and consoles:** Godot has no official console export. Console SDKs are under NDA, so an open-source project legally can't ship console export templates. The only console Godot supports directly is Steam Deck, through the Linux export. For Switch, Xbox, and PlayStation you either hire a porting house (Lone Wolf, Pineapple Works, Sickhead, and others) or license W4 Games' "W4 Consoles" middleware, which was built by former Godot project leads. W4 runs an education program that gives universities and colleges free access to its console export tools for non-commercial academic use.

## 2. The AI rules, platform by platform

| Platform | AI-assisted code | AI assets you ship | AI generated at runtime |
|---|---|---|---|
| Steam | Exempt since January 2026 | Must disclose; shown on the store page | Must disclose and describe your guardrails; players can report through the overlay |
| Epic Games Store | No rule | No rule | No public rule |
| itch.io | Code is one of the disclosure categories | Mandatory for asset pages; the field is available for games | Same disclosure field |
| Fab | Unclear for code templates | Must tag "CreatedWithAI" when a material portion is AI-generated | Not applicable |
| Microsoft Store / Xbox | No rule found | No separate rule found | Policy 11.16: disclose, keep output within policy, offer reporting |
| PlayStation / Nintendo | No public rule | No public rule | No public rule |
| Google Play | No rule | No rule | AI-Generated Content policy applies if generation is a central feature |
| Apple App Store | Not reviewed | No explicit rule found | Disclosure and consent before personal data goes to third-party AI |

### Steam (Valve)

Valve rewrote the AI section of its Content Survey around January 16–17, 2026. The disclosure now focuses on content players actually see, hear, or interact with. Coding assistants, debugging tools, and other efficiency tools are explicitly outside its scope. A game written entirely with an AI pair-programmer, but shipping hand-made art and human-written dialogue, needs no disclosure.

Two categories still require disclosure:

1. **Pre-generated content:** art, audio, voice, dialogue, localization, and store-page marketing assets created with AI and shipped with the game.
2. **Live-generated content:** anything produced by AI at runtime. Valve also asks how you prevent illegal output, and players can report AI content from inside the Steam overlay.

The disclosure appears in an "AI Generated Content Disclosure" section on the store page. As of September 2026 there was no official Steam tag or store filter for AI content. The disclosure also applies to updates and DLC, so a game released before the policy has to complete the survey when it next ships new content. Reported adoption is around one in five new releases, with more than 7,300 games disclosing by March 2026.

### Epic Games Store

The Epic Games Store has no AI disclosure requirement. Tim Sweeney has attacked Steam's rule repeatedly. In late 2025 he argued the labels were pointless because AI would be in nearly every game. On October 23, 2026 he escalated, calling Valve's policy "abhorrent" and arguing the label works as a political statement that exposes developers to backlash. Valve has kept the policy anyway. Don't expect Epic to adopt one.

### Fab (asset marketplace)

Sellers must tag content "CreatedWithAI" when a material portion of it, such as characters, backgrounds, or other key elements, was produced with generative AI. Tools that only operate on your own work, like content-aware fill, don't trigger the tag.

Enforcement has been weak. One seller uploaded tens of thousands of AI assets, many untagged. Epic responded by adding a generative-AI question to the publishing flow plus automated detection, but it declined to ban AI content. Community complaints that mislabeled assets go unpunished continue.

Separately, Epic commits not to use Fab content to train generative AI or license it for that purpose. Whether AI-*assisted code* in a Fab code template needs the tag is an open question that Epic's forums haven't resolved.

### itch.io

Since November 2024, asset creators must classify every public asset page for generative-AI use. The disclosure categories include graphics, sound, text, dialogue, and **code**. That makes itch.io the one store where AI-written code is a disclosure category. Asset pages that use AI without disclosing it are dropped from browse indexing. For games, the tag exists and is filterable, but reporting is mixed on whether it's enforced on game pages. Fill it in anyway.

### Microsoft Store and Xbox

Microsoft Store Policy 11.16, added in the October 2025 policy update, covers products whose content is generated live by AI in response to user input. Those products must:

- disclose live generative AI in the product metadata and in Partner Center at submission
- keep AI output within store policies
- give users a way to report inappropriate output

"Store" includes the Xbox-branded stores. I found no separate rule for AI assets made during development.

### PlayStation and Nintendo

Neither publishes an AI disclosure policy. Their certification requirements are under NDA, though, so "no public rule" doesn't mean "no rule." Once you're in their developer programs, ask your account manager.

### Google Play

Google's primary policy page covers apps where AI generation is a central feature: chatbots, image generators, and voice or video of real people. Developers must prevent restricted output and provide in-app flagging and reporting. It doesn't address AI used during development.

Some secondary sources describe a broader 2026 labeling mandate. I couldn't confirm that against Google's own policy pages, so check the Policy Center directly before you rely on either reading.

### Apple App Store

One reading of the June 2026 guidelines found that AI is named only once: guideline 5.1.2(i). That guideline requires you to disclose, and get explicit permission, before sending a user's personal data to a third-party AI service. How your app was written isn't part of review. Reviewers do apply the usual content-moderation expectations to AI output.

As with Google, some secondary sources claim broader AI-labeling rules. Treat those skeptically until you see them in Apple's current guidelines.

## 3. The legal layer underneath the stores

**EU AI Act, Article 50 (in force since August 2, 2026).** This applies regardless of which store you use, if you have EU players. Two parts matter for games:

- **Telling people they're talking to AI.** Players interacting with an AI system must be told so, unless it's obvious.
- **Deepfakes.** These are AI images, audio, or video that resemble real persons, objects, places, or events and would falsely appear authentic. They must be disclosed. The definition excludes clearly fantastical content.

For deepfakes inside evidently artistic, creative, or fictional works, the obligation is reduced: you disclose that such content exists, in a way that doesn't spoil the work. Commission guidance also suggests that ephemeral real-time content in games and VR may be exempt from machine-readable marking where marking is infeasible, as long as users are informed in the experience.

**US copyright.** Fully AI-generated assets get no copyright protection under the Copyright Office's January 2025 guidance. A game as a whole, with human authorship in its design, code, and arrangement, is still protectable. Individual AI-generated pieces may not be. For asset sales this matters more: you'd be licensing something you may not exclusively own, and a competitor could legally resell the same output.

## 4. How this lands on your current work

**MuseBot is the expensive part, not the Blender work.** An LLM guide that talks to visitors is runtime generative AI. It puts you in the heaviest regime on every platform that has rules:

- Steam's live-generated disclosure, with a description of your guardrails
- Microsoft Policy 11.16
- Google's AI-Generated Content policy, if the guide counts as a central feature
- Apple 5.1.2(i), if player voice or text goes to Claude's API
- EU Article 50, which requires telling players they're talking to an AI

None of these is hard to meet, but design for them from the start: an in-experience AI notice, a report button, a consent step before player input leaves the device, and logged guardrails.

**Muse-generated exhibit models need disclosure on Steam and a tag on Fab.** That's clear-cut. Buildings you construct by having Claude write Blender Python are a genuine gray zone. The geometry comes out of code an AI wrote, not out of an image or 3D generator. Steam's carve-out for efficiency tools arguably covers this, and Fab's "material portion generated with Generative AI Programs" language arguably doesn't. If you sell those buildings on Fab, the conservative move is to tag them. The cost is real: on Fab, the AI tag puts you in the most crowded and most distrusted part of the market.

**A photoreal Crystal Palace is closer to the EU deepfake definition than anything else you're making,** because it depicts a real historical place and real exhibits. It's plainly a reconstruction, so the reduced artistic and educational disclosure should cover it. A one-line note that some models are AI-assisted reconstructions is cheap insurance.

**The Claude-character platformer needs a trademark answer before any commercial release.** Building it as course reference code is one thing. Selling it, or putting it on a store page, means using Anthropic's brand, which requires Anthropic's permission no matter what any store's AI policy says.

**For CSYE 7270,** W4's education license could let students actually deploy their Godot projects to console hardware for coursework, which very few courses can offer.

## 5. Does anyone make money?

The best public data is Steam, from third-party estimators. Gamalytic's estimates for games released in 2025:

| Outcome (2025 Steam releases, gross revenue) | Share of games |
|---|---|
| Sold fewer than 100 copies | ~47% |
| Earned under $100 (less than the Steam Direct fee) | ~40% |
| Earned under $1,000 | ~66% |
| Earned over $100,000 | ~8% |
| Median gross revenue | ~$249 (October 2025 snapshot) |

The bottom 30% of games averaged about $37 in gross revenue. Alinea Analytics, using a different methodology, counted roughly 20,000 Steam launches in 2025, of which only about 300 crossed $1M. That's around 1.5%.

These are gross figures, before Valve's cut, refunds, and taxes. Gamalytic says its per-game estimates can be off by 30–50%, and it's least accurate for tiny games.

Two structural facts matter more than the medians:

1. **Steam is where the money is.** In 2025, third-party games earned an estimated $14.98B on Steam versus about $400M on Epic, a 37:1 ratio. Epic's 0% fee on the first $1M is a good deal on a much smaller audience.
2. **New releases get a shrinking share of Steam's revenue.** Alinea puts that share at 29% in the first half of 2024, 27% in the first half of 2025, and 21% in the first half of 2026. The back catalog takes the rest. You're competing with every game ever released, not just this year's.

Mobile has no comparably reliable public per-game data. Its free-to-play and ad-driven economics also make "revenue per game" a less meaningful measure.

## 6. Where I'd push back

**The "options" framing points at the wrong bottleneck.** Distribution is nearly free and nearly open; Steam costs $100 and itch.io costs nothing. The binding constraint is visibility. Choosing a store matters less than whether anyone is waiting for the game when it launches. "Steam plus itch.io, add Epic if it's cheap to do" is the default for a reason, and consoles only make sense once a PC release shows demand.

**AI disclosure is a market risk more than a policy risk.** No major PC or mobile store bans AI-made games. The real question is how buyers react to the label. Sweeney claims the label invites "hater" campaigns that damage sales, but that claim has been reported without supporting sales data. The honest position is that nobody has shown how much an AI disclosure costs a game, and the answer probably differs by genre and audience.

**The revenue statistics describe games, not developers, and they flatter neither side.** The bad numbers are inflated by a flood of low-effort releases, including asset flips and AI shovelware. A carefully built game with a pre-launch audience does much better than the median. But "much better than $249" can still be nowhere near a salary. If the goal is educational impact or a student portfolio, revenue is the wrong success metric, and a free itch.io or web release may serve it better than any paid store.

## Sources

- Steam January 2026 AI disclosure rewrite: [tbreak](https://tbreak.com/steam-ai-disclosure-policy-update-developers/), [Papo Games](https://papogames.com/en/blog/steam-ai-disclosure-2026), [Spritefy](https://spritefy.com/blog/steam-ai-disclosure), [Legal Moves Law Firm](https://legalmoveslawfirm.com/steam-ai-policy/)
- Sweeney vs. Steam, October 2026: [Notebookcheck](https://www.notebookcheck.net/Epic-CEO-Tim-Sweeney-lambasts-abhorrent-Steam-AI-Disclosure-Policy-claiming-labels-double-as-political-statement.1433682.0.html), [Game Rant](https://gamerant.com/steam-epic-games-ai-disclosure-irresponsible/)
- Epic Games Store 0% on first $1M: [PC Gamer](https://www.pcgamer.com/gaming-industry/following-its-huge-win-over-apple-epic-says-it-will-take-even-less-money-from-developers-who-use-its-store)
- Fab AI tagging and enforcement: [Unreal forums, AI policy](https://forums.unrealengine.com/t/ai-image-use/2567909), [80.lv](https://80.lv/articles/epic-games-adresses-ai-generated-content-plaguing-fab), [Fab announcement](https://gamefromscratch.com/epic-games-make-massive-fab-announcements/)
- itch.io disclosure: [Game Developer](https://gamedeveloper.com/production/itch-wants-asset-creators-to-disclose-when-they-ve-used-generative-ai), [PC Gamer](https://pcgamer.com/software/platforms/indie-distribution-platform-itch-io-now-requires-asset-creators-to-disclose-the-use-of-generative-ai-in-their-work), [Mobile Marketing](https://mobilemarketingmagazine.com/itch-io-mandates-genai-disclosure-for-creators/)
- Cross-platform overview: [The Conversation](https://theconversation.com/are-video-game-developers-using-ai-players-want-to-know-but-the-rules-are-patchy-274850)
- Microsoft Store Policy 11.16: [Neowin](https://www.neowin.net/news/microsoft-store-policies-updated-with-new-rules-on-generative-ai-child-safety-and-more/), [Asset Forge Index](https://assetforgeindex.com/policies/microsoft-store-xbox)
- Google Play AI-Generated Content policy: [Play Console Help](https://support.google.com/googleplay/android-developer/answer/14094294)
- Apple 5.1.2(i): [TechCrunch](https://techcrunch.com/2025/11/13/apples-new-app-review-guidelines-clamp-down-on-apps-sharing-personal-data-with-third-party-ai), [Newly](https://newly.app/guides/does-apple-accept-ai-generated-apps)
- Godot consoles and W4: [Godot docs](https://docs.godotengine.org/en/4.5/tutorials/platform/consoles.html), [W4 Consoles](https://www.w4games.com/w4consoles)
- EU AI Act Article 50: [GDPR Local](https://gdprlocal.com/eu-ai-act-article-50/), [William Fry](https://www.williamfry.com/knowledge/time-running-out-as-ai-transparency-guidelines-published/)
- AI assets and copyright: [Promise Legal](https://blog.promise.legal/ai-generated-assets-game-ip-disclosure/)
- Steam revenue distribution: [GamesRadar (Gamalytic)](https://www.gamesradar.com/games/over-5-000-games-released-on-steam-this-year-didnt-make-enough-money-to-recover-the-usd100-fee-to-put-a-game-on-valves-store-research-estimates/), [80.lv](https://80.lv/articles/analysts-report-drop-in-game-revenue-on-steam-despite-growing-number-of-releases), [Recognizing Patterns (Alinea, Gamalytic median)](https://recognizingpatterns.substack.com/p/valves-steam-revenue-is-an-estimate), [game-developers.org (Alinea)](https://game-developers.org/2025-steam-game-revenue-distribution)
