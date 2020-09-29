window.addEventListener('DOMContentLoaded', () => {
    const cellsContainer = document.querySelector('.cells-container')
    const searchBtn = document.querySelector('.search-btn');
    const resultTitle = document.querySelector('#result-title');

    searchBtn.addEventListener('click', async function(e) {
        e.preventDefault();

        let query = document.querySelector(".search-field").value;
        let tokens;
        if (query) {
            tokens = query.split(" ");
            resultTitle.innerText = `Showing results for ${query}:`
        }
        
        let res = await axios.get('/api/cards', { params : { 'tokens' : JSON.stringify(tokens) } })

        if (res.data.results.length > 0) {
            cellsContainer.innerHTML = "";
            for (card of res.data.results) {
                console.log(card)
                let cell = new Cell(card, true);
                cellsContainer.append(cell.cell);
            }
        } 
        else {
            cellsContainer.innerHTML = ""
            cellsContainer.innerText = "No results found"
            
        }
    });
})