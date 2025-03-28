import torch
import numpy as np
import torch.nn as nn
import glob
import dask.dataframe as dd
import dask
import pandas as pd
from matplotlib import pyplot as plt
import math




device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

torch.manual_seed(0)

import random
random.seed(0)

np.random.seed(0)

load_features = [
    "mu1_eta",
    "mu1_phi",
    "mu1_pt",
    "mu2_eta",
    "mu2_phi",
    "mu2_pt",
    "bjet1_pt",
    "bjet1_eta",
    "bjet1_phi",
    "lb_angle",
    "nbjets",
    "met",
    "min_bl_mass",

    "bjet1_mb1_dR",
    "bjet1_mb2_dR",
    "dimuon_mass",
    "dimuon_mass_gen",
    "wgt_nominal",
    "dataset",
]

class NeuralNet(nn.Module):
    def __init__(self, input_size, hidden_sizes, num_classes):
        super(NeuralNet, self).__init__()
        layers = []
        layers.append(nn.Linear(input_size, hidden_sizes[0]))
        layers.append(nn.ELU())
        
        for i in range(len(hidden_sizes)-1):

            layers.append(nn.Linear(hidden_sizes[i], hidden_sizes[i+1]))
            layers.append(nn.ELU())
            layers.append(nn.Dropout(p=0.4)) #v7 value
            #layers.append(nn.Dropout(p=0.3)) #default

        layers.append(nn.Linear(hidden_sizes[-1], num_classes))
        layers.append(nn.Sigmoid())
        self.layers = nn.ModuleList(layers)
    def forward(self, x):
        out = self.layers[0](x)
        for i in range(1, len(self.layers)):
            out = self.layers[i](out)
      
        return out


if (len(load_features)- 6) < 16:
   print(len(load_features)-5)
   input_size = (len(load_features)-6)
   print(input_size)
   hidden_sizes = [128, 64, 32, 16]
   #hidden_sizes = [6]
   learning_rate = 1e-5
   #learning_rate = 1e-5 #default
   #learning_rate = 0.0001
else:

   input_size = len(load_features) - 3
   hidden_sizes = [128, 64, 32, 16, 16, 16, 16, 16, 16]
   learning_rate = 0.0001

print("final layers ", hidden_sizes)
num_classes = 1
#num_epochs = 20
num_epochs = 40
batch_size = 512
#batch_size = 128 #default

model = NeuralNet(input_size, hidden_sizes, num_classes).to(device)
model = model.double()
criterion = nn.BCELoss()
optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)
decayRate = 0.90
my_lr_scheduler = torch.optim.lr_scheduler.ExponentialLR(optimizer=optimizer, gamma=decayRate)

#default

#testing


sig_path1 = "/depot/cms/private/users/kaur214/output/muchannel_2018_testingmuSF_iso/stage1_output/2016*/bsll_lambda1TeV_M*/*parquet"


bkg_path = "/depot/cms/private/users/kaur214/output/muchannel_2018_testingmuSF_iso/stage1_output/2016*/ttbar*/*parquet"
bkg_path1 = "/depot/cms/private/users/kaur214/output/muchannel_2018_testingmuSF_iso/stage1_output/2016*/tW/*parquet"
bkg_path2 = "/depot/cms/private/users/kaur214/output/muchannel_2018_testingmuSF_iso/stage1_output/2016*/Wantitop/*parquet"

#sig_path = "output/trainData_v1/2018/sig/bbll_4TeV_*_posLL/*parquet"
#bkg_path = "output/trainData_v1/2018/bkg/*/*parquet"
#data_path = "output/trainData_v1/2018/data/*/*parquet"


sig_files1 = glob.glob(sig_path1)

#sig_files = glob.glob(sig_path)

bkg_files = glob.glob(bkg_path)
bkg_files1 = glob.glob(bkg_path1)
bkg_files2 = glob.glob(bkg_path2)
#data_files = glob.glob(data_path)

