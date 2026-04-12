---
description: Review and improvement feedback for practical exercises
---

# Exercise Review

## Usage
```
/exercise-review [exercise number] [output folder]
```

Examples:
```
/exercise-review 4-2 output/ex4-2
/exercise-review 7-3 ~/projects/gas-demo
```

## Process

### 1. Deliverable Analysis
- Check files in the output folder
- Evaluate code quality
- Verify structure

### 2. Requirement Verification
Check each Module's exercise requirements and evaluate achievement:
- Fulfillment of mandatory requirements
- Implementation status of optional requirements
- Compliance with best practices

### 3. Improvement Feedback
- Code quality improvement suggestions
- Design pattern recommendations
- Security and performance considerations

### 4. Next Step Suggestions
- Additional topics to study
- Related practical exercises
- Expansion into real-world projects

## Evaluation Criteria

### Code Quality
| Item | Criteria |
|------|----------|
| Readability | Naming conventions, comments, structure |
| Maintainability | Module separation, dependencies |
| Testing | Coverage, edge cases |
| Error Handling | Exception handling, log output |

### Feature Fulfillment
| Level | Description |
|-------|-------------|
| A | All requirements met + additional features |
| B | All mandatory requirements met |
| C | Major requirements met |
| D | Only some requirements met |

## Output Format

```markdown
## Exercise [number] Review Results

### Summary
- Overall Rating: [A/B/C/D]
- Completion: [XX%]
- Key Strengths:
- Areas for Improvement:

### Detailed Evaluation

#### Functional Requirements
| Requirement | Status | Comments |
|-------------|--------|----------|
| Requirement 1 | OK/NG | ... |
| Requirement 2 | OK/NG | ... |

#### Code Quality
- Readability: [X/5]
- Maintainability: [X/5]
- Testing: [X/5]
- Error Handling: [X/5]

### Improvement Suggestions
1. [Priority: High] ...
2. [Priority: Medium] ...
3. [Priority: Low] ...

### Next Steps
- Related exercises: start-X-X
- Reference materials: [URL]
```

## Exercise List

### Module 6: Agent Development
- 6-1: Commands creation
- 6-2: Skills creation
- 6-3: Best practices
- 6-4: Prompt engineering
- 6-5: Debugging

### Module 7: Skill/Commands Creation
- 7-1 to 7-8: Skill/Commands practice

### Module 8: Data Analysis
- 8-1: CSV/JSON processing
- 8-2: Database integration
- 8-3: API integration
- 8-4: Visualization

### Module 9: Slack Integration
- 9-1: Slack MCP connection
- 9-2: Message automation

### Module 10: GAS
- 10-1: Clasp basics
- 10-2: Calendar integration
- 10-3: Sheets integration

### Module 11: GitHub Actions
- 11-1: Workflow creation
- 11-2: Secrets configuration

### Module 12: Notion
- 12-1: MCP connection
- 12-2: DB operations
- 12-3 to 12-6: Notion CLI integration

## Notes
- Error if the output folder does not exist
- Error if the exercise number is invalid
- Use review results as reference information
