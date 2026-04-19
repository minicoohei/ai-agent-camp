---
name: scientific-visualization
description: "A meta-skill for creating publication-quality graphs and figures for journal submission. Triggered by requests like 'Create a graph for a paper', 'Create a Nature-quality figure', 'Publication-quality visualization'."
triggers:
  - Create a graph for a paper
  - Create publication-quality figures
  - Nature-quality figure
  - Create academic figures
  - Colorblind-friendly graph
  - scientific-visualization
  - publication-ready figure
license: MIT license
metadata:
    skill-author: K-Dense Inc.
source: github.com/K-Dense-AI/claude-scientific-skills@main
---

# Scientific Visualization

## Overview

Scientific visualization transforms data into clear, accurate figures for publication. Create journal-ready plots with multi-panel layouts, error bars, significance markers, and colorblind-safe palettes. Export as PDF/EPS/TIFF using matplotlib, seaborn, and plotly for manuscripts.

## When to Use This Skill

This skill should be used when:
- Creating plots or visualizations for scientific manuscripts
- Preparing figures for journal submission (Nature, Science, Cell, PLOS, etc.)
- Ensuring figures are colorblind-friendly and accessible
- Making multi-panel figures with consistent styling
- Exporting figures at correct resolution and format
- Following specific publication guidelines
- Improving existing figures to meet publication standards
- Creating figures that need to work in both color and grayscale

## Quick Start Guide

### Basic Publication-Quality Figure

```python
import matplotlib.pyplot as plt
import numpy as np

# Apply publication style (from scripts/style_presets.py)
from style_presets import apply_publication_style
apply_publication_style('default')

# Create figure with appropriate size (single column = 3.5 inches)
fig, ax = plt.subplots(figsize=(3.5, 2.5))

# Plot data
x = np.linspace(0, 10, 100)
ax.plot(x, np.sin(x), label='sin(x)')
ax.plot(x, np.cos(x), label='cos(x)')

# Proper labeling with units
ax.set_xlabel('Time (seconds)')
ax.set_ylabel('Amplitude (mV)')
ax.legend(frameon=False)

# Remove unnecessary spines
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# Save in publication formats (from scripts/figure_export.py)
from figure_export import save_publication_figure
save_publication_figure(fig, 'figure1', formats=['pdf', 'png'], dpi=300)
```

For complete documentation including journal-specific styles, color palettes, seaborn integration, multi-panel figures, and all common tasks, please refer to the source SKILL.md file. The body content is already in English.