df_sig1 = dd.read_parquet(sig_files1)
#
sig_frames = [df_sig1]
df_sig = dd.concat(sig_frames)

#df_sig = df_sig.compute()

#df_sig = dd.read_parquet(sig_files)

#df_sig = df_sig.compute()
#for col in df_sig.columns:
#    print(col)

df_bkg0 = dd.read_parquet(bkg_files)
df_bkg1 = dd.read_parquet(bkg_files1)
df_bkg2 = dd.read_parquet(bkg_files2)

df_sig = df_sig[load_features]
df_sig = df_sig.compute()

frames = [df_bkg0, df_bkg1, df_bkg2]
df_bkg = dd.concat(frames)

df_bkg = df_bkg[load_features]
df_bkg = df_bkg.compute()

#def cal_theta(value1, value2):
#    theta1 = 2*np.arctan(np.exp(-1*value1))
#    theta2 = 2*np.arctan(np.exp(-1*value2))
#    dtheta = math.fabs(theta1-theta2)
#    return(dtheta)


#def cal_dtheta(mu1_eta,bjet1_eta):
#    theta_mu1 = 2*np.arctan(np.exp(-1*mu1_eta))
#    theta_bjet1 = 2*np.arctan(np.exp(-1*bjet1_eta))
#    dtheta = np.fabs(theta_mu1-theta_bjet1)
#    return dtheta
#
#sig_dtheta = np.ones(len(df_sig))
#bkg_dtheta = np.ones(len(df_bkg))
##bkg_dtheta = []
#
#sig_theta_plot = []
#bkg_theta_plot = []
#
#for i in range(len(df_sig)):
##    sig_mueta = df_sig["mu1_eta"].iloc[i]
##    sig_bjeteta = df_sig["bjet1_eta"].iloc[i]
##    sig_dtheta[i] = cal_dtheta(sig_mueta, sig_bjeteta)
#    sig_bjet_eta = df_sig["bjet1_eta"].iloc[i]
#    sig_dimu_eta = df_sig["dimuon_eta"].iloc[i]
#
#    sig_theta = cal_theta(sig_bjet_eta, sig_dimu_eta) 
#    sig_theta_plot.append(sig_theta)
#
#
#for i in range(len(df_bkg)):
#    bkg_bjet_eta = df_bkg["bjet1_eta"].iloc[i]
#    bkg_dimu_eta = df_bkg["dimuon_eta"].iloc[i]
#
#    bkg_theta = cal_theta(bkg_bjet_eta, bkg_dimu_eta)
#    bkg_theta_plot.append(bkg_theta)
#
#plt.hist(sig_theta_plot, alpha = 0.25, color='blue')
#plt.hist(bkg_theta_plot, alpha = 0.25, color='orange')
#plt.yscale("log")
#plt.show()

#for i in range(len(df_bkg)):
#    bkg_mueta = df_bkg["mu1_eta"].iloc[i]
#    bkg_bjeteta = df_bkg["bjet1_eta"].iloc[i]
#    bkg_dtheta[i] = cal_dtheta(bkg_mueta, bkg_bjeteta)
#
#
#df_sig["theta"] = sig_theta
#df_bkg["theta"] = bkg_theta



df_sig = df_sig.loc[(df_sig["dimuon_mass"] > 200), :]
df_bkg = df_bkg.loc[(df_bkg["dimuon_mass"] > 200), :]

df_sig = df_sig.loc[(df_sig["nbjets"] > 0), :]
df_bkg = df_bkg.loc[(df_bkg["nbjets"] > 0), :]

#df_sig = df_sig.loc[(df_sig["bjet1_mb1_dR"] == True), :]
#df_bkg = df_bkg.loc[(df_bkg["bjet1_mb1_dR"] == True), :]
#
#df_sig = df_sig.loc[(df_sig["bjet1_mb2_dR"] == True), :]
#df_bkg = df_bkg.loc[(df_bkg["bjet1_mb2_dR"] == True), :]


