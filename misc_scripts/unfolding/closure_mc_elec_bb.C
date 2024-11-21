{
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

TH1 *hmu_unfolded, *hele_unfolded, *hmu_gen1, *hele_gen, *hmu_reco, *hele_reco;
TH1 *hmu_data, *hmu_bkg, *hdy;
TFile *f1 = TFile::Open("unfolded_mc_elec_bb_data.root");
f1->GetObject("hmu_gen", hmu_data);


TFile *f3 = TFile::Open("unfolded_mc_elec_bb_data.root");
f3->GetObject("oMC", hdy);


//Double_t bins[9] = {200, 300, 400, 600, 900, 1250, 1610, 2000, 3500};
//
//TH1F *hmu_bin_reco = (TH1F*)hmu_reco->Rebin(8, "hmu_bin_reco", bins);
//TH1F *hele_bin_reco = (TH1F*)o->Rebin(8, "hel_bin_reco", bins);

//hmu_bin_reco->Sumw2();
//hele_bin_reco->Sumw2();

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

        TH1F *hdiv1 = (TH1F*)hmu_data->Clone("hdiv1"); //data
        TH1F *hdiv3 = (TH1F*)hdy->Clone("hdiv3");  //dy

//hdiv1->Add(hdiv2,-1);
hdiv1->Divide(hdiv3);
hdiv1->Draw("lep");
hdiv1->SetStats(kFALSE);
hdiv1->SetTitle("");
hdiv1->SetMarkerStyle(20);
hdiv1->SetMarkerColor(kBlack);

   hdiv1->GetYaxis()->SetLabelFont(42);
   hdiv1->GetYaxis()->SetNdivisions(20505);
   hdiv1->GetYaxis()->SetLabelSize(0.08);
   hdiv1->GetYaxis()->SetTitleSize(0.08);
   hdiv1->GetYaxis()->SetTitleOffset(0.65);
   hdiv1->GetYaxis()->SetTitleFont(42);
   hdiv1->SetLineColor(kBlue+2);
   hdiv1->SetLineWidth(2);
   hdiv1->GetYaxis()->SetRangeUser(0,2);
   hdiv1->GetXaxis()->SetTitle("m_{ee} [GeV]");
   hdiv1->GetYaxis()->SetTitle("#frac{gen}{unfolded}");

   hdiv1->GetXaxis()->SetLabelFont(42);
   hdiv1->GetXaxis()->SetLabelOffset(0.05);
   hdiv1->GetXaxis()->SetTitleSize(0.10);
   hdiv1->GetXaxis()->SetTitleOffset(1.3);
      hdiv1->GetXaxis()->SetLabelSize(0.10);

   hdiv1->GetYaxis()->CenterTitle(true);
   hdiv1->GetXaxis()->SetRangeUser(200,3490);
//line
   TLine *line = new TLine(200, 1,3500, 1);
   line->SetLineColor(kRed);
   line->Draw();


   c1->cd();
   pad2 = new TPad("pad2", "pad2",0.05,0.37,0.99,0.99);
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


        TH1F *h1data = (TH1F*)hmu_data->Clone("h1data"); //data
        TH1F *hdymc = (TH1F*)hdy->Clone("hdymc");  //dy

//h1data->Add(h1bkg,-1);


h1data->SetStats(kFALSE);
hdymc->SetStats(kFALSE);
hdymc->Draw("hist");
h1data->Draw("lep, same");

hdymc->SetFillColor(8);
hdymc->SetLineColor(8);

hdymc->SetLineWidth(2);

h1data->SetMarkerStyle(20);
h1data->SetMarkerColor(kBlack);
h1data->SetLineColor(kBlue+2);
h1data->SetMarkerSize(1.2);
h1data->SetLineWidth(1);
hdymc->GetYaxis()->SetTitle("Events/GeV");
hdymc->GetYaxis()->SetTitleSize(0.045);
hdymc->GetYaxis()->SetLabelSize(0.045);
hdymc->SetTitle("");
hdymc->GetXaxis()->SetRangeUser(200,3490);
hdymc->GetYaxis()->SetRangeUser(2e-4,1e6);

        double y_legend = 1.5e6;
        double x_legend = 350;
        TLatex *   tex = new TLatex(x_legend,y_legend,"CMS");
//      TLatex *   tex = new TLatex(105,400,"CMS");
     tex->SetTextAlign(20);
   tex->SetTextSize(0.07);
   tex->SetLineWidth(2);
        tex->Draw();
        TLatex *   tex1 = new TLatex(x_legend+500,y_legend,"#it{#bf{Preliminary}}");
   tex1->SetTextAlign(20);
   tex1->SetTextSize(0.05);

   tex1->SetLineWidth(2);
   tex1->Draw();

        TLegend *legend = new TLegend(0.57,0.650899,0.94,0.8843167,NULL,"brNDC");

        legend->SetHeader("BB category");
        legend->SetTextSize(0.055);
        legend->AddEntry(hdymc,"unfolded","f");
        legend->AddEntry(h1data,"Generated","lep");


        legend->Draw();

c1->SaveAs("plots/closure_bb_el.png");
c1->SaveAs("plots/closure_bb_el.pdf");
c1->SaveAs("plots/closure_bb_el.root");
}
