from flask import render_template, session, request, jsonify, Flask
from flask_cors import CORS
from models.user import User, Album, Song, Creator, Playlist, PlaylistSongs, Admin #, Role  # Assuming your User model is defined in models/user.py
from config import app,db
# from flask_security import Security, SQLAlchemyUserDatastore, UserMixin, RoleMixin
from flask_security.utils import hash_password
# from flask.cli import with_appcontext
# import click
from datetime import datetime
from sqlalchemy import func
CORS(app)
from tasks import send_email  # Import the Celery task
# CORS(app, resources={r"/api/*": {"origins": "http://localhost:5173"}})

# user_datastore = SQLAlchemyUserDatastore(db, User, Role)
# security = Security(app, user_datastore)
from flask_jwt_extended import JWTManager
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

app.secret_key = 'SECRET_KEY'

# @click.command(name='create_roles_and_migrate_admins')
# @with_appcontext
# def create_roles_and_migrate_admins():
#     # Ensure the 'admin' role exists
#     admin_role = Role.query.filter_by(name='admin').first()
#     if not admin_role:
#         admin_role = Role(name='admin')
#         db.session.add(admin_role)
#         db.session.commit()

#     # Migrate Admin users to User
#     for admin in Admin.query.all():
#         # Check if the user already exists to avoid duplicates
#         if not User.query.filter_by(email=admin.username).first():
#             user = User(email=admin.username, password=hash_password(admin.password), active=True)
#             user.roles.append(admin_role)
#             db.session.add(user)
#     db.session.commit()

# app.cli.add_command(create_roles_and_migrate_admins)

# @app.cli.command('init-db')
# def init_db_command():
#     """Initialize the database."""
#     with app.app_context():
#         admin_role = Role.query.filter_by(name='admin').first()
#         if not admin_role:
#             admin_role = Role(name='admin')
#             db.session.add(admin_role)
#             db.session.commit()
#         # Add more initialization logic as needed.
#         print('Database initialized.')

app.config['JWT_SECRET_KEY'] = 'your-secret-key'  # Change this to a more secure key, and consider loading it from an environment variable
jwt = JWTManager(app)

@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

@app.route('/')
def login_template():
    return render_template('login.html')

@app.route('/health')
def health():
    return jsonify({"message": "Health of server is 100%"})

@app.route('/login-validation', methods=['POST'])
def login_validation():
    data = request.json
    uname = data.get('username')
    password = data.get('password')
    
    existing_user = User.get_user_by_uname(uname)
    # print(uname) 
    if existing_user and existing_user.password == password:
        session['username'] = uname
        send_email.delay(uname, "Log-in Successful!")
        access_token = create_access_token(identity=uname)
        return jsonify({'message': f'Welcome Back {uname}', 'username': uname}), 200
    else:
        return jsonify({'message': 'Invalid Credentials'}), 401

@app.route('/register-validation', methods=['POST'])
def register_validation():
    try:
        # Allow requests from the specified origin
        print(request)
        if request.method == 'OPTIONS':
            response = jsonify({'message': 'Preflight request received'})
            response.headers.add('Access-Control-Allow-Origin', 'http://localhost:5173')  # Adjust the origin as needed
            return response

        data = request.json
        username = data.get('username')
        password = data.get('password')
        # Check if username already exists
        if User.get_user_by_uname(username):
            return jsonify({'message': 'Username already exists'}), 400

        # # Create new user
        User.create_user(username, password)
        
        send_email.delay(username, "Welcome to our service!")  
        
        return jsonify({'message': 'User created successfully'}), 201
    except Exception as e:
        return jsonify({'message': f'Error: {e}'}), 500

