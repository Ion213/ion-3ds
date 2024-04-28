#libraries needed
from flask import (
    Blueprint, 
    render_template, 
    request, 
    redirect, 
    url_for, 
    flash,
    jsonify
)
from flask_login import (
                        LoginManager,
                         login_user,
                         logout_user,
                         login_required,
                         current_user
                         )


from website import db
from website.models.database_models import Games, Links

admin_views = Blueprint('admin_views', __name__)

#add GAMES
@admin_views.route('/add_games', methods=['GET', 'POST'])
@login_required
def add_games():
    if request.method == 'POST':
        try:
            game_name = request.form.get('gamename')
            existing_game = Games.query.filter_by(game_name=game_name).first()
            if existing_game:
                flash('Game with this name already exists', category='manage_games_error')
            else:
                game = Games(game_name=game_name)
                db.session.add(game)
                db.session.commit()
                flash('Game created successfully', category='manage_games_success')
        except Exception as e:
            flash(str(e), category='manage_games_error')

    games = Games.query.all()

    return render_template('admin_manage_game.html', games=games)


#update games
@admin_views.route('/update_game', methods=['POST'])
@login_required
def update_game():
    if request.method == 'POST':
        try:
            game_id = request.form.get('updateGameId')
            new_game_name = request.form.get('updateGameName')
            
            if not new_game_name.strip():
                return jsonify({'error': 'Game name cannot be empty'}), 400
            
            game = Games.query.get(game_id)
            if game:
                # Check if a game with the new name already exists
                existing_game = Games.query.filter_by(game_name=new_game_name).first()
                if existing_game and existing_game.id != game_id:
                    return jsonify({'error': 'Game with that name already exists'}), 400
                
                game.game_name = new_game_name
                db.session.commit()
                return jsonify({'message': 'Game updated successfully'})
            else:
                return jsonify({'error': 'Game not found'}), 404

        except Exception as e:
            return jsonify({'error': str(e)}), 500

#DELETE GAMES
@admin_views.route('/delete_game/<int:game_id>', methods=['POST'])
@login_required
def delete_game(game_id):
    if request.method == 'POST':
        try:
            game = Games.query.get(game_id)
            Links.query.filter_by(game_id=game.id).delete()
            db.session.delete(game)
            db.session.commit()
            flash('Game deleted successfully', 'manage_games_success')
            return redirect(url_for('admin_views.add_games'))
        except Exception as e:
            flash(str(e), category='manage_games_error')
            
    games = Games.query.all()
    return redirect(url_for('admin_views.add_games',games=games))


#ADD LINKS
@admin_views.route('/add_links/<int:game_id>', methods=['GET', 'POST'])
@login_required
def add_links(game_id):
    game = Games.query.get(game_id)

    if request.method == 'POST':
        try:
            links = request.form.get('link')
            existing_link = Links.query.filter_by(game_id=game_id, url=links).first()
            if existing_link:
                flash('link already exists for this game', category='manage_links_error') 
            else:               
                link = Links(game_id=game.id, url=links)
                db.session.add(link)
                db.session.commit()
                flash('Game Link added successfully', category='manage_links_success')
        except Exception as e:
            flash(str(e), category='manage_links_error')
 
    return render_template('admin_manage_link.html', game=game, links=game.links)


# Update LINKS
@admin_views.route('/update_link/<int:link_id>', methods=['POST'])
@login_required
def update_link(link_id):
    if request.method == 'POST':
        try:
            new_link = request.form.get('updateLink')
            if not new_link.strip():
                return jsonify({'error': 'Link cannot be empty'}), 400

            link = Links.query.get(link_id)
            if link:
                existing_link = Links.query.filter_by(game_id=link.game_id, url=new_link).first()
                if existing_link and existing_link.id != link_id:
                    return jsonify({'error': 'Link already exists for this game'}), 400

                link.url = new_link
                db.session.commit()
                return jsonify({'message': 'Link updated successfully'})
            else:
                return jsonify({'error': 'Link not found'}), 404

        except Exception as e:
            return jsonify({'error': str(e)}), 500


#delete LINKS
@admin_views.route('/delete_links/<int:link_id>', methods=['POST'])
@login_required
def delete_links(link_id):
    link = Links.query.get(link_id)
    if request.method == 'POST':
        if link is None:
            flash('Link not found', category='manage_links_error')
            return redirect(url_for('admin_views.add_links'))

        if request.method == 'POST':
            try:
                db.session.delete(link)
                db.session.commit()
                flash('Link deleted successfully', category='manage_links_success')
            except Exception as e:
                flash(str(e), category='manage_links_error')

    return redirect(url_for('admin_views.add_links', game_id=link.game_id))
