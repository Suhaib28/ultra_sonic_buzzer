# Import necessary libraries
import RPi.GPIO as GPIO
import time

# Define GPIO pins
TRIG_PIN = 17  # Trig pin of the Ultrasonic Sensor
ECHO_PIN = 18  # Echo pin of the Ultrasonic Sensor
BUZZER_PIN = 22  # Pin for the Buzzer
KILL_SWITCH_PIN = 23  # Pin for the Kill Switch Button

# Set GPIO mode and warnings
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Set up Ultrasonic Sensor GPIO
GPIO.setup(TRIG_PIN, GPIO.OUT)
GPIO.setup(ECHO_PIN, GPIO.IN)

# Set up Buzzer GPIO
GPIO.setup(BUZZER_PIN, GPIO.OUT)

# Set up Kill Switch GPIO
GPIO.setup(KILL_SWITCH_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def measure_distance():
    # Trigger the Ultrasonic Sensor to send a pulse
    GPIO.output(TRIG_PIN, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(TRIG_PIN, GPIO.LOW)

    # Measure the time taken for the pulse to return
    while GPIO.input(ECHO_PIN) == 0:
        pulse_start_time = time.time()

    while GPIO.input(ECHO_PIN) == 1:
        pulse_end_time = time.time()

    # Calculate the distance based on the pulse duration
    pulse_duration = pulse_end_time - pulse_start_time
    distance = pulse_duration * 17150
    distance = round(distance, 2)

    return distance

def buzz_for_distance(distance):
    if distance < 30:  # Adjust this threshold as needed
        GPIO.output(BUZZER_PIN, GPIO.HIGH)
    else:
        GPIO.output(BUZZER_PIN, GPIO.LOW)

def is_kill_switch_pressed():
    return GPIO.input(KILL_SWITCH_PIN) == GPIO.LOW

try:
    while True:
        # Check if the kill switch is pressed
        if is_kill_switch_pressed():
            print("Kill switch pressed. Exiting.")
            break

        # Measure distance from Ultrasonic Sensor
        distance = measure_distance()
        print(f"Distance: {distance} cm")

        # Activate buzzer based on distance
        buzz_for_distance(distance)

        # Wait for 1 second
        time.sleep(1)

except KeyboardInterrupt:
    # Handle keyboard interrupt (Ctrl+C)
    print("Cleaning up GPIO on exit.")

finally:
    # Clean up GPIO on exit
    GPIO.cleanup()
