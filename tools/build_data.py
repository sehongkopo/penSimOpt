"""Build the slim data files in data/ from the author's result directories.

This script documents where every file in data/ came from; it runs only where the original project tree
(02_script/, 03_result/, 01_data/) exists. Large arrays are reduced to the keys that the notebooks read,
keeping their names and shapes, so that the notebooks index them exactly as the original scripts did.

    python tools/build_data.py /path/to/01_Bioprocess
"""
import os, sys, json, pickle, shutil
import numpy as np

if len(sys.argv) < 2:
    sys.exit(__doc__)
ROOT = os.path.abspath(sys.argv[1])
HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(os.path.dirname(HERE), 'data')
os.makedirs(DATA, exist_ok=True)
SLIM = 1e6          # npz files larger than this keep only the keys that are read


def slim_npz(src, dst, keys):
    z = np.load(src, allow_pickle=True)
    out = {}
    for k in keys:
        a = z[k]
        if k == 'u':                       # only the discharge rate (column 12) is read
            b = np.zeros_like(a); b[..., 12] = a[..., 12]; a = b
        elif k == 'par':                   # only par[:, 0, 74] (PAA concentration of the PAA feed) is read
            a = a[:, :1, :]
        out[k] = a
    np.savez_compressed(dst, **out)


# 1) inputs of the figure and Table 2 notebooks, traced from the original scripts
for line in open(os.path.join(HERE, 'manifest.tsv')):
    if line.startswith('#') or not line.strip():
        continue
    rel, keys = (line.rstrip('\n').split('\t') + [''])[:2]
    src = os.path.join(ROOT, rel); dst = os.path.join(DATA, os.path.basename(rel))
    keys = [k for k in keys.split(',') if k]
    if src.endswith('.npz') and keys and os.path.getsize(src) > SLIM:
        slim_npz(src, dst, keys)
    else:
        shutil.copy2(src, dst)

# 2) Table S3 and Table S4 (saved results of the imitation and APC-with-sugar-schedule runs)
for rel in ('03_result/w77_cem_imitate.json', '03_result/w77_cem_rows.npz', '03_result/w78_apc_sugar.npz'):
    shutil.copy2(os.path.join(ROOT, rel), os.path.join(DATA, os.path.basename(rel)))

# 3) Table 1: yields and 12 h PAA of pyIndPenSim with Raman-based control off and on (seeds 2000-2099)
shutil.copy2(os.path.join(ROOT, '02_script/04_gpu/raman_onoff_paa.npz'), os.path.join(DATA, 'raman_onoff_paa.npz'))

# 4) Table 1: trajectories of the 300-batch pyIndPenSim pool on the 0.2 h grid
TGRID = np.arange(0.2, 230 + 1e-9, 0.2)
sys.path.insert(0, os.path.join(ROOT, '02_script/01_indPenSim_converter'))     # classes of the pickled records
pool = pickle.load(open(os.path.join(ROOT, '03_result/py_pool_300.pkl'), 'rb'))
traj = {k: np.vstack([np.interp(TGRID, np.asarray(pool[f'Batch_{b:02d}'][k].t, float),
                                np.asarray(pool[f'Batch_{b:02d}'][k].y, float)) for b in range(1, 301)])
        for k in ('P', 'S', 'DO2', 'pH', 'T', 'V')}
np.savez_compressed(os.path.join(DATA, 'table1_pool300.npz'), tgrid=TGRID, **{f'traj_{k}': v for k, v in traj.items()})

# 5) Table 1: reference quantities from the released dataset (see extract_table1_reference.py)
os.system(f'{sys.executable} {os.path.join(HERE, "extract_table1_reference.py")} '
          f'"{os.path.join(ROOT, "01_data/01_indPenSim/02_batch_dataset/Mendeley_data")}" '
          f'"{os.path.join(DATA, "table1_reference.npz")}"')

tot = sum(os.path.getsize(os.path.join(DATA, f)) for f in os.listdir(DATA))
print(f'{len(os.listdir(DATA))} files, {tot / 1e6:.1f} MB in {DATA}')
