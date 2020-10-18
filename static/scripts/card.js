const searchBtn = document.querySelector('#search-btn');
const detailBtn = document.querySelector('#detail-btn');
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
detailBtn.addEventListener('click', function(){
    const modal = new ModalWindow().modalWindow;
    body.append(modal);
    const detailedImage = document.createElement('img');
    detailedImage.classList.add('detail-img')
    detailedImage.setAttribute('src', detailBtn.dataset.url);
    modal.append(detailedImage);
})