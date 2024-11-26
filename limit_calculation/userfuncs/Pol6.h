///////////////////////////////////////////////////////////////
//
// A simple pol6 hardcoded. I am aware of RooPolyVar, however I
// cant get it to work with the rooworkspace config langauge
// If the rooworkspace config langauge was documented, well I probably could have
// 
// Author: A bitter coder who really dislikes roofit, particularly the appalling lack of
//         documenation and is fantasising about the day he gets rid of it from his life


#ifndef POL6_H
#define POL6_H

#include "RooAbsReal.h"
#include "RooRealProxy.h"
#include "RooCategoryProxy.h"
#include "RooAbsReal.h"
#include "RooAbsCategory.h"
 
class Pol6 : public RooAbsReal {
public:
  Pol6() {} ; 
  Pol6(const char *name, const char *title,
       RooAbsReal& x,RooAbsReal& p0,RooAbsReal& p1,RooAbsReal& p2,
       RooAbsReal& p3,RooAbsReal& p4,RooAbsReal& p5,RooAbsReal& p6);
  Pol6(const Pol6& other, const char* name=0) ;
  virtual TObject* clone(const char* newname) const { return new Pol6(*this,newname); }
  inline virtual ~Pol6() { }

protected:

  RooRealProxy x_;
  RooRealProxy p0_,p1_,p2_,p3_,p4_,p5_,p6_;

  Double_t evaluate() const ;

private:

  ClassDef(Pol6,1) // Your description goes here...
};
 
#endif
