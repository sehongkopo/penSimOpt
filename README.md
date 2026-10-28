# penSimOpt

Jupyter notebooks that reproduce the figures and tables of

> Hong, S.-E. *Process optimisation of fed-batch fermentation using online measurements alone* (submitted to
> Computers & Chemical Engineering).

Every notebook reads the saved results of the study from `data/` and redraws one figure or recomputes one table.
The simulations behind those results, including the controller training, the evaluation runs and the CEM
reference, were run with [pyIndPenSim](https://github.com/sehongkopo/pyIndPenSim), the Python port of the
industrial-scale penicillin fermentation simulator IndPenSim (Goldrick et al., 2015, 2019). They are not repeated
here.

## Quick start

```bash
git clone https://github.com/sehongkopo/penSimOpt.git
cd penSimOpt
python3.12 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
jupyter lab notebooks/            # or run all of them:
jupyter nbconvert --to notebook --execute --inplace notebooks/*.ipynb
```

The notebooks are stored with their outputs, so they can also be read on GitHub without running them. Figures and
tables are written to `output/`.

## Notebooks

| Notebook | Reproduces | Run time |
|---|---|---|
| `Table1.ipynb` | Table 1, agreement of pyIndPenSim with the released IndPenSim dataset | seconds |
| `Fig1.ipynb` | Fig. 1, set-point control of PAA and the narrowing of the operating record | seconds |
| `Fig3.ipynb` | Fig. 3, prediction of PAA from the sixteen on-line channels | seconds |
| `Fig4.ipynb` | Fig. 4, Bayesian optimisation of the controller that sets the PAA feed from the predicted PAA | about 1 min |
| `Fig6.ipynb` | Fig. 6, operating conditions of PPO and CEM, and the yield of all controllers | seconds |
| `Fig7.ipynb` | Fig. 7, how PPO raises the yield | seconds |
| `Table2.ipynb` | Table 2, feed use and yield coefficients on the 200 evaluation batches | about 1 min |
| `Fig8.ipynb` | Fig. 8, trajectories on the 200 evaluation batches by yield class | seconds |
| `Fig9.ipynb` | Fig. 9, narrowing of the operating record and retraining of the controllers | seconds |
| `FigS1.ipynb` | Fig. S1, PPO and SAC trained under the same conditions | seconds |
| `TableS3.ipynb` | Table S3, held-out R² for predicting the settings chosen by CEM | about 1 min |
| `TableS4.ipynb` | Table S4, APC with the sugar-feed schedule of PPO or of the BO-tuned controller | seconds |

Figs. 2 and 5 are schematics and are given as images in `static/`. Table S1 lists the operating variables and
on-line channels and involves no computation.

With the package versions in `requirements.txt`, the figures of Fig. 1, 3, 4, 6 and S1 are byte-identical to those
in the manuscript. Figs. 7–9 were drawn for the manuscript with matplotlib 3.11.2, and with 3.10.8 they differ only
in the anti-aliasing of text; every plotted value is the same. All numbers in the tables agree with the
manuscript.

## Data

`data/` holds 242 files, about 130 MB. Most are the per-batch results of the controllers on the 200 evaluation
batches and the 100 validation batches, stored as NumPy `.npy`/`.npz` and JSON files under the names used in the
study. Large result files were reduced to the arrays that the notebooks read, keeping their names and shapes.

`tools/build_data.py` documents how each file was made from the original result directories, and
`tools/manifest.tsv` lists the source of every file and the arrays kept. These scripts run only where the original
project tree exists.

The reference quantities in `data/table1_reference.npz` were extracted with `tools/extract_table1_reference.py`
from `100_Batches_IndPenSim_V3.csv` and `100_Batches_IndPenSim_Statistics.csv`, the released dataset of Goldrick
et al. (2019) on Mendeley Data. That dataset is distributed under the licence stated on its Mendeley Data page, and
users of the extracted file should cite it.

## Licence

The code is released under the BSD 3-Clause licence (see `LICENSE`).

## References

- Goldrick, S., Ştefan, A., Lovett, D., Montague, G., Lennox, B., 2015. The development of an industrial-scale
  fed-batch fermentation simulation. *J. Biotechnol.* 193, 70–82. https://doi.org/10.1016/j.jbiotec.2014.10.029
- Goldrick, S., Duran-Villalobos, C.A., Jankauskas, K., Lovett, D., Farid, S.S., Lennox, B., 2019. Modern day
  monitoring and control challenges outlined on an industrial-scale benchmark fermentation process.
  *Comput. Chem. Eng.* 130, 106471. https://doi.org/10.1016/j.compchemeng.2019.05.037
