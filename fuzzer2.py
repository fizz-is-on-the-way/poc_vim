import os
import string
import subprocess
import sys

def fuzz_test(input_data, num_tests, exe_cmd):
    exe_cmd.append("./seed")
    for i in range(num_tests):
        #test_data = ''.join(random.choices(string.ascii_letters + string.digits + string.punctuation, k=len(input_data)))
        data_len = int(os.urandom(1).encode('hex'), 16)
        data_len = data_len + 1
        test_data = os.urandom(data_len)
        with open('./seed', 'w') as f:
            f.write(test_data)
        
        process = subprocess.Popen(exe_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        
        if process.returncode != 0:
            print("Test {" + str(i) +"}: Program crashed with input: {" + test_data + "}")
        elif b"ERROR" in stderr:
            print("Test {" + str(i) +"}: Program returned an error with input: {" + test_data + "}")
        else:
            print("Test {" + str(i) +"}: Program ran successfully with input: {" + test_data + "}")

if __name__ == "__main__":
    input_data = "example_input_data"
    num_tests = 999
    args = sys.argv[1:]
    program_path = args[0]
    p_args = args[1]
    exe_cmd = []
    exe_cmd.append(program_path)
    exe_cmd.append(p_args)
    fuzz_test(input_data, num_tests, exe_cmd)