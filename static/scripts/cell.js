class Cell {
    constructor(json, isCardCell) {
        this.cell = document.createElement('div');
        this.isCardCell = isCardCell;
        this.imageView = document.createElement('div');
        this.titleArea = document.createElement('p');
        this.json = json
        this.init()
    }

    init() {
        this.addClassToCell();
        //this.addImageViewToCell();
        this.addClassToImageView();
        this.addImageToImageView();
        this.addTitleAreaToCell();
        this.addTitleToTitleArea();
    }

    addClassToCell() {
        this.cell.classList.add('collection-cell');
    }

    addClassToImageView() {
        this.imageView.classList.add('cell-image-container')

    }

    addImageToImageView() {
        const image = document.createElement('img');
        let imgUrl = this.json.img_url;
        if (!imgUrl) {
            imgUrl = '/static/images/no-avatar.png'
        }
        image.setAttribute('src', imgUrl)
        image.classList.add('avatar')
        this.imageView.append(image);
        this.cell.append(this.imageView)
    }

    addTitleAreaToCell() {
        this.titleArea.classList.add('cell-title-user')
        this.cell.append(this.titleArea);
    }

    addTitleToTitleArea() {
        this.titleArea.innerText = this.json.username;
    }


}