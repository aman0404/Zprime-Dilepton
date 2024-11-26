// Do NOT change. Changes will be lost next time file is generated

#define R__DICTIONARY_FILENAME dIdepotdIcmsdIprivatedIusersdIkaur214dIanalysis_facilitydIlimitsdIdestructivedIZPrimeCombinedIdOdIuserfuncsdIZPrimeVoigtian_cxx_ACLiC_dict
#define R__NO_DEPRECATION

/*******************************************************************/
#include <stddef.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <assert.h>
#define G__DICTIONARY
#include "ROOT/RConfig.hxx"
#include "TClass.h"
#include "TDictAttributeMap.h"
#include "TInterpreter.h"
#include "TROOT.h"
#include "TBuffer.h"
#include "TMemberInspector.h"
#include "TInterpreter.h"
#include "TVirtualMutex.h"
#include "TError.h"

#ifndef G__ROOT
#define G__ROOT
#endif

#include "RtypesImp.h"
#include "TIsAProxy.h"
#include "TFileMergeInfo.h"
#include <algorithm>
#include "TCollectionProxyInfo.h"
/*******************************************************************/

#include "TDataMember.h"

// The generated code does not explicitly qualify STL entities
namespace std {} using namespace std;

// Header files passed as explicit arguments
#include "/depot/cms/private/users/kaur214/analysis_facility/limits/destructive/ZPrimeCombine/./userfuncs/ZPrimeVoigtian.cxx"

// Header files passed via #pragma extra_include

   namespace ROOTDict {
      inline ::ROOT::TGenericClassInfo *GenerateInitInstance();
      static TClass *ROOT_Dictionary();

      // Function generating the singleton type initializer
      inline ::ROOT::TGenericClassInfo *GenerateInitInstance()
      {
         static ::ROOT::TGenericClassInfo 
            instance("ROOT", 0 /*version*/, "Rtypes.h", 105,
                     ::ROOT::Internal::DefineBehavior((void*)nullptr,(void*)nullptr),
                     &ROOT_Dictionary, 0);
         return &instance;
      }
      // Insure that the inline function is _not_ optimized away by the compiler
      ::ROOT::TGenericClassInfo *(*_R__UNIQUE_DICT_(InitFunctionKeeper))() = &GenerateInitInstance;  
      // Static variable to force the class initialization
      static ::ROOT::TGenericClassInfo *_R__UNIQUE_DICT_(Init) = GenerateInitInstance(); R__UseDummy(_R__UNIQUE_DICT_(Init));

      // Dictionary for non-ClassDef classes
      static TClass *ROOT_Dictionary() {
         return GenerateInitInstance()->GetClass();
      }

   }

namespace ROOT {
   static void *new_ZPrimeVoigtian(void *p = nullptr);
   static void *newArray_ZPrimeVoigtian(Long_t size, void *p);
   static void delete_ZPrimeVoigtian(void *p);
   static void deleteArray_ZPrimeVoigtian(void *p);
   static void destruct_ZPrimeVoigtian(void *p);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const ::ZPrimeVoigtian*)
   {
      ::ZPrimeVoigtian *ptr = nullptr;
      static ::TVirtualIsAProxy* isa_proxy = new ::TInstrumentedIsAProxy< ::ZPrimeVoigtian >(nullptr);
      static ::ROOT::TGenericClassInfo 
         instance("ZPrimeVoigtian", ::ZPrimeVoigtian::Class_Version(), "userfuncs/ZPrimeVoigtian.h", 17,
                  typeid(::ZPrimeVoigtian), ::ROOT::Internal::DefineBehavior(ptr, ptr),
                  &::ZPrimeVoigtian::Dictionary, isa_proxy, 4,
                  sizeof(::ZPrimeVoigtian) );
      instance.SetNew(&new_ZPrimeVoigtian);
      instance.SetNewArray(&newArray_ZPrimeVoigtian);
      instance.SetDelete(&delete_ZPrimeVoigtian);
      instance.SetDeleteArray(&deleteArray_ZPrimeVoigtian);
      instance.SetDestructor(&destruct_ZPrimeVoigtian);
      return &instance;
   }
   TGenericClassInfo *GenerateInitInstance(const ::ZPrimeVoigtian*)
   {
      return GenerateInitInstanceLocal(static_cast<::ZPrimeVoigtian*>(nullptr));
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_DICT_(Init) = GenerateInitInstanceLocal(static_cast<const ::ZPrimeVoigtian*>(nullptr)); R__UseDummy(_R__UNIQUE_DICT_(Init));
} // end of namespace ROOT

