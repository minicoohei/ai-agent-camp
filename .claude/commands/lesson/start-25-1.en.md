---
description: "Lesson command"
category: "lesson"
chapter: "courses/aiagent/lesson03-core/module25-google-ads"
duration: "~60 min"
prerequisites: ["start-24-1"]
level: "intermediate"
tags: ["google-ads", "ads", "gaql", "oauth"]
nonInteractiveMode: incompatible
---
# Lesson 25-1: Google Ads Integration Introduction

## What You'll Do

Learn how to handle the **Google Ads API** safely from an AI agent: account hierarchy, Developer Token / OAuth, read-only API calls, and mutation design built around dry-run.

## Prerequisites

- Be able to prepare a Google Ads account, GCP project, and Python environment
- Use `/setup-google-ads` to proceed through MCC, Developer Token, OAuth, five secrets, and the dry-run connection check
- Browser-based OAuth approval is required, so this lesson cannot be completed in non-interactive mode

## Goals

1. Understand the Google Ads hierarchy: MCC, account, campaign, ad group, and keywords/ads
2. Confirm the roles of Developer Token, OAuth Client, refresh_token, and LOGIN_CUSTOMER_ID
3. Understand why to start with read-only API calls such as campaign lists and GAQL reports
4. Organize safe mutation patterns with dry-run, PAUSED creation, JSON logs, and confirmation gates

## Related Page

- Lesson Page: [Module 25](https://ai-agent.camp/en/course/module-25?slideId=module-overview)

## Next Steps

Next, run `/start-29-1` to continue to slide generation with slide-forge.
