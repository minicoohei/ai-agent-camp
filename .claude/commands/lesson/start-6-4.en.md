---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module06-agent-development"
prerequisites: ["start-6-1", "start-6-2", "start-6-3"]
duration: "~40 min"
level: "advanced"
tags: ["agent", "subagent", "orchestration"]
---

# 🎓 Lesson 6-4: SubAgent Integration

## 📍 What You'll Do

**Lesson 6-4: SubAgent Integration** !

| Item | Details |
|------|---------|
| Goal | Design and implement an architecture combining multiple SubAgents to build efficient workflows |
| Duration | ~40 min |
| Skills Used | Claude Code SubAgent, task decomposition and orchestration |
| Prerequisites | Lesson 6-1 through Lesson 6-3 completed |
| Course Page | [Module 6: Agent Development](https://ai-agent.camp/en/course/module-6) in parallel |

**Session flow:**
1. Design SubAgent architecture
2. Define and link specialized Agents
3. Verify operation of the integrated flow

By the end of this session, a workflow combining multiple Agents will be operational.

> **💡 Hint**: If the AI response stops midway, type "please continue" or "it stopped" to resume. This is a Cursor behavior, not a malfunction.

---

## 🎯 Readiness Check

Let's verify that everything is ready.

**AskQuestion configuration:**
```json
{
  "title": "🎯 Pre-session confirmation",
  "questions": [{
    "id": "readiness",
    "prompt": "Are you ready?",
    "options": [
      {"id": "ready", "label": "Ready! Let's start"},
      {"id": "check_prereq", "label": "I want to check prerequisites"},
      {"id": "view_html", "label": "I want to see the course page first"},
      {"id": "different_lesson", "label": "I want to go to a different lesson"}
    ]
  }]
}
```

(ready → Go to Step 1)
(check_prereq → Run prerequisite check)
(view_html → Show course page path)
(different_lesson → Show module list)

---

## 🚀 Step 1: Design SubAgent Architecture

Use AskUserQuestion (AskQuestion) to choose "Continue / Just review examples / Skip."

**AskQuestion configuration example:**
```json
{
  "title": "🚀 Step 1: Design SubAgent architecture",
  "questions": [{
    "id": "step_action",
    "prompt": "What would you like to do with this step?",
    "options": [
      {"id": "practice", "label": "Continue as-is"},
      {"id": "review", "label": "Just review examples"},
      {"id": "skip", "label": "Skip"}
    ]
  }]
}
```

**After selection (example)**:
Input:
```
Create the directory structure for the SubAgent system:

mkdir -p .claude/subagents/orchestrator
mkdir -p .claude/subagents/content_agent
mkdir -p .claude/subagents/review_agent
mkdir -p .claude/subagents/publish_agent
mkdir -p .claude/subagents/common

Create an __init__.py file in each directory.

Verify the structure.
```

**Expected result**: The SubAgent system directory structure is created.

---

## 🚀 Step 2: Implement Orchestrator Agent

Use AskUserQuestion (AskQuestion) to choose "Continue / Just review examples / Skip."

**AskQuestion configuration example:**
```json
{
  "title": "🚀 Step 2: Implement Orchestrator Agent",
  "questions": [{
    "id": "step_action",
    "prompt": "What would you like to do with this step?",
    "options": [
      {"id": "practice", "label": "Continue as-is"},
      {"id": "review", "label": "Just review examples"},
      {"id": "skip", "label": "Skip"}
    ]
  }]
}
```

**After selection (example)**:
Input:
```
Create the file .claude/subagents/orchestrator/agent.py with the following content:

import asyncio
from typing import Dict, Any, List, Optional
from enum import Enum
import logging

logger = logging.getLogger(__name__)

class TaskStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"

class OrchestratorAgent:
    """Top-level Agent that coordinates multiple SubAgents"""

    def __init__(self):
        self.tasks: Dict[str, Dict[str, Any]] = {}
        self.task_queue = asyncio.Queue()

    def submit_task(self, task_id: str, task_data: Dict[str, Any]) -> str:
        """Submit a task to the queue"""
        self.tasks[task_id] = {
            **task_data,
            'status': TaskStatus.PENDING,
            'progress': 0,
            'result': None
        }
        self.task_queue.put_nowait({'id': task_id, **task_data})
        logger.info(f"Task submitted: {task_id}")
        return task_id

    async def process_workflow(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Process the task workflow"""
        task_id = task['id']
        self.tasks[task_id]['status'] = TaskStatus.IN_PROGRESS

        try:
            # Step 1: Content generation
            logger.info(f"Step 1: Content generation for {task_id}")
            self.tasks[task_id]['progress'] = 33
            content = f"Generated content for: {task.get('prompt', 'default')}"

            # Step 2: Review
            logger.info(f"Step 2: Review for {task_id}")
            self.tasks[task_id]['progress'] = 66
            review_passed = True

            # Step 3: Publish
            logger.info(f"Step 3: Publish for {task_id}")
            self.tasks[task_id]['progress'] = 100

            self.tasks[task_id]['status'] = TaskStatus.COMPLETED
            self.tasks[task_id]['result'] = {
                'content': content,
                'review_passed': review_passed,
                'published': True
            }

            return self.tasks[task_id]

        except Exception as e:
            logger.error(f"Workflow failed for {task_id}: {e}")
            self.tasks[task_id]['status'] = TaskStatus.FAILED
            self.tasks[task_id]['error'] = str(e)
            return self.tasks[task_id]

    def get_task_status(self, task_id: str) -> Optional[Dict[str, Any]]:
        """Get task status"""
        return self.tasks.get(task_id)

    def get_all_tasks(self) -> List[Dict[str, Any]]:
        """Get all tasks"""
        return list(self.tasks.values())

# Usage example
async def main():
    orchestrator = OrchestratorAgent()

    # Submit task
    task_id = orchestrator.submit_task("task_001", {
        "prompt": "Article about AI agents",
        "priority": "high"
    })

    # Execute workflow
    task_data = orchestrator.tasks[task_id]
    result = await orchestrator.process_workflow({'id': task_id, **task_data})

    print(f"Result: {result}")

if __name__ == "__main__":
    asyncio.run(main())
```

**Expected result**: The Orchestrator Agent is implemented.

---

## 🚀 Step 3: Implement Content Agent

Use AskUserQuestion (AskQuestion) to choose "Continue / Just review examples / Skip."

**AskQuestion configuration example:**
```json
{
  "title": "🚀 Step 3: Implement Content Agent",
  "questions": [{
    "id": "step_action",
    "prompt": "What would you like to do with this step?",
    "options": [
      {"id": "practice", "label": "Continue as-is"},
      {"id": "review", "label": "Just review examples"},
      {"id": "skip", "label": "Skip"}
    ]
  }]
}
```

**After selection (example)**:
Input:
```
Create the file .claude/subagents/content_agent/agent.py with the following content:

from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

class ContentAgent:
    """SubAgent specialized in content generation"""

    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.model = self.config.get('model', 'claude-3-5-sonnet')

    async def generate(
        self,
        prompt: str,
        context: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Generate content based on a prompt"""

        logger.info(f"Generating content for prompt: {prompt[:50]}...")

        # In a real implementation, call the Claude API
        # Here we simulate
        content = f"""
# {prompt}

## Overview
This content was auto-generated.

## Details
- Point 1: Important information
- Point 2: Additional information
- Point 3: Summary

## Conclusion
The above is the explanation of {prompt}.
"""

        return {
            'content': content.strip(),
            'tokens_used': len(content.split()),
            'model': self.model
        }

    async def summarize(self, text: str, max_length: int = 100) -> str:
        """Summarize text"""
        logger.info("Summarizing text...")

        # Simulation
        words = text.split()[:max_length]
        return ' '.join(words) + "..."

    async def translate(self, text: str, target_lang: str = "en") -> str:
        """Translate text"""
        logger.info(f"Translating to {target_lang}...")

        # Simulation
        return f"[Translated to {target_lang}]: {text[:100]}..."

# For testing
async def test_content_agent():
    agent = ContentAgent()
    result = await agent.generate("AI agent design patterns")
    print(result['content'])

if __name__ == "__main__":
    import asyncio
    asyncio.run(test_content_agent())
```

**Expected result**: The Content Agent is implemented.

---

## 🚀 Step 4: Implement Review Agent

Use AskUserQuestion (AskQuestion) to choose "Continue / Just review examples / Skip."

**AskQuestion configuration example:**
```json
{
  "title": "🚀 Step 4: Implement Review Agent",
  "questions": [{
    "id": "step_action",
    "prompt": "What would you like to do with this step?",
    "options": [
      {"id": "practice", "label": "Continue as-is"},
      {"id": "review", "label": "Just review examples"},
      {"id": "skip", "label": "Skip"}
    ]
  }]
}
```

**After selection (example)**:
Input:
```
Create the file .claude/subagents/review_agent/agent.py with the following content:

from typing import Dict, Any, List
import logging

logger = logging.getLogger(__name__)

class ReviewAgent:
    """SubAgent that performs review and quality checks"""

    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.rules = {
            'min_length': 100,
            'max_length': 5000,
            'forbidden_words': ['test', 'TODO'],
            'quality_threshold': 7
        }

    async def review(
        self,
        content: str,
        custom_rules: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Review content"""

        rules = {**self.rules, **(custom_rules or {})}
        feedback = []
        score = 10

        # Check 1: Length check
        length = len(content)
        if length < rules['min_length']:
            feedback.append(f"Content too short: {length} chars (min: {rules['min_length']})")
            score -= 2

        if length > rules['max_length']:
            feedback.append(f"Content too long: {length} chars (max: {rules['max_length']})")
            score -= 2

        # Check 2: Forbidden word check
        for word in rules.get('forbidden_words', []):
            if word in content:
                feedback.append(f"Forbidden word found: '{word}'")
                score -= 1

        # Judgment
        approved = score >= rules.get('quality_threshold', 7)

        logger.info(f"Review completed: score={score}, approved={approved}")

        return {
            'approved': approved,
            'score': max(0, score),
            'feedback': feedback,
            'details': {
                'length': length,
                'forbidden_words_found': sum(1 for w in rules.get('forbidden_words', []) if w in content)
            }
        }

# For testing
async def test_review_agent():
    agent = ReviewAgent()

    # Short content
    result1 = await agent.review("Short")
    print(f"Short content: {result1}")

    # Normal content
    normal_content = "This is normal content. " * 20
    result2 = await agent.review(normal_content)
    print(f"Normal content: {result2}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(test_review_agent())
```

**Expected result**: The Review Agent is implemented.

---

## 🚀 Step 5: Integration Test

Use AskUserQuestion (AskQuestion) to choose "Continue / Just review examples / Skip."

**AskQuestion configuration example:**
```json
{
  "title": "🚀 Step 5: Integration test",
  "questions": [{
    "id": "step_action",
    "prompt": "What would you like to do with this step?",
    "options": [
      {"id": "practice", "label": "Continue as-is"},
      {"id": "review", "label": "Just review examples"},
      {"id": "skip", "label": "Skip"}
    ]
  }]
}
```

**After selection (example)**:
Input:
```
Create and run integration tests for the SubAgent system.

Create the file .claude/subagents/tests/test_integration.py:

import pytest
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from orchestrator.agent import OrchestratorAgent, TaskStatus
from content_agent.agent import ContentAgent
from review_agent.agent import ReviewAgent

@pytest.mark.asyncio
async def test_orchestrator_submit_task():
    """Orchestrator task submission test"""
    orchestrator = OrchestratorAgent()
    task_id = orchestrator.submit_task("test_001", {"prompt": "test"})

    assert task_id == "test_001"
    assert orchestrator.tasks[task_id]['status'] == TaskStatus.PENDING

@pytest.mark.asyncio
async def test_orchestrator_workflow():
    """Orchestrator workflow test"""
    orchestrator = OrchestratorAgent()
    task_id = orchestrator.submit_task("test_002", {"prompt": "AI article"})

    result = await orchestrator.process_workflow({'id': task_id, 'prompt': 'AI article'})

    assert result['status'] == TaskStatus.COMPLETED
    assert result['progress'] == 100

@pytest.mark.asyncio
async def test_content_agent_generate():
    """ContentAgent generation test"""
    agent = ContentAgent()
    result = await agent.generate("test prompt")

    assert 'content' in result
    assert len(result['content']) > 0

@pytest.mark.asyncio
async def test_review_agent_approve():
    """ReviewAgent approval test"""
    agent = ReviewAgent()
    long_content = "This is normal content. " * 50

    result = await agent.review(long_content)

    assert result['approved'] == True
    assert result['score'] >= 7

@pytest.mark.asyncio
async def test_review_agent_reject():
    """ReviewAgent rejection test"""
    agent = ReviewAgent()
    short_content = "short"

    result = await agent.review(short_content)

    assert result['approved'] == False

Run the tests:
cd .claude/subagents && pytest tests/test_integration.py -v
```

**Expected result**: All integration tests pass.

---

## ⚠️ Common Issues and Solutions

Use AskUserQuestion (AskQuestion) to select your issue and get guided assistance.

**AskQuestion configuration example:**
```json
{
  "title": "Select your issue",
  "questions": [{
    "id": "trouble",
    "prompt": "Please select the one that applies",
    "options": [
      {"id": "trouble_1", "label": "asyncio error"},
      {"id": "trouble_2", "label": "Module import error"},
      {"id": "trouble_3", "label": "Async processing hangs"},
      {"id": "trouble_4", "label": "Task does not complete"}
    ]
  }]
}
```


### Issue 1: "asyncio error"
**Cause**: The event loop is not configured correctly
**Solution prompt**:
```
Install pytest-asyncio:
pip install pytest-asyncio

Configure in pytest.ini or pyproject.toml:
[pytest]
asyncio_mode = auto
```

### Issue 2: "Module import error"
**Cause**: __init__.py is missing, or the path is not set
**Solution prompt**:
```
Create __init__.py in each directory.
Add the project root to sys.path.
```

### Issue 3: "Async processing hangs"
**Cause**: Missing await, or deadlock
**Solution prompt**:
```
Add await to all async function calls.
Set timeouts with asyncio.wait_for().
```

### Issue 4: "Task does not complete"
**Cause**: An exception is occurring within the workflow
**Solution prompt**:
```
Catch errors with try-except and log them.
Set TaskStatus.FAILED appropriately.
```

---

## ✅ Checkpoint
- [ ] SubAgentDirectory structure is created
- [ ] Orchestrator Agent is implemented
- [ ] Content Agent is implemented
- [ ] Review Agent is implemented
- [ ] Integration tests pass


---

## 📋 Output Preview

### Expected Output
```
📁 output/
└── {project-name}/  (agent/code artifacts)
```

### Verification Commands
```bash
# Check file existence and size
ls -lh output/{project-name}/

# Check the beginning (first 30 lines)
head -30 output/{project-name}/
```

> 💡 View full text: `cat output/{project-name}/` to display the full text

---

## ✅ Completion Check
Paste the following into Cursor chat to verify completion:

```
# Completion check: Verify that expected output files have been generated in the output/ folder.
```

**Expected result**: A pass/fail judgment and any missing items are displayed.

---

## ➡️ Next Steps

This section is now complete. Start the next section, or open a new window to begin a new section.

Use AskUserQuestion (AskQuestion) to choose.

**AskQuestion configuration example:**
```json
{
  "title": "Select next step",
  "questions": [{
    "id": "next_step",
    "prompt": "Please select the next action",
    "options": [
      {"id": "next_auto", "label": "Start the next section (/next_lesson)"},
      {"id": "next_window", "label": "Start in new window (/start-6-5)"},
      {"id": "finish", "label": "End here"}
    ]
  }]
}
```

**After selection (example)**:
- next_auto → /next_lesson
- next_window → Open new window with /start-6-5
- finish → End
