import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import messagebox, scrolledtext

graph_shown = False

def fifo(pages, capacity):
    memory = []
    page_faults = 0
    result = ""
    for page in pages:
        if page not in memory:
            if len(memory) == capacity:
                memory.pop(0)
            memory.append(page)
            page_faults += 1
        result += f"Memory: {memory}\n"
    result += f"\nTotal Page Faults (FIFO): {page_faults}\n"
    return result

def lru(pages, capacity):
    memory = []
    page_faults = 0
    result = ""
    recently_used = []

    for page in pages:
        if page not in memory:
            if len(memory) == capacity:
                lru_page = recently_used.pop(0)
                memory.remove(lru_page)
            memory.append(page)
            page_faults += 1
        else:
            recently_used.remove(page)
        recently_used.append(page)
        result += f"Memory: {memory}\n"
    result += f"\nTotal Page Faults (LRU): {page_faults}\n"
    return result

def optimal(pages, capacity):
    memory = []
    page_faults = 0
    result = ""

    for i in range(len(pages)):
        if pages[i] not in memory:
            if len(memory) == capacity:
                future_indices = []
                for item in memory:
                    try:
                        future_indices.append(pages[i+1:].index(item))
                    except ValueError:
                        future_indices.append(float('inf'))
                memory.pop(future_indices.index(max(future_indices)))
            memory.append(pages[i])
            page_faults += 1
        result += f"Memory: {memory}\n"
    result += f"\nTotal Page Faults (Optimal): {page_faults}\n"
    return result

def run_simulation():
    global graph_shown

    ref_str = entry_ref.get()
    capacity = entry_frame.get()

    try:
        pages = list(map(int, ref_str.split(',')))
        capacity = int(capacity)
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter valid integers.")
        return

    # Run all algorithms
    output_fifo = fifo(pages, capacity)
    output_lru = lru(pages, capacity)
    output_opt = optimal(pages, capacity)

    # Extract page fault numbers
    pf_fifo = int(output_fifo.strip().split()[-1])
    pf_lru = int(output_lru.strip().split()[-1])
    pf_opt = int(output_opt.strip().split()[-1])

    # Get selected algorithm for detailed output
    algo = algo_var.get()
    if algo == "FIFO":
        detailed_output = output_fifo
    elif algo == "LRU":
        detailed_output = output_lru
    elif algo == "Optimal":
        detailed_output = output_opt
    else:
        detailed_output = "Please select an algorithm."

    output_text.delete(1.0, tk.END)
    output_text.insert(tk.END, detailed_output)

    # Show graph only the first time
    if not graph_shown:
        graph_shown = True  # Update flag

        algorithms = ['FIFO', 'LRU', 'Optimal']
        faults = [pf_fifo, pf_lru, pf_opt]

        plt.figure(figsize=(6, 4))
        bars = plt.bar(algorithms, faults, color=['blue', 'orange', 'green'])
        plt.title("Page Faults Comparison")
        plt.ylabel("Page Faults")
        plt.ylim(0, max(faults) + 2)

        # Add value labels
        for bar in bars:
            yval = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2.0, yval + 0.1, yval, ha='center', va='bottom')

        plt.tight_layout()
        plt.show()


# GUI setup
root = tk.Tk()
root.title("Page Replacement Simulator")
root.geometry("500x500")

tk.Label(root, text="Reference String (comma-separated):").pack()
entry_ref = tk.Entry(root, width=50)
entry_ref.pack()

tk.Label(root, text="Number of Frames:").pack()
entry_frame = tk.Entry(root, width=10)
entry_frame.pack()

tk.Label(root, text="Select Algorithm:").pack()
algo_var = tk.StringVar(value="FIFO")
tk.OptionMenu(root, algo_var, "FIFO", "LRU", "Optimal").pack()

tk.Button(root, text="Run Simulation", command=run_simulation).pack(pady=10)

output_text = scrolledtext.ScrolledText(root, width=60, height=20)
output_text.pack()

root.mainloop()
