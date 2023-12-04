import ctypes

# Load the DLL
example_lib = ctypes.CDLL('G:/project/c/CMAKE/out/build/x64-Debug/python_dll/python_dll.dll')  # Adjust the path as needed

# Call the C++ function
result = example_lib.add(2, 4)
print(result)
