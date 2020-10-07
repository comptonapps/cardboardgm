class Cell {
    constructor(json) {
        this.cell;
        this.imageContainer;
        this.json = json;
        this.imageElement;
        this.titleContainer;
        this.init();
    }

    init() {
        this.cell = this.getCell();
        this.imageElement = this.getImageElement();
        this.imageContainer = this.getImageContainer();
        this.cell.append(this.imageContainer);
        
    }

    getCell() {
        const cell = this.getElement('div');
        cell.classList.add('collection-cell');
        return cell;
    }

    getImageContainer() {
        const container = this.getElement('div');
        container.classList.add('cell-image-container');
        container.append(this.imageElement);
        return container;
    }

    getImageElement() {
        const img = this.getElement('img');
        return img;
    }

    getElement(type) {
        return document.createElement(type);
    }

    setImageSource(src) {
        this.imageElement.setAttribute('src', src);
    }
}

class CardCell extends Cell {
    constructor(json) {
        super(json);
        this.ccinit();

    }

    ccinit() {
        this.titleContainer = this.getTitleContainer();
        this.cell.append(this.titleContainer);
        const imgUrl = this.json.thumb_url;
        if (imgUrl) {
            this.setImageSource(imgUrl);
        } else {
            this.setImageSource('/static/images/default.jpg');
        }
    }

    getTitleContainer() {
        const container = this.getElement('p');
        container.classList.add('cell-title');
        container.innerText = this.json.title;
        return container;
    }



}

class UserCell extends Cell {
    constructor(json) {
        super(json);
        this.ucinit();
    }

    ucinit() {
        this.titleContainer = this.getTitleContainer()
        this.cell.append(this.titleContainer);
        const imgUrl = this.json.thumb_url;
        if (imgUrl) {
            this.setImageSource(imgUrl);
            
        } else {
            this.setImageSource('/static/images/no-avatar.png')
        }
        this.imageElement.classList.add('avatar');
    }

    getTitleContainer() {
        const container = this.getElement('p');
        container.classList.add('cell-title-user');
        container.innerText = this.json.username;
        return container;
    }
}