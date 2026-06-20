## Uplift — Design System Reference (HIG-Integrated)

**App:** PyQt6 macOS upload tool. Supports macOS Light and Dark appearance. Panels use Liquid Glass (semi-transparent backgrounds that blur the desktop behind them). All values are overridable at runtime via `~/.uplift-theme.json`.

**Design principles:** Follow Apple Human Interface Guidelines for color, typography, and accessibility. Contrast ratios follow WCAG AA: 4.5:1 minimum for normal text (17px and below), 3:1 minimum for large text (18px+) and bold text, 3:1 minimum for icons and meaningful graphics. When text sits on glass, calculate contrast against the worst-case backdrop (bright desktop in light mode, bright window in dark mode).

### Backgrounds

| Token | Light | Dark | Used on | Glass-safe? |
| --- | --- | --- | --- | --- |
| `BG` | `#F1F0F0` | `#1C1C1E` | Window chrome, queue area fill | No (opaque) |
| `SURFACE` | `#FFFFFF` | `#2C2C2E` | Form panel, job tiles, input boxes, file rows | No (opaque) |
| `SURFACE2` | `#F7F7F7` | `#3A3A3C` | Inactive tab bg, badge bg, strip rows, combo boxes | No (opaque) |
| `SIDEBAR_BG` | `#eae9e9` | `#3A3A3C` *(add this)* | Sidebar (if present) | No (opaque) |

Glass variants (60% opacity over blurred desktop):

- Light: `rgba(241,240,240,0.60)` / `rgba(255,255,255,0.55)` / `rgba(247,247,247,0.58)`
- Dark: `rgba(28,28,30,0.60)` / `rgba(44,44,46,0.55)` / `rgba(58,58,60,0.58)`

### Text

| Token | Light | Dark | Used on | Min surface |
| --- | --- | --- | --- | --- |
| `INK` | `#000000` | `#FFFFFF` | Primary text: filenames, labels, input text | Any (glass or solid) |
| `GRAPHITE` | `#404040` | `#C0C0C0` | Section headers, secondary labels | Any (glass or solid) |
| `STONE` | `#6B6B6B` | `#98989D` | Placeholder text, status text, badge text | Solid `SURFACE` or `SURFACE2` only. Never on bare glass. |
| `MIST` | `#D9D9D9` | `#48484A` | Dividers, horizontal rules, borders | N/A (decorative) |

**Contrast ratios (approximate, verify with a checker):**

| Combination | Light | Dark | WCAG AA (normal text) |
| --- | --- | --- | --- |
| `INK` on `SURFACE` | 21:1 | 14:1 | Pass |
| `INK` on `BG` | 18.5:1 | 16:1 | Pass |
| `INK` on glass | varies | varies | Pass (high contrast white/black survives glass) |
| `GRAPHITE` on `SURFACE` | 12:1 | 9:1 | Pass |
| `GRAPHITE` on glass | varies | varies | Pass (still well above 4.5:1 in worst case) |
| `STONE` on `SURFACE` | 5.9:1 | 4.8:1 | Pass, but dark mode is borderline |
| `STONE` on glass | unpredictable | unpredictable | Fail. Do not place STONE text on glass backgrounds. |
| `STONE` on `SURFACE2` | 5.6:1 | 4.2:1 | Dark mode FAILS. Use GRAPHITE instead on SURFACE2 in dark mode. |

### Brand / Accent Palette (Teal family)

| Token | Hex | Used on |
| --- | --- | --- |
| `TEAL` | `#0089a6` | Active tab bg, primary buttons, WATCH badge background, progress bar fill |
| `TEAL_DEEP` | `#04657e` | Button hover state, Settings/Accounts link color, WATCH badge text, drop zone label text |
| `TEAL_MID` | `#3d9eb6` | Drop zone border (idle), hover borders on inputs and buttons, focus ring |
| `TEAL_SOFT` | `#77b2c6` | Disabled primary button, progress bar gradient end |
| `TEAL_PALE` | `#cfe1e7` | Input/button borders, job tile border, tree widget border, progress bar track |
| `TEAL_WASH` | `#eaf2f5` | Button/input hover background, uploading file row tint, drop zone idle background |

**Accent contrast rules:**

| Combination | Ratio | Status |
| --- | --- | --- |
| `INK` (white) on `TEAL` (`#0089a6`) | ~5.2:1 | Pass for normal text |
| `INK` (white) on `TEAL_DEEP` (`#04657e`) | ~7:1 | Pass |
| `INK` (white) on `TEAL_SOFT` (`#77b2c6`) | ~2.4:1 | FAIL. Disabled buttons must use `STONE` text, not `INK`. `#77b2c6` is too light for white text. |
| `TEAL_DEEP` (`#04657e`) on `SURFACE` (light) | ~5.9:1 | Pass for link text in light mode |
| `TEAL_DEEP` (`#04657e`) on `SURFACE` (dark `#2C2C2E`) | ~2.1:1 | FAIL. In dark mode, use `TEAL` (`#0089a6`) or `TEAL_MID` (`#3d9eb6`) for link/accent text on dark surfaces. `TEAL_MID` on `#2C2C2E` is approximately 3.5:1, which passes for large/bold text only. |

