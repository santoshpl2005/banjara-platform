from flask import Flask, render_template, request, jsonify, redirect, url_for, session, flash
import pymysql
pymysql.install_as_MySQLdb()

from flask_mysqldb import MySQL
from config import Config
import os
import hashlib
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config.from_object(Config)
mysql = MySQL(app)

ALLOWED_IMG = {'jpg','jpeg','png','gif','webp'}
ALLOWED_AUD = {'mp3','wav','ogg'}
ALLOWED_VID = {'mp4','webm','ogg'}

def allowed_file(filename, allowed):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in allowed

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()
def get_all_media():
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM media ORDER BY uploaded_at DESC")
        result = cur.fetchall()
        cur.close()
        return result
    except:
        return []

def get_media_stats():
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT COUNT(*) FROM media")
        total = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM media WHERE media_type='image'")
        images = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM media WHERE media_type='audio'")
        audios = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM media WHERE media_type='video'")
        videos = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM media WHERE section='temples'")
        temples = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM media WHERE section='culture'")
        culture = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM media WHERE section='gallery'")
        gallery = cur.fetchone()[0]
        cur.close()
        return {'total':total,'images':images,'audios':audios,
                'videos':videos,'temples':temples,'culture':culture,'gallery':gallery}
    except:
        return {'total':0,'images':0,'audios':0,'videos':0,
                'temples':0,'culture':0,'gallery':0}
# ─────────────────────────────────────
#  PUBLIC PAGES
# ─────────────────────────────────────
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/culture')
def culture():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM cultural_content")
    items = cur.fetchall()
    cur.execute("SELECT * FROM media WHERE section='culture'")
    media = cur.fetchall()
    cur.close()
    return render_template('culture.html', items=items, media=media)

@app.route('/temples')
def temples():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM temples")
    temples_list = cur.fetchall()
    cur.execute("SELECT * FROM media WHERE section='temples'")
    media = cur.fetchall()
    cur.close()
    return render_template('temples.html', temples=temples_list, media=media)

@app.route('/gallery')
def gallery():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM media WHERE media_type='image'")
    images = cur.fetchall()
    cur.execute("SELECT * FROM media WHERE media_type='audio'")
    audios = cur.fetchall()
    cur.execute("SELECT * FROM media WHERE media_type='video'")
    videos = cur.fetchall()
    # Get YouTube videos
    yt_videos = []
    try:
        cur.execute("SELECT * FROM youtube_videos ORDER BY added_at DESC")
        yt_videos = cur.fetchall()
    except:
        pass
    cur.close()
    return render_template('gallery.html',
        images=images, audios=audios,
        videos=videos, yt_videos=yt_videos)

@app.route('/quiz')
def quiz():
    return render_template('quiz.html')

@app.route('/ai_chat')
def ai_chat():
    return render_template('ai_chat.html')

# ─────────────────────────────────────
#  USER AUTH
# ─────────────────────────────────────
@app.route('/login', methods=['GET','POST'])
def login():
    if session.get('user_id'):
        return redirect(url_for('home'))
    error = None
    if request.method == 'POST':
        email = request.form['email']
        password = hash_password(request.form['password'])
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE email=%s AND password=%s", (email, password))
        user = cur.fetchone()
        cur.close()
        if user:
            session['user_id'] = user[0]
            session['user_name'] = user[1]
            session['user_email'] = user[2]
            return redirect(url_for('home'))
        else:
            error = 'Invalid email or password!'
    return render_template('login.html', error=error)

@app.route('/register', methods=['GET','POST'])
def register():
    if session.get('user_id'):
        return redirect(url_for('home'))
    error = None
    success = None
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = hash_password(request.form['password'])
        cur = mysql.connection.cursor()
        try:
            cur.execute("INSERT INTO users (name, email, password) VALUES (%s,%s,%s)",
                        (name, email, password))
            mysql.connection.commit()
            success = 'Account created! Please login.'
        except:
            error = 'Email already exists!'
        cur.close()
    return render_template('register.html', error=error, success=success)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

