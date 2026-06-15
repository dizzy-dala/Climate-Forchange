document.addEventListener('DOMContentLoaded', function () {
  const dataUrl = '/monitor/data.json';
  const ctx = document.getElementById('requestsChart');
  if (!ctx) return;

  fetch(dataUrl)
    .then(r => r.json())
    .then(payload => {
      if (payload.error) return;
      const counts = payload.counts || [];
      const labels = counts.map(c => c.day);
      const values = counts.map(c => c.cnt);

      // create chart
      const scriptExists = typeof Chart !== 'undefined';
      if (!scriptExists) return;

      const chart = new Chart(ctx.getContext('2d'), {
        type: 'line',
        data: {
          labels: labels,
          datasets: [{
            label: 'Weather requests (last 7 days)',
            data: values,
            fill: true,
            backgroundColor: 'rgba(79,70,229,0.12)',
            borderColor: 'rgba(79,70,229,0.9)',
            tension: 0.25,
          }]
        },
        options: {
          responsive: true,
          plugins: {
            legend: { display: false }
          }
        }
      });
    })
    .catch(err => console.error('monitor data error', err));
});