**Accent rules:**

1. `TEAL_DEEP` is for text/links on light surfaces only. In dark mode, switch to `TEAL_MID` for accent text, but only at 12px+ bold (to meet the 3:1 large-text threshold).
2. Never use `TEAL` or any teal shade as body text color. Teals are for: button backgrounds, borders, badges, icons, links, and progress bars.
3. Disabled primary buttons: use `TEAL_SOFT` background with `STONE` text (not `INK`). This is a change from your current spec where disabled buttons presumably keep white text.
4. `TEAL_MID` is the focus ring color. When an input or button receives keyboard focus, paint a 2px `TEAL_MID` outline with 2px inset. Do not confuse hover border with focus ring.

### Toggle Switches (Zip / Email toggles)

| Token | Hex | Used on |
| --- | --- | --- |
| `TOGGLE_ON` | `#3d9eb6` | Pill background when switch is ON |
| `TOGGLE_OFF` | `#D9D9D9` | Pill background when switch is OFF, light mode |
| `TOGGLE_OFF_DARK` | `#48484A` | Pill background when switch is OFF, dark mode |
| `TOGGLE_KNOB` | `#FFFFFF` | Sliding circle on top of pill |

Toggle pill size: 36x16px, radius 8px. Knob: 14x14px circle, animates between x=1 (off) and x=21 (on).

Contrast: `#FFFFFF` knob on `#3d9eb6` (ON) is approximately 2.4:1. This is below WCAG for text but toggles are graphical controls, not text. Apple HIG allows 3:1 for graphical objects. The knob boundary is visible due to the shadow/inset. Acceptable but if the knob ever looks lost, add a 1px `#000000` at 20% opacity border around the knob.

### Status Colors

| Token | Hex | Used on |
| --- | --- | --- |
| `GREEN` | `#197a26` | Status dot (connected), "Done" text, "Watching" indicator, email sent |
| `RED` | `#cc2222` | Failed upload, error dialogs, email failed |
| `YELLOW` | `#9b6e00` | Retry status, pending indicators |

**Contrast findings:**

| Combination | Light ratio | Dark ratio | Normal text (4.5:1) | Large/bold text (3:1) | Icons (3:1) |
| --- | --- | --- | --- | --- | --- |
| `GREEN` on `SURFACE` | ~5.3:1 | ~2.7:1 | Light pass, Dark FAIL | Light pass, Dark FAIL | Light pass, Dark FAIL |
| `RED` on `SURFACE` | ~3.9:1 | ~3.6:1 | FAIL both | Pass both | Pass both |
| `YELLOW` on `SURFACE` | ~4.6:1 | ~3.1:1 | Light pass, Dark FAIL | Pass both | Pass both |

**Status color rules (important):**

