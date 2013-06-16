#include <windows.h>
#include <stdio.h>

#define DLL_EXPORT extern "C" __declspec(dllexport)

#include "dllToHook.h"

BOOL APIENTRY DllMain(HINSTANCE hInstance,
                     HINSTANCE hPrevInstance,
                     LPSTR     lpCmdLine
					 )
{ 	
	printf("Before the hello World call!");
	helloWorld();
	printf("This was printed from the inside the dll entry point!");
	return 0;
}

void helloWorld(){

	printf("Printed something to the command line!");
}