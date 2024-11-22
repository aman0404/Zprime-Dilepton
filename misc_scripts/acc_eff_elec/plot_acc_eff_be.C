{
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
TH1 *hbbll_deno, *hbbll, *hbbll_0b, *hbbll_1b, *hbbll_2b;

TFile *f1 = TFile::Open("dy_BE.root");
f1->GetObject("h_deno", hdy_deno);
f1->GetObject("h_mu_acc_eff", hdy);
f1->GetObject("h_mu_acc_eff_0b", hdy_0b);
f1->GetObject("h_mu_acc_eff_1b", hdy_1b);
f1->GetObject("h_mu_acc_eff_2b", hdy_2b);

TFile *f2 = TFile::Open("bbll_10TeV_BE.root");
f2->GetObject("h_deno", hbbll_deno);
f2->GetObject("h_mu_acc_eff", hbbll);
f2->GetObject("h_mu_acc_eff_0b", hbbll_0b);
f2->GetObject("h_mu_acc_eff_1b", hbbll_1b);
f2->GetObject("h_mu_acc_eff_2b", hbbll_2b);

TH1F *hhdy_deno= (TH1F*)hdy_deno->Clone("hhdy_deno");
TH1F *hhbbll_deno= (TH1F*)hbbll_deno->Clone("hhbbll_deno");

hdy->Divide(hhdy_deno);
hdy_0b->Divide(hhdy_deno);
hdy_1b->Divide(hhdy_deno);
hdy_2b->Divide(hhdy_deno);

hbbll_0b->Divide(hhbbll_deno);

//hdy->Draw("lp");
hdy_0b->Draw("lp");
hbbll_0b->Draw("lp, same");
//hdy_1b->Draw("lp");
//hdy_2b->Draw("lp, same");

hdy_0b->SetMarkerColor(kMagenta);
hbbll_0b->SetMarkerColor(kGreen);
hbbll_0b->SetLineColor(kGreen);

hdy_0b->SetLineWidth(2);
hbbll_0b->SetLineWidth(2);

hdy_1b->SetMarkerColor(kGreen);
hdy_2b->SetMarkerColor(kBlue);

hdy_0b->SetLineColor(kMagenta);
hdy_1b->SetLineColor(kGreen);
hdy_2b->SetLineColor(kBlue);

hdy_0b->SetStats(kFALSE);
hdy_0b->SetTitle("");
hdy_0b->GetYaxis()->SetTitle("acc #times eff");
hdy_0b->GetXaxis()->SetTitle("M_{#mu#mu} [GeV]");

hdy_0b->GetYaxis()->SetRangeUser(0, 1.1);
hdy_0b->GetXaxis()->SetRangeUser(0, 3500);

        double y_legend = 1.11;
        //double y_legend = 0.12;
        double x_legend = 300;
        TLatex *   tex = new TLatex(x_legend,y_legend,"CMS");
//      TLatex *   tex = new TLatex(105,400,"CMS");
     tex->SetTextAlign(20);
   tex->SetTextSize(0.055);
   tex->SetLineWidth(2);
        tex->Draw();
        TLatex *   tex1 = new TLatex(x_legend+500,y_legend,"#it{#bf{Simulation}}");
   tex1->SetTextAlign(20);
   tex1->SetTextSize(0.035);

   tex1->SetLineWidth(2);
   tex1->Draw();

TLegend *legend = new TLegend(0.6361186,0.7468707,0.9326146,0.9193324,NULL,"brNDC");
legend->SetTextSize(0.035);
legend->AddEntry(hdy_0b,  "DY+Jets","lep");
legend->AddEntry(hbbll_0b,"bbll #Lambda=10 TeV","lep");
legend->Draw();

c1->SaveAs("plots/acc_eff_muon_be.png");
c1->SaveAs("plots/acc_eff_muon_be.pdf");
c1->SaveAs("plots/acc_eff_muon_be.root");

}