1. **Status colors are for icons and indicator dots first.** A status-colored dot or icon next to text is the preferred pattern. Use `INK` or `GRAPHITE` for the accompanying text label.
2. **`RED` as text**: fails 4.5:1 on both light and dark surfaces. Only use `RED` for text at 12px+ bold (meets 3:1 large-text threshold). For normal-sized error text, use `INK` (or `GRAPHITE`) for the message text and a `RED` icon/border alongside it.
3. **`GREEN` in dark mode**: fails even the 3:1 threshold on `#2C2C2E`. In dark mode, use `GREEN` for dots/icons on `SURFACE2` (`#3A3A3C`, slightly better contrast) or lighten it. Consider `#30D158` (Apple's system green dark variant) for dark mode status dots.
4. **`YELLOW` in dark mode**: approximately 3.1:1 on `#2C2C2E`. Passes for icons and large/bold text only. Use `YELLOW` for dots, not small text, in dark mode.
5. **Never use status colors as text on glass backgrounds.** Glass backdrop variability makes contrast unpredictable. Status-colored icons on glass are acceptable since the 3:1 threshold is lower and icons are larger.

**Suggested dark mode status color overrides** (add to dark variant of `~/.uplift-theme.json`):

| Token | Light (current) | Dark (suggested) | Rationale |
| --- | --- | --- | --- |
| `GREEN` | `#197a26` | `#30D158` | Apple system green (dark), passes 3:1 on `#2C2C2E` |
| `RED` | `#cc2222` | `#FF453A` | Apple system red (dark), passes 3:1 on `#2C2C2E` |
| `YELLOW` | `#9b6e00` | `#FF9F0A` | Apple system orange (dark), passes 3:1 on `#2C2C2E` |

These are Apple's own dark-mode system colors, which are specifically tuned for contrast on dark surfaces. Your light-mode values can stay as-is since they're your brand.

### Spacing (pixels)

| Token | Value | Used on |
| --- | --- | --- |
| `SP_PANEL_H` | 20 | Top form panel left/right padding |
| `SP_PANEL_V` | 10 | Top form panel top/bottom padding |
| `SP_QUEUE_H` | 20 | Queue area left/right margin |
| `SP_TILE_GAP` | 10 | Vertical gap between job tiles |
| `SP_ROW_GAP` | 4 | Vertical gap between form rows |

**Base unit rule:** All spacing values must be multiples of 4. Current tokens already comply. Any new padding/margin/gap must follow this (4, 8, 12, 16, 20, 24, 32, 40, 48).

### Typography

Fonts are system (`Helvetica Neue` / `Arial`). Sizes used:

| Size | Weight | Used on | Contrast token |
| --- | --- | --- | --- |
| 10px | Regular | Labels ("Drive:", "Acct:", section headers, small caps) | `GRAPHITE` minimum. Not `STONE` at this size. |
| 11px | Regular | Body text, status labels, button text | `INK` or `GRAPHITE` |
| 12px | Regular | Primary body, drop zone text, toggle labels | `INK` or `GRAPHITE` |
| 13px | Medium | Primary action buttons | `INK` on `TEAL`/`TEAL_DEEP` |
| 15px | Semibold | Window title / wordmark | `INK` |

Semibold used on: tab labels, job tile names, primary buttons, section headers. Monospaced (`SF Mono` / system mono) used on: filenames in file rows and the folder strip.

**Typography rules:**

1. Minimum text size: 10px. Acceptable only for small caps labels and metadata. Use `GRAPHITE`, never `STONE` at 10px (contrast too low at small sizes).
2. Body text minimum: 11px. Use `INK` or `GRAPHITE`.
3. Placeholder text: 11px minimum, `STONE` color, on solid `SURFACE` only.
4. Status text: 12px+ bold if using status colors. Otherwise use `INK`/`GRAPHITE` with a status-colored icon.

### Interactive states (supplements existing tokens)

These states are currently missing from the system. Add them:

| Token | Light | Dark | Used on |
| --- | --- | --- | --- |
| `SURFACE_HOVER` | `#F0F0F0` | `#3A3A3C` | Hover on SURFACE elements (file rows, job tiles, list items) |
| `SURFACE_PRESSED` | `#E5E5E5` | `#323234` | Pressed/clicked on SURFACE elements |
| `INK_DISABLED` | `#B0B0B0` | `#6B6B6B` | Disabled text/icon color (replaces INK on disabled controls) |
| `FOCUS_RING` | `#3d9eb6` | `#3d9eb6` | 2px outline on focused inputs/buttons (same as TEAL_MID) |

### Glass surface rules

1. Text on glass: only `INK` is safe. `INK` (pure black in light, pure white in dark) maintains adequate contrast even when the glass backdrop varies. `GRAPHITE` is safe on glass in light mode (dark gray on bright glass) but risky in dark mode (light gray on potentially bright glass). Use `GRAPHITE` on glass only in light mode.
2. `STONE` on glass: never. Always place `STONE` text on a solid `SURFACE`, `SURFACE2`, or `SURFACE_HOVER` panel behind it.
3. Status colors on glass: icons only, never text. The 3:1 threshold for icons is more forgiving, but even so, prefer placing status icons on solid surfaces when possible.
4. Glass opacity: current 60% is acceptable. Do not go below 50%. Below 50%, the blur effect weakens and contrast becomes too unpredictable.
5. When applying glass to a container (Phase 2), ensure any `STONE` or status-colored text inside that container sits on a nested solid `SURFACE` panel. Do not let low-contrast text float on glass.

### Key UI Structure

- **Top panel** (`JobCreationPanel`): glass surface. Contains tab switcher (Upload Files / Watch Folder), destination folder button, account combo, Zip/Email toggles. All text in this panel must be `INK` or `GRAPHITE` since it sits on glass.
- **Queue panel**: glass background, scrollable list of `JobTile` widgets. No text directly on this glass surface; all text is inside `JobTile` on solid `SURFACE`.
- **JobTile**: glass outer border (`TEAL_PALE`), solid `SURFACE` inner. Header row + folder strip (`SURFACE2`) + file rows + progress bar. All text in JobTile sits on solid `SURFACE` or `SURFACE2`, so `STONE` is safe here.
- **FileRow**: `SURFACE` normally, `TEAL_WASH` while uploading. Shows filename, size, gradient progress bar, status label. Status label text: use `GRAPHITE` with a status-colored dot, or `INK`. Status color as text only at 12px+ bold.
- **TitleBar**: `BG` background with macOS traffic light dots, wordmark, status dot + text, Settings/Accounts links. Settings/Accounts links: `TEAL_DEEP` in light mode, `TEAL_MID` in dark mode (see accent rules above).