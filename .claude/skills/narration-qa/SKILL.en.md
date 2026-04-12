---
name: narration-qa
description: "Skill for automatically verifying the quality of narration audio generated with ElevenLabs. Triggered by requests like 'narration check', 'audio verification', 'pronunciation check', etc."
triggers:
  - narration check
  - audio verification
  - pronunciation check
  - narration-qa
  - narration quality verification
  - TTS verification
---

# Narration QA Skill

A skill for automatically verifying the quality of narration audio generated with ElevenLabs.
**Always follow this skill's flow when generating narration.**

## Triggers

- Quality check requests after narration generation
- "Narration check", "Audio verification", "Pronunciation check"
- **All MV production tasks that include narration generation** (automatically applied)

For the complete workflow including TTS input text rules, Japanese romanization rules, number expansion rules, ElevenLabs settings, Gemini Flash transcription verification, NG determination criteria, regeneration loop decision tree, volume balance adjustment, and QA result reporting format, refer to the original SKILL.md.
