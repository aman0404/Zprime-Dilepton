
#ifndef ZPRIMEVOIGTIAN
#define ZPRIMEVOIGTIAN

#include "RooAbsPdf.h"
#include "RooRealProxy.h"
#include "RooCategoryProxy.h"
#include "RooAbsReal.h"
#include "RooAbsCategory.h"


#include <limits> 


//basically truncates the Voigtian more than 3 widths away from the peak 

class ZPrimeVoigtian : public RooAbsPdf {
public:
  ZPrimeVoigtian() {} ; 
  ZPrimeVoigtian(const char *name, const char *title,
		 RooAbsReal& x,
		 RooAbsReal& mean,
		 RooAbsReal& width,
		 RooAbsReal& sigma, 
		 Bool_t doFast=kFALSE);
	   
  ZPrimeVoigtian(const ZPrimeVoigtian& other, const char* name=0) ;
  virtual TObject* clone(const char* newname) const { return new ZPrimeVoigtian(*this,newname); }
  inline virtual ~ZPrimeVoigtian() { }

protected:
  RooRealProxy x_; 
  RooRealProxy mean_;
  RooRealProxy width_;
  RooRealProxy sigma_;
  bool doFast_;
  mutable double approxWidth_;
  mutable double cachedWidth_;
  mutable double cachedSigma_;
  static const double kInvRootPi_; 

  Double_t evaluate() const ;


private:

  Double_t voigtian_()const;
  double calApproxWidth_()const{return 0.5346*2*width_ + sqrt(0.21566*4*width_*width_+pow(2*sigma_*sqrt(2*log(2)),2));} //an approximation of the full width at half maximum

  ClassDef(ZPrimeVoigtian,1) // Your description goes here...
};
 
#endif
