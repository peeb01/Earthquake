import tensorflow as tf

if tf.test.is_gpu_available():
    print("GPU is available")
    gpu_devices = tf.config.experimental.list_physical_devices('GPU')
    for device in gpu_devices:
        print("Name:", device.name)
        # print("Memory limit:", tf.config.experimental.get_memory_limit(device))
else:
    print("GPU is not available, running on CPU")
