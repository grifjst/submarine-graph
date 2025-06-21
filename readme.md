# ⚓ Submarine GitHub Grid Animation

A SVG animation of a submarine navigating across a 52x7 grid that mimics GitHub's contribution graph layout — with no actual contribution data required.

<div align="center">
  <img src="https://raw.githubusercontent.com/grifjst/submarine-graph/output/submarine-graph.svg" alt="Submarine GitHub Grid Animation" />
</div>

---

## ⚙️ How It Works

- Generates a 52x7 grid that resembles GitHub's contribution graph layout.
- Submarine animates along randomly selected cells.
- Uses `svgwrite` to render the SVG with custom shapes, animation, and bubbles.
- Outputs an animated SVG file: `submarine-graph.svg`.

---

## 🔒 Security Notice
Make sure to keep your GitHub token private. Do not commit your .env file or token to public repositories.

## 📂 Output
After running the script, the SVG file submarine_grid.svg will be created in the project folder. Open it in a browser to see your animated submarine on the contribution grid.

## 🛠️ Troubleshooting
If the script fails with an API error, verify that your GitHub token is set correctly.

Ensure your environment variables are loaded if using .env.

## 🛠️ Setup Instructions

1. **Clone this repository**:

```bash
git clone https://github.com/grifjst/submarine-graph.git
cd submarine-graph

2. **Install required Python packages:**

```bash
pip install requests svgwrite

3. **Create a .env file in the root folder with this content:**

```bash
GITHUB_TOKEN=your_token_here

4. **Run the script:**








