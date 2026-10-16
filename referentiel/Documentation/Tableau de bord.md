# ISAP Reporting — Modular Dashboard: User Guide

## What Is the Modular Dashboard?

The Modular Dashboard is your operational command center. It lets you build custom views by combining information widgets — KPI counters, activity feeds, maps, charts, equipment controls, and more — into a drag-and-drop grid. You can create multiple dashboard tabs for different operational needs (e.g., one for daily monitoring, one for security events, one for equipment control).

Dashboards are stored in the database and scoped to your current working folder — each folder has its own set of dashboard tabs. Access is controlled by three roles: **Reader** (view only), **Writer** (create and edit), and **Administrator** (full control including locking); super-administrators always have full access. Your layouts are saved automatically so they're always there when you come back.

## Getting Started

When you first open the Dashboard page, you'll see an empty screen titled **"Your dashboard is empty"**, with the hint *"Open the widget catalog and drag widgets onto the dashboard to build your custom view."*

<!-- SCREENSHOT: Empty dashboard state showing the "dashboard_customize" icon, the "Your dashboard is empty" title, and the "Add widgets" button -->

**To add your first widget:**

Step 1: Click the **hamburger menu** (☰) at the far left of the toolbar to open the widget catalog, or click the **Add widgets** button in the middle of the empty dashboard. *(Both controls only appear if you have Writer or Administrator rights on an unlocked tab — see [Permissions & Access](#permissions--access).)*

<!-- SCREENSHOT: Toolbar with the hamburger menu button highlighted -->

Step 2: Browse the available widgets by category, or use the search bar to find one by name. Click a widget to add it to your dashboard.

<!-- SCREENSHOT: Widget catalog sidebar open, showing the Statistics / Incidents / Maps / Operations / General categories with widget entries -->

Step 3: The widget appears on your grid at the first free position (or where you dropped it).

Step 4: To move, resize or configure it, switch on **Edit layout** in the toolbar (or press and hold the widget for about a second). You can then drag it by its title bar and resize it with the handle in its bottom-right corner.

<!-- SCREENSHOT: A single KPI widget placed on the grid in edit mode, with the drag handle and the resize handle visible -->

Your dashboard is saved automatically — there is no save button.

## Core Concepts

| Term | What it means |
|------|---------------|
| **Widget** | A self-contained information card placed on your dashboard. Each widget shows a specific type of data (incidents, charts, map, etc.) |
| **Tab** | A separate dashboard page. You can have multiple tabs, each with its own set of widgets and settings. Think of tabs like separate desks in your control room. |
| **Edit Mode** | A special mode (toggled with the **Edit layout** button) that lets you move, resize, configure, and delete widgets. When edit mode is off, the dashboard is "locked" for normal use. Requires Writer or Administrator role. |
| **Config Mode** | Same as Edit Mode — the terms are interchangeable. |
| **Dashboard Lock** | An administrator-only toggle that prevents Writers from editing a specific dashboard tab. Only Administrators can modify or unlock a locked dashboard. |
| **Widget Catalog** | The sidebar (or bottom sheet on mobile) listing all available widget types you can add to your dashboard. |
| **Board** | A special widget type that contains other widgets inside it — a dashboard within a dashboard. |
| **Visual Rules** | Configurable behaviors that change how incident data looks: blinking for new incidents, color gradients for aging, threshold alerts, sounds, and more. |
| **Period Selector** | An optional date-range picker that controls the time window for data displayed in all widgets on the current tab. It is shown only when the tab option **Show period selector** is enabled. |
| **Folder** | An organizational unit in ISAP (typically a site or zone). The dashboard shows data from your currently selected folders. Each folder has its own set of dashboard tabs — switching folders loads a different set of dashboards. |

## The Toolbar at a Glance

From left to right, the dashboard toolbar contains:

| Control | Icon | Shown to |
|---------|------|----------|
| Toggle widget catalog | ☰ (`menu` / `menu_open`) | Writer or Administrator, on a tab you are allowed to modify |
| "Dashboard" title | — | Everyone |
| Tab bar | tab labels (icons only on small screens) | Everyone |
| Add tab | `+` | Writer or Administrator |
| Period selector | date range picker | Everyone, only if the active tab has **Show period selector** enabled |
| Tab settings | ⚙ `settings` | Writer or Administrator, on a tab you are allowed to modify |
| Lock / Unlock dashboard | 🔒 `lock` / `lock_open` | Administrator only |
| Edit layout / Editing | `edit` (pencil) → `lock_open` when active | Writer or Administrator, on a tab you are allowed to modify |
| Lock all / Unlock all widgets | 🔒 `lock` / `lock_open` | Only while edit mode is active |
| More options (⋮) | `more_vert` | Any user with Dashboard rights (Reader and above) or a super-administrator |

<!-- SCREENSHOT: The full dashboard toolbar with every control visible, annotated left to right -->

On screens narrower than ~1024 px the tab labels are replaced by the tab icon (with a tooltip), and the **Edit layout** button shows only its icon.

## Features

---

### Feature: Dashboard Tabs

**What it does:**
Tabs let you organize multiple independent dashboard layouts. Each tab has its own widgets, layout, name, icon, accent color, data source and period-selector setting.

**When to use it:**
Use multiple tabs when you need different views for different tasks — e.g. a "Daily Operations" tab with KPI widgets and tables, and a "Security Overview" tab with charts and maps.

**How to use it:**

Step 1: Click the **+** button next to the existing tabs in the toolbar to add a new tab. It is created immediately with the name "Dashboard *n*". *(Requires Writer or Administrator role.)*

<!-- SCREENSHOT: Toolbar showing existing tabs and the "+" button to add a new tab -->

Step 2: Click on a tab to switch to it. Switching a tab reloads the data for that tab.

<!-- SCREENSHOT: Toolbar with multiple tabs, one actively selected (highlighted with the primary color indicator) -->

Step 3: To configure tabs, click the **gear icon** (⚙) in the toolbar. The **Tab settings** panel slides in from the right. *(Requires Writer or Administrator role.)*

<!-- SCREENSHOT: Tab settings drawer open on the right side, showing the tab list on the right and the config form on the left -->

Step 4: Select a tab in the list to edit it. The configuration form appears next to the list (on narrow screens it replaces the list, with a back arrow to return).

<!-- SCREENSHOT: Tab config form showing the name input, icon selector, color picker, data source dropdown, period selector toggle, and the "Widget positions" lock/unlock buttons -->

Step 5: Click **Validate** to save your changes, or **Cancel** to discard them.

**Options & settings:**

| Setting | What it does |
|---------|-------------|
| Tab name | The label shown in the toolbar tab bar |
| Tab icon | One of 10 icons (dashboard, monitor, security, map, analytics, notifications, groups, videocam, tune, star). Used in the tab list and shown instead of the label on small screens |
| Top bar color | A colored accent line under the toolbar, also used by widget title bars that are set to "Use tab colors" |
| Data source | Filters the type of data displayed: All, Incidents, Security events, Activities, Resources |
| Show period selector | Adds a date-range picker to the toolbar so you can choose exactly what time period to view |
| Widget positions | Two buttons — **Lock all widgets** / **Unlock all widgets** — that apply to every widget of the selected tab |

**Adding and deleting tabs from the panel:**
- The **Add tab** button at the bottom of the tab list creates a new tab.
- A **trash icon** appears on each tab you are allowed to delete. Deleting asks for confirmation ("Do you want to delete the dashboard "…"?").
- The delete button is disabled when only one tab remains.
- Tabs locked by an administrator are shown with a yellow padlock and are read-only for Writers.

**Tips & best practices:**
- You can scroll the tab bar with the mouse wheel when there are more tabs than fit on screen.
- Tabs cannot be reordered by drag and drop.
- When you delete a tab, all of its widgets are removed permanently.
- An Administrator can **lock** a dashboard tab (padlock in the toolbar) to prevent Writers from modifying it. Only Administrators can edit, unlock or delete a locked tab.
- If a tab is locked while you are editing it, you are automatically kicked out of edit mode and the catalog closes.

**What can go wrong:**
- Tab deletion cannot be undone. Export the tab layout first if you may need it again (super-administrators only — see [Export & Import](#feature-export--import)).

---

### Feature: Adding Widgets

**What it does:**
Lets you place new information cards on your dashboard from a catalog of available widget types.

**When to use it:**
Whenever you want to add a new piece of information to your view.

**How to use it (Desktop):**

Step 1: Click the **hamburger menu** (☰), or the **Add widgets** button shown when the dashboard is empty, to open the catalog sidebar. Use the search field at the top to filter the list.

<!-- SCREENSHOT: Widget catalog sidebar showing the search field, widget categories and entries with drag handles -->

Step 2: You can either:
- **Click** a widget to place it automatically at the first available position
- **Drag** a widget from the catalog and **drop** it onto the grid at the exact position you want (a ghost preview shows where it will land)

<!-- SCREENSHOT: A widget being dragged from the catalog with a drop preview ghost visible on the grid -->

**How to use it (Mobile/Tablet):**

Step 1: Tap the hamburger menu to open the widget catalog as a bottom sheet.

<!-- SCREENSHOT: Mobile bottom sheet showing the widget catalog with widgets listed vertically -->

Step 2: Either:
- **Tap** a widget to add it to the dashboard (the sheet closes automatically)
- Use the **drag handle** on the right side of each entry to touch-drag it to a specific position

<!-- SCREENSHOT: Touch drag ghost floating over the dashboard grid on a mobile device -->

The device back button closes the catalog.

**Available widget categories:**

| Category | Widget Types |
|----------|-------------|
| **Statistics** | KPI, Chart |
| **Incidents** | Incident table, Activity feed |
| **Maps** | Map |
| **Operations** | Action panel, Quick action |
| **General** | Clock, Board |

**Notes:**
- The **Action panel** widget is hidden from the catalog entirely if you do not have webhypervisor rights.
- Adding a widget does *not* switch the dashboard into edit mode — use the **Edit layout** button to arrange it.
- Each widget type has a default size and a list of allowed sizes (see [Widget Configuration](#feature-widget-configuration)).
- If no widget matches your search, the catalog displays "No widgets found."

---

### Feature: Edit Mode (Drag, Resize, Configure, Delete)

**What it does:**
Toggles the dashboard into a mode where you can move widgets around, resize them, access their settings, and remove them.

**Requirements:**
- Requires **Writer** or **Administrator** role.
- If the current dashboard tab is **locked**, only an **Administrator** can enter edit mode.

**When to use it:**
Whenever you want to rearrange, customize, or clean up your dashboard layout.

**How to use it:**

Step 1: Click the **Edit layout** button (pencil icon) in the toolbar. It turns into a highlighted **Editing** button to indicate that edit mode is active.

<!-- SCREENSHOT: Toolbar showing the "Editing" button in its active/highlighted state -->

Step 2: Widgets now show a drag handle on the left of their title bar and three action buttons on the right:
- **Lock / Unlock widget position** (🔒/🔓) — Prevent or allow moving and resizing this widget
- **Configure widget** (⚙) — Open the widget's configuration dialog
- **Delete widget** (✕) — Remove the widget from the dashboard (no confirmation, no undo)

<!-- SCREENSHOT: A widget in edit mode showing the drag handle on the left and lock/settings/delete buttons on the right in the title bar -->

Step 3: **Drag** a widget by its title bar to reposition it. Other widgets are pushed down to make room. Press **Escape** during a drag to cancel it and restore the original positions.

<!-- SCREENSHOT: A widget being dragged with a semi-transparent ghost showing the target position -->

Step 4: **Resize** a widget by dragging the handle in its bottom-right corner. The handle is hidden on locked widgets.

<!-- SCREENSHOT: A widget being resized, showing the resize handle cursor in the bottom-right corner -->

Step 5: Press **Escape** to exit edit mode, or click the **Editing** button again.

**Tips & best practices:**
- **Multi-select:** Hold **Ctrl** (or **Cmd** on Mac) and click several widgets to select them. Selected widgets show an accent-colored border, and dragging one of them moves the whole group.
- **Select all:** Press **Ctrl+A** to select every widget on the tab.
- **Delete selected:** Press **Delete** or **Backspace** to remove all selected widgets at once.
- **Long press:** Pressing and holding a widget for 600 ms (mouse or touch) switches the dashboard into edit mode and selects that widget.
- **Lock/Unlock all:** The padlock button that appears in the toolbar in edit mode locks or unlocks every widget at once. The same pair of buttons is available in **Tab settings → Widget positions**. Locked widgets cannot be moved or resized but can still be configured, renamed and deleted.
- Keyboard shortcuts are ignored while you are typing in a text field.

**What can go wrong:**
- Deleting a widget is immediate and permanent. There is no confirmation and no undo.
- If you can't move a widget, check whether it's locked (yellow padlock in its title bar).
- If you can't enter edit mode at all, check whether the tab is locked by an administrator (yellow padlock next to the Edit layout button) or whether you have Writer/Administrator rights.

---

### Feature: Widget Configuration

**What it does:**
Each widget has its own **Configure widget** dialog where you can change its size, what data it shows, how it looks, and which visual rules apply.

**When to use it:**
Use this to fine-tune a widget's behavior — filtering incident levels, changing chart types, enabling visual alerts, etc.

**How to use it:**

Step 1: Enter edit mode, then click the **gear icon** (⚙) on the widget you want to configure.

<!-- SCREENSHOT: Widget config dialog open, showing the size selector at the top and configuration fields below -->

Step 2: Adjust the settings. The dialog contains:
- **Size** — A set of predefined sizes, shown only when the widget supports more than one
- **Configuration fields** — Type-specific options (filters, toggles, selectors, colors)
- **Visual rules** — Collapsible groups (Blink rules, Age rules, Status rules, Threshold rules, Notification rules) on incident-aware widgets
- **Widget colors** — A collapsible group available on every widget: either **Use tab colors** (default) or custom **Title bar color**, **Border color** and **Text color**

<!-- SCREENSHOT: Widget config dialog showing the expanded "Visual rules" section with its blink, age, status, threshold, and notification sub-groups -->

Step 3: Click **Validate** to apply, or **Cancel** (or the ✕) to discard. Changes are not applied until you validate.

**Available sizes per widget type** (width × height, in grid cells):

| Widget | Default size | Allowed sizes |
|--------|--------------|---------------|
| KPI | 1×1 | 1×1, 2×1 |
| Chart | 2×2 | 2×1, 2×2, 3×2 |
| Map | 2×2 | 2×2, 3×2 |
| Activity feed | 1×2 | 1×2, 2×2 |
| Incident table | 3×2 | 2×2, 3×2, 4×2, 4×3 |
| Clock | 1×1 | 1×1 (fixed) |
| Board | 4×3 | 3×2, 4×3, 6×3, 6×4 |
| Action panel | 2×2 | 2×1, 2×2, 3×2, 4×2 |
| Quick action | 1×1 | 1×1, 2×1, 2×2 |

You are not limited to these presets — resizing a widget by its corner handle allows any size the grid can accommodate.

**What happens behind the scenes:**
The configuration is stored with the widget's layout data in the database and saved automatically after a short delay (800 ms) so that rapid edits are batched. Changing a data-related option triggers a refresh of the dashboard data.

---

### Feature: Widget Renaming

**What it does:**
Lets you give a custom name to any widget, overriding the default type label.

**When to use it:**
When you have several widgets of the same type and need to tell them apart (e.g. "Critical incidents" vs. "Low priority incidents").

**How to use it:**

Step 1: **Double-click** the widget's title text in the title bar.

<!-- SCREENSHOT: A widget title bar with the text selected in an inline text input, ready for editing -->

Step 2: Type the new name and press **Enter**, or click away, to confirm. Press **Escape** to cancel.

**Tips:**
- Renaming works both in edit mode and in normal mode.
- The custom name is saved with the layout and persists across sessions.

---

### Feature: KPI Widget

**What it does:**
Displays a large, at-a-glance numeric value. It has two display modes:

- **Count mode** (default) — Counts records from one or more data sources (incidents, mentions, security events) with optional severity filtering and an optional color-coded icon.
- **Value mode** — Shows a live numeric value coming from a value provider (counting zones, sensors…), with entity selection, attribute selection and an aggregation (sum, average, latest).

> **Note:** no value provider is registered in the current build, so the **Value source** list is empty and value mode displays `0`. Use count mode until a provider is deployed.

**When to use it:**
Place this widget prominently when you need instant visibility into how many incidents are active.

**How it looks (count mode):**
- The number is displayed large and centered, with the widget name underneath. While data is loading, a dash (—) is shown.
- If **Color-coded icon** is enabled, a speedometer icon appears above the number and changes color with the count: **green** below 2, **orange** from 2 to 4, **red** from 5 upwards. When the option is off (the default), no icon is displayed at all.
- The icon pulses when the **Threshold alert** visual rule is exceeded.

<!-- SCREENSHOT: Three KPI widgets side by side: one green (0), one orange (3), one red with pulsing animation (12) -->

**Configuration options (count mode):**

| Option | Values | Default |
|--------|--------|---------|
| Display mode | Count / Value | Count |
| Data sources | Incidents, Mentions, Security events (multi-select) | Incidents |
| Level | 0–5 (multi-select) | none (all levels) |
| Show closed | on/off | off |
| Color-coded icon | on/off | off |

**Configuration options (value mode):** Value source, Entities, Attribute, Aggregation (sum / average / latest).

**Visual rules available:** blink rules, threshold rules and notification rules. Age and status rules do not apply to this widget.

**Interaction:** the KPI widget is display-only — clicking it does not open anything.

---

### Feature: Incident Table Widget

**What it does:**
Shows a scrollable, multi-source table with configurable columns, row highlighting and the ability to click a record to open its detail view.

**When to use it:**
When you need detailed operational information — not just a count, but names, statuses, timestamps, descriptions and more — across several data sources.

<!-- SCREENSHOT: Incident Table widget showing columns for Level, Timestamp, Name, and Status with color-coded status text -->

**Key behaviors:**
- Click any row to open its detail drawer (full incident view with editing capabilities, where applicable). Clicking also acknowledges a blinking row.
- Cells modified by another user are briefly highlighted (the highlight clears automatically after a few seconds).
- Supports several data sources at once: incidents, security events, mentions (police log) and activities.
- Supports all visual rules: blink, age gradient, stale alert, unacknowledged alert, level stripe, fade resolved, auto-hide closed, closure-time highlight and threshold alert.
- Status text is colored: Opened red, Acknowledged amber, Resolved green, Closed grey — all four are customizable.

**Configuration highlights:**

| Option | Values | Default |
|--------|--------|---------|
| Data sources | Incidents, Security events, Mentions, Activities | Incidents |
| Show mentions | on/off — includes police log entries alongside incidents | on |
| Level | 0–5 | none (all) |
| Status | Opened, Acknowledged, Resolved, Closed | none (all) |
| Sort by | Timestamp, Level, Status | Timestamp |
| Max items | number | 20 |
| Adaptive columns | on/off — when on, the visible columns are chosen automatically from the widget size | off |
| Visible columns | multi-select; the list adapts to the selected data sources. Chips can be reordered with the ‹ › arrows | Level, Timestamp, Name, Status |
| Font size | Small / Medium / Large | Small |
| Compact | on/off | on |
| Status colors | Per status: highlight toggle, background color and text color | see above |

<!-- SCREENSHOT: Widget config dialog for the Incident table showing the "Status colors" group expanded with color pickers for each status -->

---

### Feature: Activity Feed Widget

**What it does:**
Shows a chronological feed of recent activity: incident modifications, status changes, field updates — which field changed, to what value, when and by whom.

**When to use it:**
When you want to monitor real-time operational activity across all incidents without opening individual incident records.

<!-- SCREENSHOT: Activity Feed widget showing entries with the changed field, its new value, the timestamp and the author -->

**Key behaviors:**
- Loads more entries automatically as you scroll down (infinite scroll).
- New activities can blink to draw attention (blink rules); the default blink color for this widget is light green.
- Click an entry to acknowledge its blink.
- When there is nothing to show, the widget displays "No recent activities." (or your own custom empty-state message).

**Configuration:**

| Option | Values | Default |
|--------|--------|---------|
| Text alignment | Left / Center / Right | Left |
| Text wrap | on/off | on |
| Empty state message | free text | — |

**Visual rules available:** blink rules and status rules. Age, threshold and notification rules do not apply to this widget.

---

### Feature: Chart Widget

**What it does:**
Renders visual charts of incident or security event data.

**When to use it:**
When you need to visualize data distribution — incidents by level, or security event statistics.

**Available chart types:** Bar, Horizontal bar, Line, Pie, Doughnut, Radar, Polar area

<!-- SCREENSHOT: Four chart widgets showing the same data in bar, pie, doughnut, and radar chart formats -->

**Configuration:**

| Option | Values | Default |
|--------|--------|---------|
| Chart type | the 7 types listed above | Bar |
| Data source | Incidents / Security events | Incidents |
| Legend position | Auto, Top, Bottom, Left, Right | Auto |

**Key behaviors:**
- With the **Incidents** source, data is grouped by level and colored using the configured level colors. With **Security events**, the chart shows security-event statistics grouped by source and type.
- "Auto" legend placement picks a position from the widget's shape, and hides the legend on chart types where it adds no information.
- Fonts, padding and label visibility shrink automatically in small widgets.
- The chart is display-only — clicking a segment does nothing.

---

### Feature: Map Widget

**What it does:**
Displays an interactive map showing the geographic positions of incidents, resources (personnel) and cameras.

**When to use it:**
When you need spatial awareness of your operational situation — where incidents are happening, where your teams are, and what cameras cover which areas.

<!-- SCREENSHOT: Map widget showing incident markers (colored by severity level), person icons for resources, and camera icons, with a search bar at the top -->

**Key behaviors:**
- Markers are clustered when zoomed out and split into individual markers as you zoom in.
- Click a marker to see its details in a popup.
- Real-time updates: markers appear, move or disappear as the backend sends notifications for incidents, resources and cameras.
- The map is read-only in the dashboard — clicking a feature does not open the incident detail drawer.

**Configuration:**

| Option | Values | Default |
|--------|--------|---------|
| Base map type | OpenStreetMap / Satellite | OpenStreetMap |
| Initial zoom | number | 14 |
| Show search bar | on/off | on |
| Show controls | on/off | on |
| Show incidents | on/off | on |
| Show resources | on/off | on |
| Show cameras | on/off | off |
| Show layer panel | on/off | off |

---

### Feature: Action Panel Widget

**What it does:**
Lists equipment entities (sensors, standard accesses, DAS, interphones, macro-objects) with their current state, and lets you execute actions on them directly from the dashboard.

**When to use it:**
When you need to monitor and control physical security equipment without navigating to the full Synoptic/Consignes interface.

<!-- SCREENSHOT: Action Panel widget showing a list of sensors with state icons and an action button on the right of each row -->

**Requirements:**
- Requires **webhypervisor** permissions. Without them the widget is not even listed in the catalog, and an existing one shows a padlock with an "insufficient rights" message.

**Key behaviors:**
- The available actions for an entity are fetched from the server (and already filtered by your permissions) when you open its action menu.
- Every state-changing action asks for confirmation, naming both the entity and the action.
- Actions are debounced: only one action at a time can be in flight per entity, and the button shows a spinner meanwhile.
- The state column shows the entity state: Active, Triggered, Disrupted, Tampered, Failure, Inhibited, Inactive.
- Sorting by state ranks the most critical states first.

**Configuration:**

| Option | Values | Default |
|--------|--------|---------|
| Element type | Sensor, Standard access, DAS, Interphone, Macro object | Sensor |
| Type filter | multi-select of the types available for that element type | all types |
| Attribute filters | per boolean attribute: Any / True / False | Any |
| Name filter | free text; a trailing `*` acts as a prefix wildcard | empty |
| Visible columns | multi-select (Name, Identifier, Type, Description, Label, Model, ID…) | type-dependent |
| Sort by | Name / Type / State | Name |
| Sort direction | Ascending / Descending | Ascending |
| Show state | on/off | on |
| Show actions | on/off | off |
| Compact | on/off | on |
| Font size | Small / Medium / Large | Small |

---

### Feature: Clock Widget

**What it does:**
Displays the current time (updated every second) and the localized date, automatically sized to fill the widget.

**When to use it:**
When you want a clear clock visible on your operational dashboard.

<!-- SCREENSHOT: Clock widget showing "14:36:54" in large text with the localized date below it -->

**Configuration:**
- **24-hour format** (on by default). Turn it off for a 12-hour AM/PM display.

The clock widget has a single fixed size (1×1 cell).

---

### Feature: Board Widget (Nested Dashboard)

**What it does:**
Creates a container widget that holds other widgets inside it — essentially a mini-dashboard within your dashboard.

**When to use it:**
When you want to group related widgets together in a single resizable container, for example several KPI widgets (one per level) inside one board.

<!-- SCREENSHOT: A Board widget containing three smaller widgets: a KPI widget, a Clock, and an Activity Feed, arranged in an inner grid -->

**Key behaviors:**
- The board has its own inner grid with a configurable column count and cell height.
- In edit mode the board shows a mini toolbar with an **add widget** button (its catalog excludes the Board type), an **import layout** button, a column selector and the widget count.
- You can drag a widget from the main grid and drop it into a board; it is removed from the main grid and becomes a child of the board.
- The inner layout can be exported and imported as a JSON file, independently of the tab layout.
- Widgets inside a board are fully interactive in normal mode.

**Configuration:**

| Option | Values | Default |
|--------|--------|---------|
| Columns | 2, 4, 6 or 8 | 4 |
| Cell height | pixels | 80 |

---

### Feature: Quick Action Widget

**What it does:**
A single-purpose button widget that opens a form for performing one operational action: creating an incident, creating a police log entry (mention), broadcasting an alert message, or processing a task.

**When to use it:**
When you want one-tap access to a frequent action without navigating away from the dashboard.

<!-- SCREENSHOT: Four Quick Action widgets configured for different actions: Create incident, Create mention, Create alert message, Process task -->

**How to use it:**

Step 1: Click the action button on the widget.

Step 2: Fill in the form fields in the dialog that opens. Required fields are validated before submission ("This field is required").

<!-- SCREENSHOT: Quick Action form dialog open for "Create incident" showing fields for Name, Level, Status, Type, Place, and Description -->

Step 3: Click **Submit**. A success or failure message is displayed.

**Form fields per action type:**

| Action type | Fields |
|-------------|--------|
| Create incident | Name, Level, Status, Type, Place, Description |
| Create mention | Name (required), Description |
| Create alert message | Alert title (required), Text (required) |
| Process task | Task (required), Create mention on processing |

**Other options:** custom button label, button icon and button color.

**Post-action behavior:**
- **Reset** (default): the form clears, ready for the next action.
- **Navigate**: the newly created entity opens in a detail drawer for further editing.

**Notes & requirements:**
- Create incident / Create mention: requires logbook writer rights.
- Create alert message: requires administrator rights.
- Process task: requires access to the Consignes module.
- If you lack the rights for the configured action, the widget shows "Insufficient rights for this action." instead of the button.
- For **Create incident**, the level field is locked when the selected incident type imposes a default level ("Level set by incident type").
- Closing the dialog with unsaved input asks for confirmation.

---

### Feature: Export & Import

The **three-dot menu** (⋮) at the right end of the toolbar gathers all export/import commands. Which entries you see depends on your rights:

| Menu entry | Who sees it | What it does |
|------------|-------------|--------------|
| **Export PDF** | Any user with Dashboard rights (Reader and above) | Renders one or more dashboard tabs into a PDF document |
| **Export layout** | Super-administrators only | Downloads the current tab (settings + widgets) as a JSON file |
| **Import layout** | Writer or Administrator | Creates a new tab from a previously exported JSON file |

<!-- SCREENSHOT: Three-dot menu open showing "Export PDF", "Export layout" and "Import layout" options -->

#### Export PDF

Step 1: Open the three-dot menu and choose **Export PDF**.

Step 2: In the dialog, tick the tabs you want to include (or use **Select all**) and choose whether to export in **landscape** orientation (on by default).

<!-- SCREENSHOT: Export PDF dialog showing the tab checkbox list and the "Export in landscape" toggle -->

Step 3: Click **Export PDF**. Each selected tab is opened, refreshed and captured in turn, so the export takes a few seconds per tab. The file is saved as `Dashboard_YYYY-MM-DD.pdf`.

**Notes:**
- Each tab starts on a new page, preceded by a colored title bar using the tab's top bar color. Long dashboards are split across several pages.
- Maps and charts are re-rendered for the capture; a map tile server that refuses cross-origin access may result in a blank map area.
- Do not change the working folder while an export is running — the export aborts to avoid mixing data from two folders.

#### Export / Import layout (JSON)

**When to use it:**
- Share a dashboard layout with a colleague
- Back up a layout before making major changes
- Copy a layout to another folder or another ISAP deployment

**What is exported:** the active tab only — its name and settings, its widgets with their configuration, and the per-breakpoint positions.

The file is named `dashboard-tab-<Tab_name>-YYYY-MM-DD.json`.

<!-- SCREENSHOT: File save dialog showing a file named "dashboard-tab-Daily_Operations-2026-04-29.json" -->

**What happens on import:**
- The imported layout always creates a **new dashboard tab** in the current folder — it never overwrites an existing tab.
- Tab settings (name, color, icon, data source, period selector) from the file are applied to the new tab.
- Data is refreshed immediately, and the message "Layout imported successfully" is displayed.

**What can go wrong:**
- A file that is not valid dashboard JSON is rejected with the message "Invalid file".
- Importing requires Writer or Administrator rights and at least one selected folder.

> Board widgets have their own, separate import/export buttons for their inner layout (visible in the board's mini toolbar in edit mode).

---

### Feature: Visual Rules (Blink, Age Gradient, Alerts, Sounds)

**What it does:**
Visual rules are display behaviors you can enable per widget. They draw attention to critical situations using animations, colors, sounds and browser notifications.

**When to use it:**
Enable these when you're monitoring a live operational environment and need automated visual cues for incidents that need attention.

**Available rule types:**

| Group | Rule | What you see | Default settings |
|-------|------|-------------|------------------|
| Blink | Blink new incidents | Newly appeared records flash with a colored background | off, 5 min, light yellow |
| Blink | Acknowledge blink on interaction | Clicking the widget/row stops the blinking | off (always on for KPI) |
| Blink | Blink critical | Records at or above a severity threshold blink continuously, using the level color | off, threshold 4 |
| Blink | Flash max level | The whole widget flashes with a red border while a level-5 record is present | off |
| Age | Age gradient | Open records gradually take on a warning color as they age | off, 60 min, orange |
| Age | Stale alert | A clock icon marks records untouched for too long | off, 30 min |
| Age | Closure time highlight | Left border shows resolution speed: blue when closed fast, orange when closed slowly | off, 5 min / 240 min |
| Status | Level stripe | A colored left border shows the severity level | off |
| Status | Unacknowledged alert | A warning icon marks records not acknowledged in time | off, 10 min |
| Status | Fade resolved | Resolved/closed records become semi-transparent | off, 40% |
| Status | Auto-hide closed | Closed records disappear after a delay | off, 30 min |
| Threshold | Threshold alert | A colored border glows around the widget when the record count reaches the threshold; KPI icons also pulse | off, 10, red |
| Notifications | Sound on new | Plays a sound when new records appear | off, beep |
| Notifications | Browser notification | Sends a browser notification for new records at or above a minimum level | off, level 3 |

The **Visual rules** group also contains an **Empty state message** field, which replaces the default "No incidents." / "No recent activities." text.

<!-- SCREENSHOT: An Incident table widget with several visual rules active: age gradient, level stripes, a stale clock icon, and a blinking new row -->

**Which widgets support which rules:**

| Widget | Blink | Age | Status | Threshold | Notifications |
|--------|-------|-----|--------|-----------|---------------|
| Incident table | ✓ | ✓ | ✓ | ✓ | ✓ |
| KPI | ✓ | | | ✓ | ✓ |
| Activity feed | ✓ | | ✓ | | |

Other widgets (Chart, Map, Clock, Board, Action panel, Quick action) do not use visual rules.

**How to enable:**
Open the widget's configuration dialog (gear icon in edit mode) and expand the **Visual rules** section, then the relevant sub-group.

---

## Settings & Preferences

Dashboards are stored as database entities, scoped to the current working folder. There is no manual save — all changes are saved automatically (with an 800 ms delay so that drag operations don't cause a write per pixel). Only changes that actually differ from the last saved state are written.

**What is saved:**
- Tab structure (names, icons, colors, data source, period selector option)
- Widget positions, sizes, types and configurations (including custom titles, lock state and widget colors)
- Per-dashboard lock state
- Per-breakpoint layout snapshots, so your desktop, tablet and phone layouts are preserved independently

**Where it's stored:**
Dashboards are stored in the server database as entities attached to your current working folder. They are shared by all users with access to that folder — they are not per-user. This means:
- Switching folders loads a different set of dashboards
- Changes made by one user become visible to the others in real time (server notifications)
- Dashboards follow the folder, not the user

**Screen adaptation:** the grid uses four sizes, each with its own saved arrangement:

| Screen width | Columns | Row height |
|--------------|---------|-----------|
| < 600 px (phone) | 2 | 120 px |
| 600–1023 px (tablet) | 4 | 130 px |
| 1024–1439 px (small desktop) | 8 | 140 px |
| ≥ 1440 px (large desktop) | 12 | 140 px |

<!-- SCREENSHOT: The dashboard toolbar showing all persistent elements: tabs, edit button, lock toggle, period selector, settings gear, three-dot menu -->

## Keyboard Shortcuts & Power User Tips

| Shortcut | Action | Requires |
|----------|--------|----------|
| **Escape** | Exit edit mode (or cancel the drag in progress) | Edit mode active |
| **Delete** / **Backspace** | Delete the selected widget(s) | Edit mode + at least one widget selected |
| **Ctrl+A** | Select all widgets | Edit mode active |
| **Ctrl+Click** | Add/remove a widget from the selection | Edit mode active |
| **Double-click title** | Rename a widget | — |
| **Long press** (600 ms) | Enter edit mode and select the widget | Writer/Administrator on an editable tab |
| **Mouse wheel** over the tab bar | Scroll through tabs | More tabs than fit on screen |

Shortcuts are ignored while the focus is in a text field.

## Notifications & Alerts

The dashboard can raise two kinds of alerts when the corresponding visual rules are enabled:

1. **Browser notifications** — A native notification appears when new records at or above the configured level are detected. The browser asks for permission the first time; if you refuse it, no notification is shown.
2. **Sound alerts** — Three sounds are available:
   - **Beep** — a short 880 Hz tone
   - **Chime** — a three-note ascending chime (C–E–G)
   - **Alert** — three rapid square-wave pulses

Both are configured per widget, in **Visual rules → Notification rules**, and are only available on the KPI and Incident table widgets.

## Permissions & Access

### Dashboard Roles

Access to dashboard features is controlled by your **Dashboard rights** role, assigned by an administrator in the Admin page:

| Role | View | Edit (unlocked tabs) | Edit (locked tabs) | Lock/Unlock tabs | Create tabs | Delete (unlocked) | Delete (locked) | Export PDF | Export JSON | Import JSON |
|------|------|---------------------|-------------------|-----------------|------------|-------------------|-----------------|-----------|-------------|-------------|
| **Reader** | ✓ | | | | | | | ✓ | | |
| **Writer** | ✓ | ✓ | | | ✓ | ✓ | | ✓ | | ✓ |
| **Administrator** | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | | ✓ |
| **Super-administrator** | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |

- **Reader**: can view dashboards and interact with widgets (click incidents, use maps, run quick actions they are entitled to) but cannot modify any layout or configuration.
- **Writer**: can add/remove/configure widgets and tabs on unlocked dashboards. Cannot modify, unlock or delete locked dashboards.
- **Administrator**: full control — can edit locked dashboards, lock/unlock tabs, and delete any dashboard.
- **Export layout (JSON)** is reserved for super-administrators; everyone else uses the PDF export.

### Widget-specific Permissions

| Capability | Required Rights |
|-----------|----------------|
| View dashboard | Dashboard Reader (or higher) |
| Add/configure/delete widgets | Dashboard Writer (or higher) |
| Edit a locked dashboard tab | Dashboard Administrator |
| Lock/Unlock a dashboard tab | Dashboard Administrator |
| Use the Action panel widget | `webhypervisor` (`$ItfConsignes` + `$ItfAction` proxies) |
| Quick action: Create incident / mention | Logbook writer rights |
| Quick action: Create alert message | Administrator rights |
| Quick action: Process task | Consignes module access |
| View incident details (click a table row) | Standard incident read access |

## FAQ

**Q: Where did my dashboard go?**
A: Dashboards are stored per folder in the database. If your dashboards disappeared, check that you're in the correct **working folder** — switching folders loads a different set of dashboards. If dashboards were deleted by another user, they cannot be recovered.

**Q: Can I share my dashboard with colleagues?**
A: Dashboards are already shared — all users with access to the same folder see the same dashboard tabs. To copy a layout to another folder, a super-administrator can export it (⋮ → Export layout), switch to the target folder and import it there. Importing always creates a new tab.

**Q: Why can't I move or resize a widget?**
A: Several possible reasons:
- The widget is **locked** — look for a yellow padlock in its title bar. Click it to unlock, or use **Unlock all widgets** in the toolbar (visible in edit mode) or in Tab settings.
- The entire **dashboard tab is locked** — only an Administrator can unlock it (padlock next to the Edit layout button).
- You don't have **Writer or Administrator** rights — contact your administrator.

**Q: Why does my dashboard look different on my phone?**
A: The grid adapts to your screen size (2, 4, 8 or 12 columns). Each size keeps its own arrangement, so your desktop layout is preserved and restored when you return to a larger screen.

**Q: Can I undo deleting a widget?**
A: No. Widget deletion is immediate, without confirmation, and cannot be undone. You can re-add the widget from the catalog and reconfigure it. Tab deletion does ask for confirmation, but is equally permanent.

**Q: Another user changed the dashboard while I was editing. What happens?**
A: The dashboard detects external modifications in real time via server notifications and reloads the affected tab. If you were mid-edit, your unsaved changes may be overwritten.

**Q: Why can't I see the Edit layout button or the + tab button?**
A: These controls are only shown to users with Writer or Administrator dashboard rights. With Reader rights the dashboard is view-only. Contact your administrator to upgrade your permissions.

**Q: I locked a dashboard tab by accident. How do I unlock it?**
A: Click the padlock (🔒) next to the Edit layout button in the toolbar. This toggle is only visible to Administrators.

**Q: Why is the Action panel showing a padlock?**
A: You don't have the required permissions (webhypervisor rights). Contact your administrator.

**Q: Why is the KPI "Value" mode empty?**
A: No value provider is registered in the current build, so the value source list is empty and the widget shows 0. Use count mode instead.

**Q: Can I put a Board inside a Board?**
A: The board's own catalog excludes the Board type, but a board dropped into another board from the main grid is not rejected. Deeply nested boards are not recommended — they become unusable on small screens.

**Q: What time range does the dashboard use for data?**
A: By default, from midnight today until now. If the tab has "Show period selector" enabled, the toolbar picker defines the range; it opens on the period configured for your folder (start hour and duration, by default the current 24-hour day).

**Q: Why don't I hear the notification sounds?**
A: Browsers require a user interaction before allowing audio. Click anywhere in the page first. Also check that the tab isn't muted and that **Sound on new** is enabled in the widget's Visual rules.

**Q: What data does the Chart widget show?**
A: With the "Incidents" data source it shows incidents grouped by level. With "Security events" it shows security event statistics grouped by source and type.

**Q: The PDF export produced an empty or partial page. Why?**
A: Each tab is given a fixed delay to render before being captured. Widgets that are still loading (large maps, slow queries) may be captured empty. Re-run the export once the data is displayed, and avoid switching folders during the export.

## Glossary

| Term | Definition |
|------|-----------|
| **Incident** | A recorded security event requiring attention — has a level (0–5), status (Opened/Acknowledged/Resolved/Closed), timestamp, and description |
| **Police Log / Mention** | A textual record (like a logbook entry) associated with incident management, also known as "main courante" |
| **Activity** | A recorded modification to an incident — who changed what field and when |
| **Security Event** | A lower-level event from physical security systems (sensors, access points) |
| **Folder** | An organizational unit, typically representing a physical site or zone |
| **Level** | Incident severity from 0 (informational) to 5 (critical emergency) |
| **Status** | Incident lifecycle stage: Opened → Acknowledged → Resolved → Closed |
| **Acknowledged** | An operator has seen and accepted responsibility for handling the incident |
| **Resolved** | The incident has been addressed but not yet formally closed |
| **Webhypervisor** | An elevated permission role that allows controlling physical equipment (sensors, access points) |
| **DAS** | Device — a type of physical security equipment entity |
| **Macro Object** | A logical grouping of multiple physical entities that can be controlled as one |
| **Breakpoint** | A screen-width threshold where the grid changes its column count to adapt to the available space. Four are used: 2, 4, 8 and 12 columns |
| **Dashboard Rights** | Role-based permissions (Reader/Writer/Administrator) controlling what a user can do on dashboards |
| **ICE** | Internet Communications Engine — the protocol used for backend communication (not a user-facing concept, but referenced in error messages) |