df_bkg = df_bkg[(~((df_bkg["dataset"] == "ttbar_lep_inclusive") & (df_bkg["dimuon_mass_gen"] > 500))) & (~((df_bkg["dataset"] == "WWinclusive") & (df_bkg["dimuon_mass_gen"] > 200)))]

#df_sig = df_sig[load_features]
#df_bkg = df_bkg[load_features]

print(df_sig) 
#print(df_bkg) 

df_sig["label"] = 1.0
df_bkg["label"] = 0

#bkg_yield = sum(df_bkg.wgt_nominal)
#sig_yield = sum(df_sig.wgt_nominal)
#df_sig["wgt_nominal"] = df_sig["wgt_nominal"]*(bkg_yield/sig_yield)

dataset = pd.concat([df_sig, df_bkg], ignore_index=True)


print("signal ",len(df_sig.dropna()), " bkg ",len(df_bkg.dropna()))

print("size ",len(dataset.dropna()))

#dataset = dataset.dropna()
dataset.fillna(dataset.mean(), inplace=True)


dataset = dataset.sample(frac=1.)
print("size ",len(dataset))
train_size = int(0.80*len(dataset))
train_data = dataset.iloc[:train_size, :]

#train_data["mu1_pt"] = train_data["mu1_pt"]/train_data["dimuon_mass"]
#train_data["mu1_eta"] = train_data["mu1_eta"]/train_data["dimuon_mass"]
#train_data["mu1_phi"] = train_data["mu1_phi"]/train_data["dimuon_mass"]
#
#train_data["mu2_pt"] = train_data["mu2_pt"]/train_data["dimuon_mass"]
#train_data["mu2_phi"] = train_data["mu2_phi"]/train_data["dimuon_mass"]
#train_data["mu2_eta"] = train_data["mu2_eta"]/train_data["dimuon_mass"]


train_data.to_parquet("/home/kaur214/Zp_analysis/Zprime-Dilepton/output/trainData_v1/2016/train_data.parquet")

print("train data parameters ", len(train_data))
#train_data = train_data.loc[train_data["dimuon_mass"] > 200., :].copy()

train = train_data.drop(columns = ["wgt_nominal", "dataset", "label", "dimuon_mass", "dimuon_mass_gen", "bjet1_mb1_dR", "bjet1_mb2_dR"]).values


#train = train_data.drop(columns = ["wgt_nominal", "dataset", "label", "dimuon_mass", "nbjets", "mu1_phi"]).values
#train = train_data.drop(columns = ["wgt_nominal", "dataset", "label", "dimuon_mass","nbjets","mu1_phi", "mmj_min_dEta", "dtheta"]).values

train_labels = train_data["label"].values
train_wgt = train_data["wgt_nominal"].values
val_data = dataset.iloc[train_size:, :]

#val_data["mu1_pt"] = val_data["mu1_pt"]/val_data["dimuon_mass"]
#val_data["mu1_eta"] = val_data["mu1_eta"]/val_data["dimuon_mass"]
#val_data["mu1_phi"] = val_data["mu1_phi"]/val_data["dimuon_mass"]
#
#val_data["mu2_pt"] = val_data["mu2_pt"]/val_data["dimuon_mass"]
#val_data["mu2_phi"] = val_data["mu2_phi"]/val_data["dimuon_mass"]
#val_data["mu2_eta"] = val_data["mu2_eta"]/val_data["dimuon_mass"]

print("val data parameters ", len(val_data))
val_data.to_parquet("/home/kaur214/Zp_analysis/Zprime-Dilepton/output/trainData_v1/2016/val_data.parquet")

#val_data = val_data.loc[val_data["dimuon_mass"] > 200., :].copy()

val = val_data.drop(columns = ["wgt_nominal", "dataset", "label", "dimuon_mass", "dimuon_mass_gen", "bjet1_mb1_dR", "bjet1_mb2_dR"]).values

