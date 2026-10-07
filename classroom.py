import pandas as pd


def next_temp(T, T_outside, hvac, occupancy, dt):
    k = 0.10
    alpha = 1.5
    beta = 0.02

    return T + dt * (k * (T_outside - T) + alpha * hvac + beta * occupancy)


data = pd.read_excel("data/classroom_data.xlsx")
print("Data loaded\n")
print(data)

#Initial classroom temperature
T = 20.0

#Time: 1 hour
dt = 1.0

print("With default data: \n")

for index, row in data.iloc[:-1].iterrows():
    T_outside = row["outside_temp"]
    occupancy = row["occupants"]
    hvac = row["hvac"]
    T = next_temp(T, T_outside, hvac, occupancy, dt)

print(f"Inside temperature at 18:00: {T:.2f} °C\n")

#Scenarios

#------------------------------------------------------------------------------

print("\nScenario 1: Outside temperature drops by 10 °C\n")
for index, row in data.iloc[:-1].iterrows():
    T_outside = row["outside_temp"] - 10
    occupancy = row["occupants"]
    hvac = row["hvac"]

    T = next_temp(T, T_outside, hvac, occupancy, dt)
print(f"Inside temperature at 18:00: {T:.2f} °C\n")

#------------------------------------------------------------------------------

print("\nScenario 2: The room has 50 students (constantly)\n")
T = 20.0
for index, row in data.iloc[:-1].iterrows():
    T_outside = row["outside_temp"]
    occupancy = 50.0
    hvac = row["hvac"]

    T = next_temp(T, T_outside, hvac, occupancy, dt)

print(f"Inside temperature at 18:00: {T:.2f} °C\n")

#------------------------------------------------------------------------------

print("\nScenario 3: The heating starts one hour earlier\n")
T = 20.0
first_row = data.iloc[0]
T = next_temp(T, first_row["outside_temp"], 1, 0, dt)

for index, row in data.iloc[:-1].iterrows():
    T_outside = row["outside_temp"]
    occupancy = row["occupants"]
    hvac = row["hvac"]

    T = next_temp(T, T_outside, hvac, occupancy, dt)

print(f"Inside temperature at 18:00: {T:.2f} °C\n")

#------------------------------------------------------------------------------

print("\nScenario 4: The controller uses a different set point\n")

def scenario_4(setpoint):
    T = 20.0
    for index, row in data.iloc[:-1].iterrows():
        T_outside = row["outside_temp"]
        occupancy = row["occupants"]
        hvac = row["hvac"]

        if T < setpoint:
            hvac = 1
        else:
            hvac = 0

        T = next_temp(T, T_outside, hvac, occupancy, dt)

    return T
print(f"Inside temperature at 18:00 with the setpoint set to 24 °C: {scenario_4(24):.2f}\n")
