---
title: "SEO Optimization for a Website in 2026: A Practical Step-by-Step Guide"
published: true
description: "Technical SEO, content, speed, schema, links — what actually moves a site in Google in 2026. A step-by-step guide with real numbers from 70 pages of our own project."
tags: seo, webdev, marketing, productivity
canonical_url: https://uriy-as.org/en/blog/seo-optimization-guide.html
---

# SEO Optimization for a Website in 2026: A Practical Step-by-Step Guide

SEO is not a checklist you run once. It's a loop: fix what breaks, measure, fix the next thing. This guide is the order we actually work in — based on 70 pages of our own project, indexed and tracked in Google Search Console.

## Step 1: Technical audit before touching content

Before writing a single keyword, check what Google can even see:

- Does every page return 200? (Not 301-loops, not soft-404s)
- Is there exactly one `<h1>` per page?
- Is `sitemap.xml` present, valid, and submitted?
- Does `robots.txt` block anything you need indexed?
- Are there broken internal links?

On our project this caught **55 broken internal links** that nobody noticed for months. Fixing them took an hour; it changed how Google crawled the whole site.

## Step 2: Fix duplicate URLs — the most common silent killer

WordPress creates duplicates in two ways that look innocent:

1. The homepage with and without a trailing slash (`/` and `""`) — Google sees two pages with the same title and description.
2. Paginated URLs (`?paged=2`, `?paged=3`) canonicalised back to page 1 — Google sees every page as a copy of the homepage.

Both show up in Search Console as "Duplicate without user-selected canonical" or "Duplicate title and description header".

**The fix:**
- 301 redirect one variant of the URL to the other
- Set a hard `canonical` on the main version
- **Paginated pages must canonicalise to themselves**, not to page 1
- Add `rel=next` / `rel=prev` for the chain

One client lost 40% of their indexed pages to exactly this. A one-line canonical config would have saved them.

## Step 3: Metadata that earns the click

Your title is not a label — it's an ad. Rules that hold:

- **Title: 50-60 characters**, keyword near the front, one concrete number or benefit
- **Description: 120-160 characters**, the problem in the client's words, plus a reason to click
- Never duplicate: if title and description are identical across pages, Google downranks both

Compare:
- ❌ "SEO optimization services | WebStudio"
- ✅ "SEO Optimization for a Website in 2026: 7 Steps That Work"

The second one earns the click because it promises a specific outcome.

## Step 4: Speed — where most sites fail

Core Web Vitals are ranking inputs. The thresholds:

| Metric | Good | Needs work | Poor |
|---|---|---|---|
| LCP (largest paint) | ≤ 2.5s | 2.5-4s | > 4s |
| CLS (layout shift) | ≤ 0.1 | 0.1-0.25 | > 0.25 |
| INP (interaction) | ≤ 200ms | 200-500ms | > 500ms |

Cheapest wins, in order:
1. Compress images (WebP/AVIF, correct `width`/`height` to avoid CLS)
2. Defer non-critical JS
3. Preload the LCP image
4. Serve from a CDN

Our pages are **92-97 KB** total. That's why they load instantly on mobile data.

## Step 5: Schema.org — structured data that earns rich results

Add JSON-LD for the things Google actually rewards:

- `Article` / `BlogPosting` — for articles
- `FAQPage` — for Q&A blocks (can produce "People also ask" placement)
- `BreadcrumbList` — shows the path in search results
- `LocalBusiness` — for a business with an address
- `HowTo` — for step-by-step guides

JSON-LD (a `<script type="application/ld+json">` block) is the format to use. It stays valid even when the page design changes.

## Step 6: Internal linking — the cheapest traffic you own

Every article should link to 3-5 related pages, and every important page should be linked *to* from somewhere else on the site.

The rule that matters: **anchor text describes the target**, not the source. Link to your pricing page with "сколько стоит разработка сайта", not with "нажмите сюда".

We use 3-4 links per article with descriptive anchors — it keeps orphaned pages out of the index and distributes page authority.

## Step 7: Get links from outside (the part everyone skips)

On-page work caps out. Rankings need signals from other domains.

What worked for us:
- Publishing genuinely useful articles on platforms with existing authority (Dev.to, Medium, Habr) with a `canonical` pointing back to the site
- Answering real questions on Q&A platforms with a genuine profile link
- Getting a link from every client project — the site footer, the case study, the "built by" credit

We published 21 articles on Dev.to. They brought 439 views and backlinks from a domain with real authority.

**Don't buy links.** One spam forum network can drag a domain down for years — the classic SEO mistake is trading a safe, slow gain for a fast, risky one.

## Step 8: Measure and repeat

Set up the loop before you start optimising:

1. Google Search Console — which queries actually bring impressions
2. PageSpeed Insights (or Lighthouse) — Core Web Vitals per key template
3. A simple crawl check for broken links and duplicate titles
4. Weekly: fix the three worst pages, not all of them

## What actually matters, ranked

If you only do three things:

1. **Fix duplicate URLs and canonicals** — cheapest, biggest structural win
2. **Write titles and descriptions that earn clicks** — directly affects CTR
3. **Get 3-5 links from outside** — the only thing on-page work can't do

Everything else — schema, internal linking, speed tuning — compounds on top of these.

---

*Yuriy Astapyev — WebStudio. We build and maintain websites that rank. [uriy-as.org](https://uriy-as.org)*