from flask import Flask, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
import plotly.express as px
import plotly.graph_objects as go
import plotly.utils
import json
from data_loader import load_all_health_data
from analysis_utils import calculate_statistics, create_health_indicators_chart

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///health_data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# User model for future authentication
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

@app.route('/')
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
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0') 