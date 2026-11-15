from pathlib import Path
import matplotlib.pyplot as plt
from PIL import Image


OUT = Path(__file__).resolve().parent

ASSETS = {
    "cap-units-chain": [r"$1\,\mathrm{F}=1{,}000{,}000\,\mu\mathrm{F}\qquad 1\,\mu\mathrm{F}=1{,}000\,\mathrm{nF}\qquad 1\,\mathrm{nF}=1{,}000\,\mathrm{pF}$"],
    "cap-convert-220nf": [r"$220\,\mathrm{nF}\left(\frac{1\,\mu\mathrm{F}}{1000\,\mathrm{nF}}\right)=0.220\,\mu\mathrm{F}$"],
    "cap-qcv": [r"$Q=CV$"],
    "cap-qcv-white": [r"$Q=CV$"],
    "cap-given-68uf": [r"$\mathrm{GIVEN}\quad C=68\,\mu\mathrm{F}\qquad V=9.0\,\mathrm{V}$"],
    "cap-unknown-q": [r"$\mathrm{UNKNOWN}\quad Q\;\mathrm{in\ coulombs}$"],
    "cap-equation-qcv": [r"$\mathrm{EQUATION}\quad Q=CV$"],
    "cap-convert-68uf": [r"$68\,\mu\mathrm{F}\left(\frac{1\,\mathrm{F}}{1{,}000{,}000\,\mu\mathrm{F}}\right)=68\times10^{-6}\,\mathrm{F}$"],
    "cap-q-solution": [r"$Q=CV$", r"$Q=(68\times10^{-6}\,\mathrm{F})(9.0\,\mathrm{V})$", r"$Q=612\times10^{-6}\,\mathrm{C}$", r"$Q=612\,\mu\mathrm{C}$"],
    "cap-energy": [r"$E=\frac{CV^2}{2}$"],
    "cap-energy-white": [r"$E=\frac{CV^2}{2}$"],
    "rc-start-v": [r"$v_C(0)=0\,\mathrm{V}$"],
    "rc-start-v-white": [r"$v_C(0)=0\,\mathrm{V}$"],
    "rc-start-i": [r"$i(0)=\frac{V_S}{R}$"],
    "rc-start-i-white": [r"$i(0)=\frac{V_S}{R}$"],
    "rc-steady-v": [r"$v_C(\infty)=V_S$"],
    "rc-steady-v-white": [r"$v_C(\infty)=V_S$"],
    "rc-steady-i": [r"$i(\infty)=0\,\mathrm{A}$"],
    "rc-steady-i-white": [r"$i(\infty)=0\,\mathrm{A}$"],
    "rc-landmarks": [r"$t=\tau:\quad v_C\approx0.632V_S\;\mathrm{charging},\quad v_C\approx0.368V_0\;\mathrm{discharging}$", r"$t=5\tau:\quad \mathrm{use\ the\ practical\ final\ value}$"],
    "rc-worked-model": [r"$\mathrm{GIVEN}\quad V_S=12.0\,\mathrm{V},\quad t=\tau\;\mathrm{and}\;5\tau$", r"$\mathrm{UNKNOWN}\quad v_C(\tau),\quad v_C(5\tau)$", r"$\mathrm{EQUATIONS}\quad v_C(\tau)\approx0.632V_S,\quad v_C(5\tau)\approx0.993V_S$"],
    "rc-worked-solutions": [r"$v_C(\tau)=0.632(12.0\,\mathrm{V})=7.58\,\mathrm{V}$", r"$v_C(5\tau)=0.993(12.0\,\mathrm{V})=11.9\,\mathrm{V}$"],
    "rc-tau": [r"$\tau=RC$"],
    "rc-tau-white": [r"$\tau=RC$"],
    "rc-unit-shortcuts": [r"$\Omega\cdot\mathrm{F}=\mathrm{s}$", r"$\mathrm{k}\Omega\cdot\mu\mathrm{F}=\mathrm{ms}$", r"$\mathrm{M}\Omega\cdot\mu\mathrm{F}=\mathrm{s}$"],
    "rc-given-model": [r"$\mathrm{GIVEN}\quad R=15\,\mathrm{k}\Omega,\quad C=47\,\mu\mathrm{F}$", r"$\mathrm{UNKNOWN}\quad \tau,\quad 5\tau$", r"$\mathrm{EQUATION}\quad \tau=RC$"],
    "rc-time-solution": [r"$\tau=(15\,\mathrm{k}\Omega)(47\,\mu\mathrm{F})=705\,\mathrm{ms}=0.705\,\mathrm{s}$", r"$5\tau=5(0.705\,\mathrm{s})=3.525\,\mathrm{s}$"],
    "rc-time-line-1": [r"$\tau=(15\,\mathrm{k}\Omega)(47\,\mu\mathrm{F})=705\,\mathrm{ms}=0.705\,\mathrm{s}$"],
    "rc-time-line-2": [r"$5\tau=5(0.705\,\mathrm{s})=3.525\,\mathrm{s}$"],
    "rc-unit-ms": [r"$\mathrm{k}\Omega\cdot\mu\mathrm{F}=\mathrm{ms}$"],
    "rc-r-formula": [r"$R=\frac{\tau}{C}$"],
    "rc-r-formula-white": [r"$R=\frac{\tau}{C}$"],
    "rc-r-design": [r"$\mathrm{TARGET}\quad \tau=2.0\,\mathrm{s}$", r"$\mathrm{CHOOSE}\quad C=100\,\mu\mathrm{F}$", r"$\mathrm{SOLVE}\quad R=\frac{2.0\,\mathrm{s}}{100\,\mu\mathrm{F}}$", r"$\mathrm{SELECT}\quad R\approx20\,\mathrm{k}\Omega$"],
    "rc-c-formula": [r"$C=\frac{\tau}{R}$"],
    "rc-c-formula-white": [r"$C=\frac{\tau}{R}$"],
    "rc-c-design": [r"$\mathrm{TARGET}\quad \tau=0.50\,\mathrm{s}$", r"$\mathrm{CHOOSE}\quad R=10\,\mathrm{k}\Omega$", r"$\mathrm{SOLVE}\quad C=\frac{0.50\,\mathrm{s}}{10\,\mathrm{k}\Omega}$", r"$\mathrm{SELECT}\quad C\approx50\,\mu\mathrm{F}$"],
    "rc-charge-model": [r"$v_C(t)=V_S\left(1-e^{-t/(RC)}\right)$"],
    "rc-discharge-model": [r"$v_C(t)=V_0e^{-t/(RC)}$"],
}

