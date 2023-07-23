#include <string>
#include <math.h>
#include <stdexcept>

float relErrQuadrature(float rel_err1, float rel_err2) {
   /*
   function that adds two relative errors in quadrature
   */
   return std::pow(std::pow(rel_err1, 2.0) + std::pow(rel_err2, 2.0), 0.5);
}

void plotter()
{

int nbjets = 0;
int year = 2018;
std::string region = "bb";

TCanvas *c1 = new TCanvas("c1", "stacked hists",61,24,744,744);
   c1->Range(-29.17415,-0.08108108,263.2406,0.6466216);
   c1->SetFillColor(0);
   c1->SetBorderMode(0);
   c1->SetBorderSize(2);
//   c1->SetGridx();
//   c1->SetGridy();
   c1->SetRightMargin(0.04528012);
   c1->SetTopMargin(0.06406685);
   c1->SetBottomMargin(0.1114206);
   c1->SetFrameBorderMode(0);
   c1->SetFrameBorderMode(0);
   c1->SetLogx();
   c1->SetLogy();

TH1 *h1, *h2, *h3, *h4;

TFile *f = TFile::Open("dy_sys_BB.root");
// TFile *f1 = TFile::Open("dy_sys_BB.root"); // not sure why we need multiple file instances ... -> sth to try fix later
f->GetObject("h_dy", h1);

// TFile *f2 = TFile::Open("dy_sys_BB.root");
f->GetObject("h_data", h2);

// TFile *f3 = TFile::Open("dy_sys_BB.root");
f->GetObject("h_bkg", h3);

// TFile *f4 = TFile::Open("dy_sys_BB.root");
f->GetObject("h_ttbar", h4);

std::cout<< "flag" << std::endl;

TPad *pad1 = new TPad("pad1", "pad1",0.05,0.03114206,0.99,0.39);
pad1->Draw();
pad1->cd();
pad1->Range(-49.46043,-0.4895868,524.2806,1.328879);
pad1->SetFillColor(0);
pad1->SetBorderMode(0);
pad1->SetBorderSize(2);
//   pad1->SetGridx();
pad1->SetRightMargin(0.04);
//  pad1->SetTopMargin(0.00101554);
pad1->SetBottomMargin(0.4);
pad1->SetFrameBorderMode(0);
pad1->SetFrameBorderMode(0);
pad1->SetLeftMargin(0.14);
pad1->SetFrameBorderMode(0);
pad1->SetFrameBorderMode(0);

TH1F *hbkg = (TH1F*)h3->Clone("hbkg");
TH1F *hdiv1 = (TH1F*)h2->Clone("hdiv1"); // data
TH1F *hdy = (TH1F*)h1->Clone("hdy"); 
//   std::cout<< "flag2" << std::endl;
TH1F *hdiv2 = (TH1F*)h4->Clone("hdiv2"); // ttbar
//   std::cout<< "flag3" << std::endl;
TH1F *hsf = (TH1F*)h4->Clone("hdiv2");// SF histogram
hsf->Reset();

// apply the egamma SF
// source: https://twiki.cern.ch/twiki/bin/viewauth/CMS/EgammaUL2016To2018#HEEP_ID_Scale_Factor_for_UL

float barrel_SF, barrel_SF_err_stat, barrel_SF_err_syst, endcap_SF,endcap_SF_err_stat, endcap_SF_err_syst;
if (year == 2018){
   barrel_SF = 0.973;
   barrel_SF_err_stat = 0.001;
   barrel_SF_err_syst = 0.004;
   endcap_SF = 0.980;
   endcap_SF_err_stat = 0.002;
   endcap_SF_err_syst = 0.011;
}
else if (year == 2017){ 
   barrel_SF = 0.979;
   barrel_SF_err_stat = 0.001;
   barrel_SF_err_syst = 0.005;
   endcap_SF = 0.987;
   endcap_SF_err_stat = 0.002;
   endcap_SF_err_syst = 0.010;
}
else if (year == 2016){
   barrel_SF = 0.985;
   barrel_SF_err_stat = 0.001;
   barrel_SF_err_syst = 0.004;
   endcap_SF = 0.990;
   endcap_SF_err_stat = 0.003;
   endcap_SF_err_syst = 0.007;
}
else{
   throw std::invalid_argument("invalid value for year");
}

// add barrel_SFs and endcap_SFs to make BB_SF and BE_SF
float barrel_SF_err = barrel_SF* relErrQuadrature(
   barrel_SF_err_stat/barrel_SF, 
   barrel_SF_err_syst/barrel_SF 
);

float endcap_SF_err = endcap_SF* relErrQuadrature(
   endcap_SF_err_stat/endcap_SF, 
   endcap_SF_err_syst/endcap_SF 
);

float BB_SF = barrel_SF*barrel_SF;
float BB_SF_err = BB_SF* relErrQuadrature(
   barrel_SF_err/barrel_SF, 
   barrel_SF_err/barrel_SF 
);

float BE_SF = barrel_SF*endcap_SF;
float BE_SF_err = BE_SF* relErrQuadrature(
   barrel_SF_err/barrel_SF, 
   endcap_SF_err/endcap_SF 
);

float hsf_SF, hsf_SF_err;
if (region == "bb" || region == "BB"){
   hsf_SF = BB_SF;
   hsf_SF_err = BB_SF_err;
}
else if (region == "be" || region == "BE"){
   hsf_SF = BE_SF;
   hsf_SF_err = BE_SF_err;
}
else{
   throw std::invalid_argument("invalid value for region");
}

for(int i = 1; i < hsf->GetNbinsX()+1; i++){
   hsf->SetBinContent(i, hsf_SF);
	hsf->SetBinError(i, hsf_SF_err);
}

// apply hsf to all the MC histograms
hbkg->Multiply(hsf);
hdy->Multiply(hsf);
hdiv2->Multiply(hsf);

// get ttbar SF and error
hdiv1->Add(hbkg, -1); // substract dy and bkg from data
hdiv1->Add(hdy, -1);
//hdiv1->Add(hbkg, -1);

//error calculation
double err1;
double err2;
double val1 = hdiv1->IntegralAndError(1, -1, err1);
double val2 = hdiv2->IntegralAndError(1, -1, err2);
// double val1 = hdiv1->IntegralAndError(1, total_nbins, err1);
// double val2 = hdiv2->IntegralAndError(1, total_nbins, err2);



std::cout<<"data total yield: "<<val1<<" error = "<<err1<<std::endl;


std::cout<<"ttbar MC   = "<<val2<<" error = "<<err2<<std::endl;

std::cout<<"GetNbins center: "<<hdiv1->GetXaxis()->GetNbins()<<std::endl;

int total_nbins = hdiv1->GetXaxis()->GetNbins();
std::cout<<"last bin center: "<<hdiv1->GetXaxis()->GetBinCenter(total_nbins)<<std::endl; // -1 instead of total_nbins doesn't work

double ratio = val1/val2;
double e1 = (err1/val1);
double e2 = (err2/val2);

double er = ratio*sqrt((e1*e1) + (e2*e2));

std::cout<<"ttbar SF: "<< ratio<<". err SF: "<<er<<std::endl;

//plotting results

hdiv1->Divide(hdiv2);
hdiv1->Draw();
hdiv1->SetStats(kFALSE);
hdiv1->SetTitle("");
hdiv1->SetMarkerStyle(20);

   hdiv1->GetYaxis()->SetLabelFont(42);
   hdiv1->GetYaxis()->SetNdivisions(20505);
   hdiv1->GetYaxis()->SetLabelSize(0.08);
   hdiv1->GetYaxis()->SetTitleSize(0.08);
   hdiv1->GetYaxis()->SetTitleOffset(0.65);
   hdiv1->GetYaxis()->SetTitleFont(42);
   hdiv1->SetLineColor(kBlue+2);
   hdiv1->SetLineWidth(2);
   hdiv1->GetYaxis()->SetRangeUser(0,2);
   // hdiv1->GetYaxis()->SetRangeUser(-1000,1000);
   hdiv1->GetXaxis()->SetRangeUser(100,1000);
   hdiv1->GetXaxis()->SetTitle("M_{emu} [GeV]");
   hdiv1->GetYaxis()->SetTitle("#frac{Data - non ttbar MC}{ ttbar MC}");

   hdiv1->GetXaxis()->SetLabelFont(42);
   hdiv1->GetXaxis()->SetLabelOffset(0.05);
   hdiv1->GetXaxis()->SetTitleSize(0.10);
   hdiv1->GetXaxis()->SetTitleOffset(1.3);
      hdiv1->GetXaxis()->SetLabelSize(0.08);

   hdiv1->GetYaxis()->CenterTitle(true);

std::cout<< "flag2" << std::endl;

//line
   TLine *line = new TLine(100, 1,1000, 1);
   line->SetLineColor(kRed);
   line->Draw();


   c1->cd();
   TPad *pad2 = new TPad("pad2", "pad2",0.05,0.37,0.99,0.99);
   pad2->Draw();
   pad2->cd();
   pad2->Range(-44.421,-161.3852,528.7119,36963.49);
   pad2->SetFillColor(0);
   pad2->SetBorderMode(0);
   pad2->SetBorderSize(2);
   pad2->SetLogy();

//   pad2->SetGridx();
   pad2->SetRightMargin(0.04);
   pad2->SetLeftMargin(0.14);
   pad2->SetTopMargin(0.0806685);
   pad2->SetBottomMargin(0);
   pad2->SetFrameBorderMode(0);
   pad2->SetFrameBorderMode(0);

        TH1F *hs_bkg = (TH1F*)h3->Clone("hs_bkg");
        TH1F *hs_data = (TH1F*)h2->Clone("hs_data");
        TH1F *hs_dy = (TH1F*)h1->Clone("hs_dy");
        TH1F *hs_ttbar = (TH1F*)h4->Clone("hs_ttbar");

// apply hsf to all the MC histograms
hs_bkg->Multiply(hsf);
hs_dy->Multiply(hsf);
hs_ttbar->Multiply(hsf);

std::cout<< "flag3" << std::endl;

auto hs  = new THStack("hs", "");
hs->Add(hs_dy);
if (nbjets == 0){ // ttbar is not domninant bkg
   hs->Add(hs_ttbar);
   hs->Add(hs_bkg);
}
else { // ttbar is domninant bkg, so added last
   hs->Add(hs_bkg);
   hs->Add(hs_ttbar);
}


std::cout<< "flag4" << std::endl;
hs_data->SetStats(kFALSE);

hs->Draw("hist");
hs_data->Draw("lep, same");


hs->SetTitle("");

hs_dy->SetLineColor(kBlue+7);
hs_dy->SetFillColor(kBlue+7);

hs_bkg->SetLineColor(kGreen);
hs_bkg->SetFillColor(kGreen);

hs_ttbar->SetFillColor(kRed);
hs_ttbar->SetLineColor(kRed);

std::cout<< "flag5" << std::endl;

hs_data->SetMarkerStyle(22);
hs_data->SetMarkerSize(1.0);
hs->GetXaxis()->SetRangeUser(100,1000);
hs->GetYaxis()->SetTitle("Events");
hs->GetYaxis()->SetTitleSize(0.045);
hs->GetYaxis()->SetLabelSize(0.045);

hs->SetMinimum(2.);
// hs->SetMaximum(1e12);
hs->SetMaximum(1e4);


        TLegend *legend = new TLegend(0.57,0.650899,0.94,0.8843167,NULL,"brNDC");

        legend->SetHeader("BB category");
        legend->SetTextSize(0.055);
        legend->AddEntry(hs_data,"Data","lep");
        legend->AddEntry(hs_dy,"DY MC","f");
        legend->AddEntry(hs_bkg,"Other bkgs MC","f");
        legend->AddEntry(hs_ttbar,"ttbar MC","f");


        legend->Draw();

if (nbjets == 0){
   c1->SaveAs("plots/emu_ttbar_all_nbjets_eq_0.png");
   c1->SaveAs("plots/emu_ttbar_all_nbjets_eq_0.pdf");
   c1->SaveAs("plots/emu_ttbar_all_nbjets_eq_0.root");
}
else if (nbjets == 1) {
   c1->SaveAs("plots/emu_ttbar_all_nbjets_eq_1.png");
   c1->SaveAs("plots/emu_ttbar_all_nbjets_eq_1.pdf");
   c1->SaveAs("plots/emu_ttbar_all_nbjets_eq_1.root");
}
else { // nbjets == 2
   c1->SaveAs("plots/emu_ttbar_all_nbjets_greater_1.png");
   c1->SaveAs("plots/emu_ttbar_all_nbjets_greater_1.pdf");
   c1->SaveAs("plots/emu_ttbar_all_nbjets_greater_1.root");
}



}