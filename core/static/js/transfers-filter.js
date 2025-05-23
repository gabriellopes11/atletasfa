// Função para filtrar as transferências por tipo (jogador/treinador)
document.addEventListener('DOMContentLoaded', function() {
    const transferTypeLinks = document.querySelectorAll('[data-filter]');
    
    if (transferTypeLinks.length > 0) {
        transferTypeLinks.forEach(link => {
            link.addEventListener('click', function(e) {
                e.preventDefault();
                
                // Remover classe active de todos os links
                transferTypeLinks.forEach(l => l.classList.remove('active'));
                
                // Adicionar classe active ao link clicado
                this.classList.add('active');
                
                // Atualizar texto do botão dropdown
                const dropdownButton = document.getElementById('transferTypeDropdown');
                let filterText = 'Todos';
                
                if (this.dataset.filter === 'player') {
                    filterText = 'Apenas Jogadores';
                } else if (this.dataset.filter === 'coach') {
                    filterText = 'Apenas Treinadores';
                }
                
                dropdownButton.innerHTML = `<i class="fas fa-filter me-1"></i> ${filterText}`;
                
                // Filtrar a tabela
                filterTransfers(this.dataset.filter);
            });
        });
    }
    
    function filterTransfers(filterType) {
        const rows = document.querySelectorAll('#transfersTableBody tr');
        
        rows.forEach(row => {
            if (filterType === 'all') {
                row.style.display = '';
            } else if (filterType === 'player' && row.classList.contains('transfer-type-player')) {
                row.style.display = '';
            } else if (filterType === 'coach' && row.classList.contains('transfer-type-coach')) {
                row.style.display = '';
            } else {
                row.style.display = 'none';
            }
        });
    }
});