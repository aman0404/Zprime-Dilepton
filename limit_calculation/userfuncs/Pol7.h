///////////////////////////////////////////////////////////////
//
// A simple pol6 hardcoded. I am aware of RooPolyVar, however I
// cant get it to work with the rooworkspace config langauge
// If the rooworkspace config langauge was documented, well I probably could have
// 
// Author: A bitter coder who really dislikes roofit, particularly the appalling lack of
//         documenation and is fantasising about the day he gets rid of it from his life


#ifndef POL7_H
#define POL7_H

#include "RooAbsReal.h"
#include "RooRealProxy.h"
#include "RooCategoryProxy.h"
#include "RooAbsReal.h"
#include "RooAbsCategory.h"
 
class Pol7 : public RooAbsReal {
public:
  Pol7() {} ; 
  Pol7(const char *name, const char *title,
       RooAbsReal& x,RooAbsReal& p0,RooAbsReal& p1,RooAbsReal& p2,
       RooAbsReal& p3,RooAbsReal& p4,RooAbsReal& p5,RooAbsReal& p6,
       RooAbsReal& p7);
  Pol7(const Pol7& other, const char* name=0) ;
  virtual TObject* clone(const char* newname) const { return new Pol7(*this,newname); }
  inline virtual ~Pol7() { }

protected:

  RooRealProxy x_;
  RooRealProxy p0_,p1_,p2_,p3_,p4_,p5_,p6_,p7_;

  Double_t evaluate() const ;

private:

  ClassDef(Pol7,1) // Your description goes here...
};
 
#endif
