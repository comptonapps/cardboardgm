class EbayCell {
    constructor(json) {
        this.info = json
        this.cell;
        this.image = document.createElement('img')
        this.init()
    }

    init() {
        this.cell = this.createCell()
        this.image.setAttribute('src', this.info.img_url)
    }

    createCell() {
        const cell = document.createElement('div');
        cell.classList.add('ebay-cell')
        const imageContainer = document.createElement('div');
        imageContainer.classList.add('ebay-image-container');
        imageContainer.append(this.image);
        cell.append(imageContainer);
        const titleContainer = document.createElement('div');
        titleContainer.classList.add('ebay-title-container');
        const titleLink = document.createElement('a');
        titleLink.innerText = this.info.title;
        titleLink.setAttribute('href', this.info.ebay_url);
        titleContainer.append(titleLink);
        cell.append(titleContainer);
        const priceContainer = document.createElement('div');
        priceContainer.classList.add('ebay-price');
        priceContainer.innerText = this.info.price;
        cell.append(priceContainer);
        return cell;
        
    }
}