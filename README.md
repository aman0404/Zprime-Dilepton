## Zprime-dilepton - A data analyis framework for the high-mass dilepton search based on NanoAOD


The full documentation of the Analyzer can be found in the wiki page of this repository:

https://github.com/aman0404/Zprime-Dilepton/wiki

**A brief overview:**

- Data analysis is performed based on the CMS NanoAOD data format using the [columnar approach](https://indico.cern.ch/event/759388/contributions/3306852/attachments/1816027/2968106/ncsmith-how2019-columnar.pdf), making use of the tools provided by [coffea](https://github.com/CoffeaTeam/coffea) package
- This framework uses the [copperhead](https://github.com/Run3HmmAnalysis/copperhead) framework developed for the H&rarr;µµ analysis by [Dmitry Kondratyev](https://github.com/kondratyevd) et. al. as a backend, re-implementing only analysis-specific code

### Framework structure, data formats, used packages
The input data for the framework should be in `NanoAOD` format.

The analysis workflow contains three stages:
- **NanoAOD processing** (WIP )includes event and object selection, application of corrections, and construction of new variables. All event weights, including normalization of MC events to luminosity, are applied already in this step. The data columns are handled via `coffea`'s `NanoEvents` format which relies on *jagged arrays* implemented in [Awkward Array](https://github.com/scikit-hep/awkward-1.0) package. After event selection, the jagged arrays are converted to flat [pandas](https://github.com/pandas-dev/pandas) dataframes and saved into [Apache Parquet](https://github.com/apache/parquet-format) files.
- **Analysis** (WIP) event categorization and production of histograms and unbinned datasets. In the future it might contain also the evaluation of MVA methods (boosted decision trees, deep neural networks),  The workflow is structured as follows:
  - Outputs of the NanoAOD processing (`Parquet` files) are loaded as partitions of a [Dask DataFrame](https://docs.dask.org/en/stable/dataframe.html) (similar to Pandas DF, but partitioned and "lazy").
  - The Dask DataFrame is (optionally) re-partitioned to decrease number of partitions.
  - The partitions are processed in parallel; for each partition, the following sequence is executed:
    - Partition of the Dask DataFrame is "computed" (converted to a Pandas Dataframe).
    - Definition of event categories.
    - Creating 1D or 2D histograms using [scikit-hep/hist](https://github.com/scikit-hep/hist).
    - Saving histograms.
    - (Optionally) Saving individual columns (can be used later for unbinned fits).

- **Result** (WIP) contains / will contain plotting, parametric fits, preparation of datacards for statistical analysis. The plotting is done via [scikit-hep/mplhep](https://github.com/scikit-hep/mplhep).

### Job parallelization
The analysis workflow is efficiently parallelised using [dask/distributed](https://github.com/dask/distributed) with either a local cluster (uses CPUs on the same node where the job is launched), or a distributed `Slurm` cluster initialized over multiple computing nodes. The instructions for the Dask client initialization in both modes can be found [here](docs/dask_client.md).

It is possible to create a cluster with other batch submission systems (`HTCondor`, `PBS`, etc., see full list in [Dask-Jobqueue API](https://jobqueue.dask.org/en/latest/api.html#)) and support will be added in collaboration with users.

