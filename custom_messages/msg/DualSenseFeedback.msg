std_msgs/Header header

# LED light bar (0-255)
uint8 led_r
uint8 led_g
uint8 led_b

# Vibration (0-255)
uint8 rumble_left
uint8 rumble_right

# Adaptive triggers (0=Off, 1=Rigid, 2=Pulse_A)
uint8 trigger_l_mode
uint8 trigger_l_force
uint8 trigger_r_mode
uint8 trigger_r_force
