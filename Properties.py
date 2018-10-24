import tkinter as tk

class Properties(tk.Toplevel):
  def __init__(me, master, apply_func):
    tk.Toplevel.__init__(me, master)
    me.apply_func = apply_func
    me.properties = {}
    me.frame = tk.Frame(me)
    me.frame.grid(column=0, row=0, columnspan=2)
    me.protocol("WM_DELETE_WINDOW", me.destroy_all)
    tk.Button(me, text="Apply",    command=me.apply).grid(column=0, row=1)
    tk.Button(me, text='Cancel', command=me.destroy_all).grid(column=1, row=1)
  def __getitem__(me, get):
    return me.properties[get].get()
  def add_property(me, labeltxt, default):
    row = len(me.properties)
    tk.Label(me.frame, text=labeltxt).grid(column=0, row=row)
    entry = tk.Entry(me.frame)
    entry.insert(0, default)
    entry.grid(column=1, row=row)
    me.properties.update({labeltxt: entry})
  def add_toggle(me, labeltxt, default, *, describe=""):
    row = len(me.properties)
    tk.Label(me.frame, text=labeltxt).grid(column=0, row=row)
    var = tk.IntVar(); var.set(default)
    tk.Checkbutton(me.frame, text=describe, variable=var).grid(column=1, row=row)
    me.properties.update({labeltxt: var})
  def destroy_all(me):
    for gs in me.frame.grid_slaves():
      gs.destroy()
    me.destroy()
  def apply(me):
    me.apply_func(me)
    me.destroy_all()
