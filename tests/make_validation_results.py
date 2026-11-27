"""Run pytest verbosely and write reproducible project validation details."""
from datetime import datetime
import subprocess, sys, re
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import numpy as np
import PIL, matplotlib
try:
    import streamlit
except ImportError:
    streamlit = None
from math_engine.converter import RGB_TO_YIQ, GRAYSCALE_MATRIX
from math_engine.matrix import determinant, matrix_inverse, matrix_rank
from math_engine.converter import grayscale_null_space

def main():
    run=subprocess.run([sys.executable,"-m","pytest","-v"],capture_output=True,text=True)
    output=run.stdout + "\n" + run.stderr
    output=re.sub(r"\x1b\[[0-9;]*m", "", output)
    passed=[line.strip() for line in output.splitlines() if " PASSED" in line]
    summary=next((re.sub(r"=+","",l).strip() for l in output.splitlines() if re.search(r"\d+ passed",l)),"Summary unavailable")
    a=np.asarray(RGB_TO_YIQ,dtype=float)
    sample=np.array([255.,120.,60.])
    diff_pixel=float(np.max(np.abs(np.asarray([[sum(RGB_TO_YIQ[i][j]*sample[j] for j in range(3))] for i in range(3)]).ravel()-a@sample)))
    det_diff=abs(determinant(RGB_TO_YIQ)-float(np.linalg.det(a)))
    inv_diff=float(np.max(np.abs(np.asarray(matrix_inverse(RGB_TO_YIQ))-np.linalg.inv(a))))
    rank_diff=abs(matrix_rank(RGB_TO_YIQ)-int(np.linalg.matrix_rank(a)))
    v=np.asarray(grayscale_null_space()[0])
    null_diff=float(np.linalg.norm(np.asarray(GRAYSCALE_MATRIX)@v))
    lines=["# Validation Results","",f"Date: {datetime.now().astimezone().isoformat(timespec='seconds')}",
    f"Python: {sys.version.split()[0]}",f"NumPy: {np.__version__}",f"Pillow: {PIL.__version__}",
    f"Streamlit: {getattr(streamlit,'__version__','not installed') if streamlit else 'not installed'}",f"Matplotlib: {matplotlib.__version__}","",
    "## Pytest result","",f"`{summary}`","","## Passed tests",""]
    lines += [f"- `{x}`" for x in passed]
    lines += ["","## From-scratch vs NumPy comparison","","| Check | Maximum absolute difference |","|---|---:|",
    f"| Sample pixel (255,120,60) to YIQ | {diff_pixel:.3e} |",
    f"| Determinant | {det_diff:.3e} |",f"| Inverse matrix | {inv_diff:.3e} |",
    f"| Rank | {rank_diff:.3e} |",f"| Null-space check ||Gv|| | {null_diff:.3e} |",""]
    (Path(__file__).with_name("validation_results.md")).write_text("\n".join(lines), encoding="utf-8")
    print(output)
    if run.returncode: raise SystemExit(run.returncode)
if __name__=="__main__": main()
