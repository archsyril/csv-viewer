import tkinter as tk
import csv

def csv_dimensions(f):
  cols, rows = 0,0
  for row in csv.reader(f):
    size = len(row)
    if size > cols:
      cols = size
    rows += 1
  f.seek(0)
  return cols, rows

class CSV_Grid(tk.Frame):
  def __init__(me, master):
    tk.Frame.__init__(me, master, borderwidth=0, width=0, height=0)
    me.en_width = 10
    me.entries = []
    me.columns, me.rows = 0,0
    def event_jump_down(event):
      x,y = me.focus_get().id
      try:
        focus = me.entries[y+1][x]
      except IndexError:
        focus = me.entries[0][x]
      focus.focus_set()
      focus.icursor(0)
    def event_jump_up(event):
      x,y = me.focus_get().id
      focus = me.entries[y-1][x]
      focus.focus_set()
      focus.icursor(0)
    master.bind('<Return>', event_jump_down)
    master.bind('<Shift-Return>', event_jump_up)
    master.bind('<Control-Shift-C>', lambda e:me.insert_column())
    master.bind('<Control-Alt-C>',   lambda e:me.delete_column())
    master.bind('<Control-Shift-R>', lambda e:me.insert_row())
    master.bind('<Control-Alt-R>',   lambda e:me.delete_row())
  def __getitem__(me, get):
    return me.entries[get]
  def update_all(me, **update_with):
    """Update each entry with a key = value"""
    for row in me.entries:
      for en in row:
        for key in update_with:
          en[key] = update_with[key]
  def set_width(me, new_width):
    """Set width of each existing entry. New entries will also be made with this width"""
    me.en_width = new_width
    me.update_all(width = new_width)
  def entry(me, col, row):
    """Make entry at correct width, with an .id and placed in the grid"""
    en = tk.Entry(me, width=me.en_width)
    en.id = (col, row,)
    en.grid(column=col, row=row)
    return en
  def clear(me):
    """Clear text within all entries"""
    for row in me.entries:
      for en in row:
        en.delete(0, 'end')
  def destroy(me):
    """Delete all entries"""
    for row in me.entries:
      for en in row:
        en.destroy()
    me.entries = []
    me.columns, me.rows = 0, 0
  def resize(me, new_cols, new_rows):
    """Add or remove entries. Preserves existing entries, if any"""
    if new_rows < me.rows: # need less than current
      me.delete_row(me.rows - new_rows)
    elif new_rows > me.rows: # need more than current
      me.insert_row(new_rows - me.rows)
    if new_cols < me.columns: # need less than current
      me.delete_column(me.columns - new_cols)
    elif new_cols > me.columns: # need more than current
      me.insert_column(new_cols - me.columns)
  def load(me, fn, skip=False):
    """Loads file into the grid, use skip to not reformat grid"""
    try:
      f = open(fn, 'r')
    except: return False
    if not skip:
      if me.entries:
        me.clear()
        me.resize(*csv_dimensions(f))
      else:
        me.generate(*csv_dimensions(f))
    for y, row in enumerate(csv.reader(f)):
      for x, data in enumerate(row):
        me.entries[y][x].insert(0, data)
    return True
  def refresh(me):
    """Refreshes internal data of each widget. Should be done manually after inserting/deleting columns or rows"""
    me.grid_forget()
    for y, row in enumerate(me.entries):
      for x, en in enumerate(row):
        en.grid(column=x, row=y)
        en.id = (x,y,)
        en.lift()
  def generate(me, cols, rows):
    """Create a brand new grid"""
    if me.entries:
      me.destroy()
    for row in range(rows):
      nr = [me.entry(col,row) for col in range(cols)]
      me.entries.append(nr)
    me.columns, me.rows = cols, rows
    try:
      me[0][0].focus_set()
    except: return
  def insert_row(me, amnt=1):
    for row in range(amnt):
      nr = [me.entry(i, me.rows + row) for i in range(me.columns)]
      me.entries.append(nr)
    me.rows += amnt
  def insert_column(me, amnt=1):
    for row in range(me.rows):
      nr = [me.entry(me.columns + col, row) for col in range(amnt)]
      me.entries[row].extend(nr)
      for en in me.entries[row]:
        en.lift()
    me.columns += amnt
  def delete_row(me, amnt=1):
    for row in me.entries[-amnt:]:
      for en in row:
        en.destroy()
    me.entries = me.entries[0:-amnt]
    me.rows -= amnt
    if me.rows < 0: me.rows = 0
  def delete_column(me, amnt=1):
    for row in range(me.rows):
      for en in me.entries[row][-amnt:]:
        en.destroy()
      me.entries[row] = me.entries[row][0:-amnt]
    me.columns -= amnt
    if me.columns < 0: me.columns = 0
  def insert_row_at(me, abv_row, amnt=1):
    if abv_row >= me.rows:
      raise IndexError("Cannot insert row above a row which doesn't exist: current max is %i (zero-indexed), can't add above that." % (me.rows-1))
    new_rows = []
    for row in range(amnt):
      new_rows.append([tk.Entry(me, width=me.en_width) for col in range(me.columns)])
    me.entries = me.entries[:abv_row] + new_rows + me.entries[abv_row:]
    me.rows += amnt
  def insert_column_at(me, left_of_col, amnt=1):
    if left_of_col >= me.columns:
      raise IndexError("Cannot insert column left of a column which doesn't exist: current max is %i (zero-indexed), can't add above that." % (me.columns-1))
    for row in range(me.rows):
      new_cols = [tk.Entry(me, width=me.en_width) for col in range(amnt)]
      me.entries[row] = me.entries[row][:left_of_col] + new_cols + me.entries[row][left_of_col:]
    me.columns += amnt
  def delete_row_at(me, row_index, amnt=1):
    for row in range(amnt):
      row += row_index
      for en in me.entries[row]:
        en.destroy()
    me.entries = me.entries[:row_index] + me.entries[row_index+amnt:]
    me.rows -= amnt
    if me.rows < 0: me.rows = 0
  def delete_column_at(me, col_index, amnt=1):
    for row in range(me.rows):
      rows = me.entries[row]
      for en in rows[col_index:col_index+amnt]:
        en.destroy()
      me.entries[row] = rows[:col_index] + rows[col_index+amnt:]
    me.columns -= amnt
    if me.columns < 0: me.columns = 0
