"""Extract the reference (MATLAB) quantities used in Table 1 from the released IndPenSim dataset.

Source: Goldrick et al. (2019), "100_Batches_IndPenSim_V3.csv" and "100_Batches_IndPenSim_Statistics.csv"
(Mendeley Data, CC BY 4.0). Batches 1-30 are recipe-driven with Raman-based control off, 61-90 are under
Raman-based PAA control, 91-100 contain faults.

Output data/table1_reference.npz:
  yield_kg (100,)            net penicillin yield of every batch, kg
  fault (100,)               fault flag of every batch
  paa_off_mgL, paa_times     off-line PAA samples (mg/L) of each batch and their times (h), object arrays
  traj_<var> (90, G)         S, DO2, pH, T, V and P of the 90 fault-free batches on the 0.2 h grid TGRID
"""
import sys, numpy as np, pandas as pd

src = sys.argv[1] if len(sys.argv) > 1 else '.'
out = sys.argv[2] if len(sys.argv) > 2 else 'data/table1_reference.npz'
TGRID = np.arange(0.2, 230 + 1e-9, 0.2)
TS = {'P': 'Penicillin concentration(P:g/L)', 'S': 'Substrate concentration(S:g/L)',
      'DO2': 'Dissolved oxygen concentration(DO2:mg/L)', 'pH': 'pH(pH:pH)', 'T': 'Temperature(T:K)',
      'V': 'Vessel Volume(V:L)'}
PAA = 'PAA concentration offline(PAA_offline:PAA (g L^{-1}))'

st = pd.read_csv(f'{src}/100_Batches_IndPenSim_Statistics.csv'); st.columns = [c.strip() for c in st.columns]
y = st['Penicllin_yield_total (kg)'].to_numpy(float) / 1000.0          # the column is recorded in g
fault = st['Fault ref(0-NoFault 1-Fault)'].to_numpy(int)
df = pd.read_csv(f'{src}/100_Batches_IndPenSim_V3.csv', usecols=['Time (h)', PAA] + list(TS.values()))
t = df['Time (h)'].to_numpy()
start = np.where(np.r_[True, np.diff(t) <= 0])[0]; bounds = list(start) + [len(t)]
assert len(start) == 100
paa = np.empty(100, object); paa_t = np.empty(100, object); traj = {k: [] for k in TS}
for b in range(100):
    i0, i1 = bounds[b], bounds[b + 1]
    v = df[PAA].to_numpy()[i0:i1]; ok = np.isfinite(v) & (v > 0)        # recorded in mg/L despite the header
    paa[b] = v[ok]; paa_t[b] = t[i0:i1][ok]
    if fault[b] == 0:
        for k, col in TS.items(): traj[k].append(np.interp(TGRID, t[i0:i1], df[col].to_numpy()[i0:i1]))
np.savez_compressed(out, yield_kg=y, fault=fault, paa_off_mgL=paa, paa_times=paa_t, tgrid=TGRID,
                    **{f'traj_{k}': np.vstack(v) for k, v in traj.items()})
print('saved', out, {k: np.vstack(v).shape for k, v in traj.items()})
