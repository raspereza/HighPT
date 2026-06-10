//////////////////////////////////////////////////////////
// This class has been automatically generated on
// Sun Apr 19 17:32:48 2026 by ROOT version 6.30/07
// from TTree tree/tree
// found on file: root://eoscms.cern.ch//eos/cms/store/group/phys_tau/rasp/HighPT/2025/wjets/Muon0_Run2025C_wjets.root
//////////////////////////////////////////////////////////

#ifndef tree_h
#define tree_h

#include <TROOT.h>
#include <TChain.h>
#include <TFile.h>

// Header file for the classes stored in the TTree if any.

class tree {
public :
   TTree          *fChain;   //!pointer to the analyzed TTree or TChain
   Int_t           fCurrent; //!current Tree number in a TChain

// Fixed size dimensions of array or collections stored in the TTree if any.

   // Declaration of leaf types
   Int_t           run;
   Int_t           lumi;
   Int_t           evt;
   Bool_t          data;
   Int_t           npv;
   Int_t           npv_good;
   Float_t         rho;
   Bool_t          metfilter;
   Bool_t          mettrigger;
   Bool_t          tautrigger1;
   Bool_t          tautrigger2;
   Bool_t          tautrigger3;
   Bool_t          tautrigger4;
   Float_t         weight;
   Int_t           njets;
   Int_t           ncjets;
   Float_t         met;
   Float_t         metphi;
   Float_t         metnomu;
   Float_t         mhtnomu;
   Float_t         mt_1;
   Float_t         metdphi_1;
   Float_t         mt_jet_1;
   Float_t         metdphi_jet_1;
   Bool_t          extraelec_veto;
   Bool_t          extramuon_veto;
   Bool_t          extratau_veto;
   Bool_t          hotjet_veto;
   Float_t         pt_1;
   Float_t         eta_1;
   Float_t         phi_1;
   Float_t         dxy_1;
   Float_t         dz_1;
   Int_t           q_1;
   Float_t         iso_1;
   Bool_t          idMedium_1;
   Bool_t          idTight_1;
   Int_t           idHighPt_1;
   Float_t         pt_2;
   Float_t         eta_2;
   Float_t         phi_2;
   Float_t         m_2;
   Int_t           q_2;
   Int_t           dm_2;
   Float_t         rawDeepTau2018v2p5VSe_2;
   Float_t         rawDeepTau2018v2p5VSmu_2;
   Float_t         rawDeepTau2018v2p5VSjet_2;
   Int_t           idDeepTau2018v2p5VSe_2;
   Int_t           idDeepTau2018v2p5VSmu_2;
   Int_t           idDeepTau2018v2p5VSjet_2;
   Float_t         jpt_match_2;
   Float_t         jeta_match_2;
   Float_t         jpt_ratio_2;
   Float_t         dphi;

   // List of branches
   TBranch        *b_run;   //!
   TBranch        *b_lumi;   //!
   TBranch        *b_evt;   //!
   TBranch        *b_data;   //!
   TBranch        *b_npv;   //!
   TBranch        *b_npv_good;   //!
   TBranch        *b_rho;   //!
   TBranch        *b_metfilter;   //!
   TBranch        *b_mettrigger;   //!
   TBranch        *b_tautrigger1;   //!
   TBranch        *b_tautrigger2;   //!
   TBranch        *b_tautrigger3;   //!
   TBranch        *b_tautrigger4;   //!
   TBranch        *b_weight;   //!
   TBranch        *b_njets;   //!
   TBranch        *b_ncjets;   //!
   TBranch        *b_met;   //!
   TBranch        *b_metphi;   //!
   TBranch        *b_metnomu;   //!
   TBranch        *b_mhtnomu;   //!
   TBranch        *b_mt_1;   //!
   TBranch        *b_metdphi_1;   //!
   TBranch        *b_mt_jet_1;   //!
   TBranch        *b_metdphi_jet_1;   //!
   TBranch        *b_extraelec_veto;   //!
   TBranch        *b_extramuon_veto;   //!
   TBranch        *b_extratau_veto;   //!
   TBranch        *b_hotjet_veto;   //!
   TBranch        *b_pt_1;   //!
   TBranch        *b_eta_1;   //!
   TBranch        *b_phi_1;   //!
   TBranch        *b_dxy_1;   //!
   TBranch        *b_dz_1;   //!
   TBranch        *b_q_1;   //!
   TBranch        *b_iso_1;   //!
   TBranch        *b_idMedium_1;   //!
   TBranch        *b_idTight_1;   //!
   TBranch        *b_idHighPt_1;   //!
   TBranch        *b_pt_2;   //!
   TBranch        *b_eta_2;   //!
   TBranch        *b_phi_2;   //!
   TBranch        *b_m_2;   //!
   TBranch        *b_q_2;   //!
   TBranch        *b_dm_2;   //!
   TBranch        *b_rawDeepTau2018v2p5VSe_2;   //!
   TBranch        *b_rawDeepTau2018v2p5VSmu_2;   //!
   TBranch        *b_rawDeepTau2018v2p5VSjet_2;   //!
   TBranch        *b_idDeepTau2018v2p5VSe_2;   //!
   TBranch        *b_idDeepTau2018v2p5VSmu_2;   //!
   TBranch        *b_idDeepTau2018v2p5VSjet_2;   //!
   TBranch        *b_jpt_match_2;   //!
   TBranch        *b_jeta_match_2;   //!
   TBranch        *b_jpt_ratio_2;   //!
   TBranch        *b_dphi;   //!

