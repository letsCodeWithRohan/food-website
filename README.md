<h1>Food Ordering Website in flask</h1>

<h3>Created By Nitesh Nadar</h3>

<h3>Technology Used</h3>
<ul>
<li>HTML</li>
<li>CSS</li>
<li>TailwindCSS</li>
<li>JavaScript</li>
<li>Python(Flask)</li>
</ul>

<h4>Steps to download and run this project</h4>

<ol start="1">
<li>Download and Extract This Repository</li>
<li>Open command prompt in that folder</li>
<li><p>Install virtualenv if you don't have it</p>  
    
```bash
pip install virtualenv
```

</li>
<li><p>create virtual environment for this project by using</p>

```bash
python -m venv .venv
```
<p align="center">OR</p>

```bash
virtualenv .venv
```
</li>
<li>
<p>Activate virtual environment</p>

```bash
.venv\Scripts\activate
```
</li>
<li>
<p>Install required dependencies</p>
    
```bash
pip install flask flask_mysqldb
```
</li>
<li>
<p>Setup Database</p>
<ul>
<li>Open XAMPP CONTROL PANEL.</li>
<li>Start <mark>Apache</mark> and <mark>MySQL</mark></li>
<li>Open <kbd>Admin</kbd> of MySQL</li>
<li>Create New Database as your wish Ex : "food"</li>
<li>Click on it then open <kbd>SQL</kbd> Tab </li>
<li>
<p>Paster The below Query to create table</p>

<p><kbd>users</kbd> table</p> 

```SQL
CREATE TABLE Users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    phone VARCHAR(20),
    password VARCHAR(255) NOT NULL
);
```
<p><kbd>product</kbd> table</p> 

```SQL
CREATE TABLE product (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    photo VARCHAR(255),
    category VARCHAR(100),
    price DECIMAL(10, 2) NOT NULL,
    description VARCHAR(255)
);
```
<p><kbd>cart</kbd> table</p> 

```SQL
CREATE TABLE cart (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    product_id INT,
    quantity INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES product(id) ON DELETE CASCADE
);
```
<p><kbd>orders</kbd> table</p> 


```SQL
CREATE TABLE orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    product_id INT,
    quantity INT NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    address VARCHAR(255) NOT NULL,
    city VARCHAR(100) NOT NULL,
    state VARCHAR(100) NOT NULL,
    zip_code VARCHAR(20) NOT NULL,
    country VARCHAR(100) NOT NULL,
    status ENUM('Pending', 'Out for delivery', 'Delivered') NOT NULL,
    order_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES product(id) ON DELETE CASCADE
);
```

<li>Run The Query by clicking <kbd>Go</kbd></li>
</ul>
</li>
<li>
<p>Run the Project</p>

```bash
python app.py
```
</li>

</ol>








