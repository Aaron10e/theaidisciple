# -*- coding: utf-8 -*-
"""FAQ content. Rendered into HTML <details> and into FAQPage JSON-LD from one source."""

# (question, answer_html, show_on_homepage)
FAQS = [
    ("What does an AI consultant actually do?",
     "<p>An AI consultant finds the specific tasks in your organization that artificial intelligence can "
     "reliably take over, builds those workflows, and trains your staff to run them. In practice my work "
     "breaks into four parts: an assessment of how your team spends its week, a design and build phase for "
     "the three to five workflows worth automating, hands-on training with your actual staff, and ongoing "
     "support once it is live.</p>"
     "<p>What it is not: selling you software, running a generic prompt webinar, or telling you that AI will "
     "transform your business. Most of the value comes from unglamorous work &mdash; quoting, reporting, "
     "research, drafting, scheduling, translation and data clean-up.</p>", True),

    ("Do I need to be technical to work with you?",
     "<p>No. Most of my clients are business owners, office managers, pastors and nonprofit directors with no "
     "technical background at all. I explain things in plain English, and the workflows I build are designed "
     "so that a non-technical person on your staff can run them every day without help.</p>"
     "<p>My own background is technical &mdash; 35 years of professional software development &mdash; but that is "
     "there so you do not have to be.</p>", True),

    ("What size organizations do you work with?",
     "<p>Small and medium organizations, typically between 2 and 200 people. That includes independent "
     "businesses, professional practices, churches, schools and nonprofits. I am deliberately built for "
     "organizations that do not have an IT department and cannot justify a large consulting firm.</p>", True),

    ("How much does AI consulting cost?",
     "<p>Pricing depends on scope, so I quote each engagement individually after the free call. What I can tell "
     "you up front is the structure: engagements begin with a paid assessment, project work is quoted as a "
     "fixed scope, and ongoing help runs as a monthly retainer with a meaningful discount for agreements of "
     "six months or longer.</p>"
     "<p>The free 20-minute call is genuinely free and you will get a realistic cost range on it. I would rather "
     "tell you the number early than waste both our time.</p>", True),

    ("Where are you located, and do you work remotely?",
     "<p>I am based in Fresno, California, and work in person with organizations across Fresno, Clovis and the "
     "wider Central Valley. Everything else &mdash; assessments, workflow build, training sessions and retainer "
     "support &mdash; works over video call, and I have clients and collaborators outside the United States, "
     "including in Kenya and Pakistan.</p>", True),

    ("What kinds of tasks can AI realistically take off my plate?",
     "<p>The tasks that work best share three traits: they repeat, they follow a pattern, and a human can check "
     "the result quickly. Common examples from real engagements:</p>"
     "<ul>"
     "<li>Drafting quotes, proposals, invoices and follow-up emails from a template</li>"
     "<li>Summarizing long documents, contracts, reports and meeting notes</li>"
     "<li>Market and competitor research that used to eat a full afternoon</li>"
     "<li>Turning one piece of content into newsletter, social and website versions</li>"
     "<li>Cleaning up, reformatting and cross-checking spreadsheet data</li>"
     "<li>Translating material for bilingual congregations and communities</li>"
     "<li>Writing first drafts of policies, job descriptions and training material</li>"
     "</ul>"
     "<p>Tasks that do not work well: anything requiring a legally binding judgment, anything where being "
     "confidently wrong is expensive and hard to spot, and anything that depends on information the model has "
     "no access to.</p>", True),

    ("We already tried ChatGPT and it did not really help. What is different?",
     "<p>This is the most common thing I hear, and it is almost never a tool problem. Somebody on staff used "
     "ChatGPT for a week, got a few impressive answers and a few embarrassing ones, and quietly went back to "
     "the old way.</p>"
     "<p>A workflow that actually sticks needs five things a casual chat session does not have: a defined input, "
     "a tested prompt, a place the output goes, a person who owns it, and a check that catches it when it is "
     "wrong. Building those five things is most of what I do.</p>", True),

    ("Is my company's data safe if we use AI?",
     "<p>It depends entirely on which tool you use and how it is configured, and this is worth getting right "
     "before you start. Consumer accounts and business accounts of the same product often have completely "
     "different data-retention and training policies.</p>"
     "<p>Part of every engagement is a plain-language review of what data is going where, which tools are "
     "appropriate for sensitive material, what should never be pasted into a chat window, and a short written "
     "usage policy your team can actually follow. If you handle medical, financial or minors' data, we design "
     "around that from the start.</p>", False),

    ("Will AI replace my employees?",
     "<p>In the organizations I work with, no &mdash; and I would be suspicious of any consultant who promises "
     "it will. What changes is the mix of work. The repetitive, low-judgment portion of a role shrinks, and the "
     "part that needs a person who knows your customers grows.</p>"
     "<p>Practically, that usually means your staff stop spending Friday afternoon on paperwork. I have never "
     "run an engagement where the goal was headcount reduction, and I am not interested in one.</p>", False),

    ("How long before we see results?",
     "<p>The assessment happens within a week or two of the first call. The first working workflow is usually "
     "live within two to four weeks of that, because I deliberately start with the highest-value, lowest-risk "
     "task rather than trying to change everything at once.</p>"
     "<p>Broader adoption &mdash; the point where AI is a normal part of how the team works rather than a "
     "project &mdash; typically takes three to six months.</p>", False),

    ("Which AI tools do you recommend?",
     "<p>I am not a reseller for anyone, so the honest answer is: whichever tool fits your budget, your data "
     "requirements and your team's habits. In practice I work across the major assistants and models, plus "
     "purpose-built tools for video, image, transcription and automation.</p>"
     "<p>I will usually recommend fewer tools than you expect. Two well-adopted tools beat seven half-used "
     "subscriptions every time.</p>", False),

    ("Do you work with churches and nonprofits specifically?",
     "<p>Yes, and it is a large part of the practice. Churches and nonprofits usually have the same "
     "administrative load as a business with a fraction of the staff, which makes them an unusually good fit "
     "for this work: sermon and lesson preparation support, bulletin and newsletter production, grant and donor "
     "communication, volunteer scheduling, translation for bilingual congregations, and media production.</p>"
     "<p>I also bring a Christian perspective when it is relevant, with a strong emphasis on verifying what a "
     "model tells you against actual sources rather than trusting it.</p>", False),

    ("Do you build websites and software as well?",
     "<p>Yes. I spent 35 years as a professional software developer, working in C#, ASP.NET, Angular and modern "
     "web technologies. That comes up more often than you would think, because an AI plan frequently runs into "
     "an aging system, a broken form or a website that nobody can update.</p>"
     "<p>I take on website modernization and custom development work either on its own or as part of a wider AI "
     "engagement.</p>", False),

    ("What is your background?",
     "<p>Thirty-five years of professional software development and five years working hands-on with generative "
     "AI, including AI consulting work at IBM. Alongside the consulting practice I produce AI-assisted "
     "educational video &mdash; 84 films published so far in English and Urdu &mdash; which is where a lot of my "
     "production workflow experience comes from.</p>"
     "<p>The full story is on the <a href=\"/about.html\">about page</a>.</p>", False),

    ("Do you offer training for our whole staff?",
     "<p>Yes. Training runs in three formats: a half-day introductory workshop for the whole team, focused "
     "role-specific sessions for the people who will use AI daily, and short follow-up clinics a few weeks "
     "later once real questions have surfaced. The follow-up clinics matter more than people expect &mdash; "
     "that is where adoption is usually won or lost.</p>"
     "<p>All training uses your real work, not generic examples.</p>", False),

    ("Do you work in languages other than English?",
     "<p>Yes. I regularly produce and review material in Urdu alongside English, and have produced Swahili "
     "content for partners in Kenya. For bilingual congregations, schools and community organizations, "
     "translation and dual-language publishing is one of the fastest wins AI offers.</p>", False),

    ("What happens to the workflows if we stop working together?",
     "<p>They keep running. Everything I build is documented and taught to your team, and it lives in your "
     "accounts, not mine. I am explicitly trying to make myself unnecessary for day-to-day operation &mdash; "
     "the retainer exists for new questions, not for keeping the lights on.</p>", False),

    ("Do you work with churches?",
     "<p>Yes. Churches, ministries and Christian nonprofits are a core part of the practice, not a sideline. "
     "That covers two different things: video production &mdash; narrated Scripture films, teaching series, "
     "children's Bible material, testimony and appeal films &mdash; and practical AI help for the church office, "
     "from turning one sermon into every format you publish, to translation for partner congregations, to a "
     "written rule about what must never be typed into a chat window.</p>"
     "<p>Churches that are just getting started also get real things at no charge: the free AI training course, "
     "the free children's Bible library, a free consultation and an honest answer about whether AI helps you at "
     "all. There is a full page on <a href=\"/for-churches.html\">working with churches</a>.</p>", True),

    ("What is a narrated Scripture film?",
     "<p>A narrated Scripture film tells a Bible event in the voice of a witness to it &mdash; Moses recounting "
     "creation or the flood, John describing what he saw on Patmos &mdash; while the visuals carry the scene. It "
     "is not actors performing a play, and it is not a sermon. It is a visual aid designed to run behind or "
     "alongside the message a pastor is already preaching, so a congregation sees the story instead of only "
     "hearing about it.</p>"
     "<p>They are produced as single films or as multi-week series, in English, Urdu or another language, with "
     "short cut-downs for social media. You can watch finished examples on the "
     "<a href=\"/for-churches.html\">for churches page</a>.</p>", False),

    ("Can you make videos for our church?",
     "<p>Yes. Tell me the passage and what you want people walking out with, and I will write a script for you "
     "to approve before anything is produced. Then narration, visuals, music, captions and thumbnails, delivered "
     "as files you own and can run from ProPresenter, YouTube or a projector, with one round of revisions "
     "included.</p>"
     "<p>The proof is public: 471 videos produced and published in the last nine months, including narrated "
     "Genesis and Revelation series, true-story biographies, archaeology explainers and 84 animated Bible "
     "stories for children. Start with the free call &mdash; there is no charge to talk about it.</p>", False),

    ("Is the free AI training really free?",
     "<p>Yes. There is no fee, no card, no subscription and no trial that turns into a bill. It is a beginner "
     "course &mdash; <em>AI basics for total beginners</em> &mdash; open to anyone regardless of whether you will "
     "ever be a client: business owners, church staff, students, job seekers, retirees, volunteers.</p>"
     "<p>Six short lessons cover what AI actually is, your first hour with it, how to ask so you get something "
     "usable, how to catch a confident mistake, what should never be typed into a chat window, and how to turn "
     "it into one habit that sticks.</p>", False),

    ("How do I get the free AI training videos?",
     "<p>Send a request through the <a href=\"/contact.html?interest=training\">contact form</a> and choose "
     "<strong>Free AI training</strong> from the dropdown. Aaron emails you a private link to the videos "
     "personally, normally within one business day.</p>"
     "<p>The reason it goes through the form rather than a download button is so the link comes from a real "
     "person you can write back to with questions. Your email is used to send the link and answer you &mdash; "
     "there is no list and no newsletter unless you ask for one. Details are on the "
     "<a href=\"/free-training.html\">free training page</a>.</p>", True),

    ("How do we get started?",
     "<p>Book the free 20-minute call. Come with one honest answer to one question: what does your team keep "
     "doing by hand that everyone quietly hates? That is almost always where the first workflow lives.</p>"
     "<p>You can <a href=\"/contact.html\">book a call here</a> or email "
     "<a href=\"mailto:aaron@theaidisciple.com\">aaron@theaidisciple.com</a>.</p>", True),
]
