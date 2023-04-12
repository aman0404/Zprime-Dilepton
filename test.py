import pandas as pd
import numpy as np

df = pd.read_parquet("/depot/cms/private/users/kaur214/output/elec_channel_v1_overlap/stage1_output/2018/tW/da419a1b36d934b9549cf2fbe1d8f89d.parquet")

#arccos = np.arccos(df["lb_angle"].unique())

#print(arccos[arccos < 0.1])

#mask = (df["bjet1_mb1_dR"] == False)

#newdf = df.where(mask)

#newdff = newdf.dropna()


#new_df_final = pd.DataFrame(newdff, columns=["b1l1_dR", "mu1_pt", "bjet1_pt", "mu1_eta", "bjet1_eta", "mu1_phi", "bjet1_phi"])
print(df["wgt_nominal"])
#for col in (df.columns):
#     print(col)
