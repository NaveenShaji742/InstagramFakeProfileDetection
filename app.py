from flask import Flask, request, render_template, redirect, url_for
import instaloader
import sqlite3

app = Flask(__name__)

def create_table():
    conn = sqlite3.connect('account_analysis.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS search_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            search_id INTEGER,
            username TEXT,
            fraud_score INTEGER,
            category TEXT,
            posts INTEGER,
            followers INTEGER,
            following INTEGER
        )
    ''')
    conn.commit()
    conn.close()

create_table()

def scrape_profile_data(username):
    loader = instaloader.Instaloader()
    profile = instaloader.Profile.from_username(loader.context, username)
    
    profile_data = {
        'profile_picture': profile.profile_pic_url,
        'posts': profile.mediacount,
        'followers': profile.followers,
        'following': profile.followees
    }
    
    return profile_data

def calculate_fraud_score(profile_data):
    score = 0
    if not profile_data.get('profile_picture'):
        score += 30
    if profile_data.get('posts', 0) < 5:
        score += 20
    if profile_data.get('followers', 0) < 100:
        score += 20
    if profile_data.get('following', 0) > 1000:
        score += 30
    if profile_data.get('followers') < profile_data.get('following'):
        score += 30
    
    return score

def categorize_account(fraud_score):
    if fraud_score >= 80:
        return "Fake"
    elif 50 <= fraud_score < 80:
        return "Warning"
    else:
        return "Real"

def save_to_sqlite(results, search_id, db_name='account_analysis.db', table_name='search_results'):
    try:
        conn = sqlite3.connect(db_name)
        for result in results:
            result['search_id'] = search_id
            conn.execute(f"INSERT INTO {table_name} (search_id, username, fraud_score, category, posts, followers, following) VALUES (:search_id, :username, :fraud_score, :category, :posts, :followers, :following)", result)
        conn.commit()
        conn.close()
        print(f"Results saved to {db_name} in table {table_name}")
    except Exception as e:
        print(f"Error saving to SQLite database: {e}")

def analyze_usernames(usernames):
    results = []
    
    for username in usernames:
        try:
            profile_data = scrape_profile_data(username)
        except Exception as e:
            print(f"Error scraping profile for {username}: {e}")
            continue
        
        fraud_score = calculate_fraud_score(profile_data)
        category = categorize_account(fraud_score)
        
        results.append({
            'username': username,
            'fraud_score': fraud_score,
            'category': category,
            'posts': profile_data['posts'],
            'followers': profile_data['followers'],
            'following': profile_data['following']
        })
        
    return results

def get_next_search_id(db_name='account_analysis.db', table_name='search_results'):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute(f"SELECT MAX(search_id) FROM {table_name}")
    result = cursor.fetchone()
    next_id = result[0] + 1 if result[0] is not None else 1
    conn.close()
    return next_id

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        usernames = request.form['usernames'].split()
        results = analyze_usernames(usernames)
        search_id = get_next_search_id()
        save_to_sqlite(results, search_id)
        return redirect(url_for('results'))
    return render_template('index.html')

@app.route('/results', methods=['GET', 'POST'])
def results():
    if request.method == 'POST':
        selected_ids = request.form.getlist('selected')
        conn = sqlite3.connect('account_analysis.db')
        cursor = conn.cursor()
        for id in selected_ids:
            cursor.execute("DELETE FROM search_results WHERE id = ?", (id,))
        conn.commit()
        conn.close()
        return redirect(url_for('results'))
    
    conn = sqlite3.connect('account_analysis.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM search_results")
    rows = cursor.fetchall()
    conn.close()

    results = [
        {
            'id': row[0],
            'search_id': row[1],
            'username': row[2],
            'fraud_score': row[3],
            'category': row[4],
            'posts': row[5],
            'followers': row[6],
            'following': row[7]
        }
        for row in rows
    ]
    return render_template('result.html', results=results)

if __name__ == "__main__":
    app.run(debug=True)
