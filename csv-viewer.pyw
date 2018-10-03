import csv, os
import tkinter as tk
import tkinter.filedialog as fd

DEFAULT_ENTRY_WIDTH = 10

class Properties(tk.Toplevel):
  def __init__(me, master, apply_command):
    tk.Toplevel.__init__(me, master)
    me.title('Properties')
    me.entries = {}
    me.apply_command = apply_command
    me.frame = tk.Frame(me)
    me.frame.grid(column=0, row=0, columnspan=1)
    tk.Button(me, text='Apply', command=me.apply).grid(column=1, row=1)
    def delete_window():
      master.properties_open = False
      me.destroy()
    me.protocol("WM_DELETE_WINDOW", delete_window )
  def add_property(me, name, entry_text):
    tk.Label(me, text=name).grid(column=0, row=len(me.entries))
    entry = tk.Entry(me)
    entry.insert(0, entry_text)
    entry.grid(column=1, row=len(me.entries))
    me.entries.update({name: entry})
  def apply(me):
    me.apply_command(me)

class Grid(tk.Frame):
  def __init__(me, master):
    tk.Frame.__init__(me, master, borderwidth=0, width=0, height=0)
    me.fn = ''
    me.entries = []
    me.entry_width = DEFAULT_ENTRY_WIDTH
    me.properties_open = False
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
          en = tk.Entry(me, width=me.entry_width)
          en.insert(0, item)
          en.grid(column=x, row=y)
          entry_row.append(en)
        for x in range(len(row), max_width):
          en = tk.Entry(me, width=me.entry_width)
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
  def properties(me):
    if me.properties_open: return
    me.properties_open = True
    def apply(me):
      refresh = False
      new_width = me.entries["Grid Width"].get()
      if new_width.isdigit() and int(new_width) != me.master.entry_width:
        me.master.entry_width = int(new_width)
        refresh = True
      if refresh:
        me.master.refresh()
    prop = Properties(me, apply)
    prop.add_property('Grid Width', me.entry_width)

root = tk.Tk()
root.title("csvgui - No file")
root.minsize(256, 32)
ctrl = Grid(root)
ctrl.pack()

menu = tk.Menu(root)
menu_file = tk.Menu(menu, tearoff=0)
menu_file.add_command(label="Open", command=ctrl.open)
menu_file.add_command(label="Refresh", command=ctrl.refresh)
menu_file.add_command(label="Save", command=ctrl.save)
menu_file.add_command(label="Save As", command=ctrl.saveas)
menu_file.add_separator()
menu_file.add_command(label="Exit", command=root.destroy)
menu.add_cascade(label="File", menu=menu_file)
menu_settings = tk.Menu(menu, tearoff=0)
menu_settings.add_command(label="Properties", command=ctrl.properties)
menu.add_cascade(label="Settings", menu=menu_settings)

root.config(menu=menu)
root.mainloop()
