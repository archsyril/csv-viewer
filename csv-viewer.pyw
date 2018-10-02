import csv, os
import tkinter as tk
import tkinter.filedialog as fd

ENTRY_WIDTH = 16
class Control(tk.Frame):
  def __init__(me, master):
    tk.Frame.__init__(me, master)
    me.fn = ''
    me.entries = []
    me.entry_width = 10
  def open(me):
    me.fn = fd.askopenfilename(parent=me)
    if me.fn:
      me.master.title("csvgui - " + me.fn)
      me.refresh()
  def refresh(me):
    if len(me.entries):
      ls = me.grid_slaves()
      for item in ls:
        item.destroy()
    me.entries = []
    max_width = 0
    if me.fn:
      f = open(me.fn, 'r', newline='')
      for row in csv.reader(f):
        width = len(row)
        if width > max_width:
          max_width = width
      f.seek(0)
      for y, row in enumerate(csv.reader(f)):
        entry_row = []
        for x, item in enumerate(row):
          en = tk.Entry(me, width=ENTRY_WIDTH)
          en.insert(0, item)
          en.grid(column=x, row=y)
          entry_row.append(en)
        for x in range(len(row), max_width):
          en = tk.Entry(me, width=ENTRY_WIDTH)
          en.grid(column=x, row=y)
          entry_row.append(en)
        me.entries.append(entry_row)
      f.close()
  def save(me, fn=None):
    if not fn:
      fn = me.fn
    f = open(fn, 'w', newline='')
    writer = csv.writer(f)
    for row in me.entries:
      writer.writerow([item.get() for item in row])
    f.close()
  def saveas(me):
    savefn = fd.asksaveasfilename(parent=me)
    if savefn:
      me.save(savefn)

root = tk.Tk()
root.title("csvgui - No file")
root.minsize(256, 32)
ctrl = Control(root)
ctrl.pack()

menu = tk.Menu(root)
menu_file = tk.Menu(menu, tearoff=0)
menu_file.add_command(label="Open", command=ctrl.open)
menu_file.add_command(label="Refresh", command=ctrl.refresh)
menu_file.add_command(label="Save", command=ctrl.save)
menu_file.add_command(label="Save As", command=ctrl.saveas)
menu_file.add_separator()
menu_file.add_command(label="Exit", command=root.quit)
menu.add_cascade(label="File", menu=menu_file)

root.config(menu=menu)
root.mainloop()
