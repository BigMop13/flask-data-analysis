from flask import Flask, render_template, jsonify
from flask_login import LoginManager, login_required
import plotly.express as px
import plotly.graph_objects as go
import plotly.utils
import json
from data_loader import load_all_health_data
from analysis_utils import calculate_statistics, create_health_indicators_chart
from models import db, User, login_manager
from auth import auth
import os
import time
from sqlalchemy.exc import OperationalError

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///health_data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

# Register blueprints
app.register_blueprint(auth)

# Create database tables with retry logic
def init_db():
    max_retries = 5
    retry_delay = 2  # seconds
    
    for attempt in range(max_retries):
        try:
            with app.app_context():
                db.create_all()
            print("Database initialized successfully")
            return
        except OperationalError as e:
            if attempt < max_retries - 1:
                print(f"Database initialization attempt {attempt + 1} failed. Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                print("Failed to initialize database after multiple attempts")
                raise

init_db()

@app.route('/')
@login_required
def index():
    try:
        dfs = load_all_health_data()
        years = [str(year) for year in range(2017, 2024)]
        
        # Create doctors and nurses trend chart
        poland_data = dfs['doctors'][dfs['doctors']['Kod'] == '0000000']
        doctors_data = poland_data[[f'lekarze;{year};[osoba]' for year in years]].values[0]
        nurses_data = poland_data[[f'pielęgniarki łącznie z mgr pielęgniarstwa;{year};[osoba]' for year in years]].values[0]
        
        fig1 = px.line(
            x=years,
            y=[doctors_data, nurses_data],
            labels={'x': 'Rok', 'y': 'Liczba osób', 'variable': 'Kategoria'},
            title='Liczba lekarzy i pielęgniarek w Polsce (2017-2023)'
        )
        fig1.data[0].name = 'Lekarze'
        fig1.data[1].name = 'Pielęgniarki'
        
        # Create health indicators chart
        fig2 = create_health_indicators_chart(dfs)
        
        # Create regional distribution chart for 2023
        regional_data = dfs['doctors'][dfs['doctors']['Kod'] != '0000000'].sort_values('lekarze;2023;[osoba]', ascending=False)
        fig3 = px.bar(
            regional_data,
            x='Nazwa',
            y='lekarze;2023;[osoba]',
            title='Liczba lekarzy według województw (2023)',
            labels={'Nazwa': 'Województwo', 'lekarze;2023;[osoba]': 'Liczba lekarzy'}
        )
        
        # Calculate statistics
        stats = calculate_statistics(dfs)
        
        return render_template('index.html',
                             plot1=json.dumps(fig1, cls=plotly.utils.PlotlyJSONEncoder),
                             plot2=json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder),
                             plot3=json.dumps(fig3, cls=plotly.utils.PlotlyJSONEncoder),
                             years=years,
                             stats=stats)
    except Exception as e:
        return f"Wystąpił błąd: {str(e)}", 500

@app.route('/get_regional_data/<year>')
@login_required
def get_regional_data(year):
    try:
        dfs = load_all_health_data()
        regional_data = dfs['doctors'][dfs['doctors']['Kod'] != '0000000'].sort_values(f'lekarze;{year};[osoba]', ascending=False)
        
        fig = px.bar(
            regional_data,
            x='Nazwa',
            y=f'lekarze;{year};[osoba]',
            title=f'Liczba lekarzy według województw ({year})',
            labels={'Nazwa': 'Województwo', f'lekarze;{year};[osoba]': 'Liczba lekarzy'}
        )
        
        return jsonify({
            'plot': json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0') 