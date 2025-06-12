import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# Poland's population (approximate values for 2017-2023)
population = {
    '2017': 38433600,
    '2018': 38386000,
    '2019': 38383000,
    '2020': 38369000,
    '2021': 38187000,
    '2022': 37697000,
    '2023': 37400000
}

def calculate_statistics(dfs):
    years = [str(year) for year in range(2017, 2024)]
    stats = {}
    
    for year in years:
        # Get Poland's data (Kod 0000000)
        poland_hospitals = dfs['hospitals'][dfs['hospitals']['Kod'] == '0000000']
        poland_doctors = dfs['doctors'][dfs['doctors']['Kod'] == '0000000']
        poland_expenditure = dfs['expenditure'][dfs['expenditure']['Kod'] == '0000000']
        poland_deaths = dfs['deaths'][dfs['deaths']['Kod'] == '0000000']
        
        stats[year] = {
            # Doctors and nurses statistics
            'total_doctors': dfs['doctors'][f'lekarze;{year};[osoba]'].sum(),
            'total_nurses': dfs['doctors'][f'pielęgniarki łącznie z mgr pielęgniarstwa;{year};[osoba]'].sum(),
            'avg_doctors_per_region': dfs['doctors'][dfs['doctors']['Kod'] != '0000000'][f'lekarze;{year};[osoba]'].mean(),
            'max_doctors_region': dfs['doctors'].loc[dfs['doctors'][f'lekarze;{year};[osoba]'].idxmax(), 'Nazwa'],
            'min_doctors_region': dfs['doctors'].loc[dfs['doctors'][f'lekarze;{year};[osoba]'].idxmin(), 'Nazwa'],
            'doctor_nurse_ratio': dfs['doctors'][f'pielęgniarki łącznie z mgr pielęgniarstwa;{year};[osoba]'].sum() != 0 and dfs['doctors'][f'lekarze;{year};[osoba]'].sum() / dfs['doctors'][f'pielęgniarki łącznie z mgr pielęgniarstwa;{year};[osoba]'].sum() or float('nan'),
            
            # Hospital statistics
            'total_hospitals': poland_hospitals[f'szpitale;{year};[ob.]'].values[0],
            'total_beds': poland_hospitals[f'łóżka w szpitalach;{year};[-]'].values[0],
            'beds_per_1000': (poland_hospitals[f'łóżka w szpitalach;{year};[-]'].values[0] / population[year]) * 1000,
            
            # Health expenditure statistics
            'total_expenditure': poland_expenditure[f'ogółem;{year};[zł]'].values[0] / 1000000,  # Convert to millions
            'expenditure_per_capita': poland_expenditure[f'ogółem;{year};[zł]'].values[0] / population[year],
            
            # Death statistics
            'total_deaths': poland_deaths[f'razem;{year};[-]'].values[0],
            'deaths_per_1000': (poland_deaths[f'razem;{year};[-]'].values[0] / population[year]) * 1000,
            'covid_deaths': poland_deaths[f'COVID-19;{year};[-]'].values[0],
            'circulatory_deaths': poland_deaths[f'choroby układu krążenia ogółem;{year};[-]'].values[0],
            'cancer_deaths': poland_deaths[f'nowotwory ogółem;{year};[-]'].values[0],
            'respiratory_deaths': poland_deaths[f'choroby układu oddechowego ogółem;{year};[-]'].values[0]
        }
    
    return stats

def create_health_indicators_chart(dfs):
    years = [str(year) for year in range(2017, 2024)]
    
    # Get Poland data
    poland_doctors = dfs['doctors'][dfs['doctors']['Kod'] == '0000000']
    poland_hospitals = dfs['hospitals'][dfs['hospitals']['Kod'] == '0000000']
    poland_expenditure = dfs['expenditure'][dfs['expenditure']['Kod'] == '0000000']
    poland_deaths = dfs['deaths'][dfs['deaths']['Kod'] == '0000000']
    
    # Create figure with secondary y-axis
    fig = go.Figure()
    
    # Add doctors line
    fig.add_trace(go.Scatter(
        x=years,
        y=poland_doctors[[f'lekarze;{year};[osoba]' for year in years]].values[0],
        name="Liczba lekarzy",
        line=dict(color='blue')
    ))
    
    # Add hospital beds line
    fig.add_trace(go.Scatter(
        x=years,
        y=poland_hospitals[[f'łóżka w szpitalach;{year};[-]' for year in years]].values[0],
        name="Liczba łóżek szpitalnych",
        line=dict(color='red')
    ))
    
    # Add health expenditure line (convert to millions)
    expenditure_data = poland_expenditure[[f'ogółem;{year};[zł]' for year in years]].values[0] / 1000000
    fig.add_trace(go.Scatter(
        x=years,
        y=expenditure_data,
        name="Wydatki na zdrowie (mln zł)",
        line=dict(color='green')
    ))
    
    # Add deaths line
    fig.add_trace(go.Scatter(
        x=years,
        y=poland_deaths[[f'razem;{year};[-]' for year in years]].values[0],
        name="Liczba zgonów",
        line=dict(color='purple')
    ))
    
    fig.update_layout(
        title='Wskaźniki zdrowotne w Polsce (2017-2023)',
        xaxis_title='Rok',
        yaxis_title='Wartość',
        hovermode='x unified'
    )
    
    return fig 