// Função para filtrar os times por região
document.addEventListener('DOMContentLoaded', function() {
    const regionFilter = document.getElementById('regionFilter');
    
    if (regionFilter) {
        regionFilter.addEventListener('change', function() {
            const selectedRegion = this.value;
            const rows = document.querySelectorAll('#rankingTableBody tr');
            
            rows.forEach(row => {
                if (selectedRegion === 'all') {
                    row.style.display = '';
                } else {
                    if (row.classList.contains('region-' + selectedRegion)) {
                        row.style.display = '';
                    } else {
                        row.style.display = 'none';
                    }
                }
            });
            
            // Atualizar a numeração das posições visíveis
            updatePositions();
        });
    }
    
    // Função para atualizar as posições dos times visíveis
    function updatePositions() {
        const visibleRows = Array.from(document.querySelectorAll('#rankingTableBody tr')).filter(row => 
            row.style.display !== 'none'
        );
        
        visibleRows.forEach((row, index) => {
            const positionBadge = row.querySelector('.position-badge');
            if (positionBadge) {
                positionBadge.textContent = index + 1;
            }
        });
    }
});