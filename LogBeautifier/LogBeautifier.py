import re
from datetime import datetime
from collections import defaultdict

def parse_log_file(file_path):
    # Regular expression patterns
    pattern_sender = re.compile(r'\(Team #\d+\) (\w+) sent (.+?) to (\w+)')
    pattern_time = re.compile(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}')

    # Dictionary to store sender-receiver pairs and their items with timestamps
    sender_receiver_items = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))

    with open(file_path, 'r') as file:
        for line in file:
            # Extract sender, receiver, and item sent from the line
            match_sender = pattern_sender.search(line)
            match_time = pattern_time.search(line)

            if match_sender and match_time:
                sender = match_sender.group(1)
                receiver = match_sender.group(3)
                item = match_sender.group(2)
                time = match_time.group()

                # Store item and its timestamp
                sender_receiver_items[sender][receiver][item].append(time)

    return sender_receiver_items

def print_sender_receiver_pairs(sender_receiver_items, output_file):
    # Print sender-receiver pairs organized by sender
    with open(output_file, 'w') as f:
        f.write("# All Current Sends As Of " + str(datetime.now()) + "\n\n")
        max_length = 0
        for sender, receiver_items in sender_receiver_items.items():
            for receiver, items_time in receiver_items.items():
                # Find the maximum length of item names and counts
                max_length = max(max_length, max(len(item) + len(f"(x{len(timestamps)})") for item, timestamps in items_time.items()))
        
        for sender, receiver_items in sender_receiver_items.items():
            f.write(f"## {sender} sends to:\n")
            f.write("---------------------\n")
            for receiver, items_time in receiver_items.items():
                f.write(f"### {receiver}:\n")
                # Sort items based on their timestamps
                sorted_items = sorted(items_time.items(), key=lambda x: max(x[1]))
                for item, timestamps in sorted_items:
                    recent_time = max(timestamps)
                    count = len(timestamps)
                    # Pad the item name and count with spaces to ensure alignment
                    padded_item = (f"{item} (x{count})\n")
                    # f.write(f"{padded_item} - {recent_time}\n")
                f.write("\n")








def main():
    input_file = 'log_file.txt'  # Update with your log file path
    output_file = 'output.txt'    # Update with your desired output file path
    sender_receiver_items = parse_log_file(input_file)
    print_sender_receiver_pairs(sender_receiver_items, output_file)

if __name__ == "__main__":
    main()
