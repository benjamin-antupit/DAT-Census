| Method/Module     | Methods & Parameters                                                                                                                                                                                                                                                                                                 |
|-------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| parser            | Parameter(s) – N/A Creates File Output according to user input                                                                                                                                                                                                                                                       |
| random_sample     | Parameter(s) – df, sample_size, fraction, column  df – Data in a DF format  sample_size – size of sample. If empty, will return nothing.  Fraction – fraction of full dataset to sample  Column – String with name of question  Returns a randomly sampled section of the data                                       |
| weighted_sample   | Parameter(s) – df, column, n, frac, weights  df – Data in a DF format  column – column to apply weights to  n – sample size  frac - sample size as a fraction of dataframe length  weights – weights to be applied. If empty, all weights will be equal.  Returns a sampled section of the data based off of weights |
| stratified_sample | Parameter(s) – df, column, n, weights  df – Data in a DF format  Column – string of column name to stratify  n – sample size  Fraction – fraction of full dataset to sample  Must enter either n or fraction. Returns a stratified sample of the data.                                                               |