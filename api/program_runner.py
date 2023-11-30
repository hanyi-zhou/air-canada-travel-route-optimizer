import subprocess

def run_program_with_input(input_str):
    # Run the Python program using subprocess
    process = subprocess.Popen(["python", "process.py"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)

    # Write the input to the program's standard input
    process.stdin.write(input_str)
    process.stdin.close()

    # Read the standard output line by line
    output_lines = process.stdout.readlines()

    # Wait for the program to finish running
    process.wait()

    # Return the output as a list
    return [line.strip() for line in output_lines]

# 测试
input_str = "8 9\nVancouver\nYellowknife\nEdmonton\nCalgary\nWinnipeg\nToronto\nMontreal\nHalifax\nVancouver Edmonton\nVancouver Calgary\nCalgary Winnipeg\nWinnipeg Toronto\nToronto Halifax\nMontreal Halifax\nEdmonton Montreal\nEdmonton Yellowknife\nEdmonton Calgary\n"
result = run_program_with_input(input_str)
print(result)