#val = val_data.drop(columns = ["wgt_nominal", "dataset", "label", "dimuon_mass", "nbjets", "mu1_phi"]).values
#val = val_data.drop(columns = ["wgt_nominal", "dataset", "label", "dimuon_mass","nbjets","mu1_phi", "mmj_min_dEta", "dtheta"]).values
val_labels = val_data["label"].values
val_wgt = val_data["wgt_nominal"].values

#train = torch.from_numpy(train)
#train_label = torch.from_numpy(train_label)
#train_wgt = torch.from_numpy(train_wgt)

total_step = train_size
validationloss = []
trainingloss = []

validationloss_wgt = []
trainingloss_wgt = []

for epoch in range(num_epochs):
    print("RUNNING ")
    mean_loss = 0
    tot_wgt = 0
    val_mean_loss = 0
    val_tot_wgt = 0
    for i in range(int(train_size/batch_size)):  
        # Move tensors to the configured device
        data = torch.from_numpy(train[i*batch_size: (i+1)*batch_size]).to(device)
        label = torch.from_numpy(train_labels[i*batch_size: (i+1)*batch_size].reshape((batch_size,1))).to(device)
        #w = torch.from_numpy(train_wgt[i]).to(device)
        w = torch.from_numpy(train_wgt[i*batch_size: (i+1)*batch_size]).to(device)
        # Forward pass
        outputs = model(data.double()) 
        loss = criterion(outputs, label.double())
        weight_loss = loss*w
        # Backward and optimize
        optimizer.zero_grad()
        weight_loss.mean().backward()
        optimizer.step()
        mean_loss += weight_loss.mean().item()*batch_size
        tot_wgt += sum(w.cpu().detach().numpy())
        if i%4 == 0:
            j = int(i/4)
            val_data = torch.from_numpy(val[j*batch_size: (j+1)*batch_size]).to(device)
            val_label = torch.from_numpy(val_labels[j*batch_size: (j+1)*batch_size].reshape(val_labels[j*batch_size: (j+1)*batch_size].shape[0],1)).to(device)
            val_w = torch.from_numpy(val_wgt[j*batch_size: (j+1)*batch_size]).to(device)
            val_outputs = model(val_data.double())
            #if abs(val_outputs)>1:
            #    print(val_data)
            #    print(val_output)
            val_loss = criterion(val_outputs, val_label.double())
            val_mean_loss += (val_loss*val_w).mean().item()*batch_size
            val_tot_wgt += sum(val_w.cpu().detach().numpy())    

        if (i+1) % 100 == 0:
            print ('Epoch [{}/{}], Step [{}/{}], Train Loss: {:.4f}, Val Loss: {:.4f}' 
                   .format(epoch+1, num_epochs, i+1, int(total_step/batch_size), mean_loss/tot_wgt, val_mean_loss/val_tot_wgt))

            mean_loss=0
            tot_wgt=0
            val_mean_loss=0
            val_tot_wgt=0

    trainingloss_wgt.append(mean_loss/tot_wgt)
    validationloss_wgt.append(val_mean_loss/val_tot_wgt)

    trainingloss.append(mean_loss)
    validationloss.append(val_mean_loss)

    my_lr_scheduler.step()

plt.plot(trainingloss_wgt, label='train_loss')
plt.plot(validationloss_wgt,label='val_loss')
plt.legend()
#plt.ylim(0.0, 0.05)
plt.xlim(0., num_epochs)
plt.xlabel("Epochs")
plt.ylabel("Loss")
plt.savefig("/depot/cms/users/kaur214/analysis_facility/ML_plots/loss_epochs_wgt_div_bbll_2016.png")
plt.clf()

plt.plot(trainingloss, label='train_loss')
plt.plot(validationloss,label='val_loss')
plt.legend()
#plt.ylim(0.0, 3.0)
plt.xlim(0., num_epochs)
plt.xlabel("Epochs")
plt.ylabel("Loss")
plt.savefig("/depot/cms/users/kaur214/analysis_facility/ML_plots/loss_epochs_div_bbll_2016.png")
plt.clf()


torch.save(model.state_dict(), 'model_year2016_div_bbll_vtest.ckpt')




