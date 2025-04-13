# Salary Prediction with Linear Regression & DVC Pipeline

This project builds a simple Linear Regression model to predict salaries based on years of experience. It uses a modular, reproducible pipeline powered by **DVC (Data Version Control)** and tracks all data and model changes.

---

## Project Structure
├── data/ │ ├── raw/ │ │ └── Salary_dataset.csv │ └── processed/ │ ├── X_train.csv │ ├── X_test.csv │ ├── y_train.csv │ └── y_test.csv ├── models/ │ └── model.pkl ├── src/ │ ├── preprocess.py │ ├── train.py │ └── evaluate.py ├── metrics.json ├── params.yaml ├── dvc.yaml └── README.md

# What is DVC?
DVC (Data Version Control) is an open-source tool for managing data, machine learning models, and pipelines — similar to how Git manages code. It brings structure, reproducibility, and scalability to ML projects.

# Key Features:

1. Data Versioning
Track and version large datasets and models without bloating your Git repo.

2. Reproducible Pipelines
Define ML workflows (e.g., preprocessing → training → evaluation) as pipeline stages. DVC detects which stages to re-run when data or code changes.

3. Metrics Tracking
Automatically log and track evaluation metrics like accuracy, MAE, MSE, etc., and compare them across versions.

4. Experiments
Run experiments with different parameters, datasets, or model versions, and compare their performance easily.

5. Remote Storage Support
Seamlessly push and pull large files to/from cloud storage like Google Drive, S3, GCS, etc.

# How It Works

-- Git for Metadata
DVC doesn't store your large data files or models directly in Git. Instead, it creates lightweight .dvc files that act as pointers to those files stored elsewhere (like in an S3 bucket or Google Drive). These .dvc files, along with pipeline configuration files like dvc.yaml and params.yaml, are committed to Git — allowing you to version-control metadata, not the heavy files themselves.
So when you switch Git branches or commit histories, DVC knows which version of the data or model to use based on the linked .dvc files.

-- Version Control
When you make changes to your data, model, or parameters.
DVC tracks the changes through updated hashes in .dvc files or dvc.lock.
You commit these updated files to Git, preserving the exact version of data used at any point.

-- Remote Storage
Use dvc remote add to set up a bucket (e.g., S3, GDrive). Then push large files via:

-- Metrics & Experiments
Store metrics in metrics.json, track them with DVC, and compare across experiments:



## DVC Setup

### Initialize DVC

```bash
dvc init
```

---

## Track Raw Data with DVC

```bash
dvc add data/raw/Salary_dataset.csv
git add data/raw/Salary_dataset.csv.dvc .gitignore
git commit -m "Add raw salary dataset"
```

---

## Define Pipeline Stages

### Stage 1: Preprocess

```bash
dvc stage add -n preprocess \
  -d src/preprocess.py -d data/raw/Salary_dataset.csv \
  -o data/processed/X_train.csv -o data/processed/X_test.csv \
  -o data/processed/y_train.csv -o data/processed/y_test.csv \
  python src/preprocess.py
```

### Stage 2: Train

```bash
dvc stage add -n train \
  -d src/train.py -d data/processed/X_train.csv -d data/processed/y_train.csv \
  -d params.yaml -o models/model.pkl \
  python src/train.py
```

### Stage 3: Evaluate

```bash
dvc stage add -n evaluate \
  -d src/evaluate.py -d models/model.pkl \
  -d data/processed/X_test.csv -d data/processed/y_test.csv \
  -M metrics.json \
  python src/evaluate.py
```

## Run the Full Pipeline

```bash
dvc repro
```

Runs all stages in order: `preprocess → train → evaluate`.


## Configuration via `params.yaml`

Set model parameters in a central file:

```yaml
train:
  model:
    n_jobs: -1
```

Used inside `train.py` to initialize the model.

## View Metrics

```bash
cat metrics.json
```

**Example Output:**

```json
{
  "mse": 378.79,
  "mae": 15.23,
  "r2": 0.93
}
```

## Visualize the Pipeline

```bash
dvc dag 
```

## Push Code and Data

```bash
git add .
git commit -m "Build complete DVC pipeline"
git push
```

If using a DVC remote storage:

```bash
dvc remote add -d myremote <remote-url>
dvc push
```


## Updating Pipeline

After changing raw data or parameters:

```bash
dvc repro
```

DVC will **only rerun necessary stages** based on file changes.


## How It Works

### Git for Metadata
DVC stores small `.dvc` files and pipeline configs (`dvc.yaml`, `params.yaml`) in Git. These files act as metadata pointers to data and model files.

### Version Control
Git tracks versions of the metadata; the actual large files are versioned and stored in a DVC remote (e.g., cloud storage). Each version of data/model is uniquely hashed and can be pulled by DVC at any time.

### Remote Storage
After configuring a DVC remote:

```bash
dvc remote add -d myremote <remote-url>
dvc push
```

The main files (like `model.pkl`, datasets) are pushed to the cloud or external storage, while Git only tracks metadata.

###  Auto Pipeline Trigger
Any changes to inputs (like raw data or model params) trigger the relevant pipeline stages on `dvc repro`, ensuring efficient recomputation.


## Metrics & Experiments

- Metrics (MSE, MAE, R²) are stored in `metrics.json`.
- Compare metrics over time or between experiments:

```bash
dvc metrics diff
```

- Run and track experiments:

```bash
dvc exp run
dvc exp show
```


## Notes

- `dvc.yaml` holds the pipeline structure.
- `params.yaml` holds model config.
- `metrics.json` tracks model performance.
- All scripts are modularized under the `src/` folder.

