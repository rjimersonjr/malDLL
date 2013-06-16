#ifdef DLL_EXPORT

#else

#define DLL_EXPORT extern "C" __declspec(dllexport) helloWorld();

#endif

DLL_EXPORT void helloWorld();