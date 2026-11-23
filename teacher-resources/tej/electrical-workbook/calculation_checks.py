"""Independent numerical checks for the electrical workbook answer keys."""

from math import isclose


def close(actual: float, expected: float, tolerance: float = 1e-9) -> None:
    assert isclose(actual, expected, rel_tol=tolerance, abs_tol=tolerance), (
        actual,
        expected,
    )


# Automotive relay model
source_v = 12.0
lamp_power_w = 21.0
lamp_current_a = lamp_power_w / source_v
coil_r_ohm = 80.0
coil_current_a = source_v / coil_r_ohm
coil_power_w = source_v * coil_current_a
state_b_terminal_30_a = 6.50
horn_current_a = state_b_terminal_30_a - lamp_current_a
horn_power_w = source_v * horn_current_a
total_battery_a = state_b_terminal_30_a + coil_current_a
total_battery_w = source_v * total_battery_a

close(lamp_current_a, 1.75)
close(coil_current_a, 0.150)
close(coil_power_w, 1.80)
close(horn_current_a, 4.75)
close(horn_power_w, 57.0)
close(total_battery_a, 6.65)
close(total_battery_w, 79.8)
close(lamp_power_w + horn_power_w + coil_power_w, total_battery_w)

# Poor-ground model
lamp_hot_r_ohm = source_v**2 / lamp_power_w
fault_r_ohm = 1.0
fault_current_a = source_v / (lamp_hot_r_ohm + fault_r_ohm)
lamp_voltage_v = fault_current_a * lamp_hot_r_ohm
fault_voltage_v = fault_current_a * fault_r_ohm
faulted_lamp_power_w = fault_current_a**2 * lamp_hot_r_ohm
fault_power_w = fault_current_a**2 * fault_r_ohm

close(lamp_hot_r_ohm, 6.857142857142857)
close(fault_current_a, 1.5272727272727273)
close(lamp_voltage_v, 10.472727272727273)
close(fault_voltage_v, 1.5272727272727273)
close(lamp_voltage_v + fault_voltage_v, source_v)
close(faulted_lamp_power_w, 15.994710743801653)
close(fault_power_w, 2.332561983471074)
close(faulted_lamp_power_w + fault_power_w, source_v * fault_current_a)

# Capacitor and sound estimates
student_c_f = 1000e-6
student_v = 5.0
stored_energy_j = 0.5 * student_c_f * student_v**2
buzzer_current_a = 0.012
buzzer_delta_v = 2.0
buzzer_time_s = student_c_f * buzzer_delta_v / buzzer_current_a
horn_current_assumption_a = 5.0
horn_time_s = 0.250
horn_delta_v = 4.0
horn_c_f = horn_current_assumption_a * horn_time_s / horn_delta_v
horn_energy_j = 0.5 * horn_c_f * source_v**2
capacitance_ratio = horn_c_f / student_c_f

close(stored_energy_j, 0.0125)
close(buzzer_time_s, 1 / 6)
close(horn_c_f, 0.3125)
close(horn_c_f * 1e6, 312_500.0)
close(horn_energy_j, 22.5)
close(capacitance_ratio, 312.5)

print("Electrical workbook calculation checks passed.")
print(f"Lamp current: {lamp_current_a:.3f} A")
print(f"Horn model: {horn_current_a:.3f} A, {horn_power_w:.1f} W")
print(f"Poor-ground model: {fault_current_a:.3f} A, {lamp_voltage_v:.2f} V lamp")
print(f"Horn capacitor estimate: {horn_c_f:.4f} F, {horn_energy_j:.1f} J")