@app.route('/profile')
def profile():
    if not session.get('user_id'):
        return redirect(url_for('login'))
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE id=%s", (session['user_id'],))
    user = cur.fetchone()
    cur.close()
    return render_template('profile.html', user=user)

# ─────────────────────────────────────
#  AI SEARCH
# ─────────────────────────────────────
@app.route('/ai_search', methods=['POST'])
def ai_search():
    query = request.json.get('query', '').lower()
    try:
        cur = mysql.connection.cursor()
        cur.execute("""
            SELECT title, description FROM cultural_content
            WHERE LOWER(title) LIKE %s OR LOWER(description) LIKE %s LIMIT 2
        """, ('%'+query+'%', '%'+query+'%'))
        db_results = cur.fetchall()
        cur.close()
        if db_results:
            answer = '📚 From our database: '
            for row in db_results:
                answer += f"{row[0]}: {row[1][:150]}... "
            return jsonify({'answer': answer})
    except:
        pass

    responses = {
        'festival':      '🎉 Banjara festivals: Teej (9-day), Navratri Garba, Holi with Langa-Daphl drums, Sevalal Jayanti 15 February.',
        'temple':        '🛕 Sacred temples: Poharadevi (Kashi of Banjaras), Suragondankoppa birthplace, Sevagad Andhra, Sirsi Marikamba.',
        'dress':         '👗 Banjara dress: Phetiya skirt and Kanchali blouse with Shisha mirror work. GI status Sandur Lambani embroidery.',
        'embroidery':    '🧵 Sandur Lambani embroidery has GI status — uses Shisha mirrors, shells, coins. Exported to Japan USA Europe.',
        'music':         '🎵 Banjara music: Dholak, Langa-Daphl drum, Manjeera. Folk songs called Geet in Gor-Boli language.',
        'language':      '🗣️ Gor Boli (Lambadi) — Indo-Aryan language blending Marwari, Gujarati, Hindi and Marathi.',
        'food':          '🍲 Banjara food: Bajra Roti, Daliya, Saloi goat meat. Guntur chilies and garlic. Sacred Lapsi and Churma.',
        'history':       '📜 Banjaras from Mewar Rajasthan as Rajput descendants. Nomadic salt grain traders in Tanda caravans.',
        'sevalal':       '🙏 Sant Sevalal Maharaj born 15 Feb 1739 Suragondankoppa Karnataka. Samadhi Poharadevi 4 Dec 1806.',
        'poharadevi':    '🛕 Poharadevi — Kashi of Banjaras. Samadhi of Sevalal Maharaj. Jayanti 15 February every year.',
        'birthplace':    '🌱 Sevalal birthplace: Suragondankoppa, Honnali Taluk, Davanagere District, Karnataka.',
        'tanda':         '🏘️ Tanda is Banjara settlement. Led by Naik. Every Tanda has white Jhanda flag for Sevalal Maharaj.',
        'karnataka':     '🌿 Karnataka Banjaras called Lambani. Famous in Bellary, Koppal, Raichur, Haveri. GI embroidery center Sandur.',
        'marriage':      '💒 Banjara marriage called Biyav. Rituals: Sakhi Puja, Haldi, Toran, horse procession, Phera sacred fire.',
        'saati sati':    '⭐ Seven Satis: Hoona (Matriarch), Kesi (Healer), Sita (Justice), Bheema (Warrior), Tola (Provider), Tulaja (Wisdom), Roopa (Culture).',
        'lambani':       '🎭 Lambani is Karnataka name for Banjara. Known for colorful dress, GI embroidery and rich culture.',
        'jhanda':        '🏳️ White Jhanda flag in every Tanda represents Sant Sevalal Maharaj\'s blessing and presence.',
        'naik':          '👑 Naik is headman of Banjara Tanda who settles disputes and leads community welfare decisions.',
        'marikamba':     '🌺 Goddess Marikamba Sirsi Karnataka — Sevalal Maharaj possessed her divine shakti for welfare of people.',
        'sevagad':       '🏰 Sevagad near Gooty Anantapur AP — major Banjara spiritual center. Temple complex 40 acres built 2001-2004.',
        'bajra':         '🫓 Bajra Roti pearl millet flatbread — main staple nutritious food of Banjara community.',
    }

    answer = None
    for keyword, response in responses.items():
        if keyword in query:
            answer = response
            break

    if not answer:
        answer = '🤔 Try asking about: festivals, temples, dress, music, food, history, sevalal, karnataka, marriage, saati sati!'

    try:
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO user_queries (query_text, response_text) VALUES (%s,%s)", (query, answer))
        mysql.connection.commit()
        cur.close()
    except:
        pass

    return jsonify({'answer': answer})

