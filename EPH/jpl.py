from jplephem.spk import SPK

# Load the SPK kernel file
kernel_file = 'de430t.bsp'
kernel = SPK.open(kernel_file)
print(kernel)