//______________________________________________________________________________
atomic_TClass_ptr ZPrimeVoigtian::fgIsA(nullptr);  // static to hold class pointer

//______________________________________________________________________________
const char *ZPrimeVoigtian::Class_Name()
{
   return "ZPrimeVoigtian";
}

//______________________________________________________________________________
const char *ZPrimeVoigtian::ImplFileName()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::ZPrimeVoigtian*)nullptr)->GetImplFileName();
}

//______________________________________________________________________________
int ZPrimeVoigtian::ImplFileLine()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::ZPrimeVoigtian*)nullptr)->GetImplFileLine();
}

//______________________________________________________________________________
TClass *ZPrimeVoigtian::Dictionary()
{
   fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::ZPrimeVoigtian*)nullptr)->GetClass();
   return fgIsA;
}

//______________________________________________________________________________
TClass *ZPrimeVoigtian::Class()
{
   if (!fgIsA.load()) { R__LOCKGUARD(gInterpreterMutex); fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::ZPrimeVoigtian*)nullptr)->GetClass(); }
   return fgIsA;
}

//______________________________________________________________________________
void ZPrimeVoigtian::Streamer(TBuffer &R__b)
{
   // Stream an object of class ZPrimeVoigtian.

   if (R__b.IsReading()) {
      R__b.ReadClassBuffer(ZPrimeVoigtian::Class(),this);
   } else {
      R__b.WriteClassBuffer(ZPrimeVoigtian::Class(),this);
   }
}

namespace ROOT {
   // Wrappers around operator new
   static void *new_ZPrimeVoigtian(void *p) {
      return  p ? new(p) ::ZPrimeVoigtian : new ::ZPrimeVoigtian;
   }
   static void *newArray_ZPrimeVoigtian(Long_t nElements, void *p) {
      return p ? new(p) ::ZPrimeVoigtian[nElements] : new ::ZPrimeVoigtian[nElements];
   }
   // Wrapper around operator delete
   static void delete_ZPrimeVoigtian(void *p) {
      delete (static_cast<::ZPrimeVoigtian*>(p));
   }
   static void deleteArray_ZPrimeVoigtian(void *p) {
      delete [] (static_cast<::ZPrimeVoigtian*>(p));
   }
   static void destruct_ZPrimeVoigtian(void *p) {
      typedef ::ZPrimeVoigtian current_t;
      (static_cast<current_t*>(p))->~current_t();
   }
} // end of namespace ROOT for class ::ZPrimeVoigtian