# ─────────────────────────────────────
#  ADMIN
# ─────────────────────────────────────
@app.route('/admin', methods=['GET','POST'])
def admin_login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'Santu' and password == 'Spl@2005':
            session['admin_logged_in'] = True
            return redirect(url_for('admin_dashboard'))
        else:
            error = 'Wrong username or password!'
    return render_template('admin/login.html', error=error)

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('admin_login'))

@app.route('/admin/dashboard')
def admin_dashboard():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    cur = mysql.connection.cursor()

    cur.execute("SELECT COUNT(*) FROM cultural_content")
    culture_count = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM temples")
    temple_count = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM user_queries")
    query_count = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM users")
    user_count = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM media")
    media_count = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM media WHERE media_type='image'")
    img_count = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM media WHERE media_type='audio'")
    audio_count = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM media WHERE media_type='video'")
    video_count = cur.fetchone()[0]

    # Recent AI queries
    cur.execute("SELECT * FROM user_queries ORDER BY asked_at DESC LIMIT 8")
    recent_queries = cur.fetchall()

    # Culture by category
    cur.execute("""SELECT category, COUNT(*) as cnt
                   FROM cultural_content
                   GROUP BY category
                   ORDER BY cnt DESC""")
    culture_by_cat = cur.fetchall()

    cur.close()

    return render_template('admin/dashboard.html',
        culture_count=culture_count,
        temple_count=temple_count,
        query_count=query_count,
        user_count=user_count,
        media_count=media_count,
        img_count=img_count,
        audio_count=audio_count,
        video_count=video_count,
        recent_queries=recent_queries,
        culture_by_cat=culture_by_cat,
    )

@app.route('/admin/add_culture', methods=['GET','POST'])
def add_culture():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    success = None
    if request.method == 'POST':
        title = request.form['title']
        category = request.form['category']
        description = request.form['description']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO cultural_content (title,category,description) VALUES (%s,%s,%s)",
                    (title, category, description))
        mysql.connection.commit()
        cur.close()
        success = 'Content added!'
    return render_template('admin/add_culture.html', success=success)

@app.route('/admin/add_temple', methods=['GET','POST'])
def add_temple():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    success = None
    if request.method == 'POST':
        name = request.form['name']
        location = request.form['location']
        description = request.form['description']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO temples (name,location,description) VALUES (%s,%s,%s)",
                    (name, location, description))
        mysql.connection.commit()
        cur.close()
        success = 'Temple added!'
    return render_template('admin/add_temple.html', success=success)

