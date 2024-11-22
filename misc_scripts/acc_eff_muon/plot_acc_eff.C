{
//////Script for acceptance times efficiency for two muons in BB region/////
//
//
/////////////////////////////////////////////////////////////
TCanvas *c1 = new TCanvas("c1", "stacked hists",61,24,744,744);
   c1->Range(-29.17415,-0.08108108,263.2406,0.6466216);
   c1->SetFillColor(0);
   c1->SetBorderMode(0);
   c1->SetBorderSize(2);
//   c1->SetGridx();
//   c1->SetGridy();
   c1->SetRightMargin(0.04528012);
   c1->SetLeftMargin(0.12);
   c1->SetTopMargin(0.06406685);
   c1->SetBottomMargin(0.1114206);
   c1->SetFrameBorderMode(0);
   c1->SetFrameBorderMode(0);

TH1 *hdy_deno, *hdy, *hdy_0b, *hdy_1b, *hdy_2b;
TH1 *hbbll_deno[4], *hbbll[4], *hbbll_0b[4], *hbbll_1b[4], *hbbll_2b[4];
TH1 *hdy_reco, *hbbll_reco[4];
TH1 *hdy_trig, *hbbll_trig[4];

TFile *f1 = TFile::Open("dy_BB.root");
f1->GetObject("h_deno", hdy_deno);
f1->GetObject("h_mu_trig", hdy_trig);
f1->GetObject("h_mu_reco", hdy_reco);
f1->GetObject("h_mu_acc_eff", hdy);
f1->GetObject("h_mu_acc_eff_0b", hdy_0b);
f1->GetObject("h_mu_acc_eff_1b", hdy_1b);
f1->GetObject("h_mu_acc_eff_2b", hdy_2b);

TFile *f2 = TFile::Open("bbll_6TeV_BB.root");
f2->GetObject("h_deno", hbbll_deno[0]);
f2->GetObject("h_mu_trig", hbbll_trig[0]);
f2->GetObject("h_mu_reco", hbbll_reco[0]);
f2->GetObject("h_mu_acc_eff", hbbll[0]);
f2->GetObject("h_mu_acc_eff_0b", hbbll_0b[0]);
f2->GetObject("h_mu_acc_eff_1b", hbbll_1b[0]);
f2->GetObject("h_mu_acc_eff_2b", hbbll_2b[0]);

TFile *f3 = TFile::Open("bbll_10TeV_BB.root");
f3->GetObject("h_deno", hbbll_deno[1]);
f3->GetObject("h_mu_trig", hbbll_trig[1]);
f3->GetObject("h_mu_reco", hbbll_reco[1]);
f3->GetObject("h_mu_acc_eff", hbbll[1]);
f3->GetObject("h_mu_acc_eff_0b", hbbll_0b[1]);
f3->GetObject("h_mu_acc_eff_1b", hbbll_1b[1]);
f3->GetObject("h_mu_acc_eff_2b", hbbll_2b[1]);

TFile *f4 = TFile::Open("bbll_18TeV_BB.root");
f4->GetObject("h_deno", hbbll_deno[2]);
f4->GetObject("h_mu_trig", hbbll_trig[2]);
f4->GetObject("h_mu_reco", hbbll_reco[2]);
f4->GetObject("h_mu_acc_eff", hbbll[2]);
f4->GetObject("h_mu_acc_eff_0b", hbbll_0b[2]);
f4->GetObject("h_mu_acc_eff_1b", hbbll_1b[2]);
f4->GetObject("h_mu_acc_eff_2b", hbbll_2b[2]);

TFile *f5 = TFile::Open("bbll_26TeV_BB.root");
f5->GetObject("h_deno", hbbll_deno[3]);
f5->GetObject("h_mu_trig", hbbll_trig[3]);
f5->GetObject("h_mu_reco", hbbll_reco[3]);
f5->GetObject("h_mu_acc_eff", hbbll[3]);
f5->GetObject("h_mu_acc_eff_0b", hbbll_0b[3]);
f5->GetObject("h_mu_acc_eff_1b", hbbll_1b[3]);
f5->GetObject("h_mu_acc_eff_2b", hbbll_2b[3]);


hdy_trig->Divide(hdy_deno);

hbbll_trig[0]->Divide(hbbll_deno[0]);
hbbll_trig[1]->Divide(hbbll_deno[1]);
hbbll_trig[2]->Divide(hbbll_deno[2]);
hbbll_trig[3]->Divide(hbbll_deno[3]);


hdy->Divide(hdy_reco);

hbbll[0]->Divide(hbbll_reco[0]);
hbbll[1]->Divide(hbbll_reco[1]);
hbbll[2]->Divide(hbbll_reco[2]);
hbbll[3]->Divide(hbbll_reco[3]);

hdy->Multiply(hdy_trig);

hbbll[0]->Multiply(hbbll_trig[0]);
hbbll[1]->Multiply(hbbll_trig[1]);
hbbll[2]->Multiply(hbbll_trig[2]);
hbbll[3]->Multiply(hbbll_trig[3]);


//hdy_0b->Divide(hhdy_deno);
//hdy_1b->Divide(hhdy_deno);
//hdy_2b->Divide(hhdy_deno);

//hbbll_0b->Divide(hhbbll_deno);

hdy->Draw("lp");
hbbll[0]->Draw("lp, same");
hbbll[1]->Draw("lp, same");
hbbll[2]->Draw("lp, same");
hbbll[3]->Draw("lp, same");

//hdy_0b->Draw("lp");
//hbbll_0b->Draw("lp, same");
//hdy_1b->Draw("lp");
//hdy_2b->Draw("lp, same");

hdy->SetMarkerColor(kBlack);
hbbll[0]->SetMarkerColor(kMagenta);
hbbll[1]->SetMarkerColor(kGreen);
hbbll[2]->SetMarkerColor(kOrange);
hbbll[3]->SetMarkerColor(kRed);

hdy->SetMarkerStyle(20);
hbbll[0]->SetMarkerStyle(20);
hbbll[1]->SetMarkerStyle(20);
hbbll[2]->SetMarkerStyle(20);
hbbll[3]->SetMarkerStyle(20);

hdy->SetLineColor(kBlack);
hbbll[0]->SetLineColor(kMagenta);
hbbll[1]->SetLineColor(kGreen);
hbbll[2]->SetLineColor(kOrange);
hbbll[3]->SetLineColor(kRed);

hdy->SetLineWidth(2);
hbbll[0]->SetLineWidth(2);
hbbll[1]->SetLineWidth(2);
hbbll[2]->SetLineWidth(2);
hbbll[3]->SetLineWidth(2);


//hbbll_0b->SetLineColor(kGreen);

//hdy_0b->SetLineWidth(2);
//hbbll_0b->SetLineWidth(2);

//hdy_1b->SetMarkerColor(kGreen);
//hdy_2b->SetMarkerColor(kBlue);

//hdy_0b->SetLineColor(kMagenta);
//hdy_1b->SetLineColor(kGreen);
//hdy_2b->SetLineColor(kBlue);

hdy->SetStats(kFALSE);
hdy->SetTitle("");
hdy->GetYaxis()->SetTitle("acc #times eff");
hdy->GetXaxis()->SetTitle("M_{#mu#mu} [GeV]");

hdy->GetYaxis()->SetRangeUser(0, 1.5);
hdy->GetXaxis()->SetRangeUser(0, 4070);

        double y_legend = 1.51;
        //double y_legend = 0.12;
        double x_legend = 300;
        TLatex *   tex = new TLatex(x_legend,y_legend,"CMS");
//      TLatex *   tex = new TLatex(105,400,"CMS");
     tex->SetTextAlign(20);
   tex->SetTextSize(0.055);
   tex->SetLineWidth(2);
        tex->Draw();
        TLatex *   tex1 = new TLatex(x_legend+ 600,y_legend,"#it{#bf{Simulation}}");
   tex1->SetTextAlign(20);
   tex1->SetTextSize(0.035);

   tex1->SetLineWidth(2);
   tex1->Draw();

   TLatex *   tex2 = new TLatex(2700,0.95,"#mu#mu Acc #times Eff");
   tex2->SetTextAlign(20);
   tex2->SetTextSize(0.035);
   tex2->SetLineWidth(2);
   tex2->Draw();



TLegend *legend = new TLegend(0.60,0.68,0.9326146,0.9193324,NULL,"brNDC");
legend->SetTextSize(0.035);
legend->SetHeader("BB Category");
legend->AddEntry(hdy,  "DY+Jets","lep");
legend->AddEntry(hbbll[0],"bbll #Lambda=6 TeV","lep");
legend->AddEntry(hbbll[1],"bbll #Lambda=10 TeV","lep");
legend->AddEntry(hbbll[2],"bbll #Lambda=18 TeV","lep");
legend->AddEntry(hbbll[3],"bbll #Lambda=26 TeV","lep");
legend->Draw();

c1->SaveAs("plots/acc_eff_muon.png");
c1->SaveAs("plots/acc_eff_muon.pdf");
c1->SaveAs("plots/acc_eff_muon.root");

}
