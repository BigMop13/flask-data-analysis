// Create the initial plots
Plotly.newPlot('plot1', plot1Data.data, plot1Data.layout);
Plotly.newPlot('plot2', plot2Data.data, plot2Data.layout);
Plotly.newPlot('plot3', plot3Data.data, plot3Data.layout);

// Add click handlers for year buttons
document.querySelectorAll('.year-btn').forEach(button => {
    button.addEventListener('click', function() {
        const year = this.dataset.year;
        
        // Update button styles
        document.querySelectorAll('.year-btn').forEach(btn => {
            btn.classList.remove('btn-primary');
            btn.classList.add('btn-outline-primary');
        });
        this.classList.remove('btn-outline-primary');
        this.classList.add('btn-primary');
        
        // Fetch new data for the selected year
        fetch(`/get_regional_data/${year}`)
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    console.error('Błąd:', data.error);
                    return;
                }
                const newPlot = JSON.parse(data.plot);
                Plotly.newPlot('plot3', newPlot.data, newPlot.layout);
            })
            .catch(error => console.error('Błąd:', error));
    });
});

// Set initial button state
document.querySelector('.year-btn[data-year="2023"]').classList.remove('btn-outline-primary');
document.querySelector('.year-btn[data-year="2023"]').classList.add('btn-primary'); 