@app.route('/admin/upload_media', methods=['GET','POST'])
def upload_media():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))

    success = None
    error = None

    if request.method == 'POST':
        title = request.form.get('title','').strip()
        section = request.form.get('section','gallery')
        description = request.form.get('description','')
        file = request.files.get('file')

        if not title:
            error = 'Title is required!'
        elif file and file.filename:
            filename = secure_filename(file.filename)
            ext = filename.rsplit('.',1)[-1].lower() if '.' in filename else ''

            if ext in ALLOWED_IMG:
                mtype = 'image'
                folder = f'static/images/{section}'
            elif ext in ALLOWED_AUD:
                mtype = 'audio'
                folder = 'static/audio'
            elif ext in ALLOWED_VID:
                mtype = 'video'
                folder = 'static/videos'
            else:
                error = f'File type .{ext} not supported! Use jpg/png/mp3/mp4.'
                return render_template('admin/upload_media.html',
                    error=error, success=None,
                    all_media=get_all_media(), stats=get_media_stats())

            os.makedirs(folder, exist_ok=True)

            # Unique filename to avoid overwriting
            import time
            base = filename.rsplit('.',1)[0]
            unique_filename = f"{base}_{int(time.time())}.{ext}"
            filepath = os.path.join(folder, unique_filename)
            file.save(filepath)
            db_path = filepath.replace('static/', '')

            cur = mysql.connection.cursor()
            cur.execute("""INSERT INTO media
                (title, media_type, file_path, section, description)
                VALUES (%s,%s,%s,%s,%s)""",
                (title, mtype, db_path, section, description))
            mysql.connection.commit()
            cur.close()
            success = f'✅ {mtype.capitalize()} "{title}" uploaded successfully to {section} section!'
        else:
            error = 'Please select a file to upload!'

    # Get YouTube videos data
    yt_vids = []
    yt_temples = yt_culture = yt_festival = yt_gallery = 0
    try:
        cur2 = mysql.connection.cursor()
        cur2.execute("SELECT * FROM youtube_videos ORDER BY added_at DESC")
        yt_vids = cur2.fetchall()
        cur2.execute("SELECT COUNT(*) FROM youtube_videos WHERE section='temples'")
        yt_temples = cur2.fetchone()[0]
        cur2.execute("SELECT COUNT(*) FROM youtube_videos WHERE section='culture'")
        yt_culture = cur2.fetchone()[0]
        cur2.execute("SELECT COUNT(*) FROM youtube_videos WHERE section='festival'")
        yt_festival = cur2.fetchone()[0]
        cur2.execute("SELECT COUNT(*) FROM youtube_videos WHERE section='gallery'")
        yt_gallery = cur2.fetchone()[0]
        cur2.close()
    except:
        pass

    return render_template('admin/upload_media.html',
        success=success, error=error,
        all_media=get_all_media(),
        stats=get_media_stats(),
        yt_videos=yt_vids,
        yt_temples=yt_temples,
        yt_culture=yt_culture,
        yt_festival=yt_festival,
        yt_gallery=yt_gallery)


@app.route('/admin/delete_media/<int:media_id>', methods=['POST'])
def delete_media(media_id):
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))

    cur = mysql.connection.cursor()
    cur.execute("SELECT file_path, title FROM media WHERE id=%s", (media_id,))
    media = cur.fetchone()

    if media:
        # Delete file from disk
        try:
            filepath = os.path.join('static', media[0])
            if os.path.exists(filepath):
                os.remove(filepath)
        except Exception as e:
            print(f"File delete error: {e}")

        # Delete from database
        cur.execute("DELETE FROM media WHERE id=%s", (media_id,))
        mysql.connection.commit()
        success_msg = f'✅ "{media[1]}" deleted successfully!'
    else:
        success_msg = 'Media not found.'

    cur.close()

    # Redirect back to upload page
    from flask import request as req
    referer = req.referrer or url_for('upload_media')
    return redirect(url_for('upload_media') + '?deleted=1')

@app.route('/admin/queries')
def admin_queries():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM user_queries ORDER BY asked_at DESC")
    queries = cur.fetchall()
    cur.close()
    return render_template('admin/queries.html', queries=queries)