   tree(TTree *tree=0);
   virtual ~tree();
   virtual Int_t    Cut(Long64_t entry);
   virtual Int_t    GetEntry(Long64_t entry);
   virtual Long64_t LoadTree(Long64_t entry);
   virtual void     Init(TTree *tree);
   virtual void     Loop();
   virtual Bool_t   Notify();
   virtual void     Show(Long64_t entry = -1);
};

#endif

#ifdef tree_cxx
tree::tree(TTree *tree) : fChain(0) 
{
// if parameter tree is not specified (or zero), connect the file
// used to generate this class and read the Tree.
   if (tree == 0) {
      TFile *f = (TFile*)gROOT->GetListOfFiles()->FindObject("root://eoscms.cern.ch//eos/cms/store/group/phys_tau/rasp/HighPT/2025/wjets/Muon0_Run2025C_wjets.root");
      if (!f || !f->IsOpen()) {
         f = new TFile("root://eoscms.cern.ch//eos/cms/store/group/phys_tau/rasp/HighPT/2025/wjets/Muon0_Run2025C_wjets.root");
      }
      f->GetObject("tree",tree);

   }
   Init(tree);
}

tree::~tree()
{
   if (!fChain) return;
   delete fChain->GetCurrentFile();
}

Int_t tree::GetEntry(Long64_t entry)
{
// Read contents of entry.
   if (!fChain) return 0;
   return fChain->GetEntry(entry);
}
Long64_t tree::LoadTree(Long64_t entry)
{
// Set the environment to read one entry
   if (!fChain) return -5;
   Long64_t centry = fChain->LoadTree(entry);
   if (centry < 0) return centry;
   if (fChain->GetTreeNumber() != fCurrent) {
      fCurrent = fChain->GetTreeNumber();
      Notify();
   }
   return centry;
}

