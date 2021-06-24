import sys
from subprocess import run

import numpy as np
from tqdm import tqdm

if __name__ == '__main__':
    in_path = sys.argv[1]
    out_dir = sys.argv[2]
    result = run("wc -l < %s" % in_path, shell=True, capture_output=True)
    n_lines = int(result.stdout)
    fractions = np.array([0.96, 0.02, 0.02])

    train_size, dev_size, test_size = n_lines * fractions
    choice = np.random.choice(n_lines, int(dev_size + test_size), replace=False)
    arrays = np.split(choice, [int(dev_size)])
    dev_choice = arrays[0]
    test_choice = arrays[1]
    dev_choice.sort()
    test_choice.sort()

    train_file = open(out_dir + "/train.sl", "w")
    dev_file = open(out_dir + "/dev.sl", "w")
    test_file = open(out_dir + "/test.sl", "w")

    with open(in_path, encoding="ISO-8859-1") as f:
        current_line = 0
        dev_lines = np.nditer(dev_choice)
        test_lines = np.nditer(test_choice)
        for line in tqdm(f, desc="Split corpus into train, test, dev sets", total=n_lines):
            if (not dev_lines.finished) and current_line == dev_lines.value:
                dev_file.write(line)
                dev_lines.iternext()
            elif (not test_lines.finished) and current_line == test_lines.value:
                test_file.write(line)
                test_lines.iternext()
            else:
                train_file.write(line)
            current_line += 1

    train_file.close()
    dev_file.close()
    test_file.close()