@app.route('/admin/users')
def admin_users():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, name, email, joined_at FROM users ORDER BY joined_at DESC")
    users = cur.fetchall()
    cur.close()
    return render_template('admin/users.html', users=users)

import secrets
from datetime import datetime, timedelta

# ─────────────────────────────────────
#  FORGOT PASSWORD
# ─────────────────────────────────────

@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    message = None
    error = None
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        cur = mysql.connection.cursor()
        cur.execute("SELECT id, name FROM users WHERE email=%s", (email,))
        user = cur.fetchone()
        if user:
            # Generate reset token
            token = secrets.token_urlsafe(32)
            cur.execute(
                "INSERT INTO password_resets (email, token) VALUES (%s, %s)",
                (email, token)
            )
            mysql.connection.commit()
            # In real app you'd send email — here we show the reset link directly
            reset_link = f"/reset-password/{token}"
            message = f"Reset link generated! Click here to reset your password."
            cur.close()
            return render_template('forgot_password.html',
                message=message, reset_link=reset_link, email=email)
        else:
            error = "No account found with that email address."
        cur.close()
    return render_template('forgot_password.html', message=message, error=error)


@app.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    error = None
    success = None
    cur = mysql.connection.cursor()
    # Check token valid and not used and not expired (30 min)
    cur.execute("""
        SELECT email FROM password_resets
        WHERE token=%s AND used=0
        AND created_at > NOW() - INTERVAL 30 MINUTE
    """, (token,))
    row = cur.fetchone()
    if not row:
        cur.close()
        return render_template('reset_password.html',
            error='This reset link has expired or already been used. Please request a new one.',
            token=token, expired=True)
    email = row[0]
    if request.method == 'POST':
        password = request.form.get('password', '')
        confirm = request.form.get('confirm', '')
        if len(password) < 6:
            error = 'Password must be at least 6 characters!'
        elif password != confirm:
            error = 'Passwords do not match!'
        else:
            new_hash = hash_password(password)
            cur.execute("UPDATE users SET password=%s WHERE email=%s",
                        (new_hash, email))
            cur.execute("UPDATE password_resets SET used=1 WHERE token=%s",
                        (token,))
            mysql.connection.commit()
            cur.close()
            return render_template('reset_password.html',
                success='✅ Password reset successfully! You can now login.',
                token=token)
    cur.close()
    return render_template('reset_password.html',
        error=error, token=token, email=email)


# ─────────────────────────────────────
#  EDIT MEDIA
# ─────────────────────────────────────

@app.route('/admin/edit_media/<int:media_id>', methods=['GET', 'POST'])
def edit_media(media_id):
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM media WHERE id=%s", (media_id,))
    media = cur.fetchone()
    if not media:
        cur.close()
        return redirect(url_for('upload_media'))
    success = None
    error = None
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        section = request.form.get('section', '')
        description = request.form.get('description', '')
        new_file = request.files.get('new_file')
        if not title:
            error = 'Title is required!'
        else:
            # Check if new file uploaded
            if new_file and new_file.filename:
                filename = secure_filename(new_file.filename)
                ext = filename.rsplit('.', 1)[-1].lower() if '.' in filename else ''
                if ext in ALLOWED_IMG:
                    mtype = 'image'
                    folder = f'static/images/{section}'
                elif ext in ALLOWED_AUD:
                    mtype = 'audio'
                    folder = 'static/audio'
                elif ext in ALLOWED_VID:
                    mtype = 'video'
                    folder = 'static/videos'
                else:
                    error = f'File type .{ext} not supported!'
                    cur.close()
                    return render_template('admin/edit_media.html',
                        media=media, error=error)
                import time
                base = filename.rsplit('.', 1)[0]
                unique_fn = f"{base}_{int(time.time())}.{ext}"
                os.makedirs(folder, exist_ok=True)
                filepath = os.path.join(folder, unique_fn)
                new_file.save(filepath)
                db_path = filepath.replace('static/', '')
                # Delete old file
                try:
                    old_path = os.path.join('static', media[3])
                    if os.path.exists(old_path):
                        os.remove(old_path)
                except:
                    pass
                cur.execute("""UPDATE media SET title=%s, section=%s,
                    description=%s, media_type=%s, file_path=%s WHERE id=%s""",
                    (title, section, description, mtype, db_path, media_id))
            else:
                cur.execute("""UPDATE media SET title=%s, section=%s,
                    description=%s WHERE id=%s""",
                    (title, section, description, media_id))
            mysql.connection.commit()
            success = '✅ Media updated successfully!'
            cur.execute("SELECT * FROM media WHERE id=%s", (media_id,))
            media = cur.fetchone()
    cur.close()
    return render_template('admin/edit_media.html',
        media=media, success=success, error=error)