void tree::Init(TTree *tree)
{
   // The Init() function is called when the selector needs to initialize
   // a new tree or chain. Typically here the branch addresses and branch
   // pointers of the tree will be set.
   // It is normally not necessary to make changes to the generated
   // code, but the routine can be extended by the user if needed.
   // Init() will be called many times when running on PROOF
   // (once per file to be processed).

   // Set branch addresses and branch pointers
   if (!tree) return;
   fChain = tree;
   fCurrent = -1;
   fChain->SetMakeClass(1);

   fChain->SetBranchAddress("run", &run, &b_run);
   fChain->SetBranchAddress("lumi", &lumi, &b_lumi);
   fChain->SetBranchAddress("evt", &evt, &b_evt);
   fChain->SetBranchAddress("data", &data, &b_data);
   fChain->SetBranchAddress("npv", &npv, &b_npv);
   fChain->SetBranchAddress("npv_good", &npv_good, &b_npv_good);
   fChain->SetBranchAddress("rho", &rho, &b_rho);
   fChain->SetBranchAddress("metfilter", &metfilter, &b_metfilter);
   fChain->SetBranchAddress("mettrigger", &mettrigger, &b_mettrigger);
   fChain->SetBranchAddress("tautrigger1", &tautrigger1, &b_tautrigger1);
   fChain->SetBranchAddress("tautrigger2", &tautrigger2, &b_tautrigger2);
   fChain->SetBranchAddress("tautrigger3", &tautrigger3, &b_tautrigger3);
   fChain->SetBranchAddress("tautrigger4", &tautrigger4, &b_tautrigger4);
   fChain->SetBranchAddress("weight", &weight, &b_weight);
   fChain->SetBranchAddress("njets", &njets, &b_njets);
   fChain->SetBranchAddress("ncjets", &ncjets, &b_ncjets);
   fChain->SetBranchAddress("met", &met, &b_met);
   fChain->SetBranchAddress("metphi", &metphi, &b_metphi);
   fChain->SetBranchAddress("metnomu", &metnomu, &b_metnomu);
   fChain->SetBranchAddress("mhtnomu", &mhtnomu, &b_mhtnomu);
   fChain->SetBranchAddress("mt_1", &mt_1, &b_mt_1);
   fChain->SetBranchAddress("metdphi_1", &metdphi_1, &b_metdphi_1);
   fChain->SetBranchAddress("mt_jet_1", &mt_jet_1, &b_mt_jet_1);
   fChain->SetBranchAddress("metdphi_jet_1", &metdphi_jet_1, &b_metdphi_jet_1);
   fChain->SetBranchAddress("extraelec_veto", &extraelec_veto, &b_extraelec_veto);
   fChain->SetBranchAddress("extramuon_veto", &extramuon_veto, &b_extramuon_veto);
   fChain->SetBranchAddress("extratau_veto", &extratau_veto, &b_extratau_veto);
   fChain->SetBranchAddress("hotjet_veto", &hotjet_veto, &b_hotjet_veto);
   fChain->SetBranchAddress("pt_1", &pt_1, &b_pt_1);
   fChain->SetBranchAddress("eta_1", &eta_1, &b_eta_1);
   fChain->SetBranchAddress("phi_1", &phi_1, &b_phi_1);
   fChain->SetBranchAddress("dxy_1", &dxy_1, &b_dxy_1);
   fChain->SetBranchAddress("dz_1", &dz_1, &b_dz_1);
   fChain->SetBranchAddress("q_1", &q_1, &b_q_1);
   fChain->SetBranchAddress("iso_1", &iso_1, &b_iso_1);
   fChain->SetBranchAddress("idMedium_1", &idMedium_1, &b_idMedium_1);
   fChain->SetBranchAddress("idTight_1", &idTight_1, &b_idTight_1);
   fChain->SetBranchAddress("idHighPt_1", &idHighPt_1, &b_idHighPt_1);
   fChain->SetBranchAddress("pt_2", &pt_2, &b_pt_2);
   fChain->SetBranchAddress("eta_2", &eta_2, &b_eta_2);
   fChain->SetBranchAddress("phi_2", &phi_2, &b_phi_2);
   fChain->SetBranchAddress("m_2", &m_2, &b_m_2);
   fChain->SetBranchAddress("q_2", &q_2, &b_q_2);
   fChain->SetBranchAddress("dm_2", &dm_2, &b_dm_2);
   fChain->SetBranchAddress("rawDeepTau2018v2p5VSe_2", &rawDeepTau2018v2p5VSe_2, &b_rawDeepTau2018v2p5VSe_2);
   fChain->SetBranchAddress("rawDeepTau2018v2p5VSmu_2", &rawDeepTau2018v2p5VSmu_2, &b_rawDeepTau2018v2p5VSmu_2);
   fChain->SetBranchAddress("rawDeepTau2018v2p5VSjet_2", &rawDeepTau2018v2p5VSjet_2, &b_rawDeepTau2018v2p5VSjet_2);
   fChain->SetBranchAddress("idDeepTau2018v2p5VSe_2", &idDeepTau2018v2p5VSe_2, &b_idDeepTau2018v2p5VSe_2);
   fChain->SetBranchAddress("idDeepTau2018v2p5VSmu_2", &idDeepTau2018v2p5VSmu_2, &b_idDeepTau2018v2p5VSmu_2);
   fChain->SetBranchAddress("idDeepTau2018v2p5VSjet_2", &idDeepTau2018v2p5VSjet_2, &b_idDeepTau2018v2p5VSjet_2);
   fChain->SetBranchAddress("jpt_match_2", &jpt_match_2, &b_jpt_match_2);
   fChain->SetBranchAddress("jeta_match_2", &jeta_match_2, &b_jeta_match_2);
   fChain->SetBranchAddress("jpt_ratio_2", &jpt_ratio_2, &b_jpt_ratio_2);
   fChain->SetBranchAddress("dphi", &dphi, &b_dphi);
   Notify();
}

Bool_t tree::Notify()
{
   // The Notify() function is called when a new file is opened. This
   // can be either for a new TTree in a TChain or when when a new TTree
   // is started when using PROOF. It is normally not necessary to make changes
   // to the generated code, but the routine can be extended by the
   // user if needed. The return value is currently not used.

   return kTRUE;
}

void tree::Show(Long64_t entry)
{
// Print contents of entry.
// If entry is not specified, print current entry
   if (!fChain) return;
   fChain->Show(entry);
}
Int_t tree::Cut(Long64_t entry)
{
// This function may be called from Loop.
// returns  1 if entry is accepted.
// returns -1 otherwise.
   return 1;
}
#endif // #ifdef tree_cxx
