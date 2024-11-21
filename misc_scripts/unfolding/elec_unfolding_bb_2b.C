{
TH2 *hresponse;
TH1 *hmu_data_unbin;
TH1 *hbkg_unbin;
TH1 *hmu_gen_unbin, *hmu_reco_unbin;

TH2 *hresponse_id_up;
TH2 *hresponse_id_dn;
TH2 *hresponse_scale_up;
TH2 *hresponse_scale_dn;

TH2 *hresponse_l1_up;
TH2 *hresponse_l1_dn;

TH2 *hresponse_pu_up;
TH2 *hresponse_pu_dn;

TH2 *hresponse_pdf_up;
TH2 *hresponse_pdf_dn;


//Double_t bins[8] = {200, 300, 400,500,700,1100,1900,6000};

Double_t bins[5] = {200, 400, 700,1100,6000};

TFile *f1 = TFile::Open("out_response_matrix_el_bb_script_2b.root");
f1->GetObject("response_el", hresponse);
f1->GetObject("hist2del_id_up", hresponse_id_up);
f1->GetObject("hist2del_id_dn", hresponse_id_dn);

f1->GetObject("hist2del_scale_up", hresponse_scale_up);
f1->GetObject("hist2del_scale_dn", hresponse_scale_dn);

f1->GetObject("hist2del_l1_up", hresponse_l1_up);
f1->GetObject("hist2del_l1_dn", hresponse_l1_dn);

f1->GetObject("hist2del_pu_up", hresponse_pu_up);
f1->GetObject("hist2del_pu_dn", hresponse_pu_dn);

f1->GetObject("hist2del_pdf_up", hresponse_pdf_up);
f1->GetObject("hist2del_pdf_dn", hresponse_pdf_dn);


TFile *f2 = TFile::Open("../../../reco/ee/2b_bb_2018.root");
f2->GetObject("data_obs", hmu_data_unbin);

TH1F *hmu_data = (TH1F*)hmu_data_unbin->Rebin(4,"hmu_data",bins);

TFile *f3 = TFile::Open("../../../gen/ee/2b_bb_2018.root");
f3->GetObject("DYJets", hmu_gen_unbin);

TH1F *hmu_gen = (TH1F*)hmu_gen_unbin->Rebin(4,"hmu_gen",bins);

TFile *f4 = TFile::Open("../../../reco/ee/2b_bb_2018.root");
f4->GetObject("DYJets", hmu_reco_unbin);

TH1F *hmu_reco = (TH1F*)hmu_reco_unbin->Rebin(4,"hmu_reco",bins);

TH1 *htop, *hdiboson, *hfake1;

TFile *f5fake_2b = TFile::Open("../../../reco/ee/fake_2b_bb_2018.root");
f5fake_2b->GetObject("data_obs", hfake1);

for(int i =1; i<=hfake1->GetNbinsX() ; i++){

        double hfake_err1 = 0.50 * hfake1->GetBinContent(i);
        hfake1->SetBinError(i, 0 );
        hfake1->SetBinError(i,hfake_err1);
}

TFile *f5 = TFile::Open("../../../reco/ee/2b_bb_2018.root");
f5->GetObject("Top", htop);
f5->GetObject("Diboson", hdiboson);

htop->Add(hdiboson);
htop->Add(hfake1);

TH1F *hbkg = (TH1F*)htop->Rebin(4,"hbkg",bins);

TH1F *hmu_reco_org = (TH1F*)hmu_reco->Clone("hmu_reco_org");
TH1F *hmu_data_org = (TH1F*)hmu_data->Clone("hmu_data_org");

hmu_data->Add(hbkg, -1);

std::cout<<"DY "<< hmu_reco_org->GetBinContent(1)<<std::endl;


//float acc_eff_dy[8] = {0.17675974401327488, 0.1992257177060608, 0.22249910383869853, 0.2665568181818181, 0.3152071124950572, 0.36138115384615355, 0.4028790420560745, 0.4781710893854745};


TUnfoldDensity unfold(hresponse, TUnfold::kHistMapOutputVert, TUnfold::kRegModeNone, TUnfold::kEConstraintNone);
TUnfoldDensity unfoldMC(hresponse, TUnfold::kHistMapOutputVert, TUnfold::kRegModeNone, TUnfold::kEConstraintNone);

unfoldMC.SetInput(hmu_reco);
unfold.SetInput(hmu_data);

unfold.AddSysError(hresponse_id_up, "Up1", TUnfoldDensity::kHistMapOutputVert,  TUnfoldDensity::kSysErrModeMatrix);
unfold.AddSysError(hresponse_id_dn, "Down1", TUnfoldDensity::kHistMapOutputVert,  TUnfoldDensity::kSysErrModeMatrix);

unfold.AddSysError(hresponse_l1_up, "Up2", TUnfoldDensity::kHistMapOutputVert,  TUnfoldDensity::kSysErrModeMatrix);
unfold.AddSysError(hresponse_l1_dn, "Down2", TUnfoldDensity::kHistMapOutputVert,  TUnfoldDensity::kSysErrModeMatrix);

unfold.AddSysError(hresponse_scale_up, "Up5", TUnfoldDensity::kHistMapOutputVert,  TUnfoldDensity::kSysErrModeMatrix);
unfold.AddSysError(hresponse_scale_dn, "Down5", TUnfoldDensity::kHistMapOutputVert,  TUnfoldDensity::kSysErrModeMatrix);

unfold.AddSysError(hresponse_pu_up, "Up6", TUnfoldDensity::kHistMapOutputVert,  TUnfoldDensity::kSysErrModeMatrix);
unfold.AddSysError(hresponse_pu_dn, "Down6", TUnfoldDensity::kHistMapOutputVert,  TUnfoldDensity::kSysErrModeMatrix);

unfold.AddSysError(hresponse_pdf_up, "Up7", TUnfoldDensity::kHistMapOutputVert,  TUnfoldDensity::kSysErrModeMatrix);
unfold.AddSysError(hresponse_pdf_dn, "Down7", TUnfoldDensity::kHistMapOutputVert,  TUnfoldDensity::kSysErrModeMatrix);

//MC Systematics
unfoldMC.AddSysError(hresponse_id_up, "Up1", TUnfoldDensity::kHistMapOutputVert,  TUnfoldDensity::kSysErrModeMatrix);
unfoldMC.AddSysError(hresponse_id_dn, "Down1", TUnfoldDensity::kHistMapOutputVert,  TUnfoldDensity::kSysErrModeMatrix);

unfoldMC.AddSysError(hresponse_l1_up, "Up2", TUnfoldDensity::kHistMapOutputVert,  TUnfoldDensity::kSysErrModeMatrix);
unfoldMC.AddSysError(hresponse_l1_dn, "Down2", TUnfoldDensity::kHistMapOutputVert,  TUnfoldDensity::kSysErrModeMatrix);

unfoldMC.AddSysError(hresponse_scale_up, "Up5", TUnfoldDensity::kHistMapOutputVert,  TUnfoldDensity::kSysErrModeMatrix);
unfoldMC.AddSysError(hresponse_scale_dn, "Down5", TUnfoldDensity::kHistMapOutputVert,  TUnfoldDensity::kSysErrModeMatrix);

unfoldMC.AddSysError(hresponse_pu_up, "Up6", TUnfoldDensity::kHistMapOutputVert,  TUnfoldDensity::kSysErrModeMatrix);
unfoldMC.AddSysError(hresponse_pu_dn, "Down6", TUnfoldDensity::kHistMapOutputVert,  TUnfoldDensity::kSysErrModeMatrix);

unfoldMC.AddSysError(hresponse_pdf_up, "Up7", TUnfoldDensity::kHistMapOutputVert,  TUnfoldDensity::kSysErrModeMatrix);
unfoldMC.AddSysError(hresponse_pdf_dn, "Down7", TUnfoldDensity::kHistMapOutputVert,  TUnfoldDensity::kSysErrModeMatrix);


//if(unfold.SetInput(hmu_reco)>=10000) {
//    std::cout<<"Unfolding result may be wrong\n";
//  }

unfold.DoUnfold(0.);
unfoldMC.DoUnfold(0.);

//Regularize
//Int_t nScan = 30;
//Double_t tauMin = 0.0;
//Double_t tauMax = 0.0;
//Int_t iBest = 0;
//
//TSpline *logTauX,*logTauY;
//TGraph *lCurve;
//
//iBest=unfold.ScanLcurve(nScan,tauMin,tauMax,&lCurve,&logTauX,&logTauY);

//std::cout<<"chi**2="<<unfold.GetChi2A()<<"+"<<unfold.GetChi2L()
//           <<" / "<<unfold.GetNdf()<<"\n";

std::cout<<"result smeared "<<hmu_data->Chi2Test(hmu_reco,  "UW")<<std::endl;


TH1 *o = unfold.GetOutput("o");
TH1 *oMC = unfoldMC.GetOutput("oMC");

TH1F *hunfold = (TH1F*)o->Clone("hunfold_up");
TH1F *hunfold_down = (TH1F*)o->Clone("hunfold_down");
TH1F *hunfoldMC = (TH1F*)oMC->Clone("hunfoldMC");

TH2 *histEmatTotal = unfold.GetEmatrixTotal("EmatTotal");
TH2 *histEmatInput = unfold.GetEmatrixInput("EmatInput");
TH2 *histEmatSysUncorr = unfold.GetEmatrixSysUncorr("EmatSysUncorr");

TH2 *histEmatTotalMC = unfoldMC.GetEmatrixTotal("EmatTotal");
TH2 *histEmatInputMC = unfoldMC.GetEmatrixInput("EmatInput");
TH2 *histEmatSysUncorrMC = unfoldMC.GetEmatrixSysUncorr("EmatSysUncorr");

histEmatTotal->SetName("histEmatTotal");
histEmatInput->SetName("histEmatInput");
histEmatSysUncorr->SetName("histEmatSysUncorr");

histEmatTotalMC->SetName("histEmatTotalMC");
histEmatInputMC->SetName("histEmatInputMC");
histEmatSysUncorrMC->SetName("histEmatSysUncorrMC");

for(int i=1; i<= oMC->GetNbinsX(); i++){

hunfoldMC->SetBinError(i, TMath::Sqrt(histEmatTotalMC->GetBinContent(i,i)));

}



for(int i=1; i<= o->GetNbinsX(); i++){

hunfold->SetBinError(i, TMath::Sqrt(histEmatTotal->GetBinContent(i,i)));

}

std::cout<<"result unfolded "<<o->Chi2Test(hmu_gen,  "UW")<<std::endl;
hmu_gen->Draw("lep, same");
hmu_gen->SetMarkerColor(kRed);
hmu_gen->SetLineColor(kRed);
hmu_gen->SetLineWidth(3);
hmu_gen->SetMarkerSize(1.5);
hmu_gen->SetMarkerStyle(20);

std::cout<<"DY unfolded "<< oMC->GetBinContent(1)<<std::endl;


//TFile *file1 = new TFile("unfolded_mc_elec_bb.root","RECREATE");
TFile *file1 = new TFile("unfolded_mc_elec_bb_data_2b.root","RECREATE");
file1->cd();
o->Write();
oMC->Write();
hmu_data_org->Write();
hmu_gen->Write();
hmu_reco_org->Write();
hunfold->Write();
histEmatTotal->Write();
histEmatSysUncorr->Write();
histEmatInput->Write();

hunfoldMC->Write();
histEmatTotalMC->Write();
histEmatSysUncorrMC->Write();
histEmatInputMC->Write();


file1->Close();

 //==========================================================================
 //  // print some results
 //    //
//std::cout<<"tau="<<unfold.GetTau()<<"\n";
//std::cout<<"chi**2="<<unfold.GetChi2A()<<"+"<<unfold.GetChi2L()<<" / "<<unfold.GetNdf()<<"\n";
}
