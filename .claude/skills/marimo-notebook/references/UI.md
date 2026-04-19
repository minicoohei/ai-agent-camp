marimo has a rich set of UI components. 

* `mo.ui.altair_chart(altair_chart)` - create a reactive Altair chart
* `mo.ui.button(value=None, kind='primary')` - create a clickable button
* `mo.ui.run_button(label=None, tooltip=None, kind='primary')` - create a button that runs code
* `mo.ui.checkbox(label='', value=False)` - create a checkbox
* `mo.ui.chat(placeholder='', value=None)` - create a chat interface
* `mo.ui.date(value=None, label=None, full_width=False)` - create a date picker
* `mo.ui.dropdown(options, value=None, label=None, full_width=False)` - create a dropdown menu
* `mo.ui.file(label='', multiple=False, full_width=False)` - create a file upload element
* `mo.ui.number(value=None, label=None, full_width=False)` - create a number input
* `mo.ui.radio(options, value=None, label=None, full_width=False)` - create radio buttons
* `mo.ui.refresh(options: List[str], default_interval: str)` - create a refresh control
* `mo.ui.slider(start, stop, value=None, label=None, full_width=False, step=None)` - create a slider
* `mo.ui.range_slider(start, stop, value=None, label=None, full_width=False, step=None)` - create a range slider
* `mo.ui.table(data, columns=None, on_select=None, sortable=True, filterable=True)` - create an interactive table
* `mo.ui.text(value='', label=None, full_width=False)` - create a text input
* `mo.ui.text_area(value='', label=None, full_width=False)` - create a multi-line text input
* `mo.ui.data_explorer(df)` - create an interactive dataframe explorer
* `mo.ui.dataframe(df)` - display a dataframe with search, filter, and sort capabilities
* `mo.ui.plotly(plotly_figure)` - create a reactive Plotly chart (supports scatter, treemap, and sunburst)
* `mo.ui.tabs(elements: dict[str, mo.ui.Element])` - create a tabbed interface from a dictionary
* `mo.ui.array(elements: list[mo.ui.Element])` - create an array of UI elements
* `mo.ui.form(element: mo.ui.Element, label='', bordered=True)` - wrap an element in a form

However, the user may also want to use other components. Popular alternatives include the `ScatterWidget` from the `drawdata` library, `moutils`, and `wigglystuff`. 

The wigglystuff API can be explored [here](https://koaning.github.io/wigglystuff/llms.txt). 

For custom classes and static HTML representations you can also use the `_display_` method. 

```python
class Dice:
    def _display_(self):
        import random

        return f"You rolled {random.randint(0, 7)}"
```