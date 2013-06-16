// hookDLL.cpp : Defines the exported functions for the DLL application.
//

#include "stdafx.h"
#include "hookDLL.h"

using namespace std;


namespace hookDLLFuncs
{
	void daDLLFuncs::helloWorld()
    {
		MessageBox( NULL, TEXT("Hello World"), 
			TEXT("In a DLL"), MB_OK);
    }
}

BOOL APIENTRY DllMain( HANDLE hModule,
                        DWORD  ul_reason_for_call,
                        LPVOID lpReserved )
{
	hookDLLFuncs::daDLLFuncs::helloWorld();
	MessageBox( NULL, TEXT("Hello World"), 
			TEXT("In a DLL"), MB_OK);
    return TRUE;
}

