{
TCanvas *c1 = new TCanvas("c1", "stacked hists",61,24,744,744);
   c1->Range(-29.17415,-0.08108108,263.2406,0.6466216);
   c1->SetFillColor(0);
   c1->SetBorderMode(0);
   c1->SetBorderSize(2);
//   c1->SetGridx();
//   c1->SetGridy();
   c1->SetRightMargin(0.05);
   c1->SetLeftMargin(0.14);
   c1->SetTopMargin(0.06406685);
   c1->SetBottomMargin(0.1114206);
   c1->SetFrameBorderMode(0);
   c1->SetFrameBorderMode(0);
   c1->SetLogx();
//   c1->SetLogy();

TH1 *unfolded_mu_dy , *unfolded_el_dy;
TH1 *unfolded_mu_data , *unfolded_el_data;

TFile *f1 = TFile::Open("unfolded_mc_muon_bb_data.root");
f1->GetObject("hunfoldMC", unfolded_mu_dy);

TFile *f2 = TFile::Open("unfolded_mc_elec_bb_data.root");
f2->GetObject("hunfoldMC", unfolded_el_dy);

TFile *f3 = TFile::Open("unfolded_mc_muon_bb_data.root");
f3->GetObject("hunfold_up", unfolded_mu_data);

TFile *f4 = TFile::Open("unfolded_mc_elec_bb_data.root");
f4->GetObject("hunfold_up", unfolded_el_data);



// TPad *pad1 = new TPad("pad1", "pad1",0.05,0.03114206,0.99,0.39);
//   pad1->Draw();
//   pad1->cd();
//   pad1->Range(-49.46043,-0.4895868,524.2806,1.328879);
//   pad1->SetFillColor(0);
//   pad1->SetBorderMode(0);
//   pad1->SetBorderSize(2);
////   pad1->SetGridx();
//   pad1->SetRightMargin(0.04);
// //  pad1->SetTopMargin(0.00101554);
//   pad1->SetBottomMargin(0.4);
//   pad1->SetFrameBorderMode(0);
//   pad1->SetFrameBorderMode(0);
//   pad1->SetLeftMargin(0.14);
//   pad1->SetFrameBorderMode(0);
//   pad1->SetFrameBorderMode(0);

        TH1F *hdiv1 = (TH1F*)unfolded_mu_dy->Clone("hdiv1"); //data
        TH1F *hdiv2 = (TH1F*)unfolded_el_dy->Clone("hdiv2");  //bkg
        TH1F *hdiv3 = (TH1F*)unfolded_mu_data->Clone("hdiv3");  //dy
        TH1F *hdiv4 = (TH1F*)unfolded_el_data->Clone("hdiv4");  //dy

//hdiv1->Add(hdiv2,-1);
hdiv1->Divide(hdiv2);
hdiv3->Divide(hdiv4);

hdiv1->Draw("ep");
hdiv3->Draw("ep, same");
hdiv1->SetStats(kFALSE);
hdiv1->SetTitle("");
hdiv1->SetMarkerStyle(20);
hdiv3->SetMarkerStyle(20);
hdiv1->SetMarkerColor(kRed);
hdiv3->SetMarkerColor(kBlue);
hdiv1->SetMarkerSize(1.2);
hdiv3->SetMarkerSize(1.2);

   hdiv1->GetYaxis()->SetLabelFont(42);
   hdiv1->GetYaxis()->SetNdivisions(20505);
   hdiv1->GetYaxis()->SetLabelSize(0.04);
   hdiv1->GetYaxis()->SetTitleSize(0.04);
   hdiv1->GetYaxis()->SetTitleOffset(1.3);
   hdiv1->GetYaxis()->SetTitleFont(42);
   hdiv1->SetLineColor(kBlue+2);
   hdiv1->SetLineWidth(2);
   hdiv3->SetLineWidth(2);
   hdiv1->GetYaxis()->SetRangeUser(0,3.0);
   hdiv1->GetXaxis()->SetTitle("m_{ll} [GeV]");
   hdiv1->GetYaxis()->SetTitle("R_{#mu#mu/ee}");

   hdiv1->GetXaxis()->SetLabelFont(42);
   hdiv1->GetXaxis()->SetLabelOffset(0.02);
   hdiv1->GetXaxis()->SetTitleSize(0.04);
   hdiv1->GetXaxis()->SetTitleOffset(1.1);
      hdiv1->GetXaxis()->SetLabelSize(0.04);

//   hdiv1->GetYaxis()->CenterTitle(true);
   hdiv1->GetXaxis()->SetRangeUser(200,6000);
//line
   TLine *line = new TLine(200, 1,6000, 1);
   line->SetLineColor(kRed);
   line->Draw();


//   c1->cd();
//   pad2 = new TPad("pad2", "pad2",0.05,0.37,0.99,0.99);
//   pad2->Draw();
//   pad2->cd();
//   pad2->Range(-44.421,-161.3852,528.7119,36963.49);
//   pad2->SetFillColor(0);
//   pad2->SetBorderMode(0);
//   pad2->SetBorderSize(2);
//   pad2->SetLogy();
//
////   pad2->SetGridx();
//   pad2->SetRightMargin(0.04);
//   pad2->SetLeftMargin(0.14);
//   pad2->SetTopMargin(0.0806685);
//   pad2->SetBottomMargin(0);
//   pad2->SetFrameBorderMode(0);
//   pad2->SetFrameBorderMode(0);
//
//
//        TH1F *h1data = (TH1F*)hmu_data->Clone("h1data"); //data
//        TH1F *h1bkg = (TH1F*)hmu_bkg->Clone("h1bkg");  //bkg
//        TH1F *hdymc = (TH1F*)hdy->Clone("hdymc");  //dy
//
////h1data->Add(h1bkg,-1);
//
//
//h1data->SetStats(kFALSE);
//hdymc->SetStats(kFALSE);
//hdymc->Draw("hist");
//h1data->Draw("lep, same");
//
//hdymc->SetFillColor(8);
//hdymc->SetLineColor(8);
//
//hdymc->SetLineWidth(2);
//
//h1data->SetMarkerStyle(20);
//h1data->SetMarkerColor(kBlack);
//h1data->SetLineColor(kBlue+2);
//h1data->SetMarkerSize(1.2);
//h1data->SetLineWidth(1);
//hdymc->GetYaxis()->SetTitle("Events/GeV");
//hdymc->GetYaxis()->SetTitleSize(0.045);
//hdymc->GetYaxis()->SetLabelSize(0.045);
//hdymc->SetTitle("");
//hdymc->GetXaxis()->SetRangeUser(200,3490);
//hdymc->GetYaxis()->SetRangeUser(2e-4,1e3);
//
        double y_legend = hdiv1->GetMaximum() + 0.01;
        double x_legend = 250;
        TLatex *   tex = new TLatex(x_legend,y_legend,"CMS");
//      TLatex *   tex = new TLatex(105,400,"CMS");
     tex->SetTextAlign(20);
   tex->SetTextSize(0.05);
   tex->SetLineWidth(2);
        tex->Draw();
        TLatex *   tex1 = new TLatex(x_legend+170,y_legend,"#it{#bf{Preliminary}}");
   tex1->SetTextAlign(20);
   tex1->SetTextSize(0.03);

   tex1->SetLineWidth(2);
   tex1->Draw();

        TLegend *legend = new TLegend(0.37,0.750899,0.94,0.8843167,NULL,"brNDC");

        //legend->SetHeader("BB category");
        legend->SetTextSize(0.03);
        legend->AddEntry(hdiv1,"uncorrected flavor ratio (DY MC)","lep");
        legend->AddEntry(hdiv3,"uncorrected flavor ratio (Data - bkg)","lep");


        legend->Draw();

c1->SaveAs("plots/total_fratio_bb_mc.png");
c1->SaveAs("plots/total_fratio_bb_mc.pdf");
c1->SaveAs("plots/total_fratio_bb_mc.root");
}
