#include "CMS_lumi.C"
#include "TH1.h"
#include "TH1F.h"
#include<iostream>
#include<TFile.h>
#include<TH1F.h>
#include<TH2F.h>
#include<TCanvas.h>
#include<TStyle.h>
#include<TF1.h>
#include<TF2.h>
#include<TGaxis.h>
#include<TTree.h>
#include<TMath.h>

void golden_sys_band_fratio_double_bb()

{
TCanvas *c1= new TCanvas("c1","stacked hists",0,0,700,700);
   c1->SetHighLightColor(2);
   c1->Range(0,0,1,1);
   c1->SetFillColor(0);
   c1->SetBorderMode(0);
   c1->SetBorderSize(3);
   c1->SetLeftMargin(0.12);
   c1->SetRightMargin(0.06);
   c1->SetTopMargin(0.10);
   c1->SetBottomMargin(0.12);
   c1->SetFrameBorderMode(0);

   c1->SetTickx();
   c1->SetTicky();
   c1->SetLogx();

   gPad->SetTickx();
   gPad->SetTicky();

TH1 *unfolded_mu_dy , *unfolded_el_dy;
TH1 *unfolded_mu_data , *unfolded_el_data;

Double_t bins[8] =  {200, 300, 400,500,700,1100,1900,6000};

TFile *f1 = TFile::Open("unfolded_mc_muon_bb_data.root");
f1->GetObject("hunfoldMC", unfolded_mu_dy);

TFile *f2 = TFile::Open("unfolded_mc_elec_bb_data.root");
f2->GetObject("hunfoldMC", unfolded_el_dy);

TFile *f3 = TFile::Open("unfolded_mc_muon_bb_data.root");
f3->GetObject("hunfold_up", unfolded_mu_data);

TFile *f4 = TFile::Open("unfolded_mc_elec_bb_data.root");
f4->GetObject("hunfold_up", unfolded_el_data);



TH2 *htotal, *hmc_stat, *hdata_stat;
TH2 *htotalMC, *hmc_statMC, *hdata_statMC;

TH2 *eehtotal, *eehmc_stat, *eehdata_stat;
TH2 *eehtotalMC, *eehmc_statMC, *eehdata_statMC;

f1->GetObject("histEmatTotal", htotal);
f1->GetObject("histEmatSysUncorr", hmc_stat);
f1->GetObject("histEmatInput", hdata_stat);

f2->GetObject("histEmatTotal", eehtotal);
f2->GetObject("histEmatSysUncorr", eehmc_stat);
f2->GetObject("histEmatInput", eehdata_stat);

f1->GetObject("histEmatTotalMC", htotalMC);
f1->GetObject("histEmatSysUncorrMC", hmc_statMC);
f1->GetObject("histEmatInputMC", hdata_statMC);

f2->GetObject("histEmatTotalMC", eehtotalMC);
f2->GetObject("histEmatSysUncorrMC", eehmc_statMC);
f2->GetObject("histEmatInputMC", eehdata_statMC);



TH1F *herr = (TH1F*)unfolded_mu_dy->Clone("herr");
TH1F *herr_data = (TH1F*)unfolded_mu_data->Clone("herr_data");

TH1F *herr_ee = (TH1F*)unfolded_el_dy->Clone("herr_ee");
TH1F *herr_ee_data = (TH1F*)unfolded_el_data->Clone("herr_ee_data");

std::cout << std::fixed << std::setprecision(3)<<std::endl;
for(int i = 1; i <= htotal->GetNbinsX(); i++){

double value_data = htotal->GetBinContent(i,i) - hmc_stat->GetBinContent(i,i) - hdata_stat->GetBinContent(i,i);

double value = htotalMC->GetBinContent(i,i) - hmc_statMC->GetBinContent(i,i) - hdata_statMC->GetBinContent(i,i);


herr->SetBinContent(i, 1);
herr->SetBinError(i, sqrt(value)/unfolded_mu_dy->GetBinContent(i));

herr_data->SetBinContent(i, 1);
herr_data->SetBinError(i, sqrt(value_data)/unfolded_mu_data->GetBinContent(i));


}


for(int i = 1; i <= eehtotal->GetNbinsX(); i++){

double value1_data = eehtotal->GetBinContent(i,i) - eehmc_stat->GetBinContent(i,i) - eehdata_stat->GetBinContent(i,i);
double value1 = eehtotalMC->GetBinContent(i,i) - eehmc_statMC->GetBinContent(i,i) - eehdata_statMC->GetBinContent(i,i);

herr_ee->SetBinContent(i, 1);
herr_ee->SetBinError(i, sqrt(value1)/unfolded_el_dy->GetBinContent(i));

herr_ee_data->SetBinContent(i, 1);
herr_ee_data->SetBinError(i, sqrt(value1_data)/unfolded_el_data->GetBinContent(i));


}


TH1 *hmu_trigger_up, *hmu_trigger_down, *hmu_id_up, *hmu_id_down, *hmu_dy;
TH1 *hmu_iso_up, *hmu_iso_down;

TFile *fmu = TFile::Open("/Users/amandeep/Desktop/zpmumu_analysis/signals/limits/results/post_fit/mumu/jan2024/feb2024_ANv10/raw_files/total_0b.root");
fmu->GetObject("DYJets", hmu_dy);
fmu->GetObject("DYJets_muHLTDown", hmu_trigger_down);
fmu->GetObject("DYJets_muHLTUp", hmu_trigger_up);

fmu->GetObject("DYJets_muIDDown", hmu_id_down);
fmu->GetObject("DYJets_muIDUp", hmu_id_up);

fmu->GetObject("DYJets_muISODown", hmu_iso_down);
fmu->GetObject("DYJets_muISOUp", hmu_iso_up);


TH1 *hmu_tt_trigger_up, *hmu_tt_trigger_down, *hmu_tt_id_up, *hmu_tt_id_down, *hmu_tt, *hmu_tt_iso_up, *hmu_tt_iso_down;
TH1 *hmu_vv_trigger_up, *hmu_vv_trigger_down, *hmu_vv_id_up, *hmu_vv_id_down, *hmu_vv, *hmu_vv_iso_up, *hmu_vv_iso_down;

//ttbar
fmu->GetObject("Top", hmu_tt);
fmu->GetObject("Top_muHLTDown", hmu_tt_trigger_down);
fmu->GetObject("Top_muHLTUp", hmu_tt_trigger_up);

fmu->GetObject("Top_muIDDown", hmu_tt_id_down);
fmu->GetObject("Top_muIDUp", hmu_tt_id_up);

fmu->GetObject("Top_muISODown", hmu_tt_iso_down);
fmu->GetObject("Top_muISOUp", hmu_tt_iso_up);

//vv
fmu->GetObject("Diboson", hmu_vv);
fmu->GetObject("Diboson_muHLTDown", hmu_vv_trigger_down);
fmu->GetObject("Diboson_muHLTUp", hmu_vv_trigger_up);

fmu->GetObject("Diboson_muIDDown", hmu_vv_id_down);
fmu->GetObject("Diboson_muIDUp", hmu_vv_id_up);

fmu->GetObject("Diboson_muISODown", hmu_vv_iso_down);
fmu->GetObject("Diboson_muISOUp", hmu_vv_iso_up);
//


TH1F *hel_id = (TH1F*)unfolded_mu_dy->Clone("hel_id");
TH1F *hel_trig = (TH1F*)unfolded_mu_dy->Clone("hel_trig");

double heepUncert[7] =  {0.012, 0.014, 0.016, 0.018, 0.023, 0.037, 0.037};

//DYjets Uncertainties
TH1F *hmu_trigger_upp = (TH1F*)hmu_trigger_up->Rebin(6,"hmu_trigger_upp",bins);
TH1F *hmu_trigger_downn = (TH1F*)hmu_trigger_down->Rebin(6,"hmu_trigger_downn",bins);
TH1F *hmu_dyy = (TH1F*)hmu_dy->Rebin(6,"hmu_dyy",bins);

TH1F *hmu_id_upp = (TH1F*)hmu_id_up->Rebin(6,"hmu_id_upp",bins);

TH1F *hmu_iso_upp = (TH1F*)hmu_iso_up->Rebin(6,"hmu_iso_upp",bins);

//Top+Diboson Uncertainties
hmu_tt->Add(hmu_vv);
hmu_tt_trigger_up->Add(hmu_vv_trigger_up);
hmu_tt_id_up->Add(hmu_vv_id_up);
hmu_tt_iso_up->Add(hmu_vv_iso_up);

TH1F *hmu_bkg = (TH1F*)hmu_tt->Rebin(6,"hmu_bkg",bins);
TH1F *hmu_bkg_trigger_upp = (TH1F*)hmu_tt_trigger_up->Rebin(6,"hmu_bkg_trigger_upp",bins);
TH1F *hmu_bkg_id_upp = (TH1F*)hmu_tt_id_up->Rebin(6,"hmu_bkg_id_upp",bins);
TH1F *hmu_bkg_iso_upp = (TH1F*)hmu_tt_iso_up->Rebin(6,"hmu_bkg_iso_upp",bins);

/////



TH1F *herr_sys_mu = (TH1F*)herr_data->Clone("herr_sys_mu");
TH1F *herr_sys_el = (TH1F*)herr_ee_data->Clone("herr_sys_el");

TH1F *herr_sys_mu_dy = (TH1F*)herr->Clone("herr_sys_mu_dy");
TH1F *herr_sys_el_dy = (TH1F*)herr_ee->Clone("herr_sys_el_dy");

for(int i = 1; i<=unfolded_mu_data->GetNbinsX(); i++){

//DY systematics
double mu_trig =   (hmu_trigger_upp->GetBinContent(i)/hmu_dyy->GetBinContent(i) - 1);
double mu_id = (hmu_id_upp->GetBinContent(i)/hmu_dyy->GetBinContent(i) - 1);
double mu_iso = (hmu_iso_upp->GetBinContent(i)/hmu_dyy->GetBinContent(i) - 1);

//bkg systematics
double mu_bkg_trig =   (hmu_bkg_trigger_upp->GetBinContent(i)/hmu_bkg->GetBinContent(i) - 1);
double mu_bkg_id =     (hmu_bkg_id_upp->GetBinContent(i)/hmu_bkg->GetBinContent(i) - 1);
double mu_bkg_iso =    (hmu_bkg_iso_upp->GetBinContent(i)/hmu_bkg->GetBinContent(i) - 1);

//printing bkg uncertainties

//std::cout<<"DY  sys "<<'\t'<<mu_trig<<std::endl;
//std::cout<<"DY  sys "<<mu_trig<<'\t'<<mu_id<<'\t'<<mu_iso<<std::endl;
std::cout<<"bkg sys "<<"mu_bkg_trig"<<'\t'<<"mu_bkg_id"<<'\t'<<"mu_bkg_iso"<<std::endl;
std::cout<<"bkg sys "<<mu_bkg_trig<<'\t'<<mu_bkg_id<<'\t'<<mu_bkg_iso<<std::endl;
//std::cout<<" ---- "<<std::endl;


//Assigning systematics
double pre_err = herr->GetBinError(i);
double pre_err_data = herr_data->GetBinError(i);

double total_mu_err      = sqrt(mu_trig*mu_trig + mu_id*mu_id + mu_iso*mu_iso + pre_err*pre_err);
double total_mu_err_data = sqrt(mu_bkg_trig*mu_bkg_trig + mu_bkg_id*mu_bkg_id + mu_bkg_iso*mu_bkg_iso + pre_err_data*pre_err_data);

//std::cout<<"pre_err      "<<pre_err<<'\t'<<mu_trig<<'\t'<<mu_id<<'\t'<<mu_iso<<'\t'<<total_mu_err<<std::endl;
//std::cout<<"pre_err data "<<pre_err_data<<'\t'<<mu_bkg_trig<<'\t'<<mu_bkg_id<<'\t'<<mu_bkg_iso<<'\t'<<total_mu_err_data<<std::endl;
//std::cout<<"pre_err       "<<total_mu_err<<std::endl;
//std::cout<<"pre_err data  "<<total_mu_err_data<<std::endl;

double el_pre_err = herr_ee->GetBinError(i);
double el_pre_err_data = herr_ee_data->GetBinError(i);

hel_id->SetBinContent(i, 1);
hel_id->SetBinError(i, heepUncert[i]);

hel_trig->SetBinContent(i, 1);
hel_trig->SetBinError(i, 0.03);

double total_el_err      = sqrt( el_pre_err*el_pre_err + heepUncert[i-1]*heepUncert[i-1] + 0.03*0.03); 
double total_el_err_data = sqrt( el_pre_err_data*el_pre_err_data + heepUncert[i-1]*heepUncert[i-1] + 0.03*0.03); 

//std::cout<<"pre_err       "<<total_el_err<<std::endl;
std::cout<<"pre_err data  "<<total_el_err_data<<std::endl;

//std::cout<<"pre_err_el "<<el_pre_err<<'\t'<<heepUncert[i-1]<<'\t'<<0.03<<'\t'<<total_el_err<<std::endl;

herr_sys_mu->SetBinContent(i,0);
herr_sys_mu->SetBinError(i, 0);
herr_sys_mu->SetBinContent(i,unfolded_mu_data->GetBinContent(i));
herr_sys_mu->SetBinError(i,total_mu_err_data*unfolded_mu_data->GetBinContent(i));

herr_sys_el->SetBinContent(i,0);
herr_sys_el->SetBinError(i, 0);

herr_sys_el->SetBinContent(i,unfolded_el_data->GetBinContent(i));
herr_sys_el->SetBinError(i, total_el_err_data*unfolded_el_data->GetBinContent(i));

herr_sys_mu_dy->SetBinContent(i,0);
herr_sys_mu_dy->SetBinError(i, 0);
herr_sys_mu_dy->SetBinContent(i,unfolded_mu_dy->GetBinContent(i));
herr_sys_mu_dy->SetBinError(i,total_mu_err*unfolded_mu_dy->GetBinContent(i));

herr_sys_el_dy->SetBinContent(i,0);
herr_sys_el_dy->SetBinError(i, 0);

herr_sys_el_dy->SetBinContent(i,unfolded_el_dy->GetBinContent(i));
herr_sys_el_dy->SetBinError(i, total_el_err*unfolded_el_dy->GetBinContent(i));

}

        TH1F *hdiv1 = (TH1F*)unfolded_mu_data->Clone("hdiv1"); //data
        TH1F *hdiv2 = (TH1F*)unfolded_el_data->Clone("hdiv2");  //bkg
        TH1F *hdiv3 = (TH1F*)unfolded_mu_dy->Clone("hdiv3");  //dy
        TH1F *hdiv4 = (TH1F*)unfolded_el_dy->Clone("hdiv4");  //dy


        TH1F *hdiv_mu_sys    = (TH1F*)herr_sys_mu->Clone("hdiv_mu_sys"); //data
        TH1F *hdiv_mu_sys_dy = (TH1F*)herr_sys_mu_dy->Clone("hdiv_mu_sys_dy"); //dy
        
        TH1F *hdiv_el_sys    = (TH1F*)herr_sys_el->Clone("hdiv_el_sys"); //data
        TH1F *hdiv_el_sys_dy = (TH1F*)herr_sys_el_dy->Clone("hdiv_el_sys_dy"); //dy




for(int i = 1; i<=hdiv1->GetNbinsX(); i++){

double div1_err = hdiv1->GetBinError(i)/hdiv1->GetBinContent(i);
double div2_err = hdiv2->GetBinError(i)/hdiv2->GetBinContent(i);

double div3_err = hdiv3->GetBinError(i)/hdiv3->GetBinContent(i);
double div4_err = hdiv4->GetBinError(i)/hdiv4->GetBinContent(i);

double mu_trig =   (hmu_trigger_upp->GetBinContent(i)/hmu_dyy->GetBinContent(i) - 1);
double mu_id = (hmu_id_upp->GetBinContent(i)/hmu_dyy->GetBinContent(i) - 1);
double mu_iso = (hmu_iso_upp->GetBinContent(i)/hmu_dyy->GetBinContent(i) - 1);

double total_div1_err = sqrt(div1_err*div1_err + mu_trig*mu_trig + mu_id*mu_id + mu_iso*mu_iso);
double total_div2_err = sqrt(div2_err*div2_err + heepUncert[i-1]*heepUncert[i-1] + 0.03*0.03);
 
double total_div3_err = sqrt(div3_err*div3_err + mu_trig*mu_trig + mu_id*mu_id + mu_iso*mu_iso);
double total_div4_err = sqrt(div4_err*div4_err + heepUncert[i-1]*heepUncert[i-1] + 0.03*0.03);

//std::cout<<"total_div1_err before  "<<div3_err<<std::endl;

hdiv1->SetBinError(i,0);
hdiv1->SetBinError(i,total_div1_err*hdiv1->GetBinContent(i));

hdiv2->SetBinError(i,0);
hdiv2->SetBinError(i,total_div2_err*hdiv2->GetBinContent(i));

hdiv3->SetBinError(i,0);
hdiv3->SetBinError(i,(hdiv_mu_sys_dy->GetBinError(i)/hdiv_mu_sys_dy->GetBinContent(i))*hdiv3->GetBinContent(i));

//hdiv3->SetBinError(i,total_div3_err*hdiv3->GetBinContent(i));

hdiv4->SetBinError(i,0);
hdiv4->SetBinError(i,(hdiv_el_sys_dy->GetBinError(i)/hdiv_el_sys_dy->GetBinContent(i))*hdiv4->GetBinContent(i));

//hdiv4->SetBinError(i,total_div4_err*hdiv4->GetBinContent(i));

//std::cout<<"total_div1_err after  "<<hdiv_mu_sys_dy->GetBinError(i)/hdiv_mu_sys_dy->GetBinContent(i)<<std::endl;
//std::cout<<"total_div1_err after  "<<hdiv3->GetBinError(i)/hdiv3->GetBinContent(i)<<std::endl;

//std::cout<<"yield in num "<<hdiv3->GetBinError(i)/hdiv3->GetBinContent(i)<<std::endl;
//std::cout<<"yield in deno "<<hdiv4->GetBinError(i)/hdiv4->GetBinContent(i)<<std::endl;
}


hdiv1->Divide(hdiv2);
hdiv3->Divide(hdiv4);

hdiv_mu_sys->Divide(hdiv_el_sys);

hdiv_mu_sys_dy->Divide(hdiv_el_sys_dy);

TH1F *hscale = (TH1F*)unfolded_mu_dy->Clone("hscale");
TH1F *hscale_sys = (TH1F*)unfolded_mu_dy->Clone("hscale_sys");

for(int i=1; i <= hscale->GetNbinsX(); i++)
{
hscale->SetBinContent(i,0);
hscale->SetBinError(i,0);
hscale->SetBinContent(i, 1.53346);
hscale->SetBinError(i, 0.0272988);

hscale_sys->SetBinContent(i,0);
hscale_sys->SetBinError(i,0);

hscale_sys->SetBinContent(i, 1.53346);

}

TH1F *hscale_mc = (TH1F*)unfolded_mu_dy->Clone("hscale_mc");
TH1F *hscale_mc_sys = (TH1F*)unfolded_mu_dy->Clone("hscale_mc_sys");

for(int i=1; i <= hscale_mc->GetNbinsX(); i++)
{
hscale_mc->SetBinContent(i,0);
hscale_mc->SetBinError(i,0);
hscale_mc->SetBinContent(i, 1.56442);
hscale_mc->SetBinError(i, 0.00208734);

hscale_mc_sys->SetBinContent(i,0);
hscale_mc_sys->SetBinError(i,0);

hscale_mc_sys->SetBinContent(i, 1.56442);

}

hdiv1->Divide(hscale);
hdiv3->Divide(hscale_mc);

hdiv_mu_sys->Divide(hscale_sys);
hdiv_mu_sys_dy->Divide(hscale_mc_sys);


   TPad *pad1 = new TPad("pad1", "pad1",0.0,0.0,1,0.33);

   pad1->SetTickx();
   pad1->SetTicky();
   pad1->Draw();
   pad1->cd();
   pad1->SetFillColor(0);
   pad1->SetBorderMode(-1);
   pad1->SetBorderSize(5);
   pad1->SetLeftMargin(0.12);
   pad1->SetRightMargin(0.04);
   pad1->SetTopMargin(0.02);
   pad1->SetBottomMargin(0.3);
   pad1->SetFrameBorderMode(0);
   pad1->SetFrameBorderMode(0);
   pad1->SetLogx();

TH1F *hbottom_div1 = (TH1F*)hdiv1->Clone("hbottom_div1");
TH1F *hbottom_div3 = (TH1F*)hdiv3->Clone("hbottom_div3");

TH1F *hbottom_mu_sys = (TH1F*)hdiv_mu_sys->Clone("hbottom_mu_sys");         //systematic uncertainty band in data
TH1F *hbottom_mu_sys_dy = (TH1F*)hdiv_mu_sys_dy->Clone("hbottom_mu_sys_dy");// systematic uncertainty band in MC


TH1F *hf_err_div1 = (TH1F*)hdiv1->Clone("hf_err_div1");
TH1F *hf_err_div3 = (TH1F*)hdiv3->Clone("hf_err_div3");


TH1F *hf_err_mu_sys = (TH1F*)hdiv_mu_sys->Clone("hf_err_mu_sys");
TH1F *hf_err_mu_sys_dy = (TH1F*)hdiv_mu_sys_dy->Clone("hf_err_mu_sys_dy");

hbottom_mu_sys->Divide(hbottom_mu_sys_dy);
hbottom_div1->Divide(hbottom_div3);


for(int i = 1; i<=hdiv_mu_sys->GetNbinsX(); i++)
{
//std::cout<<"errors data before"<< hdiv1->GetBinError(i)/hdiv1->GetBinContent(i)<<std::endl;
std::cout<<"sys errors before  "<< hbottom_mu_sys->GetBinError(i)/hbottom_mu_sys->GetBinContent(i)<<std::endl;
std::cout<<"errors data before "<< hf_err_mu_sys->GetBinError(i)/hf_err_mu_sys->GetBinContent(i)<<std::endl;
std::cout<<"errors MC   before "<< hf_err_mu_sys_dy->GetBinError(i)/hf_err_mu_sys_dy->GetBinContent(i)<<std::endl;

hbottom_mu_sys->SetBinError(i, 0);

double new_err_band  = hbottom_mu_sys->GetBinContent(i)*((hf_err_mu_sys->GetBinError(i)/hf_err_mu_sys->GetBinContent(i)) + (hf_err_mu_sys_dy->GetBinError(i)/hf_err_mu_sys_dy->GetBinContent(i)));
hbottom_mu_sys->SetBinError(i, new_err_band);

hbottom_div1->SetBinError(i, 0);
double new_err_bars = hbottom_div1->GetBinContent(i)*((hf_err_div1->GetBinError(i)/hf_err_div1->GetBinContent(i)) + (hf_err_div3->GetBinError(i)/hf_err_div3->GetBinContent(i)));
hbottom_div1->SetBinError(i, new_err_bars);

std::cout<<" --- <<"<<std::endl;
//std::cout<<"errors data after"<< hdiv1->GetBinError(i)/hdiv1->GetBinContent(i)<<std::endl;
std::cout<<"sys errors after"<< hbottom_mu_sys->GetBinError(i)/hbottom_mu_sys->GetBinContent(i)<<std::endl;

std::cout<<" ----- <<"<<std::endl;

}

hbottom_div1->Draw("lp E1");

hbottom_mu_sys->Draw("E2,same");
hbottom_mu_sys->SetLineWidth(0);
hbottom_mu_sys->SetLineColor(kMagenta);
hbottom_mu_sys->SetFillColor(kMagenta);
hbottom_mu_sys->SetFillStyle(3004);

hbottom_div1->Draw("lp E1, same");


//estimating chi2
//double temp = 0.0;
//for(int i=3; i<=hdiv1->GetNbinsX(); i++){

//std::cout<<herr->GetBinContent(i)<<'\t'<<herr->GetBinError(i)<<std::endl;

//std::cout<<i <<hdiv1->GetXaxis()->FindBin(400)<<std::endl;
//estimating the deviation from unity
//double value = ((hdiv1->GetBinContent(i) - 1)*(hdiv1->GetBinContent(i) - 1))/(hdiv1->GetBinError(i)*hdiv1->GetBinError(i));

//estimating the deviation from DY MC
 
//double value = ((hdiv1->GetBinContent(i) - hdiv3->GetBinContent(i))*(hdiv1->GetBinContent(i) - hdiv3->GetBinContent(i)))/(hdiv1->GetBinError(i)*hdiv1->GetBinError(i));
//double value = ((hdiv1->GetBinContent(i) - hdiv3->GetBinContent(i))*(hdiv1->GetBinContent(i) - hdiv3->GetBinContent(i)))/(hdiv3->GetBinContent(i));
//temp += value;
//
////std::cout<<hdiv1->GetBinContent(i)<<std::endl;
////std::cout<<hdiv1->GetBinError(i)<<std::endl;
////std::cout<<temp<<std::endl;
//
//}

//std::cout<<temp<<std::endl;

hbottom_div1->SetStats(kFALSE);
hbottom_div1->SetTitle("");
hbottom_div1->SetMarkerStyle(20);
hbottom_div3->SetMarkerStyle(20);
hbottom_div1->SetMarkerColor(kBlack);
hbottom_div3->SetMarkerColor(kBlue);
hbottom_div1->SetMarkerSize(1.2);
hbottom_div3->SetMarkerSize(1.2);

   hbottom_div1->GetYaxis()->SetLabelFont(42);
   hbottom_div1->GetYaxis()->SetNdivisions(20505);
   hbottom_div1->GetYaxis()->SetLabelSize(0.09);
   hbottom_div1->GetYaxis()->SetTitleSize(0.12);
   hbottom_div1->GetYaxis()->SetTitleOffset(0.4);
   hbottom_div1->GetYaxis()->SetTitleFont(42);
   hbottom_div1->SetLineColor(kBlack);
   hbottom_div1->SetLineWidth(2);
   hbottom_div3->SetLineWidth(2);
   hbottom_div1->GetYaxis()->SetRangeUser(0.1,1.89);
   //hbottom_div1->GetYaxis()->SetRangeUser(0.1,2.49);
   hbottom_div1->GetXaxis()->SetTitle("m_{ll} [GeV]");
   hbottom_div1->GetYaxis()->SetTitle("R^{Data}_{#mu^{+}#mu^{-}/e^{+}e^{-}}/R^{MC}_{#mu^{+}#mu^{-}/e^{+}e^{-}}");

   hbottom_div1->GetXaxis()->SetLabelFont(42);
   hbottom_div1->GetXaxis()->SetLabelOffset(0.02);
   hbottom_div1->GetXaxis()->SetTitleSize(0.12);
   hbottom_div1->GetXaxis()->SetTitleOffset(0.8);
   hbottom_div1->GetXaxis()->SetLabelSize(0.12);

   hbottom_div1->GetXaxis()->SetRangeUser(200, 6000);
//line
   TLine *line = new TLine(200, 1, 6000, 1);
   line->SetLineColor(kBlack);
   line->SetLineWidth(2);
   line->SetLineStyle(2);
   line->Draw();

//

   c1->cd();
   TPad *pad2 = new TPad("pad2", "pad2",0.0,0.33,1,0.99);
   pad2->SetTickx();
   pad2->SetTicky();
   pad2->Draw();
   pad2->cd();
   pad2->Range(61.49425,-1.836137,167.8161,16.52523);
   pad2->SetFillColor(0);
   pad2->SetBorderMode(-1);
   pad2->SetBorderSize(5);
   pad2->SetLeftMargin(0.12);
   pad2->SetRightMargin(0.04);
   pad2->SetTopMargin(0.08);
   pad2->SetBottomMargin(0.0001);
   pad2->SetFrameBorderMode(0);
   pad2->SetFrameBorderMode(0);
   pad2->SetLogx();

TH1F *htop_div1 = (TH1F*)hdiv1->Clone("htop_div1");
TH1F *htop_div3 = (TH1F*)hdiv3->Clone("htop_div3");

TH1F *htop_mu_sys = (TH1F*)hdiv_mu_sys->Clone("htop_mu_sys");         //systematic uncertainty band in data
TH1F *htop_mu_sys_dy = (TH1F*)hdiv_mu_sys_dy->Clone("htop_mu_sys_dy");// systematic uncertainty band in MC

htop_div1->Draw("lp E1");

htop_mu_sys->Draw("E2,same");
htop_mu_sys->SetLineWidth(0);
htop_mu_sys->SetLineColor(kMagenta);
htop_mu_sys->SetFillColor(kMagenta);
htop_mu_sys->SetFillStyle(3004);

htop_mu_sys_dy->Draw("E2,same");
htop_mu_sys_dy->SetLineWidth(2);
htop_mu_sys_dy->SetLineColor(kMagenta);
htop_mu_sys_dy->SetFillColor(kMagenta);
htop_mu_sys_dy->SetFillStyle(3004);

htop_div1->Draw("lp E1, same");
htop_div3->Draw("lep, same");

htop_div1->SetStats(kFALSE);
htop_div1->SetTitle("");
htop_div1->SetMarkerStyle(20);
htop_div3->SetMarkerStyle(20);
htop_div1->SetMarkerColor(kBlack);
htop_div3->SetMarkerColor(kBlue);
htop_div1->SetMarkerSize(1.2);
htop_div3->SetMarkerSize(1.2);

   htop_div1->GetYaxis()->SetLabelFont(42);
   htop_div1->GetYaxis()->SetNdivisions(20505);
   htop_div1->GetYaxis()->SetLabelSize(0.05);
   htop_div1->GetYaxis()->SetTitleSize(0.07);
   htop_div1->GetYaxis()->SetTitleOffset(0.6);
   htop_div1->GetYaxis()->SetTitleFont(42);
   htop_div1->SetLineColor(kBlack);
   htop_div1->SetLineWidth(2);
   htop_div3->SetLineWidth(2);
   htop_div1->GetYaxis()->SetRangeUser(0.1,2.49);
   htop_div1->GetXaxis()->SetTitle("m_{ll} [GeV]");
   htop_div1->GetYaxis()->SetTitle("R_{#mu^{+}#mu^{-}/e^{+}e^{-}}");
   //hdiv1->GetYaxis()->SetTitle("R^{Data}_{#mu^{+}#mu^{-}/e^{+}e^{-}}/R^{MC}_{#mu^{+}#mu^{-}/e^{+}e^{-}}");

   htop_div1->GetXaxis()->SetLabelFont(42);
   htop_div1->GetXaxis()->SetLabelOffset(0.02);
   htop_div1->GetXaxis()->SetTitleSize(0.04);
   htop_div1->GetXaxis()->SetTitleOffset(1.1);
   htop_div1->GetXaxis()->SetLabelSize(0.04);

//   hdiv1->GetYaxis()->CenterTitle(true);
   htop_div1->GetXaxis()->SetRangeUser(200, 6000);
//line
   TLine *line1 = new TLine(200, 1, 6000, 1);
   line1->SetLineColor(kBlack);
   line1->SetLineWidth(2);
   line1->SetLineStyle(2);
   line1->Draw();

//estimating chi2
double temp = 0.0;
for(int i=3; i<=htop_div1->GetNbinsX(); i++){

//std::cout<<herr->GetBinContent(i)<<'\t'<<herr->GetBinError(i)<<std::endl;

//std::cout<<i <<hdiv1->GetXaxis()->FindBin(400)<<std::endl;
//estimating the deviation from unity
//double value = ((hdiv1->GetBinContent(i) - 1)*(hdiv1->GetBinContent(i) - 1))/(hdiv1->GetBinError(i)*hdiv1->GetBinError(i));

//estimating the deviation from DY MC

double value = ((htop_div1->GetBinContent(i) - htop_div3->GetBinContent(i))*(htop_div1->GetBinContent(i) - htop_div3->GetBinContent(i)))/(htop_div1->GetBinError(i)*htop_div1->GetBinError(i));
//double value = ((hdiv1->GetBinContent(i) - hdiv3->GetBinContent(i))*(hdiv1->GetBinContent(i) - hdiv3->GetBinContent(i)))/(hdiv3->GetBinContent(i));
temp += value;

//std::cout<<hdiv1->GetBinContent(i)<<std::endl;
//std::cout<<hdiv1->GetBinError(i)<<std::endl;
//std::cout<<temp<<std::endl;

}

std::cout<<"chi2 "<<temp<<std::endl;

CMS_lumi( pad2, 4, 11);
pad2->Update();
pad2->Modified();

TLatex *tex2 = new TLatex(390,2.05,"n_{b} = 0 signal region");
tex2->SetTextAlign(20);
tex2->SetTextSize(0.048);
tex2->SetTextFont(52);
tex2->SetLineWidth(2);
tex2->Draw();


//
        TLegend *legend = new TLegend(0.394,0.48,0.88,0.76,NULL,"brNDC");
        //TLegend *legend = new TLegend(0.3853868,0.602963,0.8538682,0.7496296,NULL,"brNDC");
        legend->SetHeader("Barrel-Barrel + Barrel-Endcap leptons");
        legend->SetBorderSize(0);
        legend->SetTextSize(0.052);
        legend->AddEntry(line,"SM expectation","l");
        legend->AddEntry(htop_div3,"DY+jets MC (stat. #oplus syst.)","lep");
        legend->AddEntry(htop_div1,"Observed (stat. #oplus syst.) ","lep");
        legend->AddEntry(htop_mu_sys,"Systematic uncertainty ","f");


        legend->Draw();

//c1->SaveAs("plots/fratio_MC_data_total.png");
//c1->SaveAs("plots/fratio_MC_data_total.pdf");
//c1->SaveAs("plots/fratio_MC_data_total.root");

c1->SaveAs("plots/golden_fratio_0b.png");
c1->SaveAs("plots/golden_fratio_0b.pdf");
c1->SaveAs("plots/golden_fratio_0b.root");

//c1->SaveAs("plots/fratio_double_total.png");
//c1->SaveAs("plots/fratio_double_total.pdf");
//c1->SaveAs("plots/fratio_double_total.root");
}
