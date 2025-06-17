// Load and visualize alerts
fetch('alerts_data.json')
  .then(response => response.json())
  .then(data => {
    console.log("Loaded alert data:", data);

    const ctx = document.getElementById('alertsChart').getContext('2d');

    const chartData = {
      labels: ['Priority 1', 'Priority 2', 'Priority 3'],
      datasets: [{
        label: 'Number of Alerts',
        data: [data["1"] || 0, data["2"] || 0, data["3"] || 0],
        backgroundColor: ['#e74c3c', '#f39c12', '#27ae60']
      }]
    };

    const chartOptions = {
      responsive: true,
      plugins: {
        legend: { display: true }
      },
      scales: {
        y: {
          beginAtZero: true,
          ticks: { precision: 0 }
        }
      }
    };

    new Chart(ctx, {
      type: 'bar',
      data: chartData,
      options: chartOptions
    });
  })
  .catch(error => {
    console.error('Error loading alerts_data.json:', error);
  });

// Load and display alert details
fetch('alert.txt')
  .then(response => response.text())
  .then(text => {
    // Split the text into alert blocks
    const alertBlocks = text.trim().split(/\n\s*\n/); // Split by empty line

    const tableBody = document.getElementById('alertTableBody');

    alertBlocks.forEach(block => {
      const lines = block.split('\n');
      const alertName = lines[0]?.match(/\] (.+) \[\*/)?.[1] || 'Unknown';
      const priority = lines[1]?.match(/Priority: (\d+)/)?.[1] || 'N/A';
      const timestamp = lines[2]?.split(' ')[0] || 'N/A';
      const source = lines[2]?.split(' ')[1] || 'N/A';
      const destination = lines[2]?.split(' ')[3] || 'N/A';
      const protocol = lines[3]?.split(' ')[0] || 'N/A';

      const row = document.createElement('tr');
      row.innerHTML = `
        <td>${alertName}</td>
        <td>${priority}</td>
        <td>${timestamp}</td>
        <td>${source}</td>
        <td>${destination}</td>
        <td>${protocol}</td>
      `;
      tableBody.appendChild(row);
    });
  })
  .catch(error => {
    console.error('Error loading alert.txt:', error);
  });
