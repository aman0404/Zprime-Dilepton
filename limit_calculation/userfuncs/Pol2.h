///////////////////////////////////////////////////////////////
//
// A simple pol2 hardcoded. I am aware of RooPolyVar, however I
// cant get it to work with the rooworkspace config langauge
// If the rooworkspace config langauge was documented, well I probably could have
// 
// Author: A bitter coder who really dislikes roofit, particularly the appalling lack of
//         documenation and fantasising about the day he gets rid of it from his life


#ifndef POL2_H
#define POL2_H

#include "RooAbsReal.h"
#include "RooRealProxy.h"
#include "RooCategoryProxy.h"
#include "RooAbsReal.h"
#include "RooAbsCategory.h"
 
class Pol2 : public RooAbsReal {
public:
  Pol2() {} ; 
  Pol2(const char *name, const char *title,
       RooAbsReal& x,RooAbsReal& p0,RooAbsReal& p1,RooAbsReal& p2);
  Pol2(const Pol2& other, const char* name=0) ;
  virtual TObject* clone(const char* newname) const { return new Pol2(*this,newname); }
  inline virtual ~Pol2() { }

protected:

  RooRealProxy x_;
  RooRealProxy p0_,p1_,p2_;

  Double_t evaluate() const ;

private:

  ClassDef(Pol2,1) // Your description goes here...
};
 
#endif