namespace {
  void TriggerDictionaryInitialization_ZPrimeVoigtian_cxx_ACLiC_dict_Impl() {
    static const char* headers[] = {
"./userfuncs/ZPrimeVoigtian.cxx",
nullptr
    };
    static const char* includePaths[] = {
"/cvmfs/cms.cern.ch/el8_amd64_gcc12/lcg/root/6.30.07-f3322c77db1c59847b28fde88ff7218c/include",
"/depot/cms/private/users/kaur214/analysis_facility/limits/CMSSW_14_1_0_pre4/src",
"/cvmfs/cms.cern.ch/el8_amd64_gcc12/cms/cmssw/CMSSW_14_1_0_pre4/src",
"/cvmfs/cms.cern.ch/el8_amd64_gcc12/external/mctester/1.25.1-2fcdeefaec2f0c91bf65cfbf4d89dadc/include",
"/cvmfs/cms.cern.ch/el8_amd64_gcc12/external/hydjet2/2.4.3-37cb95718b65e4928b22902a845e82cf/include",
"/cvmfs/cms.cern.ch/el8_amd64_gcc12/external/dd4hep/v01-27-02-02d087b69a43429d82df59691bcd25e1/include",
"/cvmfs/cms.cern.ch/el8_amd64_gcc12/external/herwig7/7.2.2-214991300ba2c3596da336fd4401a8d9/include",
"/cvmfs/cms.cern.ch/el8_amd64_gcc12/external/tauolapp/1.1.8-87030bef0479a94c767ea13e600a476a/include",
"/cvmfs/cms.cern.ch/el8_amd64_gcc12/external/sherpa/2.2.15-c6a37612b412ad054a2c0c3c94105148/include/SHERPA-MC",
"/cvmfs/cms.cern.ch/el8_amd64_gcc12/external/lwtnn/2.14.1-6e70bd3a592a51fa96b06dd00fb0731e/include",
"/cvmfs/cms.cern.ch/el8_amd64_gcc12/external/thepeg/2.2.2-336c6a65a796f7a002e313fd2ec581bb/include",
"/cvmfs/cms.cern.ch/el8_amd64_gcc12/external/pythia8/311-841eacade319844ed6037d86b277629d/include",
"/cvmfs/cms.cern.ch/el8_amd64_gcc12/external/starlight/r193-3fa3153dcf9eaaf0d348e1b94ac08278/include",
"/cvmfs/cms.cern.ch/el8_amd64_gcc12/external/rivet/3.1.10-ee0890ec63db8f97a4bda61332b6a504/include",
"/cvmfs/cms.cern.ch/el8_amd64_gcc12/external/highfive/2.3.1-1c1e7ed74edc1757d49008526375283e/include",
"/cvmfs/cms.cern.ch/el8_amd64_gcc12/external/classlib/3.1.3-c6b100380ee001a2bc06975bb0682ffc/include",
"/cvmfs/cms.cern.ch/el8_amd64_gcc12/external/lhapdf/6.4.0-c15316a5db16cd41771a31339f71f600/include",
"/cvmfs/cms.cern.ch/el8_amd64_gcc12/external/geant4/11.2.1-f5ff70520bace30da535387a4ade176a/include",
"/cvmfs/cms.cern.ch/el8_amd64_gcc12/external/alpaka/1.1.0-ce4f30846faf06a7d6a55bcbbdbdd692/include",
"/cvmfs/cms.cern.ch/el8_amd64_gcc12/external/tkonlinesw/4.2.0-1_gcc7-83ea6dc57c1be7aca1985ffd916360de/include",
"/cvmfs/cms.cern.ch/el8_amd64_gcc12/external/pcre2/10.36-c75e887aa283481338a9a2e3cf0b953b/include",
"/cvmfs/cms.cern.ch/el8_amd64_gcc12/external/libungif/4.1.4-2f91a77bad1564f8547f5d13089fd857/include",
"/cvmfs/cms.cern.ch/el8_amd64_gcc12/external/libtiff/4.0.10-05e1ed300245d194ffbf0cbab668dfc6/include",
"/cvmfs/cms.cern.ch/el8_amd64_gcc12/external/libpng/1.6.37-e9fc63ee14d46b2aa66f88196e69e632/include",
"/cvmfs/cms.cern.ch/el8_amd64_gcc12/external/frontier_client/2.10.2-b9c2ccb38a900b44980655b68caf322e/include",
"/cvmfs/cms.cern.ch/el8_amd64_gcc12/external/pcre/8.43-e34796d17981e9b6d174328c69446455/include",
"/cvmfs/cms.cern.ch/el8_amd64_gcc12/external/zstd/1.5.2-9fdadfca3fb3629e62141e0b4e73e88d/include",
"/cvmfs/cms.cern.ch/el8_amd64_gcc12/external/xrootd/5.6.4-c96abedad1d9a60afa8be5b8db899b7b/include/xrootd/private",
"/cvmfs/cms.cern.ch/el8_amd64_gcc12/cms/vdt/0.4.3-f094bee80112624813c07f9336e08d7d/include",
"/cvmfs/cms.cern.ch/el8_amd64_gcc12/external/valgrind/3.23.0-143b83b3001a13f5bb2e0a4b5445fed5/include",
"/cvmfs/cms.cern.ch/el8_amd64_gcc12/external/utm/utm_0.12.0-6115812266ed2b30df17905175e1504a/include",
"/cvmfs/cms.cern.ch/el8_amd64_gcc12/external/sigcpp/3.2.0-1d8286563e3e21dce7bc52c496afc741/include/sigc++-3.0",
"/cvmfs/cms.cern.ch/el8_amd64_gcc12/external/sqlite/3.36.0-49157ebb9a846c99702be39683b0c263/include",
"/cvmfs/cms.cern.ch/el8_amd64_gcc12/external/rocm-rocrand/5.6.1-caf9f8c4534379b939a7fd135ee2f33c/include",
"/cvmfs/cms.cern.ch/el8_amd64_gcc12/external/pacparser/1.4.2-ad128e68130905857de87f876df4b792/include",
"/cvmfs/cms.cern.ch/el8_amd64_gcc12/external/oracle/19.11.0.0.0dbru-0ef9ee763c1e7a90d8c4515a5af97f0b/include",
"/cvmfs/cms.cern.ch/el8_amd64_gcc12/external/py3-numpy/1.24.3-0831476b9e4ddf0b4b9eb1f4c971c0d1/c-api/core/include",
"/cvmfs/cms.cern.ch/el8_amd64_gcc12/external/meschach/1.2.pCMS1-79435924678a8cc522f783c34e3865d7/include",
"/cvmfs/cms.cern.ch/el8_amd64_gcc12/external/lz4/1.9.2-e478fcd3e5e191d5bb4ade190474ad76/include",
"/cvmfs/cms.cern.ch/el8_amd64_gcc12/external/libuuid/2.34-27ce4c3579b5b1de2808ea9c4cd8ed29/include",
"/cvmfs/cms.cern.ch/el8_amd64_gcc12/external/libjpeg-turbo/2.0.2-b7b44f7f3d9310741bc23d7bc9f3e81f/include",
"/cvmfs/cms.cern.ch/el8_amd64_gcc12/external/ktjet/1.06-b87eb64a2bfce12c09130173c1645f36/include",
"/cvmfs/cms.cern.ch/el8_amd64_gcc12/external/jemalloc-prof/5.3.0-de80d9859135ad1ade5c1011acaeae4d/include",
"/cvmfs/cms.cern.ch/el8_amd64_gcc12/external/jemalloc-debug/5.3.0-26b8c2b1e630fea06966ad7f86d7fdf7/include",
"/cvmfs/cms.cern.ch/el8_amd64_gcc12/external/jemalloc/5.3.0-3416db0688377af1e4ae62ddc3410095/include",
"/cvmfs/cms.cern.ch/el8_amd64_gcc12/external/hls/2019.08-0e37f055a3ed22611ce5edecb14d0695/include",
"/cvmfs/cms.cern.ch/el8_amd64_gcc12/external/madgraph5amcatnlo/2.7.3-0a0beebae1cbe0902aa3f24b74160b35",
"/cvmfs/cms.cern.ch/el8_amd64_gcc12/external/heppdt/3.04.01-be15943ae2c3c55c5e983061c677052a/include",
"/cvmfs/cms.cern.ch/el8_amd64_gcc12/external/hector/1.3.4_patch1-455a9b1a4983dc8bc3c980eb75a1fb9e/include",
"/cvmfs/cms.cern.ch/el8_amd64_gcc12/external/protobuf/3.21.9-437f2f0c4a1cda63055784b1b4a72f71/include",
"/cvmfs/cms.cern.ch/el8_amd64_gcc12/external/libunwind/1.7.2-master-32c4640dfefb080c36ce8baa32511c29/include",
"/cvmfs/cms.cern.ch/el8_amd64_gcc12/external/giflib/5.2.0-07dfc72586a7288f078c7a02c8b17956/include",
"/cvmfs/cms.cern.ch/el8_amd64_gcc12/external/gdbm/1.10-1f0ec10a142f21150eef9d32ba579779/include",
"/cvmfs/cms.cern.ch/el8_amd64_gcc12/external/freetype/2.10.0-d5befe02435f3900b575ad514e42ac03/include",
"/cvmfs/cms.cern.ch/el8_amd64_gcc12/external/fftw3/3.3.8-5270bdf9998065b38f91e9aa053c73ec/include",
"/cvmfs/cms.cern.ch/el8_amd64_gcc12/external/fftjet/1.5.0-4c95f831c41530ec8fa31a87717d9e5b/include",
"/cvmfs/cms.cern.ch/el8_amd64_gcc12/external/fastjet/3.4.1-4b7559ffa850ea1b7be2d4a6d8178d84/include",
"/cvmfs/cms.cern.ch/el8_amd64_gcc12/external/xz/5.2.5-6f3f49b07db84e10c9be594a1176c114/include",
"/cvmfs/cms.cern.ch/el8_amd64_gcc12/lcg/root/6.30.07-f3322c77db1c59847b28fde88ff7218c/include",
"/cvmfs/cms.cern.ch/el8_amd64_gcc12/external/dcap/2.47.12-f1879e653657391134d112378033b486/include",
"/cvmfs/cms.cern.ch/el8_amd64_gcc12/external/libxml2/2.9.10-9aa207cb112032fd940a4dfd85504c15/include/libxml2",
"/cvmfs/cms.cern.ch/el8_amd64_gcc12/external/curl/7.79.0-e9aea8dd47e409f0dcfd76a7b3220112/include",
"/cvmfs/cms.cern.ch/el8_amd64_gcc12/external/cppunit/1.15.x-fb84a4bbf5a436317d208e3ef0864e91/include",
"/cvmfs/cms.cern.ch/el8_amd64_gcc12/cms/coral/CORAL_2_3_21-27ab7e52f21297bcbeaa636ca097acc7/include/LCG",
"/cvmfs/cms.cern.ch/el8_amd64_gcc12/external/pythia6/426-c430ea6f2967f65248af15c71e6c653e/include",
"/cvmfs/cms.cern.ch/el8_amd64_gcc12/external/hepmc/2.06.10-cb64022df5945e7e8948ec2000290943/include",
"/cvmfs/cms.cern.ch/el8_amd64_gcc12/external/gsl/2.6-5e2ce72ea2977ff21a2344bbb52daf5c/include",
"/cvmfs/cms.cern.ch/el8_amd64_gcc12/external/xerces-c/3.1.3-c7b88eaa36d0408120f3c29826a04bf6/include",
"/cvmfs/cms.cern.ch/el8_amd64_gcc12/external/expat/2.4.8-b093687a482bf386f8f8c236c5b2efa2/include",
"/cvmfs/cms.cern.ch/el8_amd64_gcc12/external/zlib/1.2.11-1a082fc322b0051b504cc023f21df178/include",
"/cvmfs/cms.cern.ch/el8_amd64_gcc12/external/clhep/2.4.7.1-8e40efd27b7394c1fa4e9c7e432d85cd/include",
"/cvmfs/cms.cern.ch/el8_amd64_gcc12/external/vecgeom/v1.2.7-a835f26582a68cd5d06d2fea9585a5f5/include",
"/cvmfs/cms.cern.ch/el8_amd64_gcc12/external/vecgeom/v1.2.7-a835f26582a68cd5d06d2fea9585a5f5/include/VecGeom",
"/cvmfs/cms.cern.ch/el8_amd64_gcc12/external/bz2lib/1.0.6-d065ccd79984efc6d4660f410e4c81de/include",
"/cvmfs/cms.cern.ch/el8_amd64_gcc12/external/tbb/v2021.9.0-a7089dd5ec356e9a0bc222e109b15cef/include",
"/cvmfs/cms.cern.ch/el8_amd64_gcc12/external/cuda/12.4.1-fc5cb0e72dba64b6abbf00089f3a044c/include",
"/cvmfs/cms.cern.ch/el8_amd64_gcc12/external/boost/1.80.0-941b136a4a3be6f8bc1e903d36ddc172/include",
"/cvmfs/cms.cern.ch/el8_amd64_gcc12/external/xgboost/1.7.5-d0dc099a6916fd0fc90fc77ce3b14aea/include",
"/cvmfs/cms.cern.ch/el8_amd64_gcc12/external/tinyxml2/6.2.0-88fe0ec301baf763fa3c485e5b67ed91/include",
"/cvmfs/cms.cern.ch/el8_amd64_gcc12/external/rdma-core/50.0-c5f6da04850268e223ce3665b69d022e/include",
"/cvmfs/cms.cern.ch/el8_amd64_gcc12/external/ittnotify/16.06.18-e7bdf646a1ce643ba6ad35661112659a/include",
"/cvmfs/cms.cern.ch/el8_amd64_gcc12/external/gosamcontrib/2.0-20150803-3fd28e0213ceb2e9dc1eae1945774558/include",
"/cvmfs/cms.cern.ch/el8_amd64_gcc12/external/fmt/8.0.1-258b4791803c34b7e98cf43693e54d87/include",
"/cvmfs/cms.cern.ch/el8_amd64_gcc12/external/eigen/3bb6a48d8c171cf20b5f8e48bfb4e424fbd4f79e-3ca740c03e68b1a067f3ed0679234a78/include/eigen3",
"/cvmfs/cms.cern.ch/el8_amd64_gcc12/external/rocm/5.6.1-de54589aefe827587dc365bc864f87dc/include",
"/usr/local/include",
"/usr/include",
"/cvmfs/cms.cern.ch/el8_amd64_gcc12/lcg/root/6.30.07-f3322c77db1c59847b28fde88ff7218c/etc/",
"/cvmfs/cms.cern.ch/el8_amd64_gcc12/lcg/root/6.30.07-f3322c77db1c59847b28fde88ff7218c/etc//cling",
"/cvmfs/cms.cern.ch/el8_amd64_gcc12/lcg/root/6.30.07-f3322c77db1c59847b28fde88ff7218c/etc//cling/plugins/include",
"/cvmfs/cms.cern.ch/el8_amd64_gcc12/lcg/root/6.30.07-f3322c77db1c59847b28fde88ff7218c/include/",
"/cvmfs/cms.cern.ch/el8_amd64_gcc12/external/python3/3.9.14-c10287ae9cadff55334e60003302c349/include",
"/cvmfs/cms.cern.ch/el8_amd64_gcc12/external/python3/3.9.14-c10287ae9cadff55334e60003302c349/include/python3.9",
"/data/cmsbld/jenkins/workspace/ib-run-pr-tests/testBuildDir/BUILD/el8_amd64_gcc12/lcg/root/6.30.07-f3322c77db1c59847b28fde88ff7218c/build/include",
"/data/cmsbld/jenkins/workspace/ib-run-pr-tests/testBuildDir/el8_amd64_gcc12/external/zstd/1.5.2-9fdadfca3fb3629e62141e0b4e73e88d/include",
"/data/cmsbld/jenkins/workspace/ib-run-pr-tests/testBuildDir/el8_amd64_gcc12/external/xz/5.2.5-6f3f49b07db84e10c9be594a1176c114/include",
"/data/cmsbld/jenkins/workspace/ib-run-pr-tests/testBuildDir/el8_amd64_gcc12/external/tbb/v2021.9.0-a7089dd5ec356e9a0bc222e109b15cef/include",
"/data/cmsbld/jenkins/workspace/ib-run-pr-tests/testBuildDir/BUILD/el8_amd64_gcc12/lcg/root/6.30.07-f3322c77db1c59847b28fde88ff7218c/build/include/",
"/depot/cms/private/users/kaur214/analysis_facility/limits/destructive/ZPrimeCombine/",
"/cvmfs/cms.cern.ch/el8_amd64_gcc12/lcg/root/6.30.07-f3322c77db1c59847b28fde88ff7218c/include/",
"/depot/cms/private/users/kaur214/analysis_facility/limits/destructive/ZPrimeCombine/",
nullptr
    };
    static const char* fwdDeclCode = R"DICTFWDDCLS(
#line 1 "ZPrimeVoigtian_cxx_ACLiC_dict dictionary forward declarations' payload"
#pragma clang diagnostic ignored "-Wkeyword-compat"
#pragma clang diagnostic ignored "-Wignored-attributes"
#pragma clang diagnostic ignored "-Wreturn-type-c-linkage"
extern int __Cling_AutoLoading_Map;
class __attribute__((annotate("$clingAutoload$./userfuncs/ZPrimeVoigtian.cxx")))  ZPrimeVoigtian;
)DICTFWDDCLS";
    static const char* payloadCode = R"DICTPAYLOAD(
#line 1 "ZPrimeVoigtian_cxx_ACLiC_dict dictionary payload"

#ifndef __ACLIC__
  #define __ACLIC__ 1
#endif

#define _BACKWARD_BACKWARD_WARNING_H
// Inline headers
#include "./userfuncs/ZPrimeVoigtian.cxx"

#undef  _BACKWARD_BACKWARD_WARNING_H
)DICTPAYLOAD";
    static const char* classesHeaders[] = {
"", payloadCode, "@",
"ROOT::GenerateInitInstance", payloadCode, "@",
"ZPrimeVoigtian", payloadCode, "@",
"ZPrimeVoigtian::fgIsA", payloadCode, "@",
"ZPrimeVoigtian::kInvRootPi_", payloadCode, "@",
nullptr
};
    static bool isInitialized = false;
    if (!isInitialized) {
      TROOT::RegisterModule("ZPrimeVoigtian_cxx_ACLiC_dict",
        headers, includePaths, payloadCode, fwdDeclCode,
        TriggerDictionaryInitialization_ZPrimeVoigtian_cxx_ACLiC_dict_Impl, {}, classesHeaders, /*hasCxxModule*/false);
      isInitialized = true;
    }
  }
  static struct DictInit {
    DictInit() {
      TriggerDictionaryInitialization_ZPrimeVoigtian_cxx_ACLiC_dict_Impl();
    }
  } __TheDictionaryInitializer;
}
void TriggerDictionaryInitialization_ZPrimeVoigtian_cxx_ACLiC_dict() {
  TriggerDictionaryInitialization_ZPrimeVoigtian_cxx_ACLiC_dict_Impl();
}