WHITE_ASSETS = {
    "cap-qcv-white",
    "cap-energy-white",
    "rc-start-v-white",
    "rc-start-i-white",
    "rc-steady-v-white",
    "rc-steady-i-white",
    "rc-tau-white",
    "rc-r-formula-white",
    "rc-c-formula-white",
}


def render(name: str, lines: list[str]) -> None:
    width = 14
    height = max(1.4, 1.05 * len(lines))
    fig = plt.figure(figsize=(width, height), dpi=220, facecolor="none")
    fig.patch.set_alpha(0)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_axis_off()
    for index, line in enumerate(lines):
        y = 1 - (index + 0.5) / len(lines)
        color = "white" if name in WHITE_ASSETS else "#12202F"
        ax.text(0.5, y, line, color=color, fontsize=34, ha="center", va="center")
    output_path = OUT / f"{name}.png"
    fig.savefig(output_path, transparent=True, bbox_inches="tight", pad_inches=0.08)
    plt.close(fig)
    image = Image.open(output_path).convert("RGBA")
    alpha_bounds = image.getchannel("A").getbbox()
    if alpha_bounds:
        left, top, right, bottom = alpha_bounds
        padding = 24
        cropped = image.crop((max(0, left - padding), max(0, top - padding), min(image.width, right + padding), min(image.height, bottom + padding)))
        cropped.save(output_path)


for asset_name, asset_lines in ASSETS.items():
    render(asset_name, asset_lines)

print(f"Generated {len(ASSETS)} transparent LaTeX-style equation assets.")
