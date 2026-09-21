class DiskScheduling:

    @staticmethod
    def fcfs(requests, head):
        sequence = [head] + requests
        movement = sum(abs(sequence[i] - sequence[i - 1]) for i in range(1, len(sequence)))
        return sequence, movement

    @staticmethod
    def sstf(requests, head):
        requests = requests.copy()
        sequence = [head]
        movement = 0

        while requests:
            closest = min(requests, key=lambda x: abs(x - head))
            movement += abs(closest - head)
            head = closest
            sequence.append(head)
            requests.remove(closest)

        return sequence, movement

    @staticmethod
    def cscan(requests, head, disk_size=200):
        left = sorted([x for x in requests if x < head])
        right = sorted([x for x in requests if x >= head])

        sequence = [head]
        movement = 0

        for x in right:
            movement += abs(x - head)
            head = x
            sequence.append(x)

        if left:
            movement += abs((disk_size - 1) - head)
            head = disk_size - 1
            sequence.append(head)

            movement += disk_size - 1
            head = 0
            sequence.append(head)

            for x in left:
                movement += abs(x - head)
                head = x
                sequence.append(x)

        return sequence, movement

    @staticmethod
    def clook(requests, head):
        left = sorted([x for x in requests if x < head])
        right = sorted([x for x in requests if x >= head])

        sequence = [head]
        movement = 0

        for x in right:
            movement += abs(x - head)
            head = x
            sequence.append(x)

        if left:
            movement += abs(head - left[0])
            head = left[0]
            sequence.append(head)

            for x in left[1:]:
                movement += abs(x - head)
                head = x
                sequence.append(x)

        return sequence, movement

    @staticmethod
    def rss(requests, head):
        requests = requests.copy()
        sequence = [head]
        movement = 0

        while requests:
            closest = min(requests, key=lambda x: abs(x - head))

            movement += abs(closest - head)
            head = closest
            sequence.append(head)
            requests.remove(closest)

        return sequence, movement


class SimpleFileSystem:

    def __init__(self, total_blocks=50):
        self.total_blocks = total_blocks
        self.blocks = [None] * total_blocks
        self.directory = {}

    def create_file(self, filename, content):
        if filename in self.directory:
            print("\nFile already exists.")
            return

        required_blocks = max(1, (len(content) + 9) // 10)

        free_blocks = [
            i for i in range(self.total_blocks)
            if self.blocks[i] is None
        ]

        if len(free_blocks) < required_blocks:
            print("\nNot enough free blocks.")
            return

        allocated = free_blocks[:required_blocks]

        for block in allocated:
            self.blocks[block] = filename

        self.directory[filename] = {
            "content": content,
            "blocks": allocated
        }

        print("\nFile created successfully.")
        print("Allocated blocks:", allocated)

    def read_file(self, filename):
        if filename not in self.directory:
            print("\nFile not found.")
            return

        file_data = self.directory[filename]

        print("\nFile Name:", filename)
        print("Content:", file_data["content"])
        print("Blocks:", file_data["blocks"])

    def delete_file(self, filename):
        if filename not in self.directory:
            print("\nFile not found.")
            return

        blocks = self.directory[filename]["blocks"]

        for block in blocks:
            self.blocks[block] = None

        del self.directory[filename]

        print("\nFile deleted successfully.")

    def list_files(self):
        if not self.directory:
            print("\nDirectory is empty.")
            return

        print("\nDirectory:")
        print("-" * 50)

        for filename, data in self.directory.items():
            print(
                f"File: {filename} | "
                f"Blocks: {data['blocks']} | "
                f"Size: {len(data['content'])} characters"
            )

    def show_blocks(self):
        print("\nBlock Allocation:")
        print("-" * 50)

        for i, owner in enumerate(self.blocks):
            if owner is None:
                print(f"Block {i}: Free")
            else:
                print(f"Block {i}: {owner}")


def disk_scheduling_menu():
    print("\n" + "=" * 60)
    print("DISK SCHEDULING")
    print("=" * 60)

    requests = list(map(
        int,
        input("Enter disk request queue: ").split()
    ))

    head = int(input("Enter initial head position: "))

    disk_size = int(input("Enter disk size (default 200): ") or "200")

    print("\n1. FCFS")
    print("2. SSTF")
    print("3. C-SCAN")
    print("4. C-LOOK")
    print("5. RSS")
    print("6. Run All")

    choice = input("Enter choice: ")

    algorithms = {
        "1": ("FCFS", DiskScheduling.fcfs),
        "2": ("SSTF", DiskScheduling.sstf),
        "3": ("C-SCAN", lambda r, h: DiskScheduling.cscan(r, h, disk_size)),
        "4": ("C-LOOK", DiskScheduling.clook),
        "5": ("RSS", DiskScheduling.rss)
    }

    if choice == "6":
        for name, function in algorithms.values():
            sequence, movement = function(requests, head)

            print("\n" + "-" * 60)
            print(name)
            print("-" * 60)
            print("Head Movement Sequence:")
            print(" -> ".join(map(str, sequence)))
            print("Total Head Movement:", movement)

    elif choice in algorithms:
        name, function = algorithms[choice]

        sequence, movement = function(requests, head)

        print("\n" + "-" * 60)
        print(name)
        print("-" * 60)
        print("Head Movement Sequence:")
        print(" -> ".join(map(str, sequence)))
        print("Total Head Movement:", movement)

    else:
        print("\nInvalid choice.")


def file_system_menu(file_system):
    while True:
        print("\n" + "=" * 60)
        print("SIMPLE FILE SYSTEM")
        print("=" * 60)

        print("1. Create File")
        print("2. Read File")
        print("3. Delete File")
        print("4. List Directory")
        print("5. Show Block Allocation")
        print("6. Back")

        choice = input("Enter choice: ")

        if choice == "1":
            filename = input("Enter file name: ")
            content = input("Enter file content: ")

            file_system.create_file(filename, content)

        elif choice == "2":
            filename = input("Enter file name: ")

            file_system.read_file(filename)

        elif choice == "3":
            filename = input("Enter file name: ")

            file_system.delete_file(filename)

        elif choice == "4":
            file_system.list_files()

        elif choice == "5":
            file_system.show_blocks()

        elif choice == "6":
            break

        else:
            print("\nInvalid choice.")


def main():
    file_system = SimpleFileSystem(50)

    while True:
        print("\n" + "=" * 60)
        print("OPERATING SYSTEM SIMULATION")
        print("=" * 60)

        print("1. Disk Scheduling")
        print("2. Simple File System")
        print("3. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            disk_scheduling_menu()

        elif choice == "2":
            file_system_menu(file_system)

        elif choice == "3":
            print("\nProgram terminated.")
            break

        else:
            print("\nInvalid choice.")


if __name__ == "__main__":
    main()
