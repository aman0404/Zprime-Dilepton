#include "ZPrimeVoigtian.h"
#include "Riostream.h" 

#include "RooAbsReal.h" 
#include "RooAbsCategory.h" 
#include <cmath>
#include <complex>
#include "TMath.h" 
#include "RooMath.h"

ClassImp(ZPrimeVoigtian) 

const double ZPrimeVoigtian::kInvRootPi_= 1./sqrt(atan2(0.,-1.));
 
ZPrimeVoigtian::ZPrimeVoigtian(const char *name, const char *title, 
			       RooAbsReal& x,
			       RooAbsReal& mean,
			       RooAbsReal& width,
			       RooAbsReal& sigma, 
			       Bool_t doFast):
   RooAbsPdf(name,title), 
   x_("x","Dependent",this,x),
   mean_("mean","Mean",this,mean),
   width_("width","Breit-Wigner Width",this,width),
   sigma_("sigma","Gauss Width",this,sigma),
   cachedWidth_(width_),
   cachedSigma_(sigma_),
   doFast_(doFast)
{ 
  

  approxWidth_= calApproxWidth_();//an approximation of the full width at half maximum
				       
 } 
    


ZPrimeVoigtian::ZPrimeVoigtian(const ZPrimeVoigtian& other, const char* name) :  
  RooAbsPdf(other,name), 
  x_("x",this,other.x_),
  mean_("mean",this,other.mean_),
  width_("width",this,other.width_),
  sigma_("sigma",this,other.sigma_),
  doFast_(other.doFast_),
  approxWidth_(other.approxWidth_),
  cachedWidth_(other.cachedWidth_),
  cachedSigma_(other.cachedSigma_)
  
{ 
} 



Double_t ZPrimeVoigtian::evaluate() const 
{ 
  
  //  std::cout <<"x "<<x_<<" mean "<<mean_<<" width "<<width_<<" sigma "<<sigma_<<" result "<<voigtian_()<<" ";
  
  if(std::abs(width_-cachedWidth_)>0.001*width_ || std::abs(sigma_-cachedSigma_)>0.001*sigma_){
    //   std::cout <<"recomputing approxwidth ";//<<std::endl;
    approxWidth_=calApproxWidth_();
    cachedWidth_=width_;
    cachedSigma_=sigma_;
  }

  if(std::abs(x_-mean_)<approxWidth_*3){
    //  std::cout <<"returning actual value "<<std::endl;
    return voigtian_();
  }else{
    //   std::cout <<"returning zero "<<std::endl;
    return 0;
  }
  // ENTER EXPRESSION IN TERMS OF VARIABLE ARGUMENTS HERE 
  //   return exp(mass*bkg_a+mass*mass*bkg_b)*pow(mass,bkg_c)*(bkg_syst_a+bkg_syst_a*mass) ; 
} 

//stolen from RooVoigtian
Double_t ZPrimeVoigtian::voigtian_()const
{
  Double_t s = (sigma_>0) ? sigma_ : -sigma_ ;
  Double_t w = (width_>0) ? width_ : -width_ ;

  Double_t coef= -0.5/(s*s);
  Double_t arg = x_ - mean_;

  // return constant for zero width and sigma
  if (s==0. && w==0.) return 1.;

  // Breit-Wigner for zero sigma
  if (s==0.) return (1./(arg*arg+0.25*w*w));

  // Gauss for zero width
  if (w==0.) return exp(coef*arg*arg);

  // actual Voigtian for non-trivial width and sigma
  Double_t c = 1./(sqrt(2.)*s);
  Double_t a = 0.5*c*w;
  Double_t u = c*arg;
  std::complex<Double_t> z(u,a) ;
  std::complex<Double_t> v(0.) ;

  if (doFast_) {
    v = RooMath::faddeeva_fast(z);
  } else {
    v = RooMath::faddeeva(z);
  }
  return c*kInvRootPi_*v.real();
}
