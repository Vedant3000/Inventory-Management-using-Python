from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_api_key'

# database connection setup
def init_db():
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()
    cursor.execute(''' CREATE TABLE IF NOT EXISTS items
                   (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                   name TEXT NOT NULL,
                   quantity INTEGER NOT NULL,
                   volume INTEGER NOT NULL) ''')
    conn.commit()
    conn.close()
    
# Home route
@app.route('/')
def index():
    return render_template('index.html')

# View items
@app.route('/inventory')
def view_inventory():
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM items")
    items = cursor.fetchall()
    conn.close()
    return render_template('view_inventory.html', items=items)

# Add a new item
@app.route('/add', methods=['GET', 'POST'])
def add_item():
    if request.method == 'POST':
        name = request.form['name']
        quantity = request.form['quantity']
        volume = request.form['volume']
        if name and quantity and volume:
            conn = sqlite3.connect('inventory.db')
            cursor = conn.cursor()
            cursor.execute("INSERT INTO items (name, quantity, volume) VALUES (?, ?, ?)", 
                           (name, int(quantity), int(volume)))
            conn.commit()
            conn.close()
            flash(f"Item '{name}' added successfully")
            return redirect(url_for('view_inventory'))
        else:
            flash("Please fill in all fields")
    return render_template('add_item.html')

# Update an item 
@app.route('/update/<int:item_id>', methods=['GET', 'POST'])
def update_item(item_id):
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM items WHERE id = ?", (item_id))
    item = cursor.fetchone()
    conn.close()
    
    if request.method == 'POST':
        name = request.form['name']
        quantity = request.form['quantity']
        volume = request.form['volume']
        conn = sqlite3.connect('inventory.db')
        cursor = conn.cursor()
        cursor.execute("UPDATE items SET name = ?, quantity = ?, volume = ? WHERE id = ?", 
                       (name, int(quantity), float(volume), item_id))
        conn.commit()
        conn.close()
        flash(f"Item '{name}' updated successfully")
        return redirect(url_for('view_inventory'))
    return render_template('update_item.html', item=item)

# Delete an item
@app.route('/delete/<int:item_id>')
def delete_item(item_id):
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM items WHERE id = ?", (item_id,))
    conn.commit()
    conn.close()
    flash(f"Item with id {item_id} deleted successfully")
    return redirect(url_for('view_inventory'))

if __name__=='__main__':
    init_db()
    app.run(debug=True)