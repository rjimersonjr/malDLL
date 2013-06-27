#ifdef DLL_EXPORT

#define DLL_EXPORT extern "C" __declspec(dllexport)

#else

#endif

DLL_EXPORT void helloWorld();