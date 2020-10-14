const collection = document.querySelector('.collection-container')
    const body = document.querySelector('body');
    body.addEventListener('click', async function(e) {
        
        let target = e.target
        if (e.target.classList.contains('ebay')){
            e.preventDefault();
            const modal = new ModalWindow().modalWindow;
        body.append(modal);
        const resultsContainer = document.createElement('div')
        resultsContainer.classList.add('results-container');
        modal.append(resultsContainer);
        let res = await axios.get('/api/ebay', { params : {'item' : target.dataset.search }})
        console.log(res)
        if (res.data.length > 0) {
            for (item of res.data) {
            let cell = new EbayCell(item).cell;
            resultsContainer.append(cell);
            }
        } else {
            const noResults = document.createElement('h1');
            noResults.innerText = "NO RESULTS FOUND";
            noResults.classList.add('no-results');
            resultsContainer.append(noResults);
        }
        };
        
        
    })