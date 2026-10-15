import tkinter as tk
from tkinter import messagebox


class Node:
    def __init__(self, node_id):
        self.node_id = node_id
        self.active = True


class LeaderElectionApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Distributed Leader Election Simulator")
        self.root.geometry("1000x700")
        self.root.configure(bg="#f4f6f8")

        self.nodes = []
        self.leader = None

        self.show_start_screen()

    # ================= START SCREEN =================

    def show_start_screen(self):

        self.clear_window()

        title = tk.Label(
            self.root,
            text="Distributed Leader Election",
            font=("Helvetica", 28, "bold"),
            bg="#f4f6f8",
            fg="#1f2937"
        )
        title.pack(pady=(120, 10))

        subtitle = tk.Label(
            self.root,
            text="Bully Algorithm Simulator",
            font=("Helvetica", 14),
            bg="#f4f6f8",
            fg="#6b7280"
        )
        subtitle.pack(pady=5)

        box = tk.Frame(
            self.root,
            bg="white",
            padx=40,
            pady=35,
            highlightbackground="#dddddd",
            highlightthickness=1
        )
        box.pack(pady=35)

        label = tk.Label(
            box,
            text="Enter Number of Nodes",
            font=("Helvetica", 14, "bold"),
            bg="white",
            fg="#374151"
        )
        label.pack(pady=(0, 12))

        self.node_entry = tk.Entry(
            box,
            font=("Helvetica", 16),
            width=10,
            justify="center",
            relief="solid",
            borderwidth=1
        )
        self.node_entry.pack(pady=5)
        self.node_entry.insert(0, "5")

        create_button = tk.Button(
            box,
            text="Create Network",
            command=self.create_network,
            font=("Helvetica", 12, "bold"),
            bg="#2563eb",
            fg="white",
            activebackground="#1d4ed8",
            activeforeground="white",
            relief="flat",
            padx=30,
            pady=12,
            cursor="hand2"
        )
        create_button.pack(pady=(20, 5))

        info = tk.Label(
            self.root,
            text="Example: Enter 5 to create Node 1 - Node 5",
            font=("Helvetica", 10),
            bg="#f4f6f8",
            fg="#6b7280"
        )
        info.pack()

    # ================= CREATE NETWORK =================

    def create_network(self):

        try:
            number = int(self.node_entry.get())

            if number < 2:
                raise ValueError

            if number > 30:
                messagebox.showwarning(
                    "Too Many Nodes",
                    "Please enter a maximum of 30 nodes."
                )
                return

        except ValueError:
            messagebox.showerror(
                "Invalid Input",
                "Please enter a number between 2 and 30."
            )
            return

        self.nodes = [
            Node(i) for i in range(1, number + 1)
        ]

        self.leader = None

        self.show_dashboard()

    # ================= DASHBOARD =================

    def show_dashboard(self):

        self.clear_window()

        # Header
        header = tk.Frame(
            self.root,
            bg="white",
            height=90
        )
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(
            header,
            text="Distributed Leader Election",
            font=("Helvetica", 24, "bold"),
            bg="white",
            fg="#1f2937"
        ).pack(pady=(15, 0))

        tk.Label(
            header,
            text="Bully Algorithm • Runtime Node Simulator",
            font=("Helvetica", 11),
            bg="white",
            fg="#6b7280"
        ).pack()

        # Dashboard cards
        cards = tk.Frame(
            self.root,
            bg="#f4f6f8"
        )
        cards.pack(fill="x", padx=30, pady=20)

        self.active_value = self.create_card(
            cards,
            "ACTIVE NODES",
            str(len(self.nodes)),
            "#2563eb"
        )

        self.active_value.pack(
            side="left",
            fill="both",
            expand=True,
            padx=6
        )

        self.leader_value = self.create_card(
            cards,
            "CURRENT LEADER",
            "None",
            "#16a34a"
        )

        self.leader_value.pack(
            side="left",
            fill="both",
            expand=True,
            padx=6
        )

        self.status_value = self.create_card(
            cards,
            "NETWORK STATUS",
            "Ready",
            "#9333ea"
        )

        self.status_value.pack(
            side="left",
            fill="both",
            expand=True,
            padx=6
        )

        # Nodes title
        tk.Label(
            self.root,
            text="Network Nodes",
            font=("Helvetica", 17, "bold"),
            bg="#f4f6f8",
            fg="#1f2937"
        ).pack(anchor="w", padx=30)

        # Nodes area
        self.nodes_frame = tk.Frame(
            self.root,
            bg="#f4f6f8"
        )
        self.nodes_frame.pack(
            fill="x",
            padx=25,
            pady=10
        )

        self.node_cards = {}

        self.display_nodes()

        # Buttons
        controls = tk.Frame(
            self.root,
            bg="#f4f6f8"
        )
        controls.pack(fill="x", padx=30, pady=10)

        tk.Button(
            controls,
            text="▶  Start Election",
            command=self.start_election,
            font=("Helvetica", 11, "bold"),
            bg="#2563eb",
            fg="white",
            relief="flat",
            padx=22,
            pady=10,
            cursor="hand2"
        ).pack(side="left", padx=5)

        tk.Button(
            controls,
            text="⚠  Fail Leader",
            command=self.fail_leader,
            font=("Helvetica", 11, "bold"),
            bg="#dc2626",
            fg="white",
            relief="flat",
            padx=22,
            pady=10,
            cursor="hand2"
        ).pack(side="left", padx=5)

        tk.Button(
            controls,
            text="↻  Reset",
            command=self.reset_network,
            font=("Helvetica", 11, "bold"),
            bg="white",
            fg="#374151",
            relief="solid",
            padx=22,
            pady=9,
            cursor="hand2"
        ).pack(side="left", padx=5)

        tk.Button(
            controls,
            text="←  Change Nodes",
            command=self.show_start_screen,
            font=("Helvetica", 11),
            bg="white",
            fg="#374151",
            relief="solid",
            padx=18,
            pady=9,
            cursor="hand2"
        ).pack(side="right", padx=5)

        # Activity log
        tk.Label(
            self.root,
            text="Election Activity",
            font=("Helvetica", 17, "bold"),
            bg="#f4f6f8",
            fg="#1f2937"
        ).pack(anchor="w", padx=30, pady=(5, 5))

        self.log_box = tk.Text(
            self.root,
            height=8,
            font=("Menlo", 10),
            bg="white",
            fg="#374151",
            relief="solid",
            borderwidth=1
        )
        self.log_box.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=(0, 20)
        )

        self.log("Network created successfully.")
        self.log(
            f"{len(self.nodes)} nodes are ready for election."
        )

    # ================= CARD =================

    def create_card(self, parent, title, value, color):

        card = tk.Frame(
            parent,
            bg="white",
            height=100,
            highlightbackground="#dddddd",
            highlightthickness=1
        )

        tk.Label(
            card,
            text=title,
            font=("Helvetica", 10, "bold"),
            bg="white",
            fg="#6b7280"
        ).pack(pady=(15, 2))

        value_label = tk.Label(
            card,
            text=value,
            font=("Helvetica", 22, "bold"),
            bg="white",
            fg=color
        )
        value_label.pack()

        card.value_label = value_label

        return card

    # ================= DISPLAY NODES =================

    def display_nodes(self):

        for widget in self.nodes_frame.winfo_children():
            widget.destroy()

        self.node_cards = {}

        for node in self.nodes:

            card = tk.Frame(
                self.nodes_frame,
                bg="white",
                height=110,
                highlightbackground="#d1d5db",
                highlightthickness=1
            )

            card.pack(
                side="left",
                fill="both",
                expand=True,
                padx=4
            )

            card.pack_propagate(False)

            icon = tk.Label(
                card,
                text="●",
                font=("Helvetica", 22),
                bg="white",
                fg="#22c55e"
            )
            icon.pack(pady=(12, 0))

            name = tk.Label(
                card,
                text=f"Node {node.node_id}",
                font=("Helvetica", 12, "bold"),
                bg="white",
                fg="#1f2937"
            )
            name.pack()

            status = tk.Label(
                card,
                text="ACTIVE",
                font=("Helvetica", 9, "bold"),
                bg="white",
                fg="#16a34a"
            )
            status.pack()

            self.node_cards[node.node_id] = {
                "card": card,
                "icon": icon,
                "name": name,
                "status": status
            }

    # ================= ELECTION =================

    def start_election(self):

        active_nodes = [
            node for node in self.nodes
            if node.active
        ]

        if not active_nodes:
            messagebox.showerror(
                "Election Failed",
                "No active nodes are available."
            )
            return

        self.log("")
        self.log("========== ELECTION STARTED ==========")

        for node in active_nodes:
            self.log(
                f"Node {node.node_id} participates."
            )

        self.leader = max(
            active_nodes,
            key=lambda node: node.node_id
        )

        self.log(
            f"Node {self.leader.node_id} has highest ID."
        )

        self.log(
            f"🏆 Node {self.leader.node_id} is elected Leader!"
        )

        self.update_display()

    # ================= FAIL LEADER =================

    def fail_leader(self):

        if self.leader is None:
            messagebox.showwarning(
                "No Leader",
                "Start an election first."
            )
            return

        failed_id = self.leader.node_id

        self.leader.active = False
        self.leader = None

        self.log("")
        self.log(
            f"⚠ Node {failed_id} (Leader) has FAILED."
        )

        self.update_display()

        active_nodes = [
            node for node in self.nodes
            if node.active
        ]

        if active_nodes:

            self.log(
                "Automatic election started..."
            )

            self.leader = max(
                active_nodes,
                key=lambda node: node.node_id
            )

            self.log(
                f"🏆 Node {self.leader.node_id} "
                f"is the NEW LEADER!"
            )

            self.update_display()

        else:

            self.log("No active nodes remain.")

    # ================= RESET =================

    def reset_network(self):

        for node in self.nodes:
            node.active = True

        self.leader = None

        self.log("")
        self.log("Network reset.")
        self.log("All nodes are active again.")

        self.update_display()

    # ================= UPDATE =================

    def update_display(self):

        active_count = sum(
            node.active for node in self.nodes
        )

        self.active_value.value_label.config(
            text=str(active_count)
        )

        if self.leader:

            self.leader_value.value_label.config(
                text=f"Node {self.leader.node_id}"
            )

            self.status_value.value_label.config(
                text="Leader Active"
            )

        else:

            self.leader_value.value_label.config(
                text="None"
            )

            self.status_value.value_label.config(
                text="Ready"
            )

        for node in self.nodes:

            card = self.node_cards[node.node_id]

            if node.active:

                card["icon"].config(
                    fg="#22c55e"
                )

                card["status"].config(
                    text="ACTIVE",
                    fg="#16a34a"
                )

            else:

                card["icon"].config(
                    fg="#ef4444"
                )

                card["status"].config(
                    text="FAILED",
                    fg="#dc2626"
                )

            if self.leader == node:

                card["card"].config(
                    highlightbackground="#16a34a",
                    highlightthickness=3
                )

                card["name"].config(
                    text=f"Node {node.node_id} 🏆"
                )

            else:

                card["card"].config(
                    highlightbackground="#d1d5db",
                    highlightthickness=1
                )

                card["name"].config(
                    text=f"Node {node.node_id}"
                )

    # ================= LOG =================

    def log(self, message):

        self.log_box.insert(
            "end",
            message + "\n"
        )

        self.log_box.see("end")

    # ================= CLEAR =================

    def clear_window(self):

        for widget in self.root.winfo_children():
            widget.destroy()


# ================= MAIN =================

root = tk.Tk()

app = LeaderElectionApp(root)

root.mainloop()