///////////////////////////////////////////////////////////////
//
// A simple pol3 hardcoded. I am aware of RooPolyVar, however I
// cant get it to work with the rooworkspace config langauge
// If the rooworkspace config langauge was documented, well I probably could have
// 
// Author: A bitter coder who really dislikes roofit, particularly the appalling lack of
//         documenation and is fantasising about the day he gets rid of it from his life


#ifndef POL3_H
#define POL3_H

#include "RooAbsReal.h"
#include "RooRealProxy.h"
#include "RooCategoryProxy.h"
#include "RooAbsReal.h"
#include "RooAbsCategory.h"
 
class Pol3 : public RooAbsReal {
public:
  Pol3() {} ; 
  Pol3(const char *name, const char *title,
       RooAbsReal& x,RooAbsReal& p0,RooAbsReal& p1,RooAbsReal& p2,
       RooAbsReal& p3);
  Pol3(const Pol3& other, const char* name=0) ;
  virtual TObject* clone(const char* newname) const { return new Pol3(*this,newname); }
  inline virtual ~Pol3() { }

protected:

  RooRealProxy x_;
  RooRealProxy p0_,p1_,p2_,p3_;

  Double_t evaluate() const ;

private:

  ClassDef(Pol3,1) // Your description goes here...
};
 
#endif
