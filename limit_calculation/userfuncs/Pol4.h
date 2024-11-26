///////////////////////////////////////////////////////////////
//
// A simple pol4 hardcoded. I am aware of RooPolyVar, however I
// cant get it to work with the rooworkspace config langauge
// If the rooworkspace config langauge was documented, well I probably could have
// 
// Author: A bitter coder who really dislikes roofit, particularly the appalling lack of
//         documenation and is fantasising about the day he gets rid of it from his life


#ifndef POL4_H
#define POL4_H

#include "RooAbsReal.h"
#include "RooRealProxy.h"
#include "RooCategoryProxy.h"
#include "RooAbsReal.h"
#include "RooAbsCategory.h"
 
class Pol4 : public RooAbsReal {
public:
  Pol4() {} ; 
  Pol4(const char *name, const char *title,
       RooAbsReal& x,RooAbsReal& p0,RooAbsReal& p1,RooAbsReal& p2,
       RooAbsReal& p3,RooAbsReal& p4);
  Pol4(const Pol4& other, const char* name=0) ;
  virtual TObject* clone(const char* newname) const { return new Pol4(*this,newname); }
  inline virtual ~Pol4() { }

protected:

  RooRealProxy x_;
  RooRealProxy p0_,p1_,p2_,p3_,p4_;

  Double_t evaluate() const ;

private:

  ClassDef(Pol4,1) // Your description goes here...
};
 
#endif
