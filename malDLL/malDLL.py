import sys
from ctypes import *
from ctypes import wintypes

PAGE_READWRITE          =   0X04
PROCESS_ALL_ACCESS      =   ( 0x000F0000 | 0x00100000 | 0xFFF )
VIRTUAL_MEM             =   ( 0x1000 | 0x2000 )

kernel32 = windll.kernel32
kernel32.GetModuleHandleW.restype = wintypes.HMODULE
kernel32.GetModuleHandleW.argtypes = [wintypes.LPCWSTR]

pid = input("What is the PID of the process to inject the DLL to? ")
print("The pid that was just entered is: %s" % pid)
#pid     = sys.argv[1]
dll_path    = sys.argv[1]
dll_len     = len(dll_path)

print("The dll_path is: %s" % dll_path)
#print("The dll_len is: %s" % dll_len)


#Get a handle to the process we are injecting into
h_process = kernel32.OpenProcess( PROCESS_ALL_ACCESS, False, int(pid))
print("The handle to the process is: %s" % h_process)

if not h_process:
    print("[*] Couldn't get a handle to the process PID %s" % pid)
    sys.exit(0)

#Allocate some space for the DLL path
arg_address = kernel32.VirtualAllocEx(h_process, 0, dll_len, VIRTUAL_MEM, PAGE_READWRITE)
print ("[*] The address space allocated is: %s" % arg_address)

#Write the DLL path into the allocated space
written = c_int(0)
kernel32.WriteProcessMemory(h_process, arg_address, dll_path, dll_len, byref(written))

h_kernel32 = kernel32.GetModuleHandleW('kernel32.dll')

if h_kernel32 == False:
            error = GetLastError()
            print("ERROR with h_kernel32: %d - %s" % (error, FormatError(error)))
else:
            print("[*] The address for the kernel handle is %s" % hex(h_kernel32))

h_loadlib = windll.kernel32.GetProcAddress(h_kernel32, b"LoadLibraryW")

if h_loadlib == False:
            error = GetLastError()
            print("ERROR with h_loadlib: %d - %s" % (error, FormatError(error)))
else:
            print("[*] The address for the loadlibraryW handle is %s" % hex(h_loadlib))

#Now to try to create the remote thread
thread_id = c_ulong(0)

if not kernel32.CreateRemoteThread(h_process, None, 0, h_loadlib, arg_address, 0, byref(thread_id)):
    print ("[*] Failed to inject the DLL. Exiting.")

print("[*] Remote thread with ID 0x%08x created." % thread_id.value)

#Adding code to execute an exported function from the DLL
h_exportedFunc = windll.kernel32.GetProcAddress(h_loadlib, b"helloWorld")

if h_exportedFunc == False:
            error = GetLastError()
            print("ERROR with h_exportedFunc: %d - %s" % (error, FormatError(error)))
else:
            print("[*] The address for the helloWorld handle is %s" % hex(h_exportedFunc))