# ─────────────────────────────────────
#  YOUTUBE VIDEOS
# ─────────────────────────────────────

def extract_youtube_id(url):
    """Extract YouTube video ID from any YouTube URL format"""
    import re
    if not url:
        return None
    # youtu.be/ID
    m = re.search(r'youtu\.be/([a-zA-Z0-9_-]{11})', url)
    if m: return m.group(1)
    # youtube.com/watch?v=ID
    m = re.search(r'[?&]v=([a-zA-Z0-9_-]{11})', url)
    if m: return m.group(1)
    # youtube.com/embed/ID
    m = re.search(r'embed/([a-zA-Z0-9_-]{11})', url)
    if m: return m.group(1)
    # Just the ID itself
    if re.match(r'^[a-zA-Z0-9_-]{11}$', url):
        return url
    return None


@app.route('/admin/add_youtube', methods=['POST'])
def add_youtube():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    title = request.form.get('title', '').strip()
    youtube_url = request.form.get('youtube_url', '').strip()
    section = request.form.get('section', 'gallery')
    category = request.form.get('category', 'general')
    description = request.form.get('description', '')
    video_id = extract_youtube_id(youtube_url)
    if not title or not video_id:
        return redirect(url_for('upload_media') +
            '?error=Invalid YouTube URL&tab=youtube')
    cur = mysql.connection.cursor()
    cur.execute("""INSERT INTO youtube_videos
        (title, youtube_url, video_id, section, category, description)
        VALUES (%s,%s,%s,%s,%s,%s)""",
        (title, youtube_url, video_id, section, category, description))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('upload_media') + '#sec-youtube')


@app.route('/admin/delete_youtube/<int:vid_id>', methods=['POST'])
def delete_youtube(vid_id):
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM youtube_videos WHERE id=%s", (vid_id,))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('upload_media') + '#sec-youtube')


@app.route('/admin/edit_youtube/<int:vid_id>', methods=['GET', 'POST'])
def edit_youtube(vid_id):
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM youtube_videos WHERE id=%s", (vid_id,))
    video = cur.fetchone()
    if not video:
        return redirect(url_for('upload_media'))
    success = None
    error = None
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        youtube_url = request.form.get('youtube_url', '').strip()
        section = request.form.get('section', 'gallery')
        category = request.form.get('category', 'general')
        description = request.form.get('description', '')
        video_id = extract_youtube_id(youtube_url)
        if not title or not video_id:
            error = 'Invalid YouTube URL!'
        else:
            cur.execute("""UPDATE youtube_videos SET
                title=%s, youtube_url=%s, video_id=%s,
                section=%s, category=%s, description=%s
                WHERE id=%s""",
                (title, youtube_url, video_id,
                 section, category, description, vid_id))
            mysql.connection.commit()
            success = '✅ YouTube video updated!'
            cur.execute("SELECT * FROM youtube_videos WHERE id=%s", (vid_id,))
            video = cur.fetchone()
    cur.close()
    return render_template('admin/edit_youtube.html',
        video=video, success=success, error=error)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)