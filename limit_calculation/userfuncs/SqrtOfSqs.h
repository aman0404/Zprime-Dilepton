///////////////////////////////////////////////////////////////
//
// A simple function to add together two numbers in Quadrature 
// and return the square root of the result

#ifndef SQRTOFSQS_H
#define SQRTOFSQS_H

#include "RooAbsReal.h"
#include "RooRealProxy.h"
#include "RooCategoryProxy.h"
#include "RooAbsReal.h"
#include "RooAbsCategory.h"
 
class SqrtOfSqs : public RooAbsReal {
public:
  SqrtOfSqs() {} ; 
  SqrtOfSqs(const char *name, const char *title,
	    RooAbsReal& p0,RooAbsReal& p1);
  SqrtOfSqs(const SqrtOfSqs& other, const char* name=0) ;
  virtual TObject* clone(const char* newname) const { return new SqrtOfSqs(*this,newname); }
  inline virtual ~SqrtOfSqs() { }

protected:

  RooRealProxy p0_,p1_;

  Double_t evaluate() const ;

private:

  ClassDef(SqrtOfSqs,1) // Your description goes here...
};
 
#endif