@app.route('/check-creator', methods=['POST'])
def check_creator():
    try:
        data = request.json
        # username = session.get('username') 
        username = data.get('username') 
        print(username) 
        # Check if the creator already exists
        creator = Creator.query.filter_by(username=username).first()
        
        if creator:
            print("yes") 
            return jsonify({'creatorExists': True, 'username': creator.username}), 200
        else:
            print("no")
            return jsonify({'creatorExists': False}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/register-creator', methods=['POST'])
def register_creator():
    try:
        data = request.json
        username = data.get('username')
        password = data.get('password')
        number_of_albums = 0  # Assuming a new creator starts with 0 albums

        # Check if the creator already exists
        existing_creator = Creator.query.filter_by(username=username).first()
        if existing_creator:
            return jsonify({'message': 'This username is already taken by another creator'}), 400

        # Create new creator
        new_creator = Creator.create_creator(username=username, password=password, number_of_albums=number_of_albums)

        return jsonify({'message': f'Creator {username} registered successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/upload-song', methods=['POST'])
def upload_song():
    data = request.json                     # Extracting data from request
    # username = session.get('username')
    username = data.get('username')
    title = data.get('title')
    singer = data.get('singer')
    album_name = data.get('album')
    release_date = data.get('releaseDate')  # Ensure consistent naming
    lyrics = data.get('lyrics')
    genre = data.get('genre')
    print(username, title, singer, album_name, release_date, lyrics, genre)     # Validate required information 
    if not all([username, title, singer, album_name, release_date, lyrics, genre]):
        return jsonify({'message': 'All fields are required.'}), 400
    # Fetch the creator by username
    creator = Creator.query.filter_by(username=username).first()
    if not creator:
        return jsonify({'message': 'Creator not found.'}), 404      # Check for existing album by this creator
    album = Album.query.filter_by(album_name=album_name, creator_id=creator.id).first()
    if not album:
        album = Album(album_name=album_name, creator_id=creator.id)
        db.session.add(album)
        db.session.flush()
        creator.number_of_albums += 1
    if release_date:
        try:                        # Convert release_date string to date object
            release_date_obj = datetime.strptime(release_date, '%Y-%m-%d').date()
        except ValueError:
            return jsonify({'message': 'Invalid date format. Please use YYYY-MM-DD.'}), 400
    else:
        release_date_obj = None      
    try:                        # Create the song
        new_song = Song(name=title, singer_name=singer, release_date=release_date_obj, lyrics=lyrics, creator_id=creator.id, album_id=album.id, genre=genre,rating = 0)
        db.session.add(new_song)
        db.session.commit() 
        return jsonify({'message': 'Song uploaded successfully.'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Failed to upload the song.', 'error': str(e)}), 500
# name=title, singer_name=singer, release_date=release_date, lyrics=lyrics, creator=creator, album=album,genre=genre,rating=0

@app.route('/genres-and-songs', methods=['GET'])
def get_genres_and_songs():
    try:
        # Query the database to retrieve distinct genres
        genres = db.session.query(Song.genre).distinct().all()

        # Create a dictionary to store genres and their associated songs
        genres_and_songs = []

        # Iterate over each genre
        for genre in genres:
            genre_name = genre[0]
            
            # Query the database to retrieve songs for the current genre
            songs = Song.query.filter_by(genre=genre_name).all()

            # Create a list to store song details for the current genre
            genre_songs = []

            # Iterate over each song and append its details to the genre_songs list
            for song in songs:
                genre_songs.append({
                    'id': song.id,
                    'name': song.name,
                    'singer_name': song.singer_name,
                    # Add more song attributes as needed
                })

            # Append genre and its associated songs to the genres_and_songs list
            genres_and_songs.append({
                'genre': genre_name,
                'songs': genre_songs
            })

        # Return genres and their associated songs as JSON response
        return jsonify(genres_and_songs), 200
    except Exception as e:
        # Handle exceptions and return an error response
        return jsonify({'error': str(e)}), 500

# route for AddToPlaylist Page
@app.route('/playlists/<int:playlist_id>/add-song', methods=['POST'])
def add_song_to_playlist(playlist_id):
    try:
        # Retrieve data from the request
        data = request.json
        username = data.get('username')  # Assume username is passed in request
        song_id = data.get('song_id')
        print(username, song_id) 
        # Retrieve the user
        user = User.query.filter_by(username=username).first()
        if not user:
            return jsonify({'message': 'User not found'}), 404

        # Retrieve the playlist
        playlist = Playlist.query.filter_by(id=playlist_id, username=username).first()
        if not playlist:
            return jsonify({'message': 'Playlist not found'}), 404

        # Retrieve the song
        song = Song.query.get(song_id)
        if not song:
            return jsonify({'message': 'Song not found'}), 404
        
        # Check if the song is already in the playlist
        if song in playlist.songs:
            return jsonify({'message': 'Song already in playlist'}), 409

        # Add the song to the playlist
        playlist.songs.append(song)
        db.session.commit()

        return jsonify({'message': 'Song added to playlist successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# For User View Songs Page 
@app.route('/playlists/<int:playlist_id>/remove-song', methods=['POST'])
def remove_song_from_playlist(playlist_id):
    data = request.json
    username = data.get('username')  # Assume username is passed in request
    playlist_id = data.get('playlist_id')
    song_id = data.get('song_id')
    
    
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({'message': 'User not found'}), 404

    playlist = Playlist.query.filter_by(id=playlist_id, username=username).first() 
    if not playlist:
        return jsonify({'message': 'Playlist not found'}), 404

    song = Song.query.get(song_id)
    if song not in playlist.songs:
        return jsonify({'message': 'Song not found in playlist'}), 404

    playlist.songs.remove(song)
    db.session.commit()

    return jsonify({'message': 'Song removed from playlist successfully'}), 200


@app.route('/playlists/create', methods=['POST'])
def create_playlist():
    try:
        data = request.json
        username = data.get('username')
        playlist_name = data.get('name')

        if not username:
            return jsonify({'message': 'Username is required'}), 400

        if not playlist_name:
            return jsonify({'message': 'Playlist name is required'}), 400

        user = User.query.filter_by(username=username).first()
        if not user:
            return jsonify({'message': 'User not found'}), 404

        new_playlist = Playlist(name=playlist_name, username=username)  # Set the username
        db.session.add(new_playlist)

        db.session.commit()

        return jsonify({'message': 'Playlist created successfully', 'playlist_id': new_playlist.id}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/playlists/<int:playlist_id>/delete', methods=['DELETE'])
def delete_playlist(playlist_id):
    data = request.json
    username = data.get('username')  # Assume username is passed in request

    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({'message': 'User not found'}), 404

    playlist = Playlist.query.filter_by(id=playlist_id, username=username).first()
    if not playlist:
        return jsonify({'message': 'Playlist not found'}), 404

    db.session.delete(playlist)
    db.session.commit()

    return jsonify({'message': 'Playlist deleted successfully'}), 200


@app.route('/playlists', methods=['POST'])
def get_user_playlists():
    try:
        data = request.json
        # username = request.headers.get('username')  # Retrieve username from request headers
        username = data.get('username')
        print(username) 
        user = User.query.filter_by(username=username).first()
        if not user:
            return jsonify({'message': 'User not found'}), 404

        playlists = Playlist.query.filter_by(username=username).all()
        playlist_data = [{'id': playlist.id, 'name': playlist.name} for playlist in playlists]

        return jsonify({'playlists': playlist_data}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/playlists/songs', methods=['POST'])
def get_playlist_songs():
    try:
        data = request.json
        playlist_id = data.get('playlist_id')
        username = data.get('username')
        print(playlist_id,username) 
        if not playlist_id:
            return jsonify({'message': 'Playlist ID is required'}), 400
        if not username:
            return jsonify({'message': 'Username is required'}), 400
        # print("Stage 1") 
        user = User.query.filter_by(username=username).first()
        if not user:
            return jsonify({'message': 'User not found'}), 404
        # print("Stage 2") 
        playlist = Playlist.query.filter_by(id=playlist_id, username=username).first()
        print(playlist) 
        if not playlist:
            return jsonify({'message': 'Playlist not found'}), 404
        # print("Stage 3")  
        # Get songs belonging to the playlist #Error in the below line
        songs = (Song.query
                 .join(PlaylistSongs, PlaylistSongs.song_id == Song.id)
                 .filter(PlaylistSongs.playlist_id == playlist_id)
                 .filter(Playlist.username == username)
                 .all())

        # print("Stage 4")   
        # Format the songs data
        songs_data = [{
            'id': song.id,
            'name': song.name,
            'singer_name': song.singer_name,
            # Add more song attributes as needed
        } for song in songs]

        return jsonify({'songs': songs_data, 'name': playlist.name}), 200
        # return jsonify({'message': 'Everything fine'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Add these routes to your Flask app

@app.route('/creator/dashboard', methods=['POST'])
def get_creator_dashboard():
    try:
        data = request.json
        username = data.get('username')
        print(username) 
        creator = Creator.query.filter_by(username=username).first()
        if not creator:
            return jsonify({'message': 'Creator not found'}), 404

        total_songs_uploaded = len(creator.songs)
        total_albums = len(creator.albums)
        total_ratings = sum(song.rating for song in creator.songs)
        average_rating = total_ratings / total_songs_uploaded if total_songs_uploaded != 0 else 0

        return jsonify({
            'totalSongs': total_songs_uploaded,
            'averageRating': average_rating,
            'totalAlbums': total_albums,
            'albums': [{'id': album.id, 'name': album.album_name} for album in creator.albums]
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/albums/songs', methods=['POST'])
def get_album_songs():
    try:
        data = request.json
        album_id = data.get('album_id')
        username = data.get('username')
        
        if not album_id:
            return jsonify({'message': 'Album ID is required'}), 400
        if not username:
            return jsonify({'message': 'Username is required'}), 400

        user = User.query.filter_by(username=username).first()
         
        if not user:
            return jsonify({'message': 'User not found'}), 404

        album = Album.query.filter_by(id=album_id).first()
        if not album:
            return jsonify({'message': 'Album not found'}), 404
        
        # Get songs belonging to the album
        songs = Song.query.filter_by(album_id=album_id).all()
        
        # Format the songs data
        songs_data = [{
            'id': song.id,
            'name': song.name,
            'singer_name': song.singer_name,
            # Add more song attributes as needed
        } for song in songs]

        print(album_id,username) 
        return jsonify({'songs': songs_data, 'name': album.album_name}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/albums/<int:album_id>', methods=['DELETE'])
def delete_album(album_id):
    try:
        data = request.json
        username = data.get('username')

        creator = Creator.query.filter_by(username=username).first()
        if not creator:
            return jsonify({'message': 'Creator not found'}), 404

        album = Album.query.filter_by(id=album_id, creator_id=creator.id).first()
        if not album:
            return jsonify({'message': 'Album not found'}), 404

        # Decrement the number_of_albums attribute of the creator
        creator.number_of_albums -= 1
        
        db.session.delete(album)
        db.session.commit()

        return jsonify({'message': 'Album deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Route to fetch song details based on songId
@app.route('/fetch-song-details', methods=['POST'])
def fetch_song_details():
    try:
        data = request.json
        song_id = data.get('songId')

        # Retrieve song details from the database based on songId
        song = Song.query.get(song_id)
        if not song:
            return jsonify({'message': 'Song not found'}), 404
        print("fetch release_date",song.release_date)
        # Format the song details
        song_details = {
            'title': song.name,
            'singer': song.singer_name,
            'releaseDate': str(song.release_date),  # Assuming release_date is a datetime object
            'lyrics': song.lyrics,
            'genre': song.genre
            # Add more song attributes as needed
        }

        return jsonify({'song': song_details}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Route to update song details
@app.route('/update-song', methods=['POST'])
def update_song():
    try:
        data = request.json
        song_id = data.get('songId')
        print("Stage 1")
        # Retrieve the song from the database
        song = Song.query.get(song_id)  
        if not song:
            return jsonify({'message': 'Song not found'}), 404
        print("Stage 2") 
        # Update song details
        song.name = data.get('title')
        song.singer_name = data.get('singer')
        release_date_str = data.get('releaseDate')
        song.release_date = datetime.strptime(release_date_str, '%Y-%m-%d').date()
        song.lyrics = data.get('lyrics')
        song.genre = data.get('genre')
        # Update more song attributes as needed
        print("Stage 3")
        print("song_name",song.name)
        print("singer_name",song.singer_name)
        print("release_date",song.release_date)
        print("lyrics",song.lyrics)
        print("genre",song.genre)                
        # Commit the changes to the database
        # db.session.add(song)
        db.session.commit()
        print("Stage 4") 
        return jsonify({'message': 'Song details updated successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/songs/<int:song_id>', methods=['DELETE'])
def delete_song(song_id):
    try:
        # Retrieve the song from the database
        song = Song.query.get(song_id)
        if not song:
            return jsonify({'message': 'Song not found'}), 404
        
        # Delete the song
        db.session.delete(song)
        db.session.commit()

        return jsonify({'message': 'Song deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/rate-song', methods=['POST'])
def rate_song():
    try:
        data = request.json
        song_id = data.get('song_id')
        rating = data.get('rating')

        # Retrieve the song from the database
        song = Song.query.get(song_id)
        if not song:
            return jsonify({'message': 'Song not found'}), 404

        # Update the song rating
        song.rating = float(rating)

        # Save the changes to the database
        db.session.commit()

        return jsonify({'message': 'Song rating updated successfully'}), 200
    except Exception as e:
        # Handle exceptions
        return jsonify({'error': str(e)}), 500


@app.route('/search-by-name', methods=['POST'])
def search_by_name():
    try:
        data = request.json  # Extract JSON data from the request
        name = data.get('name')  # Extract the song name from the data

        if not name:
            return jsonify({'message': 'Song name is required'}), 400

        # Search for songs by name in the database
        songs = Song.query.filter(Song.name.ilike(f'%{name}%')).all()

        if not songs:
            return jsonify({'message': 'No songs found with the given name'}), 404

        # Format the songs data
        songs_data = [{
            'id': song.id,
            'name': song.name,
            'singer_name': song.singer_name,
            # Add more song attributes as needed
        } for song in songs]

        return jsonify({'songs': songs_data}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/search-by-rating', methods=['POST'])
def search_by_rating():
    try:
        data = request.json
        rating = data.get('rating')

        if not rating:
            return jsonify({'message': 'Rating is required'}), 400

        songs = Song.query.filter_by(rating=rating).all()

        if not songs:
            return jsonify({'message': 'No songs found with the given rating'}), 404

        songs_data = [{
            'id': song.id,
            'name': song.name,
            'singer_name': song.singer_name,
            # Add more song attributes as needed
        } for song in songs]

        return jsonify({'songs': songs_data}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/search-by-genre', methods=['POST'])
def search_by_genre():
    try:
        data = request.json
        genre = data.get('genre')

        if not genre:
            return jsonify({'message': 'Genre is required'}), 400

        songs = Song.query.filter_by(genre=genre).all()

        if not songs:
            return jsonify({'message': 'No songs found with the given genre'}), 404

        songs_data = [{
            'id': song.id,
            'name': song.name,
            'singer_name': song.singer_name,
            # Add more song attributes as needed
        } for song in songs]

        return jsonify({'songs': songs_data}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/search-by-album', methods=['POST'])
def search_by_album():
    try:
        data = request.json
        album = data.get('album')

        if not album:
            return jsonify({'message': 'Album name is required'}), 400

        songs = Song.query.join(Album).filter(Album.album_name.ilike(f'%{album}%')).all()

        if not songs:
            return jsonify({'message': 'No songs found in the given album'}), 404

        songs_data = [{
            'id': song.id,
            'name': song.name,
            'singer_name': song.singer_name,
            # Add more song attributes as needed
        } for song in songs]

        return jsonify({'songs': songs_data}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# @app.route('/insert-admin-data', methods=['POST'])
# def insert_admin_data_route():
#     try:
#         admin = Admin(username='yash', password='yash')
#         db.session.add(admin)
#         db.session.commit()
#         return jsonify({'message': 'Admin data inserted successfully'}), 200
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

@app.route('/admin-login', methods=['POST'])
def admin_login():
    
    try:
        data = request.json
        admin_username = data.get('username')
        admin_password = data.get('password')
        
        # Query the Admin table to fetch the admin with the provided username
        admin = Admin.query.filter_by(username=admin_username).first()
        
        
        # If admin with provided username exists, verify the password
        if admin:
            if admin.username == admin_username and admin.password == admin_password:
                return jsonify({'message': f'Welcome, {admin_username}! You are now logged in as admin.'}), 200
            else:
                return jsonify({'message': 'Invalid password for admin'}), 401
        else:
            return jsonify({'message': 'Admin not found'}), 404

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/admin/dashboard', methods=['GET'])
def admin_dashboard():
    try:
        total_users = User.query.count()
        total_creators = Creator.query.count()
        total_songs = Song.query.count()

        total_ratings = db.session.query(func.sum(Song.rating)).scalar()
        total_songs_with_rating = Song.query.filter(Song.rating.isnot(None)).count()
        average_rating_all_songs = total_ratings / total_songs_with_rating if total_songs_with_rating > 0 else 0

        creators = Creator.query.all()
        genres = db.session.query(Song.genre).distinct().all()

        formatted_genres = [genre[0] for genre in genres]

        return jsonify({
            'totalUsers': total_users,
            'totalCreators': total_creators,
            'totalSongs': total_songs,
            'averageRatingAllSongs': average_rating_all_songs,
            'creators': [{'id': creator.id, 'username': creator.username} for creator in creators],
            'genres': formatted_genres
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/admin/songs', methods=['GET'])
def get_admin_songs():
    try:
        songs = Song.query.all()  # Query all songs
        songs_data = [{
            'id': song.id,
            'name': song.name,
            'singer_name': song.singer_name,
            # Add more song attributes as needed
        } for song in songs]
        return jsonify({'songs': songs_data}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/fetch-song-lyrics', methods=['POST'])
def fetch_song_lyrics():
    try:
        data = request.json
        song_id = data.get('songId')

        # Retrieve song details from the database based on songId
        song = Song.query.get(song_id)
        if not song:
            return jsonify({'message': 'Song not found'}), 404

        # Return the lyrics of the song
        return jsonify({'lyrics': song.lyrics}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/remove_creator', methods=['POST','DELETE'])
def remove_creator():
    creator_id = request.json.get('creator_id')
    if creator_id:
        creator = Creator.query.get(creator_id)
        if creator:
            db.session.delete(creator)
            db.session.commit()
            return jsonify({'message': 'Creator, albums, and songs removed successfully.'}), 200
        else:
            return jsonify({'error': 'Creator not found.'}), 404
    else:
        return jsonify({'error': 'Creator ID not provided.'}), 400



if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
