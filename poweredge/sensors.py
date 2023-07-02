import sensors

#%%
sensors.init()
try:
    for chip in sensors.iter_detected_chips():
        print('%s at %s' % (chip, chip.adapter_name))
        for feature in chip:
            print('  %s: %.2f' % (feature.label, feature.get_value()))
finally:
    sensors.cleanup()

#%%
def get_all_sensors() -> [float]:
    all_sensors_value = []
    sensors.init()
    try:
        for chip in sensors.iter_detected_chips():
            for feature in chip:
                all_sensors_value.append(feature.get_value())
    finally:
        sensors.cleanup()
    return all_sensors_value